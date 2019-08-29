all: mypy-generate test-generate generate test-import mypy-cdp test-cdp

generate:
	python build/generate.py

mypy-cdp:
	mypy cdp/

mypy-generate:
	mypy build/

test-cdp:
	pytest test/

test-generate:
	pytest build/

test-import:
	python -c 'import cdp; print(cdp.accessibility)'
