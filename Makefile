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

publish:
	rm -fr dist chrome_devtools_protocol.egg-info
	$(PYTHON) setup.py sdist
	twine upload dist/*

test-cdp:
	pytest test/

test-generate:
	pytest generator/

test-import:
	python -c 'import cdp; print(cdp.accessibility)'
