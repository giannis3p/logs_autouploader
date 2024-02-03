import os
import tkinter as tk
from tkinter import ttk
import webbrowser
import requests
from datetime import datetime

def list_files_recursive(folder_path):
    try:
        for root, _, files in os.walk(folder_path):
            # Display files in the current folder
            files_info = []  # To store file info (path, creation time)
            for file in files:
                file_path = os.path.join(root, file)
                file_creation_time = os.path.getctime(file_path)
                files_info.append((file_path, file_creation_time))
            
            # Sort files based on creation time in reverse order
            files_info.sort(key=lambda x: x[1], reverse=True)
            
            # Display sorted files in the treeview
            for file_path, file_creation_time in files_info:
                formatted_time = datetime.fromtimestamp(file_creation_time).strftime('%Y-%m-%d')
                tree.insert('', 'end', values=(file_path, formatted_time))

    except FileNotFoundError:
        print(f"The specified folder '{folder_path}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

def open_file(event):
    selected_item = tree.selection()[0]
    file_path = tree.item(selected_item, "values")[0]
    
    # Upload the file to DPS Report
    upload_url = upload_to_dps_report(file_path)
    
    if upload_url:
        # Open the browser with the constructed URL
        webbrowser.open(upload_url)

def upload_to_dps_report(file_path):
    try:
        url = 'https://dps.report/uploadContent'
        params = {
            'json': 1,
            'generator': 'ei',  # Assuming you're using Elite Insights
        }
        files = {'file': open(file_path, 'rb')}
        
        response = requests.post(url, params=params, files=files)
        json_response = response.json()
        
        if 'permalink' in json_response:
            return f"https://dps.report/{json_response['permalink']}"
        else:
            print(f"Error uploading file: {json_response.get('error', 'Unknown error')}")
            return None

    except Exception as e:
        print(f"An error occurred during the upload: {e}")
        return None

def search_files(event):
    query = entry.get().lower()
    
    for item in tree.get_children():
        values = tree.item(item, 'values')
        if query in values[0].lower():
            tree.selection_set(item)
            tree.focus(item)
            break

# Create the main window
root = tk.Tk()
root.title("DPS Report Uploader")

# Create an Entry widget for search
entry = tk.Entry(root)
entry.pack(side="top", fill="x", pady=5)
entry.bind("<Return>", search_files)

# Create a Treeview widget
tree = ttk.Treeview(root, columns=("File/Folder", "Date Created"), show="headings")
tree.heading("#1", text="File/Folder")
tree.heading("#2", text="Date Created")

# Set up the Treeview to call open_file when an item is double-clicked
tree.bind("<Double-1>", open_file)

# Create a scrollbar
scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)

# Pack the widgets
tree.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Example: Display files in the specified path recursively
specified_path = r"C:/Users/Ioannis/Documents/Guild Wars 2/addons/arcdps/arcdps.cbtlogs"
list_files_recursive(specified_path)

# Run the main application
root.mainloop()
