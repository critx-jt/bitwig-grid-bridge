.PHONY: build-extension install-extension test test-python check docs-test docs

build-extension:
	@mvn -f extension/pom.xml package

install-extension: build-extension
	@cp extension/target/bitwig-grid-bridge-0.1.0.jar \
		"$(HOME)/Bitwig Studio/Extensions/BitwigGridBridge.bwextension"

test-python:
	@uv run pytest tests/test_bridge.py tests/osc/test_controller.py tests/test_tools.py tests/mcp/test_server.py -q

test: test-python

check:
	@uv run ruff check bitwig_mcp_server tests/test_bridge.py tests/osc/test_controller.py
	@mvn -f extension/pom.xml -q package

docs-test:
	@uv run mkdocs build --strict

docs:
	@uv run mkdocs serve
