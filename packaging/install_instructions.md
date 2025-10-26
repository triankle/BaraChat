# Packaging and Distribution

## Building Standalone Executables

### For Windows

```bash
# Install PyInstaller
pip install pyinstaller

# Build the executable
pyinstaller packaging/build.spec

# The executable will be in dist/
```

### For macOS/Linux

```bash
# Install PyInstaller
pip install pyinstaller

# Build the executable
pyinstaller packaging/build.spec

# The executable will be in dist/
```

## Distribution

1. Test the executable locally
2. Package with the server executable
3. Create installer (Inno Setup for Windows, DMG for macOS)

## Requirements

- Python 3.11+
- All dependencies from requirements.txt
- Qt runtime libraries (included by PyInstaller)

