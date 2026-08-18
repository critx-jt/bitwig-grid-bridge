.PHONY: build-extension install-extension build-python release-bundle test test-python check docs-test docs

build-extension:
	@mvn -B -f extension/pom.xml package

install-extension: build-extension
	@mkdir -p "$(HOME)/Bitwig Studio/Extensions"
	@cp extension/target/BitwigGridBridge.jar \
		"$(HOME)/Bitwig Studio/Extensions/BitwigGridBridge.bwextension"

build-python:
	@uv build

release-bundle: build-extension build-python
	@version="$$(uv run python -c 'import tomllib; print(tomllib.load(open("pyproject.toml", "rb"))["project"]["version"])')"; \
	uv run python scripts/build_release_bundle.py \
		--version "$$version" \
		--extension extension/target/BitwigGridBridge.jar \
		--output release

test-python:
	@uv run pytest tests -q

test: test-python

check: docs-test
	@uv run ruff check bitwig_mcp_server tests scripts
	@mvn -B -f extension/pom.xml -q package

docs-test:
	@uv run mkdocs build --strict

docs:
	@uv run mkdocs serve
