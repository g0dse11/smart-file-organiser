import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from collections import defaultdict

def get_file_extension(file_name):
    return os.path.splitext(file_name)[1].lower()

def organise_files(directory):
    if not os.path.exists(directory):
        messagebox.showerror("Error", f"The directory '{directory}' does not exist.")
        return
    
    file_types = {
        "Images": {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg'},
        "Documents": {'.pdf', '.doc', '.docx', '.txt', '.xlsx', '.xls', '.pptx', '.csv'},
        "Audio": {'.mp3', '.wav', '.aac', '.flac', '.ogg', '.m4a'},
        "Videos": {'.mp4', '.mov', '.avi', '.mkv', '.wmv', '.flv'},
        "Archives": {'.zip', '.rar', '.tar', '.gz', '.7z'},
        "Code": {'.py', '.java', '.cpp', '.js', '.html', '.css', '.sh', '.rb', '.php', '.go'},
        "Executables": {'.exe', '.msi', '.bat', '.sh', '.apk', '.app'},
        "Others": set()
    }
    
    file_categories = defaultdict(list)
    
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            ext = get_file_extension(file)
            category = next((key for key, exts in file_types.items() if ext in exts), "Others")
            file_categories[category].append(file_path)
    
    for category, files in file_categories.items():
        category_path = os.path.join(directory, category)
        os.makedirs(category_path, exist_ok=True)
        
        for file_path in files:
            try:
                dest_path = os.path.join(category_path, os.path.basename(file_path))
                if os.path.exists(dest_path):
                    base, ext = os.path.splitext(dest_path)
                    counter = 1
                    while os.path.exists(f"{base}_{counter}{ext}"):
                        counter += 1
                    dest_path = f"{base}_{counter}{ext}"
                shutil.move(file_path, dest_path)
            except Exception as e:
                messagebox.showerror("Error", f"Error moving {file_path}: {e}")
    
    messagebox.showinfo("Success", "Files organised successfully!")

def select_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        organise_files(folder_selected)

def main():
    root = tk.Tk()
    root.title("Smart File Organiser")
    root.geometry("400x200")
    
    label = tk.Label(root, text="Select a folder to organise", font=("Arial", 12))
    label.pack(pady=20)
    
    select_button = tk.Button(root, text="Choose Folder", command=select_folder, font=("Arial", 10), padx=10, pady=5)
    select_button.pack()
    
    exit_button = tk.Button(root, text="Exit", command=root.quit, font=("Arial", 10), padx=10, pady=5)
    exit_button.pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    main()
