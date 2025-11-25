import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image, features
import os

# Activer le support HEIF/HEIC
try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
    HEIF_SUPPORT = True
except ImportError:
    HEIF_SUPPORT = False

def get_supported_extensions():
    """Retourne la liste des extensions supportées par PIL selon l'installation"""
    # Extensions de base toujours supportées
    base_extensions = ['jpg', 'jpeg', 'png', 'bmp', 'gif', 'tiff', 'tif', 'ico']
    
    # Extensions conditionnelles selon les plugins installés
    conditional_extensions = []
    
    # Vérifier le support WebP
    if features.check('webp'):
        conditional_extensions.extend(['webp'])
    
    # Vérifier le support AVIF
    try:
        # Test de création d'une image AVIF
        test_img = Image.new('RGB', (1, 1))
        test_img.save('test.avif', 'AVIF')
        os.remove('test.avif')
        conditional_extensions.extend(['avif'])
    except:
        pass
    
    # Vérifier le support HEIF/HEIC avec le plugin activé
    if HEIF_SUPPORT:
        conditional_extensions.extend(['heif', 'heic'])
    
    # Autres extensions moins courantes
    other_extensions = ['dds', 'eps', 'pcx', 'ppm', 'sgi', 'tga', 'xbm', 'xpm']
    
    all_extensions = base_extensions + conditional_extensions + other_extensions
    return sorted(set(all_extensions))

def get_file_types():
    """Retourne les types de fichiers pour les boîtes de dialogue"""
    supported_ext = get_supported_extensions()
    
    # Construire dynamiquement la liste "All Images"
    all_images_pattern = ";".join([f"*.{ext}" for ext in supported_ext])
    
    file_types = [("All Images", all_images_pattern)]
    
    # Ajouter les types individuels seulement s'ils sont supportés
    if 'jpg' in supported_ext or 'jpeg' in supported_ext:
        file_types.append(("JPEG", "*.jpg;*.jpeg"))
    if 'png' in supported_ext:
        file_types.append(("PNG", "*.png"))
    if 'bmp' in supported_ext:
        file_types.append(("BMP", "*.bmp"))
    if 'gif' in supported_ext:
        file_types.append(("GIF", "*.gif"))
    if 'tiff' in supported_ext or 'tif' in supported_ext:
        file_types.append(("TIFF", "*.tiff;*.tif"))
    if 'webp' in supported_ext:
        file_types.append(("WebP", "*.webp"))
    if 'avif' in supported_ext:
        file_types.append(("AVIF", "*.avif"))
    if 'heif' in supported_ext or 'heic' in supported_ext:
        file_types.append(("HEIF/HEIC", "*.heif;*.heic"))
    if 'ico' in supported_ext:
        file_types.append(("ICO", "*.ico"))
    
    file_types.append(("All Files", "*.*"))
    return file_types

def adjust_resolution(image_path, output_path, new_width=None, new_height=None, new_dpi=None):
    img = Image.open(image_path)
    
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
    
    if new_dpi:
        img.save(output_path, dpi=(new_dpi, new_dpi))
    else:
        img.save(output_path)
    
    messagebox.showinfo("Success", f"Image saved in {output_path}")

