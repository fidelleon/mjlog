#!/bin/bash
# Build script to compile Qt Designer .ui files to Python

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
UI_DIR="$PROJECT_ROOT/src/mjlog/gui/ui"

echo "Building UI files from Qt Designer..."

cd "$PROJECT_ROOT"

# Compile main_window.ui
echo "  Compiling main_window.ui..."
uv run pyside6-uic "$UI_DIR/main_window.ui" -o "$UI_DIR/main_window_ui.py"

# Compile read_data_window.ui
echo "  Compiling read_data_window.ui..."
uv run pyside6-uic "$UI_DIR/read_data_window.ui" -o "$UI_DIR/read_data_window_ui.py"

echo "✅ All UI files built successfully"
