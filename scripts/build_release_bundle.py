#!/usr/bin/env python3
"""Assemble the ready-to-use assets published for a tagged release."""

from __future__ import annotations

import argparse
import re
import shutil
import tomllib
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COPY_PATHS = (
    "README.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "Makefile",
    "mkdocs.yml",
    "pyproject.toml",
    "uv.lock",
    ".omp",
    "bitwig_mcp_server",
    "docs",
    "examples",
    "extension",
    "scripts",
)


def source_versions() -> tuple[str, str, str]:
    with (ROOT / "pyproject.toml").open("rb") as file:
        python_version = tomllib.load(file)["project"]["version"]

    pom_root = ET.parse(ROOT / "extension" / "pom.xml").getroot()
    namespace = "{http://maven.apache.org/POM/4.0.0}"
    maven_version = pom_root.findtext(f"{namespace}version")
    if maven_version is None:
        raise ValueError("extension/pom.xml has no project version")

    java_source = (
        ROOT
        / "extension"
        / "src/main/java/io/github/critxjt/bitwig/gridbridge/GridBridgeExtensionDefinition.java"
    ).read_text()
    match = re.search(r'getVersion\(\)\s*\{\s*return "([^"]+)"', java_source)
    if match is None:
        raise ValueError("GridBridgeExtensionDefinition.java has no extension version")
    return str(python_version), maven_version, match.group(1)


def copy_tree(source: Path, destination: Path) -> None:
    if source.is_dir():
        shutil.copytree(
            source,
            destination,
            dirs_exist_ok=True,
            ignore=shutil.ignore_patterns(
                "__pycache__",
                ".pytest_cache",
                ".mypy_cache",
                ".ruff_cache",
                "target",
            ),
        )
    else:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


def build_bundle(version: str, extension: Path, output: Path) -> tuple[Path, Path]:
    versions = source_versions()
    if versions != (version, version, version):
        raise ValueError(f"source versions {versions} do not match release version {version}")
    if not extension.is_file():
        raise FileNotFoundError(f"built extension not found: {extension}")

    distributions = sorted((ROOT / "dist").glob(f"bitwig_grid_bridge-{version}*"))
    if not any(path.suffix == ".whl" for path in distributions):
        raise FileNotFoundError(f"no wheel found for {version} in dist/")
    if not any(path.name.endswith((".tar.gz", ".zip")) for path in distributions):
        raise FileNotFoundError(f"no source distribution found for {version} in dist/")

    output.mkdir(parents=True, exist_ok=True)
    bundle_name = f"bitwig-grid-bridge-{version}"
    bundle = output / bundle_name
    archive = output / f"{bundle_name}.zip"
    if bundle.exists():
        shutil.rmtree(bundle)
    if archive.exists():
        archive.unlink()
    bundle.mkdir()

    for relative in COPY_PATHS:
        copy_tree(ROOT / relative, bundle / relative)
    copy_tree(extension, bundle / "BitwigGridBridge.bwextension")
    for distribution in distributions:
        copy_tree(distribution, bundle / "python" / distribution.name)

    (bundle / "INSTALL.txt").write_text(
        f"""Bitwig Grid Bridge {version}

1. Copy BitwigGridBridge.bwextension to your Bitwig Extensions folder.
2. Restart Bitwig, then enable Bitwig Grid Bridge under Settings > Controllers.
3. From this directory, run `uv sync --frozen` and then `uv run bitwig-mcp`
   when an MCP client needs the optional adapter.
4. Use docs/quickstart.md and docs/workflows.md for the first verified change.

The Python wheel and source distribution are in python/. Maven is optional
for users of this bundle; rebuild the extension with `make build-extension`
only when developing the Java extension from source.
""",
    )

    shutil.copy2(extension, output / "BitwigGridBridge.bwextension")
    archive_path = Path(shutil.make_archive(str(output / bundle_name), "zip", root_dir=output, base_dir=bundle_name))
    return output / "BitwigGridBridge.bwextension", archive_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", required=True)
    parser.add_argument("--extension", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=ROOT / "release")
    args = parser.parse_args()

    standalone, archive = build_bundle(args.version, ROOT / args.extension if not args.extension.is_absolute() else args.extension, ROOT / args.output if not args.output.is_absolute() else args.output)
    print(standalone)
    print(archive)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
