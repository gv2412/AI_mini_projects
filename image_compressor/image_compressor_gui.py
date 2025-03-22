import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image
import os
from pathlib import Path
import shutil

class ImageCompressorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Compressor")
        self.root.geometry("600x400")
        self.root.configure(bg="#2C3E50")
        
        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', padding=10, background="#3498DB")
        style.configure('TLabel', background="#2C3E50", foreground="white")
        style.configure('TFrame', background="#2C3E50")
        
        # Main frame
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(padx=20, pady=20, fill='both', expand=True)
        
        # Title
        title_label = tk.Label(
            self.main_frame,
            text="Image Compressor",
            font=("Helvetica", 24, "bold"),
            bg="#2C3E50",
            fg="#ECF0F1"
        )
        title_label.pack(pady=20)
        
        # Input file frame
        self.input_frame = ttk.Frame(self.main_frame)
        self.input_frame.pack(fill='x', pady=10)
        
        self.input_path = tk.StringVar()
        self.input_entry = ttk.Entry(self.input_frame, textvariable=self.input_path, width=50)
        self.input_entry.pack(side='left', padx=5)
        
        self.browse_btn = ttk.Button(
            self.input_frame,
            text="Browse Image",
            command=self.browse_input
        )
        self.browse_btn.pack(side='left', padx=5)
        
        # Target size frame
        self.size_frame = ttk.Frame(self.main_frame)
        self.size_frame.pack(fill='x', pady=10)
        
        ttk.Label(self.size_frame, text="Target Size (KB):").pack(side='left', padx=5)
        self.target_size = tk.StringVar(value="500")
        self.size_entry = ttk.Entry(self.size_frame, textvariable=self.target_size, width=10)
        self.size_entry.pack(side='left', padx=5)
        
        # Compress button
        self.compress_btn = ttk.Button(
            self.main_frame,
            text="Compress Image",
            command=self.compress_image
        )
        self.compress_btn.pack(pady=20)
        
        # Status label
        self.status_label = tk.Label(
            self.main_frame,
            text="",
            bg="#2C3E50",
            fg="#ECF0F1",
            wraplength=500
        )
        self.status_label.pack(pady=10)
        
        # Create download buttons frame
        self.download_frame = ttk.Frame(self.main_frame)
        self.download_frame.pack(fill='x', pady=10)
        
        # Download buttons (initially hidden)
        self.download_btn = ttk.Button(
            self.download_frame,
            text="Save Compressed Image",
            command=self.save_compressed_image
        )
        
        self.quick_download_btn = ttk.Button(
            self.download_frame,
            text="Quick Download",
            command=self.quick_download
        )
        
        self.compressed_image_path = None

    def browse_input(self):
        filename = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )
        if filename:
            self.input_path.set(filename)

    def quick_download(self):
        if not self.compressed_image_path:
            return
            
        # Get default downloads folder
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        filename = os.path.basename(self.compressed_image_path)
        save_path = os.path.join(downloads_path, filename)
        
        try:
            shutil.copy2(self.compressed_image_path, save_path)
            messagebox.showinfo("Success", f"Image downloaded to:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to download: {str(e)}")

    def compress_image(self):
        if not self.input_path.get():
            messagebox.showerror("Error", "Please select an image file!")
            return
            
        try:
            target_size = float(self.target_size.get())
            if target_size <= 0:
                raise ValueError("Target size must be positive")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid target size!")
            return
            
        try:
            # Create temporary file
            input_path = self.input_path.get()
            filename, ext = os.path.splitext(os.path.basename(input_path))
            self.compressed_image_path = os.path.join(os.path.dirname(input_path), f"{filename}_compressed{ext}")
            
            # Compression logic
            img = Image.open(input_path)
            quality = 95
            
            img.save(self.compressed_image_path, quality=quality, optimize=True)
            
            while os.path.getsize(self.compressed_image_path) > target_size * 1024 and quality > 5:
                quality -= 5
                img.save(self.compressed_image_path, quality=quality, optimize=True)
            
            final_size = os.path.getsize(self.compressed_image_path) / 1024
            
            self.status_label.config(
                text=f"Compression complete!\nOriginal size: {os.path.getsize(input_path)/1024:.2f} KB\n"
                     f"Compressed size: {final_size:.2f} KB\nQuality: {quality}"
            )
            
            # Show both download buttons side by side
            self.download_btn.pack(side='left', padx=5)
            self.quick_download_btn.pack(side='left', padx=5)
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def save_compressed_image(self):
        if not self.compressed_image_path:
            return
            
        save_path = filedialog.asksaveasfilename(
            defaultextension=os.path.splitext(self.compressed_image_path)[1],
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")],
            initialfile=os.path.basename(self.compressed_image_path)
        )
        
        if save_path:
            shutil.copy2(self.compressed_image_path, save_path)
            messagebox.showinfo("Success", "Image saved successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageCompressorApp(root)
    root.mainloop()