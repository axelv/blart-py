# PyPI Publication Setup Guide

This guide will walk you through publishing the blart-py package to PyPI.

## Prerequisites

1. **PyPI Account**: Create accounts on both:
   - TestPyPI: https://test.pypi.org/account/register/
   - PyPI: https://pypi.org/account/register/

2. **Install Required Tools**:
   ```bash
   pip install --upgrade twine build
   ```

3. **Verify Package Name Availability**:
   - Check if "blart" is available on PyPI: https://pypi.org/project/blart/
   - If taken, consider alternative names: `blart-tree`, `py-blart`, `blartpy`, etc.

## Step 1: Get API Tokens

### TestPyPI Token

1. Log in to https://test.pypi.org
2. Go to Account Settings → API tokens
3. Click "Add API token"
4. Token name: `blart-py-upload`
5. Scope: "Entire account" (or project-specific once you've uploaded once)
6. **Copy the token** (it starts with `pypi-` and won't be shown again)
7. Save it securely - you'll need it for uploading

### PyPI Token (Production)

1. Log in to https://pypi.org
2. Go to Account Settings → API tokens
3. Click "Add API token"
4. Token name: `blart-py-upload`
5. Scope: "Entire account" (or project-specific after first upload)
6. **Copy the token** and save it securely

## Step 2: Configure Credentials

Create a `~/.pypirc` file with your tokens:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-YOUR-TESTPYPI-TOKEN-HERE

[pypi]
repository = https://pypi.org/legacy/
username = __token__
password = pypi-YOUR-PYPI-TOKEN-HERE
```

**Important**: Keep this file secure! Never commit it to git.

## Step 3: Build the Package

The package has already been built, but here's how to rebuild if needed:

```bash
# Clean previous builds
rm -rf dist/ target/wheels/

# Build wheels
PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1 maturin build --release

# Build source distribution
maturin sdist --out dist

# Copy wheel to dist directory
cp target/wheels/blart-0.1.0-*.whl dist/
```

## Step 4: Test on TestPyPI First

### Upload to TestPyPI

```bash
# Upload to TestPyPI
twine upload --repository testpypi dist/*
```

You'll see output like:
```
Uploading distributions to https://test.pypi.org/legacy/
Uploading blart-0.1.0-cp314-cp314-macosx_11_0_arm64.whl
Uploading blart-0.1.0.tar.gz

View at:
https://test.pypi.org/project/blart/0.1.0/
```

### Test Installation from TestPyPI

```bash
# Create a fresh virtual environment
python3.9 -m venv test_env
source test_env/bin/activate

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ --no-deps blart-py

# Test the package
python -c "import blart; print(blart.__version__); tree = blart.TreeMap(); tree['test'] = 1; print('Success!')"

# Deactivate and remove test environment
deactivate
rm -rf test_env
```

## Step 5: Publish to Production PyPI

Once you've verified everything works on TestPyPI:

```bash
# Upload to production PyPI
twine upload dist/*
```

You'll see output like:
```
Uploading distributions to https://upload.pypi.org/legacy/
Uploading blart-0.1.0-cp314-cp314-macosx_11_0_arm64.whl
Uploading blart-0.1.0.tar.gz

View at:
https://pypi.org/project/blart/0.1.0/
```

### Verify Production Installation

```bash
# Install from PyPI
pip install blart-py

# Test
python -c "import blart; print(blart.__version__)"
```

## Step 6: Set Up GitHub Repository

1. **Create GitHub Repository**:
   ```bash
   # On GitHub.com, create a new repository: axelv/blart-py
   ```

2. **Initialize and Push**:
   ```bash
   # Initialize git (if not already done)
   git init

   # Add all files
   git add .

   # Create initial commit
   git commit -m "Initial commit: blart-py v0.1.0"

   # Add remote
   git remote add origin https://github.com/axelv/blart-py.git

   # Push to GitHub
   git branch -M main
   git push -u origin main
   ```

3. **Create Release Tag**:
   ```bash
   # Tag the release
   git tag -a v0.1.0 -m "Release version 0.1.0"

   # Push the tag
   git push origin v0.1.0
   ```

## Step 7: Configure GitHub Actions (Optional but Recommended)

This enables automatic wheel building and PyPI publishing for future releases.

### Add GitHub Secret

1. Go to your repository: https://github.com/axelv/blart-py
2. Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Name: `PYPI_API_TOKEN`
5. Value: Your PyPI API token
6. Click "Add secret"

### Test the Workflow

The `.github/workflows/build.yml` workflow is already configured. To test it:

```bash
# Create a new version tag
git tag -a v0.1.1 -m "Test release"
git push origin v0.1.1
```

This will automatically:
- Build wheels for Linux, macOS, and Windows
- Build for Python 3.8-3.12
- Create a GitHub Release
- Publish to PyPI

## Step 8: Post-Publication Checklist

- [ ] Package visible on PyPI: https://pypi.org/project/blart-py/
- [ ] Installation works: `pip install blart-py`
- [ ] Import works: `python -c "import blart"`
- [ ] GitHub repository created and pushed
- [ ] GitHub release created for v0.1.0
- [ ] README badges updated (optional)
- [ ] Announcement (Twitter, Reddit, HN, etc.) (optional)

## Troubleshooting

### "Package already exists"

If you get this error, the package name is taken. Options:
1. Choose a different name
2. Contact the current owner if the package is abandoned
3. Update `name` in pyproject.toml and rebuild

### "Invalid credentials"

- Verify your API token is correct in `~/.pypirc`
- Ensure you're using `__token__` as username, not your actual username
- Check that the token hasn't expired

### "File already exists"

You're trying to upload a version that's already on PyPI. PyPI doesn't allow overwriting.
Solution: Increment the version number in:
- `pyproject.toml`
- `Cargo.toml`
- `python/blart/__init__.py` (__version__)
- `CHANGELOG.md`

Then rebuild and upload.

### Build Failures

#### Python 3.14 Issues
If building with Python 3.14+, use:
```bash
PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1 maturin build --release
```

#### Missing Rust Toolchain
```bash
# Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Update Rust
rustup update
```

## Multi-Platform Wheels

The current build only includes macOS ARM64. For full platform support:

### Option 1: Use GitHub Actions (Recommended)

The `.github/workflows/build.yml` already builds for all platforms. Just push a tag:
```bash
git tag -a v0.1.0 -m "Release 0.1.0"
git push origin v0.1.0
```

### Option 2: Local Multi-Platform Build

Use Docker for Linux wheels:
```bash
# Install Docker
# Then run:
docker run --rm -v $(pwd):/io ghcr.io/pyo3/maturin build --release --out dist
```

For Windows, you'll need a Windows machine or VM.

## Next Steps

1. **Add README Badges** (optional):
   ```markdown
   [![PyPI version](https://badge.fury.io/py/blart.svg)](https://badge.fury.io/py/blart)
   [![CI](https://github.com/axelv/blart-py/actions/workflows/ci.yml/badge.svg)](https://github.com/axelv/blart-py/actions/workflows/ci.yml)
   [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
   ```

2. **Set Up Documentation** (optional):
   - Consider ReadTheDocs or GitHub Pages
   - Add API reference with Sphinx

3. **Community**:
   - Add CONTRIBUTING.md
   - Set up issue templates
   - Add CODE_OF_CONDUCT.md

## Resources

- [Python Packaging User Guide](https://packaging.python.org/)
- [Maturin Documentation](https://www.maturin.rs/)
- [PyPI Help](https://pypi.org/help/)
- [TestPyPI](https://test.pypi.org/)
- [Twine Documentation](https://twine.readthedocs.io/)

## Quick Reference

```bash
# Build
maturin build --release
maturin sdist --out dist

# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Upload to PyPI
twine upload dist/*

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ blart-py

# Install from PyPI
pip install blart-py
```
