# The targets in this makefile should be executed inside Poetry, i.e. `poetry run make
# docs`.

.PHONY: docs

default: mypy-generate test-generate generate test-import mypy-cdp test-cdp

docs:
	$(MAKE) -C docs html

generate:
	python generator/generate.py

mypy-cdp:
	mypy cdp/

mypy-generate:
	mypy generator/

test-cdp:
	pytest test/

test-generate:
	pytest generator/

test-import:
	python -c 'import cdp; print(cdp.accessibility)'
