# VS Code Configuration for Arduino Development

This folder contains VS Code configuration files that enable IntelliSense support for Arduino development.

## Files Overview

### `c_cpp_properties.json`
Configures C/C++ IntelliSense for Arduino development with support for multiple installation types:

#### Arduino Installation Paths Supported:
- **Program Files (x86)**: Arduino IDE installed for all users (32-bit location)
- **Program Files**: Arduino IDE installed for all users (64-bit location)
- **AppData/Local/Arduino15**: Arduino packages (user installation via Board Manager)

#### Arduino Libraries Paths:
- **Program Files/Arduino/libraries**: System-wide libraries (all users installation)
- **Documents/Arduino/libraries**: User libraries (English Windows)
- **OneDrive/Documentos/Arduino/libraries**: OneDrive synced libraries (Portuguese Windows)

### `arduino.json`
Arduino-specific configuration:
- **Board**: Arduino Uno (arduino:avr:uno)
- **CPU**: ATmega328P
- **Sketch folder**: arduino/examples/
- **Build output**: ../build

### `settings.json`
VS Code workspace settings including GitHub Copilot configuration.

## How It Works

When you open this project in VS Code:

1. **Automatic Configuration Selection**: VS Code will use the "Arduino" configuration when editing `.ino` files
2. **IntelliSense Support**: You'll get autocomplete for Arduino functions like `Serial.begin()`, `digitalWrite()`, etc.
3. **Error Detection**: Real-time syntax checking and error highlighting
4. **Library Recognition**: Both the custom `SerialInputMonitor.h` and standard Arduino libraries are recognized

## Switching Configurations

To manually switch between configurations:
1. Press `Ctrl+Shift+P`
2. Type "C/C++: Select a Configuration"
3. Choose "Arduino" for `.ino` files or "Win32" for other C++ files

## Troubleshooting

If IntelliSense isn't working:

1. **Check Arduino Installation**: Ensure Arduino IDE is installed in one of the supported locations
2. **Refresh IntelliSense**: Press `Ctrl+Shift+P` → "C/C++: Reset IntelliSense Database"
3. **Verify Configuration**: Check that you're using the "Arduino" configuration for `.ino` files

## Path Variables Used

- `${workspaceFolder}`: The root folder of this project
- `${env:USERPROFILE}`: Current user's profile folder (e.g., C:/Users/YourName)
- `**`: Recursive folder search pattern

This configuration ensures the project works across different Arduino installations and Windows setups!
