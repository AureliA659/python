import tkinter as tk
from tkinter import filedialog, simpledialog
from PIL import Image

def adjust_resolution(image_path, output_path, new_width=None, new_height=None, new_dpi=None):
    # Ouvre l'image
    img = Image.open(image_path)

    # Si de nouvelles dimensions sont spécifiées, redimensionne l'image
    if new_width and new_height:
        img = img.resize((new_width, new_height))
    elif new_width:  # Si seule la largeur est spécifiée, ajuste proportionnellement
        ratio = new_width / float(img.width)
        new_height = int(float(img.height) * ratio)
        img = img.resize((new_width, new_height))
    elif new_height:  # Si seule la hauteur est spécifiée, ajuste proportionnellement
        ratio = new_height / float(img.height)
        new_width = int(float(img.width) * ratio)
        img = img.resize((new_width, new_height))

    # Si une nouvelle résolution DPI est spécifiée, l'applique
    if new_dpi:
        img.save(output_path, dpi=(new_dpi, new_dpi))
    else:
        img.save(output_path)

    print(f"Image enregistrée sous {output_path} avec la résolution et taille spécifiées.")

def upload_image():
    # Ouvre une fenêtre pour que l'utilisateur choisisse un fichier
    file_path = filedialog.askopenfilename(title="Sélectionner une image", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.gif;*.bmp")])
    
    if file_path:
        print(f"Image choisie: {file_path}")

        # Demande à l'utilisateur de spécifier la largeur (width) et la hauteur (height)
        new_width = simpledialog.askinteger("Largeur", "Entrez la largeur souhaitée en pixels :")
        new_height = simpledialog.askinteger("Hauteur", "Entrez la hauteur souhaitée en pixels :")

        if new_width is None or new_height is None:
            print("Largeur ou hauteur non spécifiée, annulation du redimensionnement.")
            return

        # Ouvre une fenêtre pour que l'utilisateur choisisse où enregistrer l'image modifiée
        save_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png"), ("BMP", "*.bmp")], title="Enregistrer l'image sous")

        if save_path:
            print(f"Image enregistrée sous : {save_path}")
            # Appelle la fonction de redimensionnement et enregistre l'image
            adjust_resolution(file_path, save_path, new_width=new_width, new_height=new_height, new_dpi=300)
            print("L'image a été redimensionnée et enregistrée.")
        else:
            print("Aucun chemin d'enregistrement sélectionné.")
        
# Création de la fenêtre Tkinter
root = tk.Tk()
root.withdraw()  # Masque la fenêtre principale

# Appelle la fonction d'upload d'image
upload_image()
