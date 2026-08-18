# Bitwig Grid Bridge project notes

Repository: https://github.com/critx-jt/bitwig-grid-bridge

## First checkout

```bash
uv sync
mvn -f extension/pom.xml package
```

Install the resulting extension into Bitwig's user Extensions directory and
enable **Bitwig Grid Bridge** under **Settings > Controllers**.

## Validation

```bash
make test
make check
make docs-test
```

Live automation validation uses only the disposable projects under
`examples/projects/`.
