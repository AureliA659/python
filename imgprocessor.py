import tkinter as tk
from tkinter import filedialog, simpledialog
from PIL import Image

def adjust_resolution(image_path, output_path, new_width=None, new_height=None, new_dpi=None):
    # Open img 
    img = Image.open(image_path)

    # if new sizes are specified, resize the image
    if new_width and new_height:
        img = img.resize((new_width, new_height))
    elif new_width:  # If only width is specified, adjust proportionally
        ratio = new_width / float(img.width)
        new_height = int(float(img.height) * ratio)
        img = img.resize((new_width, new_height))
    elif new_height:  # If only height is specified, adjust proportionally
        ratio = new_height / float(img.height)
        new_width = int(float(img.width) * ratio)
        img = img.resize((new_width, new_height))

    # If new DPI is specified, save the image with the new DPI
    if new_dpi:
        img.save(output_path, dpi=(new_dpi, new_dpi))
    else:
        img.save(output_path)

    print(f"Image saved in {output_path} with size {new_width}x{new_height} and DPI {new_dpi}")

def upload_image():
    # Open a file dialog to select an image
    file_path = filedialog.askopenfilename(title="Select an image", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.gif;*.bmp")])
    
    if file_path:
        print(f"Image selected: {file_path}")

        # Ask the user for the new dimensions
        new_width = simpledialog.askinteger("Width", "Enter the width in pixels :")
        new_height = simpledialog.askinteger("Height", "Enter the heigth in pixels :")

        if new_width is None or new_height is None:
            print("Width or height not specified.")
            return

        # Open a file dialog to select the save path
        save_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png"), ("BMP", "*.bmp")], title="Enregistrer l'image sous")

        if save_path:
            print(f"Image saved in : {save_path}")
            # Call the function to adjust the resolution
            adjust_resolution(file_path, save_path, new_width=new_width, new_height=new_height, new_dpi=300)
            print("The image has been saved.")
        else:
            print("No path selected.")
        
# Create the tkinder window
root = tk.Tk()
root.withdraw()  # Hide the main window

# Call the function to upload an image
upload_image()
