import PyInstaller.__main__
import os
import sys

print("Starting H4ck3r File Organizer build process...")

# Get the current directory
current_dir = os.getcwd()

# Icon path
icon_path = os.path.join(current_dir, "directory_documents_files_icon_143305.ico")

# Verify icon exists
if not os.path.exists(icon_path):
    print(f"ERROR: Icon file not found at: {icon_path}")
    sys.exit(1)

print(f"Using icon from: {icon_path}")
print(f"Icon file size: {os.path.getsize(icon_path)} bytes")

# PyInstaller command arguments - with additional imports for customtkinter
args = [
    'main.py',                        # Main script (entry point)
    '--name=H4ck3r_File_Organizer',   # Executable name (no spaces)
    '--onefile',                      # Single file executable
    f'--icon={icon_path}',            # Icon path
    '--noconsole',                    # No console window
    '--clean',                        # Clean build
    '--add-data=%s;.' % icon_path,    # Include icon in the package
    # Hidden imports for customtkinter
    '--hidden-import=customtkinter',
    '--hidden-import=PIL',
    '--hidden-import=PIL._tkinter_finder',
    '--collect-submodules=customtkinter',
]

# Run PyInstaller with less verbose output
print(f"Building executable with PyInstaller...")
PyInstaller.__main__.run(args)

print("Build complete! Look for H4ck3r_File_Organizer.exe in the dist folder.") 