Development
===========

This section describes aspects of the project relevant to anybody who wants to
modify the code generation process. Note that code is generated and then checked
in, so that anybody who wants to use the library can use it immediately–no build
step is required in that scenario.

The repository uses `Poetry <https://python-poetry.org/>`_ to manage dependencies. Once
you have Poetry installed, use this command to create a new virtual environment and
install PyCDP and its dependencies (including dev dependencies0 in it.

::

    $ poetry install

Next, a ``Makefile`` is included that provides the following build targets:

mypy-generate:
    Run MyPy type checker on the generator script.

test-generate:
	Run automated tests for the generator script.

generate
	Parse the CDP spec and generate the equivalent Python code in the ``cdp/`` directory.

test-import:
	Verify that the generated code can be imported. This is a simple smoke check to ensure that code generation hasn't gone completely haywire, e.g. produced blank files.

mypy-cdp:
    Run MyPy type checker on the generated CDP code.

test-cdp:
    Run a few automated tests on the generated CDP code.

Note that the verification in this project occurs in two phases:

1. Verify the *generator* code.
2. Run the generator.
3. Verify the *generated* code.

We focus most of the effort on step 1, because if the generator is correct then
the generated code is correct by definition. The default ``make`` target runs
all of these targets in order, serving as a quick way to verify the entire
project.

To make documentation (i.e. the docs you're reading right now) go into the
``docs/`` directory and run ``make html``.
