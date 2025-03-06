import qrcode
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageEnhance

# Initialize the main window
ctk.set_appearance_mode("dark")  # Cyber theme default
root = ctk.CTk()
root.title("QR Code Generator")
root.geometry("500x600")

# Global Variables
qr_label = None
theme = "cyber"


def generate_qr():
    """Generates a QR code from user input."""
    global qr_label

    text = entry.get().strip()
    if not text:
        status_label.configure(text="Please enter text or a URL!", text_color="red")
        return

    # Choose colors based on theme
    if theme == "cyber":
        fill_color, bg_color = "#00FFFF", "#1A1A1A"  # Neon Blue on Dark
    else:
        fill_color, bg_color = "#FF69B4", "#FFFFFF"  # Pastel Pink on White

    # Create the QR code
    qr = qrcode.QRCode(box_size=10, border=5)
    qr.add_data(text)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color=fill_color, back_color=bg_color)

    # Save and display
    qr_img.save("temp_qr.png")
    display_qr("temp_qr.png")


def display_qr(image_path):
    """Displays the QR code with a fade-in effect."""
    global qr_label

    img = Image.open(image_path)
    img = img.resize((250, 250), Image.LANCZOS)
    qr_photo = ImageTk.PhotoImage(img)

    if qr_label:
        qr_label.destroy()  # Remove the old QR code

    qr_label = ctk.CTkLabel(root, text="")
    qr_label.pack(pady=10)
    
    # Fade-in animation
    alpha = 0.1
    while alpha <= 1:
        img_enhanced = ImageEnhance.Brightness(img).enhance(alpha)
        qr_photo = ImageTk.PhotoImage(img_enhanced)
        qr_label.configure(image=qr_photo)
        qr_label.image = qr_photo
        root.update()
        root.after(50)  # Delay for smooth fade-in
        alpha += 0.1


def save_qr():
    """Saves the generated QR code."""
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
    if file_path:
        img = Image.open("temp_qr.png")
        img.save(file_path)
        status_label.configure(text="QR Code Saved!", text_color="green")


def switch_theme():
    """Switches between Cyber and Minimal themes."""
    global theme
    theme = "minimal" if theme == "cyber" else "cyber"
    root.configure(bg="#FFFFFF" if theme == "minimal" else "#1A1A1A")
    entry.configure(fg_color="#FFFFFF" if theme == "minimal" else "#1A1A1A")
    theme_button.configure(text="Switch to Cyber Theme" if theme == "minimal" else "Switch to Minimal Theme")


# UI Components
entry = ctk.CTkEntry(root, placeholder_text="Enter text or URL...", width=350)
entry.pack(pady=20)

generate_button = ctk.CTkButton(root, text="Generate QR", command=generate_qr)
generate_button.pack(pady=10)

save_button = ctk.CTkButton(root, text="Save QR", command=save_qr)
save_button.pack(pady=10)

theme_button = ctk.CTkButton(root, text="Switch to Minimal Theme", command=switch_theme)
theme_button.pack(pady=10)

status_label = ctk.CTkLabel(root, text="")
status_label.pack(pady=5)

root.mainloop()