# Release Checklist

This document provides a checklist for creating a new release of blart-py.

## Pre-Release

- [ ] All tests passing locally (`make test`)
- [ ] All linters passing (`make lint`)
- [ ] Code formatted (`make format`)
- [ ] Test coverage >90% (`make test-cov`)
- [ ] All examples run successfully (`make examples`)
- [ ] Documentation up to date
- [ ] CHANGELOG.md updated with changes
- [ ] Version number updated in:
  - [ ] `pyproject.toml`
  - [ ] `Cargo.toml`
  - [ ] `CHANGELOG.md`

## Version Numbering

Follow [Semantic Versioning](https://semver.org/):
- MAJOR version: incompatible API changes
- MINOR version: backwards-compatible new functionality
- PATCH version: backwards-compatible bug fixes

Examples:
- `0.1.0` → `0.1.1` (bug fix)
- `0.1.0` → `0.2.0` (new features)
- `0.9.0` → `1.0.0` (stable API, breaking changes)

## Release Process

### 1. Update Version Numbers

```bash
# Update version in pyproject.toml
# Update version in Cargo.toml
# Update CHANGELOG.md with new version and date
```

### 2. Test Release Build Locally

```bash
# Build release wheels
make build

# Test installation
pip install --force-reinstall target/wheels/*.whl

# Verify all features work
python -c "import blart; tree = blart.TreeMap(); tree['test'] = 1; print('OK')"
```

### 3. Commit Version Bump

```bash
git add pyproject.toml Cargo.toml CHANGELOG.md
git commit -m "chore: bump version to X.Y.Z"
git push origin main
```

### 4. Create Git Tag

```bash
# Create annotated tag
git tag -a vX.Y.Z -m "Release version X.Y.Z"

# Push tag to trigger build workflow
git push origin vX.Y.Z
```

### 5. Monitor GitHub Actions

- [ ] CI workflow passes on all platforms
- [ ] Build workflow completes successfully
- [ ] Wheels built for all platforms (Linux, macOS, Windows)
- [ ] Wheels built for all Python versions (3.8-3.12)
- [ ] GitHub release created automatically

### 6. Verify GitHub Release

- [ ] Release notes generated correctly
- [ ] All wheels attached to release
- [ ] Source distribution (sdist) attached
- [ ] Download and test one wheel manually

### 7. PyPI Publication

The build workflow will automatically publish to PyPI if configured. To publish manually:

```bash
# Install twine
pip install twine

# Upload to TestPyPI first
twine upload --repository testpypi dist/*

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ blart-py

# Upload to PyPI
twine upload dist/*
```

### 8. Post-Release Verification

```bash
# Install from PyPI
pip install blart-py==X.Y.Z

# Verify installation
python -c "import blart; print(blart.__version__)"

# Run quick smoke test
python examples/basic_usage.py
```

### 9. Update Documentation

- [ ] Update README.md if needed
- [ ] Update example code if API changed
- [ ] Announce release (if applicable)

### 10. Prepare for Next Development

```bash
# Update CHANGELOG.md with [Unreleased] section
# Commit changes
git add CHANGELOG.md
git commit -m "chore: prepare for next development cycle"
git push origin main
```

## Rollback Process

If a release has critical issues:

### 1. Yank Release from PyPI

```bash
# Mark version as yanked (prevents new installations)
pip install --upgrade twine
twine upload --skip-existing --repository pypi dist/*
# Then use PyPI web interface to yank the version
```

### 2. Delete Git Tag

```bash
# Delete local tag
git tag -d vX.Y.Z

# Delete remote tag
git push --delete origin vX.Y.Z
```

### 3. Delete GitHub Release

- Go to Releases page on GitHub
- Delete the problematic release

### 4. Fix Issues and Re-Release

- Fix the issues
- Increment patch version
- Follow release process again

## GitHub Secrets Configuration

For automated PyPI publishing, configure these secrets in GitHub:

- `PYPI_API_TOKEN`: PyPI API token with upload permissions
  - Create at https://pypi.org/manage/account/token/
  - Scope: Project-level for blart

## Platform-Specific Notes

### Linux (manylinux)

- Built using official manylinux2014 Docker image
- Compatible with most Linux distributions
- Includes statically linked Rust dependencies

### macOS

- Universal2 wheels for both x86_64 and arm64
- Minimum deployment target: macOS 11.0
- Tested on latest macOS versions

### Windows

- 64-bit wheels for x86_64
- Requires Visual C++ runtime (usually pre-installed)
- Tested on Windows Server 2019/2022

## Testing Matrix

Ensure testing on:

| Platform | Python Versions |
|----------|----------------|
| Ubuntu 20.04 | 3.8, 3.9, 3.10, 3.11, 3.12 |
| macOS 12 | 3.8, 3.9, 3.10, 3.11, 3.12 |
| Windows Server 2022 | 3.8, 3.9, 3.10, 3.11, 3.12 |

## Troubleshooting

### Build Fails on CI

- Check Rust version compatibility
- Verify PyO3 version supports target Python
- Check for platform-specific compilation issues
- Review CI logs for specific errors

### Wheel Installation Fails

- Verify wheel is for correct platform/Python version
- Check for missing system dependencies
- Try installing from source (`pip install --no-binary blart-py`)

### Import Errors After Installation

- Ensure all Rust dependencies are statically linked
- Check for missing .so/.dylib/.dll files
- Verify Python version compatibility

## Resources

- [Python Packaging User Guide](https://packaging.python.org/)
- [Maturin Documentation](https://www.maturin.rs/)
- [PyO3 Guide](https://pyo3.rs/)
- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)
