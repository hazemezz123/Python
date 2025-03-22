"""
H4ck3r File Organizer - A matrix-themed file organization utility

This is the entry point for the application.
"""

from program_new import HackerFileOrganizer
import customtkinter as ctk

if __name__ == "__main__":
    # Create ctk root window
    root = ctk.CTk()
    app = HackerFileOrganizer(root)
    root.mainloop() 