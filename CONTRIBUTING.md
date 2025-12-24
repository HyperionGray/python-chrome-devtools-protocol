# Contributing to PyCDP

Thank you for your interest in contributing to Python Chrome DevTools Protocol (PyCDP)! This document provides guidelines for contributing to the project.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- [Poetry](https://python-poetry.org/) for dependency management

### Setting Up Your Development Environment

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/python-chrome-devtools-protocol.git
   cd python-chrome-devtools-protocol
   ```
3. Install dependencies:
   ```bash
   poetry install
   ```

## Development Workflow

### Code Generation

This project automatically generates Python wrappers from the Chrome DevTools Protocol specification. Most code in the `cdp/` directory (except `connection.py` and `util.py`) is auto-generated.

To regenerate the protocol wrappers:
```bash
poetry run make generate
```

### Running Tests

Run the test suite:
```bash
poetry run make test-cdp
poetry run make test-generate
```

Or run all checks:
```bash
poetry run make
```

### Type Checking

We use mypy for static type checking:
```bash
poetry run make mypy-cdp
poetry run make mypy-generate
```

### Building Documentation

To build the documentation:
```bash
poetry run make docs
```

## Making Changes

### Code Style

- Follow PEP 8 style guidelines
- Use type hints for all function signatures
- Keep code clear and well-documented

### Commit Messages

- Use clear and descriptive commit messages
- Reference issue numbers when applicable
- Keep commits focused on a single change

### Pull Requests

1. Create a new branch for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Make your changes and commit them
3. Push to your fork and submit a pull request
4. Ensure all tests pass and type checking succeeds
5. Provide a clear description of your changes

## What to Contribute

### Areas for Contribution

- **Bug fixes**: Fix issues in the connection module or utility functions
- **Documentation**: Improve examples, tutorials, or API documentation
- **Tests**: Add test coverage for existing functionality
- **Examples**: Add new usage examples in the `examples/` directory

### Code Generation Changes

If you need to modify code generation:
- Edit files in the `generator/` directory
- Run the generator and verify the output
- Ensure all tests still pass
- Add tests for your generator changes

### Protocol Updates

The protocol definitions are automatically fetched from the Chrome DevTools Protocol repository. If you need to update to a newer protocol version, please open an issue first to discuss the change.

## Reporting Issues

### Bug Reports

When reporting bugs, please include:
- Python version
- PyCDP version
- Steps to reproduce
- Expected vs. actual behavior
- Error messages or stack traces

### Feature Requests

For feature requests:
- Clearly describe the feature
- Explain the use case
- Consider if it fits the project's scope

## Code of Conduct

Please be respectful and constructive in all interactions. We are committed to providing a welcoming and inclusive environment for all contributors.

## Questions?

If you have questions about contributing, please:
- Check existing issues and pull requests
- Open a new issue with your question
- Tag it appropriately for visibility

## License

By contributing to PyCDP, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing to PyCDP!
