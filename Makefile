# The targets in this makefile should be executed inside Poetry, i.e. `poetry run make
# docs`.

.PHONY: docs

default: mypy-generate test-generate generate test-import mypy-cdp test-cdp

docs:
	$(MAKE) -C docs html SPHINXBUILD="python3 -m sphinx"

generate:
	python3 generator/generate.py

mypy-cdp:
	python3 -m mypy cdp/

mypy-generate:
	python3 -m mypy generator/

test-cdp:
	python3 -m pytest test/

test-generate:
	python3 -m pytest generator/

test-import:
	python3 -c 'import cdp; print(cdp.accessibility)'
