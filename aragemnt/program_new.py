import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from pathlib import Path
import threading
import time
from PIL import Image, ImageTk
import json
import logging
from datetime import datetime
import sys

# Set the appearance mode and default color theme
ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("green")  # Themes: "blue", "green", "dark-blue"

class HackerFileOrganizer:
    def __init__(self, root):
        self.root = root
        self.root.title("H4ck3r File Organizer")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Set theme colors (Dark Node colors)
        self.colors = {
            'primary': '#00FF41',      # Matrix Green
            'secondary': '#00AA00',    # Darker Green
            'background': '#0C0C0C',   # Almost Black
            'background_light': '#1A1A1A',  # Slightly lighter black
            'text': '#00FF41',         # Matrix Green
            'success': '#00CC00',      # Green
            'warning': '#F3FF00',      # Yellow
            'error': '#FF0033',        # Red
            'entry_bg': '#101010',     # Dark Gray
            'stats_bg': '#050505',     # Very Dark Black
            'accent': '#00CF25'        # Light Green
        }
        
        # Configure root window
        self.root.configure(bg=self.colors['background'])
        
        # Load and set the icon using both methods for maximum compatibility
        try:
            icon_path = "directory_documents_files_icon_143305.ico"
            
            # Method 1: Direct iconbitmap (Windows)
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
                print(f"Successfully loaded icon using iconbitmap from {icon_path}")
            
            # Method 2: Using PIL for cross-platform compatibility
            try:
                img = Image.open(icon_path)
                photo_icon = ImageTk.PhotoImage(img)
                self.root.iconphoto(True, photo_icon)
                # Keep a reference to prevent garbage collection
                self.icon_image = photo_icon
                print("Successfully set icon using iconphoto for cross-platform compatibility")
            except Exception as e:
                print(f"Note: Could not set iconphoto: {e}")
                
        except Exception as e:
            print(f"Error loading icon: {e}")
        
        # Initialize default settings first
        default_extension_map = {
            # Videos
            'mp4': 'Videos', 'avi': 'Videos', 'mkv': 'Videos', 'mov': 'Videos', 'wmv': 'Videos',
            'flv': 'Videos', 'webm': 'Videos', 'm4v': 'Videos', '3gp': 'Videos',
            # Audio
            'mp3': 'Audio', 'wav': 'Audio', 'ogg': 'Audio', 'flac': 'Audio', 'aac': 'Audio',
            'm4a': 'Audio', 'wma': 'Audio', 'opus': 'Audio', 'mid': 'Audio', 'midi': 'Audio',
            # Documents
            'pdf': 'Documents/PDF', 
            'doc': 'Documents/Word', 'docx': 'Documents/Word', 'rtf': 'Documents/Word', 'odt': 'Documents/Word',
            'ppt': 'Documents/Presentations', 'pptx': 'Documents/Presentations', 'odp': 'Documents/Presentations',
            'txt': 'Documents/Text', 'md': 'Documents/Text',
            'xls': 'Documents/Spreadsheets', 'xlsx': 'Documents/Spreadsheets', 'csv': 'Documents/Spreadsheets', 'ods': 'Documents/Spreadsheets',
            'epub': 'Documents/EBooks',
            # Adobe Files
            'psd': 'Adobe/Photoshop',  # Photoshop files
            'psb': 'Adobe/Photoshop',  # Large Photoshop files
            'ai': 'Adobe/Illustrator',  # Illustrator files
            'eps': 'Adobe/Illustrator', # Encapsulated PostScript
            'indd': 'Adobe/InDesign',   # InDesign files
            'idml': 'Adobe/InDesign',   # InDesign Markup files
            'prproj': 'Adobe/Premiere', # Premiere Pro projects
            'aep': 'Adobe/After Effects', # After Effects projects
            'aet': 'Adobe/After Effects', # After Effects templates
            'xd': 'Adobe/XD',          # Adobe XD files
            'sesx': 'Adobe/Audition',  # Audition session files
            'aup': 'Adobe/Audition',   # Audition project files
            'fla': 'Adobe/Animate',    # Adobe Animate files
            'swf': 'Adobe/Animate',    # Flash files
            'dng': 'Adobe/Camera Raw', # Digital Negative files
            'bridge': 'Adobe/Bridge',  # Bridge files
            'crw': 'Adobe/Camera Raw', # Canon Raw files
            'cr2': 'Adobe/Camera Raw', # Canon Raw 2 files
            'cr3': 'Adobe/Camera Raw', # Canon Raw 3 files
            'arw': 'Adobe/Camera Raw', # Sony Raw files
            'nef': 'Adobe/Camera Raw', # Nikon Raw files
            # Images
            'jpg': 'Images', 'jpeg': 'Images', 'png': 'Images', 'gif': 'Images', 'bmp': 'Images',
            'svg': 'Images', 'tiff': 'Images', 'tif': 'Images', 'webp': 'Images', 'ico': 'Images',
            # Archives
            'zip': 'Archives', 'rar': 'Archives', '7z': 'Archives', 'tar': 'Archives', 'gz': 'Archives',
            'bz2': 'Archives', 'xz': 'Archives', 'iso': 'Archives',
            # Code
            'py': 'Code', 'java': 'Code', 'cpp': 'Code', 'c': 'Code', 'html': 'Code', 
            'css': 'Code', 'js': 'Code', 'php': 'Code', 'rb': 'Code', 'go': 'Code',
            'json': 'Code', 'xml': 'Code', 'sql': 'Code', 'sh': 'Code', 'bat': 'Code',
            # Executables
            'exe': 'Executables', 'msi': 'Executables', 'app': 'Executables', 'dmg': 'Executables',
            'deb': 'Executables', 'rpm': 'Executables',
            # Fonts
            'ttf': 'Fonts', 'otf': 'Fonts', 'woff': 'Fonts', 'woff2': 'Fonts', 'eot': 'Fonts'
        }
        
        # Pre-initialize settings variables
        self.extension_map = default_extension_map
        self.recursive = tk.BooleanVar(value=True)
        self.create_log = tk.BooleanVar(value=True)
        self.move_unknown = tk.BooleanVar(value=True)
        self.preserve_structure = tk.BooleanVar(value=False)
        
        # Load settings from JSON file
        self.settings_file = "organizer_settings.json"
        self.load_settings()
        
        # Stats
        self.total_files = 0
        self.organized_files = 0
        self.is_organizing = False
        
        # Create UI elements
        self.create_widgets()
        
        # Setup logging
        self.setup_logging()
    
    def load_settings(self):
        """Load settings from JSON file or use defaults"""
        default_settings = {
            "recursive": True,
            "create_log": True,
            "move_unknown": True,
            "preserve_structure": False,
            "extension_map": self.extension_map
        }
        
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    self.settings = json.load(f)
            else:
                self.settings = default_settings
                self.save_settings()
        except Exception as e:
            print(f"Error loading settings: {e}")
            self.settings = default_settings
        
        # Update BooleanVar values from loaded settings
        self.recursive.set(self.settings.get("recursive", True))
        self.create_log.set(self.settings.get("create_log", True))
        self.move_unknown.set(self.settings.get("move_unknown", True))
        self.preserve_structure.set(self.settings.get("preserve_structure", False))
        
        # Set extension map
        self.extension_map = self.settings.get("extension_map", default_settings["extension_map"])
    
    def save_settings(self):
        """Save current settings to JSON file"""
        try:
            # Check if the variables exist before trying to access them
            if hasattr(self, 'recursive') and hasattr(self, 'create_log') and \
               hasattr(self, 'move_unknown') and hasattr(self, 'preserve_structure'):
                settings = {
                    "recursive": self.recursive.get(),
                    "create_log": self.create_log.get(),
                    "move_unknown": self.move_unknown.get(),
                    "preserve_structure": self.preserve_structure.get(),
                    "extension_map": self.extension_map
                }
                with open(self.settings_file, 'w') as f:
                    json.dump(settings, f, indent=4)
            else:
                # If we're saving before the variables are created (e.g., at initialization)
                settings = {
                    "recursive": True,
                    "create_log": True,
                    "move_unknown": True,
                    "preserve_structure": False,
                    "extension_map": self.extension_map
                }
                with open(self.settings_file, 'w') as f:
                    json.dump(settings, f, indent=4)
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def setup_logging(self):
        """Setup logging configuration"""
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        log_file = os.path.join(log_dir, f"organizer_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
    
    def apply_styles(self):
        """Apply modern styling to all widgets"""
        # No need to create a CTk instance or use theme_use with customtkinter
        # customtkinter already uses its own theming system
        
        # Configure common styles with hacker look
        # Note: customtkinter doesn't use ttk styling mechanism, so this won't have an effect
        # The style settings are applied directly to widgets when they're created
        pass
    
    def create_widgets(self):
        """Create and layout all UI widgets"""
        # Setup menu bar
        self.setup_ui()
        
        # Main container with padding
        main_frame = ctk.CTkFrame(self.root, corner_radius=0)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create tabview for tabs (customtkinter's version of notebook)
        self.tabview = ctk.CTkTabview(main_frame, corner_radius=0)
        self.tabview.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.tabview.add("0RG4N1Z3R")
        self.tabview.add("F1L3 TYP3S")
        
        # Set active tab
        self.tabview.set("0RG4N1Z3R")
        
        # Main tab
        main_tab = self.tabview.tab("0RG4N1Z3R")
        
        # Header frame
        header_frame = ctk.CTkFrame(main_tab, fg_color="transparent")
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Logo/Icon section
        logo_frame = ctk.CTkFrame(header_frame, width=70, height=70, fg_color=self.colors['background_light'])
        logo_frame.pack(side=tk.LEFT, padx=(0, 15))
        logo_frame.pack_propagate(False)
        
        # Terminal-like effect
        logo_label = ctk.CTkLabel(logo_frame, text=">_", font=ctk.CTkFont(family="Consolas", size=24, weight="bold"),
                                 text_color=self.colors['primary'])
        logo_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Title and subtitle
        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.pack(side=tk.LEFT, fill=tk.X)
        
        header_label = ctk.CTkLabel(title_frame, 
                               text="H4CK3R F1L3 0RG4N1Z3R", 
                               font=ctk.CTkFont(family="Consolas", size=24, weight="bold"),
                               text_color=self.colors['primary'])
        header_label.pack(anchor=tk.W)
        
        desc_label = ctk.CTkLabel(title_frame, 
                             text="[ Organize your files with hacker precision ]",
                             font=ctk.CTkFont(family="Consolas", size=12))
        desc_label.pack(anchor=tk.W)
        
        # Folder selection section
        folder_frame = ctk.CTkFrame(main_tab)
        folder_frame.pack(fill=tk.X, pady=(0, 15), padx=10)
        
        folder_title = ctk.CTkLabel(folder_frame, 
                                 text="SELECT FOLDER",
                                 font=ctk.CTkFont(family="Consolas", size=14, weight="bold"))
        folder_title.pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        folder_input_frame = ctk.CTkFrame(folder_frame, fg_color="transparent")
        folder_input_frame.pack(fill=tk.X, pady=(5, 10), padx=10)
        
        self.folder_path_var = tk.StringVar()
        folder_entry = ctk.CTkEntry(folder_input_frame, 
                                  textvariable=self.folder_path_var,
                                  height=35,
                                  placeholder_text="Path to folder...")
        folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        browse_button = ctk.CTkButton(folder_input_frame, 
                                    text="Browse",
                                    command=self.browse_folder,
                                    height=35,
                                    font=ctk.CTkFont(family="Consolas", weight="bold"))
        browse_button.pack(side=tk.RIGHT)
        
        # Options section
        options_frame = ctk.CTkFrame(main_tab)
        options_frame.pack(fill=tk.X, pady=(0, 15), padx=10)
        
        options_title = ctk.CTkLabel(options_frame, 
                                  text="OPTIONS",
                                  font=ctk.CTkFont(family="Consolas", size=14, weight="bold"))
        options_title.pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        # Options grid
        options_grid = ctk.CTkFrame(options_frame, fg_color="transparent")
        options_grid.pack(fill=tk.X, pady=(5, 10), padx=10)
        
        # Options columns
        col1_frame = ctk.CTkFrame(options_grid, fg_color="transparent")
        col1_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        col2_frame = ctk.CTkFrame(options_grid, fg_color="transparent")
        col2_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Option checkboxes
        recursive_check = ctk.CTkCheckBox(col1_frame, 
                                      text="Scan subfolders recursively",
                                      variable=self.recursive,
                                      border_width=2,
                                      font=ctk.CTkFont(family="Consolas"))
        recursive_check.pack(anchor=tk.W, pady=8)
        
        unknown_check = ctk.CTkCheckBox(col1_frame, 
                                     text="Move unknown file types to 'Others'",
                                     variable=self.move_unknown,
                                     border_width=2,
                                     font=ctk.CTkFont(family="Consolas"))
        unknown_check.pack(anchor=tk.W, pady=8)
        
        log_check = ctk.CTkCheckBox(col2_frame, 
                                 text="Create log file",
                                 variable=self.create_log,
                                 border_width=2,
                                 font=ctk.CTkFont(family="Consolas"))
        log_check.pack(anchor=tk.W, pady=8)
        
        structure_check = ctk.CTkCheckBox(col2_frame, 
                                       text="Preserve folder structure",
                                       variable=self.preserve_structure,
                                       border_width=2,
                                       font=ctk.CTkFont(family="Consolas"))
        structure_check.pack(anchor=tk.W, pady=8)
        
        # Action buttons
        buttons_frame = ctk.CTkFrame(main_tab, fg_color="transparent")
        buttons_frame.pack(fill=tk.X, pady=(0, 15), padx=10)
        
        organize_button = ctk.CTkButton(buttons_frame, 
                                      text="Organize Files",
                                      command=self.start_organize_thread,
                                      height=40,
                                      font=ctk.CTkFont(family="Consolas", size=14, weight="bold"))
        organize_button.pack(side=tk.LEFT, padx=(0, 15))
        
        self.cancel_button = ctk.CTkButton(buttons_frame, 
                                         text="Cancel",
                                         command=self.cancel_organization,
                                         state=tk.DISABLED,
                                         fg_color=self.colors['error'],
                                         hover_color="#CC0000",
                                         height=40,
                                         font=ctk.CTkFont(family="Consolas", size=14, weight="bold"))
        self.cancel_button.pack(side=tk.LEFT)
        
        # Progress section
        progress_frame = ctk.CTkFrame(main_tab, fg_color="transparent")
        progress_frame.pack(fill=tk.X, pady=(0, 5), padx=10)
        
        progress_label = ctk.CTkLabel(progress_frame, 
                                   text="PROGRESS:",
                                   font=ctk.CTkFont(family="Consolas", size=12, weight="bold"))
        progress_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ctk.CTkProgressBar(progress_frame)
        self.progress_bar.pack(fill=tk.X)
        self.progress_bar.set(0)
        
        # Status section
        status_frame = ctk.CTkFrame(main_tab, fg_color="transparent")
        status_frame.pack(fill=tk.X, pady=(0, 10), padx=10)
        
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_label = ctk.CTkLabel(status_frame, 
                                 textvariable=self.status_var,
                                 font=ctk.CTkFont(family="Consolas", size=12, slant="italic"))
        status_label.pack(anchor=tk.W)
        
        # Stats section
        stats_frame = ctk.CTkFrame(main_tab)
        stats_frame.pack(fill=tk.BOTH, expand=True, padx=10)
        
        stats_header = ctk.CTkLabel(stats_frame, 
                                 text="STATISTICS",
                                 font=ctk.CTkFont(family="Consolas", size=14, weight="bold"))
        stats_header.pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        stats_container = ctk.CTkFrame(stats_frame, fg_color=self.colors['background_light'])
        stats_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        self.stats_text = ctk.CTkTextbox(stats_container, 
                                    font=ctk.CTkFont(family="Consolas", size=12),
                                    activate_scrollbars=True)
        self.stats_text.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Initial stats message
        self.update_stats("Ready to organize files.\n\nSelect a folder and click 'Organize Files' to begin.")
        
        # Create Supported Files tab content
        self.create_supported_files_tab(self.tabview.tab("F1L3 TYP3S"))
    
    def create_supported_files_tab(self, parent):
        """Create the Supported Files tab content"""
        # Main frame for supported files tab
        main_frame = ctk.CTkFrame(parent, fg_color="transparent")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title section
        title_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ctk.CTkLabel(title_frame, 
                               text="< SUPP0RT3D F1L3 TYP3S >",
                               font=ctk.CTkFont(family="Consolas", size=24, weight="bold"),
                               text_color=self.colors['primary'])
        title_label.pack(pady=(0, 5))
        
        subtitle_label = ctk.CTkLabel(title_frame,
                                  text="[ file signatures recognized by the system ]",
                                  font=ctk.CTkFont(family="Consolas", size=12))
        subtitle_label.pack(pady=(0, 5))
        
        # Create a scrollable frame for file types
        scrollable_frame = ctk.CTkScrollableFrame(main_frame)
        scrollable_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create sections for each category
        categories = {}
        for ext, folder in self.extension_map.items():
            category = folder.split('/')[0]
            if category not in categories:
                categories[category] = []
            categories[category].append(ext)
        
        # Display each category with hacker styling
        for category, extensions in sorted(categories.items()):
            # Category frame
            category_frame = ctk.CTkFrame(scrollable_frame)
            category_frame.pack(fill=tk.X, pady=(0, 15), padx=5)
            
            # Category header
            category_label = ctk.CTkLabel(category_frame,
                                      text=f":: {category} ::",
                                      font=ctk.CTkFont(family="Consolas", size=16, weight="bold"),
                                      text_color=self.colors['primary'])
            category_label.pack(anchor=tk.W, padx=10, pady=10)
            
            # Create grid for extensions
            extensions_frame = ctk.CTkFrame(category_frame, fg_color=self.colors['background_light'])
            extensions_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
            
            # Display extensions in a grid layout
            ext_grid = []
            row = 0
            col = 0
            cols_per_row = 4
            
            for ext in sorted(extensions):
                if col >= cols_per_row:
                    col = 0
                    row += 1
                
                ext_label = ctk.CTkLabel(extensions_frame, 
                                     text=f".{ext}",
                                     corner_radius=6,
                                     font=ctk.CTkFont(family="Consolas", size=12),
                                     fg_color=self.colors['background'],
                                     text_color=self.colors['text'])
                ext_label.grid(row=row, column=col, padx=5, pady=5, sticky="w")
                ext_grid.append(ext_label)
                
                col += 1
                
            # Add padding to bottom of grid (for multiple rows of extensions)
            if row > 0:
                padding_label = ctk.CTkLabel(extensions_frame, text="")
                padding_label.grid(row=row+1, column=0, pady=5)
    
    def setup_ui(self):
        """Setup the main UI structure"""
        # Create menu bar (using traditional tkinter as customtkinter doesn't have menus)
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        
        # File menu
        file_menu = tk.Menu(self.menu, tearoff=0, bg=self.colors['background'], fg=self.colors['text'])
        self.menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Browse...", command=self.browse_folder)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Tools menu
        tools_menu = tk.Menu(self.menu, tearoff=0, bg=self.colors['background'], fg=self.colors['text'])
        self.menu.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Apply Theme Changes", command=self.apply_theme_changes)
        
        # Help menu
        help_menu = tk.Menu(self.menu, tearoff=0, bg=self.colors['background'], fg=self.colors['text'])
        self.menu.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
    
    def update_stats(self, message):
        """Update statistics display"""
        self.stats_text.configure(state=tk.NORMAL)
        self.stats_text.delete("0.0", tk.END)
        self.stats_text.insert(tk.END, message)
        self.stats_text.configure(state=tk.DISABLED)
        logging.info(message)
    
    def browse_folder(self):
        """Open folder browser dialog"""
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.folder_path_var.set(folder_path)
            logging.info(f"Selected folder: {folder_path}")
    
    def show_about(self):
        """Show about dialog"""
        messagebox.showinfo(
            "About H4ck3r File Organizer",
            "H4ck3r File Organizer v1.0\n\n"
            "A modern utility for organizing files by type.\n\n"
            "Coded with the hacker aesthetic."
        )
    
    def apply_theme_changes(self):
        """Apply theme changes without restarting the application"""
        try:
            # Toggle between dark and light modes
            if ctk.get_appearance_mode() == "Dark":
                ctk.set_appearance_mode("Light")
                message = "Switched to Light mode"
            else:
                ctk.set_appearance_mode("Dark")
                message = "Switched to Dark mode"
            
            messagebox.showinfo("Theme Applied", f"{message}.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply theme changes: {str(e)}")
    
    def start_organize_thread(self):
        """Start file organization in a separate thread"""
        if self.is_organizing:
            return
        
        folder_path = self.folder_path_var.get()
        if not folder_path:
            messagebox.showerror("Error", "Please select a folder first")
            return
        
        if not os.path.isdir(folder_path):
            messagebox.showerror("Error", "Selected path is not a valid directory")
            return
        
        # Save current settings
        self.save_settings()
        
        # Start organization in a separate thread
        self.is_organizing = True
        self.cancel_button.configure(state=tk.NORMAL)
        
        # Reset progress
        self.progress_bar.set(0)
        self.total_files = 0
        self.organized_files = 0
        
        # Start thread
        self.organize_thread = threading.Thread(target=self.organize_files)
        self.organize_thread.daemon = True
        self.organize_thread.start()
    
    def cancel_organization(self):
        """Cancel the ongoing organization process"""
        if self.is_organizing:
            self.is_organizing = False
            self.status_var.set("Cancelling...")
            logging.info("Organization process cancelled by user")
    
    def organize_files(self):
        """Main file organization logic"""
        folder_path = self.folder_path_var.get()
        recursive = self.recursive.get()
        create_log = self.create_log.get()
        move_unknown = self.move_unknown.get()
        preserve_structure = self.preserve_structure.get()
        
        # Define system folders and files that should not be touched
        system_folders = [
            'Program Files', 'Program Files (x86)', 'Windows', 'System32', 
            'AppData', 'ProgramData', '.git', 'node_modules', 'bin', 'lib',
            'include', 'venv', 'env', '.vscode', '.idea', '__pycache__'
        ]
        
        # Critical file extensions that should not be moved
        critical_extensions = [
            'dll', 'sys', 'ini', 'config', 'exe', 'bat', 'cmd', 'com', 'msi',
            'app', 'jar', 'vbs', 'reg', 'ps1', 'sh'
        ]
        
        log_entries = []
        log_entries.append(f"File Organization Log - {time.strftime('%Y-%m-%d %H:%M:%S')}")
        log_entries.append(f"Root folder: {folder_path}")
        log_entries.append(f"Options: Recursive={recursive}, Move Unknown={move_unknown}, Preserve Structure={preserve_structure}")
        log_entries.append("-" * 80)
        
        try:
            self.status_var.set("Scanning files...")
            self.update_stats("Scanning files...\n")
            
            # First pass: count files for progress bar
            all_files = []
            skipped_files = []
            
            if recursive:
                for root, dirs, files in os.walk(folder_path):
                    # Skip system folders
                    dirs[:] = [d for d in dirs if d not in system_folders and not d.startswith('.')]
                    
                    # Skip category folders we're creating
                    dirs_to_skip = []
                    for d in dirs:
                        dir_path = os.path.join(root, d)
                        rel_dir = os.path.relpath(dir_path, folder_path)
                        
                        if d in set([p.split('/')[0] for p in self.extension_map.values()]) or d == "Others":
                            dirs_to_skip.append(d)
                    
                    dirs[:] = [d for d in dirs if d not in dirs_to_skip]
                    
                    for file in files:
                        file_path = os.path.join(root, file)
                        file_ext = Path(file).suffix.lower().lstrip('.')
                        
                        if file_ext in critical_extensions:
                            skipped_files.append(file_path)
                            continue
                            
                        all_files.append(file_path)
            else:
                for file in os.listdir(folder_path):
                    file_path = os.path.join(folder_path, file)
                    
                    if os.path.isdir(file_path):
                        folder_name = os.path.basename(file_path)
                        if (folder_name in set([p.split('/')[0] for p in self.extension_map.values()]) or 
                            folder_name == "Others" or
                            folder_name in system_folders or
                            folder_name.startswith('.')):
                            continue
                    elif os.path.isfile(file_path):
                        file_ext = Path(file).suffix.lower().lstrip('.')
                        
                        if file_ext in critical_extensions:
                            skipped_files.append(file_path)
                            continue
                            
                        all_files.append(file_path)
            
            self.total_files = len(all_files)
            skipped_count = len(skipped_files)
            
            self.status_var.set(f"Found {self.total_files} files to organize. Skipped {skipped_count} system files.")
            self.update_stats(f"Found {self.total_files} files to organize.\nSkipped {skipped_count} system files for safety.\nStarting organization...\n")
            
            # Create destination folders
            category_folders = set()
            for folder_path_str in self.extension_map.values():
                parts = folder_path_str.split('/')
                for i in range(len(parts)):
                    partial_path = '/'.join(parts[:i+1])
                    category_folders.add(partial_path)
            
            # Create all needed folders
            for folder_name in category_folders:
                folder_dir = os.path.join(folder_path, folder_name)
                if not os.path.exists(folder_dir):
                    os.makedirs(folder_dir)
                    log_entries.append(f"Created category folder: {folder_name}")
            
            # Create "Others" folder for unknown extensions
            if move_unknown:
                others_dir = os.path.join(folder_path, "Others")
                if not os.path.exists(others_dir):
                    os.makedirs(others_dir)
                    log_entries.append(f"Created category folder: Others")
            
            # Process files
            stats_by_category = {}
            
            for i, file_path in enumerate(all_files):
                if not self.is_organizing:
                    break
                
                # Update progress
                progress_percent = (i + 1) / self.total_files
                self.progress_bar.set(progress_percent)
                
                # Skip if it's a directory
                if os.path.isdir(file_path):
                    continue
                
                # Get relative path for preserving structure
                rel_path = os.path.relpath(file_path, folder_path)
                filename = os.path.basename(file_path)
                
                # Get file extension
                file_ext = Path(filename).suffix.lower().lstrip('.')
                
                # Determine destination folder
                if file_ext in self.extension_map:
                    dest_folder = self.extension_map[file_ext]
                    
                    if dest_folder not in stats_by_category:
                        stats_by_category[dest_folder] = 0
                    stats_by_category[dest_folder] += 1
                    
                elif move_unknown:
                    dest_folder = "Others"
                    
                    if "Others" not in stats_by_category:
                        stats_by_category["Others"] = 0
                    stats_by_category["Others"] += 1
                    
                else:
                    continue
                
                # Determine destination path
                if preserve_structure and os.path.dirname(rel_path):
                    rel_dir = os.path.dirname(rel_path)
                    dest_dir = os.path.join(folder_path, dest_folder, rel_dir)
                    if not os.path.exists(dest_dir):
                        os.makedirs(dest_dir)
                else:
                    dest_dir = os.path.join(folder_path, dest_folder)
                
                dest_path = os.path.join(dest_dir, filename)
                
                # Move file if it's not already in the correct folder
                if os.path.dirname(file_path) != dest_dir:
                    # Handle duplicate filenames
                    if os.path.exists(dest_path):
                        base_name, extension = os.path.splitext(filename)
                        counter = 1
                        while os.path.exists(dest_path):
                            new_filename = f"{base_name}_{counter}{extension}"
                            dest_path = os.path.join(dest_dir, new_filename)
                            counter += 1
                    
                    try:
                        # Use copy instead of move for safety
                        shutil.copy2(file_path, dest_path)
                        if os.path.exists(dest_path) and os.path.getsize(dest_path) == os.path.getsize(file_path):
                            os.remove(file_path)
                            self.organized_files += 1
                            log_entries.append(f"Moved: {rel_path} -> {dest_folder}/{os.path.basename(dest_path)}")
                        else:
                            log_entries.append(f"Error: Failed to copy {rel_path} properly")
                        
                        # Update status occasionally
                        if i % 10 == 0 or i == len(all_files) - 1:
                            self.status_var.set(f"Organizing: {i+1}/{self.total_files} files processed")
                            
                            # Update stats display
                            stats_msg = f"Progress: {i+1}/{self.total_files} files processed\n"
                            stats_msg += f"Files organized: {self.organized_files}\n\n"
                            stats_msg += "Files by category:\n"
                            for category, count in stats_by_category.items():
                                stats_msg += f"  {category}: {count} files\n"
                            
                            self.update_stats(stats_msg)
                            
                    except Exception as e:
                        log_entries.append(f"Error moving {rel_path}: {str(e)}")
            
            # Create log file
            if create_log:
                docs_folder = os.path.join(folder_path, "Documents")
                if not os.path.exists(docs_folder):
                    os.makedirs(docs_folder)
                
                logs_folder = os.path.join(docs_folder, "Logs")
                if not os.path.exists(logs_folder):
                    os.makedirs(logs_folder)
                
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                log_filename = f"file_organizer_log_{timestamp}.txt"
                log_path = os.path.join(logs_folder, log_filename)
                
                with open(log_path, 'w', encoding='utf-8') as log_file:
                    log_file.write('\n'.join(log_entries))
            
            # Final status update
            if not self.is_organizing:
                self.status_var.set("Organization cancelled")
                self.update_stats("Organization process was cancelled.\n\n" + 
                                 f"Files organized before cancellation: {self.organized_files} of {self.total_files}")
            else:
                self.status_var.set(f"Done! Organized {self.organized_files} of {self.total_files} files")
                
                # Final stats
                final_stats = f"Organization complete!\n\n"
                final_stats += f"Total files processed: {self.total_files}\n"
                final_stats += f"Files organized: {self.organized_files}\n\n"
                final_stats += "Files by category:\n"
                for category, count in sorted(stats_by_category.items()):
                    final_stats += f"  {category}: {count} files\n"
                
                if create_log:
                    final_stats += f"\nLog file created at:\nDocuments/Logs/{log_filename}"
                
                self.update_stats(final_stats)
                
                messagebox.showinfo("Success", f"Successfully organized {self.organized_files} of {self.total_files} files")
            
        except Exception as e:
            self.status_var.set("Error occurred")
            error_msg = f"An error occurred: {str(e)}"
            self.update_stats(error_msg)
            messagebox.showerror("Error", error_msg)
        
        finally:
            self.is_organizing = False
            self.cancel_button.configure(state=tk.DISABLED)

if __name__ == "__main__":
    # Create ctk root window
    root = ctk.CTk()
    app = HackerFileOrganizer(root)
    root.mainloop() 