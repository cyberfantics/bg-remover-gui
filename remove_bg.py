import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from rembg import remove
from PIL import Image, ImageTk
import os
import threading

class BackgroundRemoverApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("SalfiHacker - Background Remover")
        self.geometry("630x500")
        self.configure(bg="#0f0f0f")  # Hackerz theme background color

        # Add Developer Info
        self.dev_info = tk.Label(self, text="Developer: SalfiHacker", bg="#0f0f0f", fg="#00ff00", font=("Consolas", 12))
        self.dev_info.pack(pady=10)

        # Input Folder
        self.input_folder_label = tk.Label(self, text="Select Folder with Images:", bg="#0f0f0f", fg="#00ff00", font=("Consolas", 12))
        self.input_folder_label.pack(pady=10)

        self.input_folder_button = tk.Button(self, text="Browse", command=self.select_input_folder, bg="#00ff00", fg="#0f0f0f", font=("Consolas", 12, "bold"))
        self.input_folder_button.pack(pady=5)

        self.input_folder_path = tk.StringVar()
        self.input_folder_entry = tk.Entry(self, textvariable=self.input_folder_path, width=70, bg="#1a1a1a", fg="#00ff00", font=("Consolas", 12))
        self.input_folder_entry.pack(pady=10)

        # Output Folder
        self.output_folder_label = tk.Label(self, text="Select Output Folder:", bg="#0f0f0f", fg="#00ff00", font=("Consolas", 12))
        self.output_folder_label.pack(pady=10)

        self.output_folder_button = tk.Button(self, text="Browse", command=self.select_output_folder, bg="#00ff00", fg="#0f0f0f", font=("Consolas", 12, "bold"))
        self.output_folder_button.pack(pady=5)

        self.output_folder_path = tk.StringVar()
        self.output_folder_entry = tk.Entry(self, textvariable=self.output_folder_path, width=70, bg="#1a1a1a", fg="#00ff00", font=("Consolas", 12))
        self.output_folder_entry.pack(pady=10)

        # Process Button
        self.process_button = tk.Button(self, text="Remove Background", command=self.remove_background, bg="#00ff00", fg="#0f0f0f", font=("Consolas", 12, "bold"))
        self.process_button.pack(pady=20)

        # Progress Bar
        self.progress = ttk.Progressbar(self, orient="horizontal", length=500, mode="determinate")
        self.progress.pack(pady=20)
        self.progress_label = tk.Label(self, text="", bg="#0f0f0f", fg="#00ff00", font=("Consolas", 12))
        self.progress_label.pack(pady=5)

    def select_input_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.input_folder_path.set(folder_selected)

    def select_output_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.output_folder_path.set(folder_selected)

    def remove_background(self):
        input_folder = self.input_folder_path.get()
        output_folder = self.output_folder_path.get()

        if not input_folder or not output_folder:
            messagebox.showerror("Error", "Please select both input and output folders.")
            return

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        self.progress["value"] = 0
        self.progress["maximum"] = len([name for name in os.listdir(input_folder) if name.lower().endswith(('.png', '.jpg', '.jpeg'))])

        threading.Thread(target=self.process_images, args=(input_folder, output_folder)).start()

    def process_images(self, input_folder, output_folder):
        for i, filename in enumerate(os.listdir(input_folder)):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                input_file = os.path.join(input_folder, filename)
                output_file = os.path.join(output_folder, filename)
                
                try:
                    image = Image.open(input_file)
                    output_image = remove(image)
                    if output_image.mode == 'RGBA':
                        output_image = output_image.convert('RGB')
                    output_image.save(output_file)
                except Exception as e:
                    pass
                
            self.progress["value"] = i + 1
            self.progress_label.config(text=f"Processing: {i + 1}/{self.progress['maximum']}")
            self.update_idletasks()

        messagebox.showinfo("Success", "Background removal completed!")
        self.progress_label.config(text="")

if __name__ == "__main__":
    app = BackgroundRemoverApp()
    app.mainloop()
