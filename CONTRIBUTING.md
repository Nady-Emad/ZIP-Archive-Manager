# Contributing to ZIP Archive Manager

Thank you for your interest in contributing to ZIP Archive Manager!

## How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test your changes thoroughly
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/ZIP-Archive-Manager.git
cd ZIP-Archive-Manager

# Install dependencies
pip install -r requirements.txt

# Run examples to test
python examples.py

# Test CLI
python zip_manager_cli.py --help

# Test GUI
python zip_manager_gui.py
```

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and small
- Write clear commit messages

## Testing

Before submitting a pull request:

1. Test all compression methods (Store, Deflate, BZIP2, LZMA)
2. Test password protection features
3. Test batch operations
4. Test both GUI and CLI interfaces
5. Test on your target platform (Windows/Linux/macOS)

## Reporting Bugs

When reporting bugs, please include:

- Operating system and version
- Python version
- PyQt5 version
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Error messages or screenshots

## Feature Requests

We welcome feature requests! Please:

- Check if the feature already exists
- Clearly describe the feature
- Explain why it would be useful
- Provide examples if possible

## Questions?

Feel free to open an issue for questions or discussions.

Thank you for contributing! 🎉
