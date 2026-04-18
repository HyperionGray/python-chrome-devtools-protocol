# The targets in this makefile should be executed inside Poetry, i.e. `poetry run make
# docs`.

.PHONY: default docs generate mypy-cdp mypy-generate test-cdp test-generate test-import
.NOTPARALLEL:

PYTHON ?= $(if $(CONDA_PREFIX),$(CONDA_PREFIX)/bin/python,python)
PYTEST ?= $(PYTHON) -m pytest
MYPY ?= $(if $(CONDA_PREFIX),$(CONDA_PREFIX)/bin/mypy,mypy)
SPHINXBUILD ?= $(PYTHON) -m sphinx

default:
	$(MAKE) mypy-generate
	$(MAKE) test-generate
	$(MAKE) generate
	$(MAKE) test-import
	$(MAKE) mypy-cdp
	$(MAKE) test-cdp

MYPY_CACHE_BASE ?= .mypy_cache
MYPY_GENERATOR_CACHE ?= $(MYPY_CACHE_BASE)/generator
MYPY_CDP_CACHE ?= $(MYPY_CACHE_BASE)/cdp

docs:
	$(MAKE) -C docs SPHINXBUILD="$(SPHINXBUILD)" html

generate:
	$(PYTHON) generator/generate.py

mypy-cdp:
	$(MYPY) --cache-dir $(MYPY_CDP_CACHE) cdp/

mypy-generate:
	$(MYPY) --cache-dir $(MYPY_GENERATOR_CACHE) generator/

test-cdp:
	$(PYTEST) test/

test-generate:
	$(PYTEST) generator/

test-import:
	$(PYTHON) -c 'import cdp; print(cdp.accessibility)'
