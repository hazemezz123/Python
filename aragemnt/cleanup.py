import os
import shutil
import glob

def clean_directory():
    """Clean up the project directory to prepare for GitHub upload."""
    print("Starting cleanup...")
    
    # Files to keep (everything else will be considered for deletion)
    files_to_keep = [
        "program_new.py",
        "directory_documents_files_icon_143305.ico",
        "README.md",
        "screenshot.png",
        "build.py",
        "organizer_settings.json",
        "cleanup.py",  # Keep this script
        ".git",        # Keep git directory if exists
        ".gitignore"   # Keep gitignore if exists
    ]
    
    # Directories to delete
    dirs_to_delete = [
        "build",
        "dist",
        "logs",
        "__pycache__"
    ]
    
    # Delete all .spec files
    print("Removing .spec files...")
    for spec_file in glob.glob("*.spec"):
        try:
            os.remove(spec_file)
            print(f"  Deleted: {spec_file}")
        except Exception as e:
            print(f"  Error deleting {spec_file}: {e}")
    
    # Delete specific directories
    print("\nRemoving directories...")
    for dir_name in dirs_to_delete:
        if os.path.exists(dir_name):
            try:
                shutil.rmtree(dir_name)
                print(f"  Deleted directory: {dir_name}/")
            except Exception as e:
                print(f"  Error deleting directory {dir_name}: {e}")
    
    # Delete other files not in the keep list
    print("\nRemoving other unnecessary files...")
    for item in os.listdir('.'):
        if os.path.isfile(item) and item not in files_to_keep and not item.startswith('.'):
            try:
                os.remove(item)
                print(f"  Deleted: {item}")
            except Exception as e:
                print(f"  Error deleting {item}: {e}")
    
    # Create .gitignore file if it doesn't exist
    if not os.path.exists('.gitignore'):
        print("\nCreating .gitignore file...")
        with open('.gitignore', 'w') as f:
            f.write("# Python cache files\n")
            f.write("__pycache__/\n")
            f.write("*.py[cod]\n")
            f.write("*$py.class\n\n")
            f.write("# Distribution / packaging\n")
            f.write("dist/\n")
            f.write("build/\n")
            f.write("*.spec\n\n")
            f.write("# Logs and local settings\n")
            f.write("logs/\n")
        print("  Created .gitignore file")
    
    print("\nCleanup complete! The project is now ready for GitHub.")
    print("Remember to create a GitHub repository and push your code.")
    print("Basic git commands:\n")
    print("  git init")
    print("  git add .")
    print("  git commit -m 'Initial commit'")
    print("  git branch -M main")
    print("  git remote add origin https://github.com/your-username/h4ck3r-file-organizer.git")
    print("  git push -u origin main")

if __name__ == "__main__":
    clean_directory() 