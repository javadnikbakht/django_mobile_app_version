# Contributing to django-mobile-app-version

Thank you for your interest in contributing to django-mobile-app-version! This document provides guidelines and instructions for setting up your development environment and contributing to the project.

## Development Setup

We use [UV](https://github.com/astral-sh/uv) for fast and reliable dependency management. UV provides 10-100x faster package installation compared to traditional pip.

### Prerequisites

- Python 3.13 or higher
- Git

### Option 1: Using UV (Recommended) 🚀

UV is our recommended tool for development as it provides:
- ⚡ **10-100x faster** package installation and resolution
- 🔒 **Reproducible builds** with `uv.lock` file
- 🔄 **Unified tooling** for dependency management and virtual environments
- 📦 **Better caching** and disk space usage

#### 1. Install UV

**On macOS and Linux:**
```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**On Windows:**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### 2. Clone the Repository

```sh
git clone https://github.com/javadnikbakht/django_mobile_app_version.git
cd django_mobile_app_version
```

#### 3. Create Virtual Environment and Install Dependencies

```sh
# Create a virtual environment
uv venv

# Activate the virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# Install all dependencies (including dev dependencies) from lock file
uv sync

# Or install in editable mode with dev dependencies
uv pip install -e ".[dev]"
```

#### 4. Development Workflow with UV

**Run tests:**
```sh
uv run pytest
```

**Format code with Black:**
```sh
uv run black mobile_app_version
```

**Run type checking with MyPy:**
```sh
uv run mypy mobile_app_version
```

**Run linting:**
```sh
uv run flake8 mobile_app_version
```

**Install a new dependency:**
```sh
# Add to pyproject.toml first, then:
uv pip install <package-name>
uv lock  # Update lock file
```

### Option 2: Using pip (Traditional)

If you prefer traditional pip or don't want to use UV yet:

#### 1. Clone the Repository

```sh
git clone https://github.com/javadnikbakht/django_mobile_app_version.git
cd django_mobile_app_version
```

#### 2. Create Virtual Environment

```sh
python -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

#### 3. Install Dependencies

```sh
# Install from requirements.txt
pip install -r requirements.txt

# Install the package in editable mode
pip install -e .
```

## Migration from pip to UV

If you're currently using pip for development, migrating to UV is straightforward:

### Step 1: Install UV
```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Step 2: Use UV with Existing Setup

You can continue using `requirements.txt`:
```sh
uv pip install -r requirements.txt
```

Or migrate to `pyproject.toml`:
```sh
uv sync
```

Both methods work! The project supports both during the transition period.

### Step 3: Update Your Workflow

Replace pip commands with UV equivalents:
- `pip install <package>` → `uv pip install <package>`
- `pip install -r requirements.txt` → `uv pip install -r requirements.txt` or `uv sync`
- `pip freeze > requirements.txt` → `uv lock`

## Code Style and Quality

We follow these guidelines:
- **Black** for code formatting (line length: 88)
- **flake8** for linting
- **mypy** for type checking
- Python 3.13+ compatible code

Before submitting a pull request, please ensure:
1. Code is formatted with Black
2. No linting errors from flake8
3. Type hints pass mypy checks
4. All tests pass

## Testing

Run the test suite:
```sh
# With UV
uv run pytest

# With pip
pytest
```

## Making Changes

1. **Fork the repository** on GitHub
2. **Create a new branch** for your feature or bug fix:
   ```sh
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** following the code style guidelines
4. **Test your changes** thoroughly
5. **Commit your changes** with clear, descriptive commit messages:
   ```sh
   git commit -m "feat: add new feature"
   git commit -m "fix: resolve issue with X"
   git commit -m "docs: update documentation"
   ```
6. **Push to your fork**:
   ```sh
   git push origin feature/your-feature-name
   ```
7. **Create a Pull Request** on GitHub

## Commit Message Convention

We follow conventional commit messages:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

Reference issues in commit messages:
- `refs #123` - Reference an issue
- `closes #123` - Close an issue when merged

## Project Structure

```
django_mobile_app_version/
├── mobile_app_version/          # Main application package
│   ├── adminapi/               # Admin API endpoints
│   ├── migrations/             # Database migrations
│   ├── admin.py               # Django admin configuration
│   ├── apps.py                # App configuration
│   ├── messages.py            # Message constants
│   ├── middlewares.py         # Custom middlewares
│   ├── models.py              # Database models
│   ├── paginations.py         # API pagination
│   ├── serializers.py         # DRF serializers
│   ├── urls.py                # URL routing
│   └── views.py               # API views
├── pyproject.toml             # Project metadata and dependencies
├── uv.lock                    # UV lock file (reproducible builds)
├── requirements.txt           # Legacy pip requirements
├── setup.py                   # Package setup (legacy)
├── setup.cfg                  # Package configuration (legacy)
└── README.md                  # User documentation
```

## Questions or Need Help?

- Open an [issue](https://github.com/javadnikbakht/django_mobile_app_version/issues) for bug reports or feature requests
- Check existing issues before creating a new one
- Be respectful and follow our code of conduct

## License

By contributing to this project, you agree that your contributions will be licensed under the GNU General Public License v3 (GPLv3).

Thank you for contributing! 🎉
