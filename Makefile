all: test-generate generate test-import test-cdp

generate:
	python build/generate.py

test-cdp:
	pytest test/

test-generate:
	pytest build/

test-import:
	python -c 'import cdp; print(cdp.accessibility)'
