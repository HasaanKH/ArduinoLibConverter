import tkinter as tk
from tkinter import filedialog
import os
import zipfile
import re
import tkinter.messagebox as messagebox
import pyperclip


class GUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Arduino library converter')
        self.create_widgets()

    def create_widgets(self):
        # Create a button to select the folder
        select_folder_button = tk.Button(
            self.window, text="Select Folder", command=self.select_folder)
        select_folder_button.pack()

        # Create a text box to display file contents
        self.file_contents_text = tk.Text(self.window)
        self.file_contents_text.pack()

        # Create a button to copy the content to clipboard
        copy_button = tk.Button(
            self.window, text="Copy to Clipboard", command=self.copy_to_clipboard)
        copy_button.pack()

    def select_folder(self):
        folder_path = filedialog.askopenfilename(
            filetypes=[("ALL Files", "*.*")])
        # Perform actions with the selected folder path
        if folder_path:
            # Call the function to find and read the files
            self.read_files(folder_path)

    def read_files(self, folder_path):
        file_contents = "//start " + os.path.basename(folder_path) + "\n"

        # Check if the selected path is a zip file
        if folder_path.endswith(".zip"):
            # Extract the zip file
            with zipfile.ZipFile(folder_path, "r") as archive:
                file_list = list(reversed(archive.namelist()))
                # Read the contents of the .h and .cpp files
                for inner_file in file_list:
                    if inner_file.endswith(".cpp") or inner_file.endswith(".h"):
                        # Read the contents of each file in the archive
                        file_data = archive.read(inner_file).decode("utf-8")
                        # Remove lines starting with '//'
                        file_data = '\n'.join(line for line in file_data.split(
                            '\n') if not line.strip().startswith('//'))
                        # Remove lines enclosed between '/*' and '*/'
                        file_data = re.sub(
                            r'/\*.*?\*/', '', file_data, flags=re.DOTALL)
                        # Remove lines including '#include'
                        file_data = '\n'.join(line for line in file_data.split(
                            '\n') if '#include' not in line)
                        file_contents += file_data + "\n"
        else:
            # Find all files in the folder (including subdirectories)
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    if file.endswith(".h") or file.endswith(".cpp"):
                        # Read the contents of .h and .cpp files
                        with open(file_path, "r") as file_content:
                            file_data = file_content.read()
                            # Remove lines starting with '//'
                            file_data = '\n'.join(line for line in file_data.split(
                                '\n') if not line.strip().startswith('//'))
                            # Remove lines enclosed between '/*' and '*/'
                            file_data = re.sub(
                                r'/\*.*?\*/', '', file_data, flags=re.DOTALL)
                            # Remove lines including '#include'
                            file_data = '\n'.join(line for line in file_data.split(
                                '\n') if '#include' not in line)
                            file_contents += file_data + "\n"

        file_contents += "\n" + "\\end"
        # Update the text box with the file contents
        self.file_contents_text.delete("1.0", tk.END)
        self.file_contents_text.insert(tk.END, file_contents)

    def copy_to_clipboard(self):
        content = self.file_contents_text.get("1.0", tk.END).strip()
        # Remove empty lines
        content = "\n".join(
            line for line in content.split("\n") if line.strip())

        # Check if there is any content in the text box
        if content:
            # Copy the content to the clipboard
            pyperclip.copy(content)
            messagebox.showinfo("Success", "Content copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "No content to copy!")

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    gui = GUI()
    gui.run()