def change_extension(image_path):
    try:
        img = Image.open(image_path)
    except Exception as e:
        messagebox.showerror("Error", f"Could not open image: {e}\nMake sure pillow-heif is installed for HEIC support")
        return
    
    # Afficher toutes les extensions supportées
    supported_ext = get_supported_extensions()
    ext_list = ", ".join(supported_ext)
    
    new_extension = simpledialog.askstring(
        "Change Extension",
        f"Enter the new extension:\nSupported: {ext_list}"
    )

    if not new_extension:
        return
    
    # Nettoyer l'extension (enlever le point s'il y en a un)
    new_extension = new_extension.lower().strip('.')
    
    if new_extension not in supported_ext:
        messagebox.showerror("Error", f"Unsupported extension: {new_extension}\nInstall required plugins for AVIF/HEIF support")
        return

    save_path = filedialog.asksaveasfilename(
        defaultextension=f".{new_extension}",
        filetypes=get_file_types(),
        title="Save Image As"
    )

    if save_path:
        try:
            if new_extension == "ico":
                img = img.convert("RGBA")
                sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
                img.save(save_path, format="ICO", sizes=sizes)
            elif new_extension in ["jpg", "jpeg"]:
                # JPEG ne supporte pas la transparence
                if img.mode in ("RGBA", "LA", "P"):
                    img = img.convert("RGB")
                img.save(save_path, format="JPEG", quality=95)
            elif new_extension == "webp":
                img.save(save_path, format="WebP", quality=95, lossless=False)
            elif new_extension == "avif":
                # Vérifier si AVIF est vraiment supporté
                if new_extension not in get_supported_extensions():
                    raise Exception("AVIF format not supported. Install pillow-avif-plugin")
                img.save(save_path, format="AVIF", quality=95)
            elif new_extension in ["heif", "heic"]:
                # Pour HEIF, on sauvegarde en JPEG car pillow-heif ne supporte que la lecture
                if img.mode in ("RGBA", "LA", "P"):
                    img = img.convert("RGB")
                img.save(save_path, format="JPEG", quality=95)
                messagebox.showinfo("Info", "HEIC files are converted to JPEG for saving")
            else:
                img.save(save_path)
            
            messagebox.showinfo("Success", f"Image saved as {save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save image: {e}")

def create_favicon(image_path):
    try:
        img = Image.open(image_path).convert("RGBA")
        sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        save_path = filedialog.asksaveasfilename(
            defaultextension=".ico",
            filetypes=[("ICO file", "*.ico")],
            title="Save favicon as"
        )
        if save_path:
            # Créer des versions redimensionnées de l'image
            resized_images = []
            for size in sizes:
                resized_img = img.resize(size, Image.Resampling.LANCZOS)
                resized_images.append(resized_img)
            
            # Sauvegarder avec toutes les tailles
            img.save(save_path, format="ICO", sizes=sizes, append_images=resized_images)
            
            messagebox.showinfo("Favicon Created", f"Favicon saved as {save_path}\nWith sizes: {sizes}")
    except Exception as e:
        messagebox.showerror("Error", f"Could not create favicon: {e}")

def close_app(root):
    print("Closing the application...")
    root.quit()
    root.destroy()

def open_menu():
    root = tk.Tk()
    root.withdraw()

    root.title("Image Editor Menu")
    root.geometry("300x150")
    root.protocol("WM_DELETE_WINDOW", lambda: close_app(root))

    while True:
        choice = simpledialog.askinteger(
            "Menu",
            "1: Resize Image\n2: Change Image Extension\n3: Create Favicon (.ico)\n4: Exit",
            minvalue=1,
            maxvalue=4,
            parent=root
        )
        
        if choice == 1:
            file_path = filedialog.askopenfilename(
                title="Select an image", 
                filetypes=get_file_types(),
                parent=root
            )
            if file_path:
                new_width = simpledialog.askinteger("Width", "Enter the width in pixels:", parent=root)
                new_height = simpledialog.askinteger("Height", "Enter the height in pixels:", parent=root)
                
                if new_width and new_height:
                    save_path = filedialog.asksaveasfilename(
                        defaultextension=".jpg",
                        filetypes=get_file_types(),
                        title="Save Image As",
                        parent=root
                    )
                    if save_path:
                        adjust_resolution(file_path, save_path, new_width=new_width, new_height=new_height, new_dpi=300)

        elif choice == 2:
            file_path = filedialog.askopenfilename(
                title="Select an image", 
                filetypes=get_file_types(),
                parent=root
            )
            if file_path:
                change_extension(file_path)

        elif choice == 3:
            file_path = filedialog.askopenfilename(
                title="Select an image", 
                filetypes=get_file_types(),
                parent=root
            )
            if file_path:
                create_favicon(file_path)

        elif choice == 4:
            close_app(root)
            break

if __name__ == "__main__":
    open_menu()
