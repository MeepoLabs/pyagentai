# Contributing to autogen-agentai

Thank you for your interest in contributing to autogen-agentai! This document provides guidelines and instructions for contributing to this project.

## Development Setup

### Prerequisites

- Python 3.10 or higher
- [Poetry](https://python-poetry.org/docs/#installation) for dependency management
- [Git](https://git-scm.com/downloads) for version control

### Setting Up the Development Environment

1. Clone the repository:
   ```bash
   git clone https://github.com/meepolabs/autogen-agentai.git
   cd autogen-agentai
   ```

2. Install dependencies with Poetry:
   ```bash
   poetry install
   ```

3. Install pre-commit hooks:
   ```bash
   poetry run pre-commit install
   ```

## Development Workflow

### Code Style

We use [Ruff](https://github.com/astral-sh/ruff) for linting and formatting. The configuration is in the `pyproject.toml` file. To check your code:

```bash
poetry run ruff check .
poetry run ruff format .
```

### Type Checking

We use [MyPy](https://mypy.readthedocs.io/) for static type checking. To check your code:

```bash
poetry run mypy autogen_agentai
```

### Running Tests

We use [pytest](https://docs.pytest.org/) for testing. To run the tests:

```bash
poetry run pytest
```

To run tests with coverage:

```bash
poetry run pytest --cov=autogen_agentai
```

### Documentation

We use [Sphinx](https://www.sphinx-doc.org/) for documentation. To build the documentation:

```bash
cd docs
poetry run make html
```

## Pull Request Process

1. Fork the repository and create a new branch from `main`.
2. Make your changes and ensure they pass all tests and linting.
3. Add or update tests as necessary.
4. Update documentation as necessary.
5. Submit a pull request to the `main` branch.
6. The pull request will be reviewed by maintainers.

## Commit Message Guidelines

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification for commit messages:

- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that do not affect the meaning of the code
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `perf`: A code change that improves performance
- `test`: Adding missing tests or correcting existing tests
- `chore`: Changes to the build process or auxiliary tools

Example:
```
feat(agents): add support for planning agent
```

## Code of Conduct

Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project, you agree to abide by its terms.

## License

By contributing to autogen-agentai, you agree that your contributions will be licensed under the project's [GNU General Public License v3.0 (GPLv3)](LICENSE).
