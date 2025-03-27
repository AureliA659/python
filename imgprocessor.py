import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image

def adjust_resolution(image_path, output_path, new_width=None, new_height=None, new_dpi=None):
    """
    Resize an image to the specified dimensions and save it with the new resolution.
    """
    img = Image.open(image_path)
    
    # Resize the image based on provided dimensions
    if new_width and new_height:
        img = img.resize((new_width, new_height))
    elif new_width:
        ratio = new_width / float(img.width)
        new_height = int(float(img.height) * ratio)
        img = img.resize((new_width, new_height))
    elif new_height:
        ratio = new_height / float(img.height)
        new_width = int(float(img.width) * ratio)
        img = img.resize((new_width, new_height))
    
    # Save the image with the new DPI if specified
    if new_dpi:
        img.save(output_path, dpi=(new_dpi, new_dpi))
    else:
        img.save(output_path)
    
    messagebox.showinfo("Success", f"Image saved in {output_path}")

def change_extension(image_path):
    """
    Change the file extension of the selected image.
    """
    img = Image.open(image_path)
    new_extension = simpledialog.askstring("Change Extension", "Enter the new extension (jpg, png, bmp):")
    
    # Validate the new extension
    if new_extension not in ["jpg", "png", "bmp"]:
        messagebox.showerror("Error", "Unsupported extension.")
        return
    
    # Ask the user where to save the new file
    save_path = filedialog.asksaveasfilename(defaultextension=f".{new_extension}", filetypes=[("Image", f"*.{new_extension}")], title="Save Image As")
    
    if save_path:
        img.save(save_path)
        messagebox.showinfo("Success", f"Image saved as {save_path}")

def open_menu():
    """
    Display a menu for the user to choose an image operation.
    """
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    while True:
        # Display menu options
        choice = simpledialog.askinteger("Menu", "1: Resize Image\n2: Change Image Extension\n3: Exit", minvalue=1, maxvalue=3)
        
        if choice == 1:
            # User selects an image
            file_path = filedialog.askopenfilename(title="Select an image")
            if file_path:
                # Ask for new dimensions
                new_width = simpledialog.askinteger("Width", "Enter the width in pixels:")
                new_height = simpledialog.askinteger("Height", "Enter the height in pixels:")
                
                if new_width and new_height:
                    # Ask where to save the resized image
                    save_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png"), ("BMP", "*.bmp")], title="Save Image As")
                    
                    if save_path:
                        adjust_resolution(file_path, save_path, new_width=new_width, new_height=new_height, new_dpi=300)
        
        elif choice == 2:
            # User selects an image to change its extension
            file_path = filedialog.askopenfilename(title="Select an image")
            if file_path:
                change_extension(file_path)
        
        elif choice == 3:
            # Exit the program
            break

if __name__ == "__main__":
    open_menu()
