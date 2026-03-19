# Contributing to PyCDP

Thank you for your interest in contributing to Python Chrome DevTools Protocol (PyCDP)! This document provides guidelines for contributing to the project.

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct (see [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)).

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue on GitHub with:
- A clear description of the problem
- Steps to reproduce the issue
- Expected vs. actual behavior
- Your environment (OS, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are welcome! Please open an issue describing:
- The enhancement you'd like to see
- Why it would be useful
- Any implementation ideas you have

### Pull Requests

1. **Fork the repository** and create your branch from `master`
2. **Install development dependencies**:
   ```bash
   pip install poetry
   poetry install
   ```
3. **Make your changes** following the project's coding standards
4. **Run tests** to ensure nothing is broken:
   ```bash
   poetry run make
   ```
5. **Update documentation** if needed
6. **Commit your changes** with clear, descriptive commit messages
7. **Push to your fork** and submit a pull request

## Development Setup

### Prerequisites

- Python 3.7 or higher
- Poetry for dependency management

### Installation

```bash
# Clone the repository
git clone https://github.com/HyperionGray/python-chrome-devtools-protocol.git
cd python-chrome-devtools-protocol

# Install dependencies
poetry install
```

### Running Tests

```bash
# Run all tests
poetry run make

# Run specific test suites
poetry run pytest test/
poetry run pytest generator/

# Run type checking
poetry run mypy cdp/
poetry run mypy generator/
```

### Code Generation

This project generates Python code from the Chrome DevTools Protocol specification:

```bash
poetry run python generator/generate.py
```

The generated code is checked into version control. If you modify the generator, run it and include the updated generated files in your PR.

## Coding Standards

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines
- Use type hints for all functions and methods
- Write docstrings for public APIs
- Ensure code passes `mypy` type checking
- Keep code coverage high

## Project Structure

- `cdp/` - Generated CDP protocol bindings
- `generator/` - Code generator for CDP bindings
- `test/` - Test suite
- `docs/` - Documentation source files
- `examples/` - Example usage scripts

## Questions?

If you have questions about contributing, feel free to open an issue or reach out to the maintainers.

## License

By contributing to PyCDP, you agree that your contributions will be licensed under the MIT License.
