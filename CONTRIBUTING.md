# Contributing to PyCDP

Thank you for your interest in contributing to Python Chrome DevTools Protocol (PyCDP)! We welcome contributions from the community.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Poetry for dependency management
- Git for version control

### Setting Up Development Environment

1. Fork and clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/python-chrome-devtools-protocol.git
   cd python-chrome-devtools-protocol
   ```

2. Install dependencies:
   ```bash
   pip install poetry
   poetry install
   ```

## Development Workflow

### Code Generation

This project automatically generates Python wrappers from the Chrome DevTools Protocol specification:

```bash
poetry run python generator/generate.py
```

### Running Tests

Run the test suite:
```bash
poetry run pytest test/
poetry run pytest generator/
```

### Type Checking

We use mypy for static type checking:
```bash
poetry run mypy cdp/
poetry run mypy generator/
```

### Complete Build

Run all checks (type checking, tests, and generation):
```bash
poetry run make default
```

## Submitting Changes

### Pull Request Process

1. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and ensure:
   - All tests pass
   - Code passes type checking
   - Code follows the existing style
   - Documentation is updated if needed

3. Commit your changes with clear, descriptive messages:
   ```bash
   git commit -m "Add feature: brief description"
   ```

4. Push to your fork and submit a pull request:
   ```bash
   git push origin feature/your-feature-name
   ```

5. In your pull request description:
   - Describe what changes you made and why
   - Reference any related issues
   - Include any relevant context

### Code Review

- Maintainers will review your pull request
- Address any feedback or requested changes
- Once approved, a maintainer will merge your PR

## Reporting Issues

### Bug Reports

When reporting bugs, please include:
- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior vs. actual behavior
- Python version and environment details
- Any relevant error messages or logs

### Feature Requests

For feature requests, please:
- Clearly describe the feature and its use case
- Explain why it would be valuable
- Provide examples if possible

## Code Style

- Follow PEP 8 style guidelines
- Use type hints for function parameters and return values
- Write clear, descriptive variable and function names
- Add docstrings for public APIs
- Keep functions focused and modular

## Documentation

- Update README.md if you add new features
- Update docstrings for any modified functions or classes
- Add examples for new functionality when appropriate

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

If you have questions, feel free to:
- Open an issue for discussion
- Reach out to the maintainers

Thank you for contributing to PyCDP!
