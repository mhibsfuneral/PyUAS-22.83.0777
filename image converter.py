import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageFilter

def resize_image(image, target_width):
    original_width, original_height = image.size
    aspect_ratio = original_height / original_width
    target_height = int(target_width * aspect_ratio)
    return image.resize((target_width, target_height), Image.Resampling.LANCZOS)

def enhance_image(image):
    # Meningkatkan kualitas gambar menggunakan filter sharpening
    return image.filter(ImageFilter.SHARPEN)

def process_images():
    if not file_paths:
        messagebox.showerror("Error", "Pilih foto terlebih dahulu.")
        return

    resolution = resolution_var.get()
    output_format = format_var.get()

    if not resolution or not output_format:
        messagebox.showerror("Error", "Pilih resolusi dan format terlebih dahulu.")
        return

    output_dir = filedialog.askdirectory(title="Simpan ke")
    if not output_dir:
        messagebox.showerror("Error", "Pilih lokasi disimpan terlebih dahulu.")
        return

    resolutions = {
        "HD": 1280,
        "FHD": 1920,
        "QHD ": 2560,
        "Ultra HD": 3840,
    }
    target_width = resolutions[resolution]

    try:
        for i, file_path in enumerate(file_paths):
            with Image.open(file_path) as img:
                img_resized = resize_image(img, target_width)
                img_resized = enhance_image(img_resized)

                if output_format == "jpeg" and img_resized.mode == "RGBA":
                    img_resized = img_resized.convert("RGB")

                original_name = os.path.splitext(os.path.basename(file_path))[0]
                output_path = os.path.join(
                    output_dir, f"{original_name} - {resolution} Converted.{output_format}"
                )
                img_resized.save(output_path, output_format.upper())
        messagebox.showinfo("Selesai", f"{len(file_paths)} berhasil dikonversi.")
    except Exception as e:
        messagebox.showerror("Error", f"Ada kesalahan terjadi: {e}")

def add_files():
    global file_paths
    files = filedialog.askopenfilenames(
        title="Pilih gambar",
        filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.svg *.heif *.heic *.webp")]
    )

    total_size = sum(os.path.getsize(f) for f in file_paths) + sum(os.path.getsize(f) for f in files)
    if total_size > 100 * 1024 * 1024:
        messagebox.showerror("Error", "Ukuran total file melebihi 100MB.")
        return

    if len(file_paths) + len(files) > 20:
        messagebox.showerror("Error", "Kamu hanya dapat memilih 20 foto sekaligus.")
        return

    file_paths.extend(files)
    file_listbox.delete(0, tk.END)
    for path in file_paths:
        file_listbox.insert(tk.END, os.path.basename(path))

     # Update status label
    total_size_mb = total_size / (1024 * 1024)
    status_label.config(text=f"Gambar: {len(file_paths)}, Ukuran Total: {total_size_mb:.2f}/100 MB")

def clear_files():
    global file_paths
    file_paths = []
    file_listbox.delete(0, tk.END)
    status_label.config(text="Gambar: 0, Ukuran Total: 0.00/100 MB")

# Initialize main window
root = tk.Tk()
root.title("Image Converter")
root.geometry("600x400")

# Global variables
file_paths = []

# Resolution options
resolution_var = tk.StringVar()
resolution_label = tk.Label(root, text="Pilih Resolusi:")
resolution_label.pack(pady=5)
resolution_menu = ttk.Combobox(root, textvariable=resolution_var)
resolution_menu["values"] = ["HD", "FHD", "QHD", "Ultra HD"]
resolution_menu.pack(pady=5)

# Format options
format_var = tk.StringVar()
format_label = tk.Label(root, text="Pilih format output:")
format_label.pack(pady=5)
format_menu = ttk.Combobox(root, textvariable=format_var)
format_menu["values"] = ["png", "jpeg"]
format_menu.pack(pady=5)

# File listbox
file_listbox = tk.Listbox(root, width=50, height=10)
file_listbox.pack(pady=10)

# Status label
status_label = tk.Label(root, text="Gambar: 0, Ukuran Total: 0.00/100 MB")
status_label.pack(pady=5)

# Buttons
add_button = tk.Button(root, text="Tambahkan Gambar", command=add_files)
add_button.pack(side=tk.LEFT, padx=20, pady=10)

clear_button = tk.Button(root, text="Bersihkan Riwayat", command=clear_files)
clear_button.pack(side=tk.LEFT, padx=20, pady=10)

process_button = tk.Button(root, text="Konversi Gambar", command=process_images)
process_button.pack(side=tk.RIGHT, padx=20, pady=10)

# Run the main loop
root.mainloop()
