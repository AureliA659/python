import qrcode
import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser, simpledialog
from PIL import ImageTk, Image

# Valeurs par défaut
qr_color = "black"
bg_color = "white"
logo_path = None
qr_size = 300       # taille finale du QR code en pixels
logo_percent = 20   # pourcentage max de QR code pour le logo

def choose_qr_color():
    global qr_color
    color = colorchooser.askcolor(title="Choisir la couleur du QR code")
    if color[1]:
        qr_color = color[1]
        label_qr_color.config(text=f"Couleur QR: {qr_color}", fg=qr_color)

def choose_bg_color():
    global bg_color
    color = colorchooser.askcolor(title="Choisir la couleur du fond")
    if color[1]:
        bg_color = color[1]
        label_bg_color.config(text=f"Fond: {qr_color}", fg=qr_color)

def choose_logo():
    global logo_path
    logo_path = filedialog.askopenfilename(
        title="Choisir un logo",
        filetypes=[("Images", "*.png;*.jpg;*.jpeg")]
    )
    if logo_path:
        label_logo.config(text=f"Logo: {logo_path.split('/')[-1]}")

def set_qr_size():
    global qr_size
    size = simpledialog.askinteger("Taille QR", "Entrez la taille du QR code (px):", minvalue=100, maxvalue=2000)
    if size:
        qr_size = size
        label_qr_size.config(text=f"Taille QR: {qr_size}px")

def set_logo_percent():
    global logo_percent
    percent = simpledialog.askinteger("Taille logo", "Entrez la taille du logo (% du QR):", minvalue=5, maxvalue=50)
    if percent:
        logo_percent = percent
        label_logo_percent.config(text=f"Taille logo: {logo_percent}%")

def generate_qr():
    global logo_path
    url = entry.get()
    if not url.strip():
        messagebox.showerror("Erreur", "Veuillez entrer une URL")
        return

    filename = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("Fichiers PNG", "*.png")]
    )
    if not filename:
        return

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Fond transparent ou couleur choisie
    if var_transparent.get() == 1:
        img = qr.make_image(fill_color=qr_color, back_color="transparent").convert("RGBA")
    else:
        img = qr.make_image(fill_color=qr_color, back_color=bg_color).convert("RGBA")

    # Redimensionner le QR code à la taille finale
    img = img.resize((qr_size, qr_size), Image.Resampling.LANCZOS)

    # Ajouter un logo si choisi
    if logo_path:
        logo = Image.open(logo_path).convert("RGBA")
        logo_size = int(qr_size * (logo_percent / 100))
        logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
        pos = ((qr_size - logo_size) // 2, (qr_size - logo_size) // 2)
        img.paste(logo, pos, mask=logo)

    img.save(filename)

    # Aperçu
    img_preview = Image.open(filename)
    img_preview.thumbnail((250, 250))
    img_tk = ImageTk.PhotoImage(img_preview)
    label_img.config(image=img_tk)
    label_img.image = img_tk

    messagebox.showinfo("Succès", f"QR code généré et sauvegardé sous :\n{filename}")

# Interface
root = tk.Tk()
root.title("🎨 Générateur QR Code Pro")

frame = tk.Frame(root, padx=20, pady=20)
frame.pack()

label = tk.Label(frame, text="Entrez l'URL :")
label.pack()
entry = tk.Entry(frame, width=50)
entry.pack(pady=5)

# Couleurs QR / fond
btn_color_qr = tk.Button(frame, text="Choisir couleur QR", command=choose_qr_color)
btn_color_qr.pack(pady=2)
label_qr_color = tk.Label(frame, text=f"Couleur QR: {qr_color}", fg=qr_color)
label_qr_color.pack()

btn_color_bg = tk.Button(frame, text="Choisir couleur fond", command=choose_bg_color)
btn_color_bg.pack(pady=2)
label_bg_color = tk.Label(frame, text=f"Fond: {bg_color}", fg=bg_color)
label_bg_color.pack()

# Fond transparent
var_transparent = tk.IntVar()
check_transparent = tk.Checkbutton(frame, text="Fond transparent", variable=var_transparent)
check_transparent.pack(pady=5)

# Logo
btn_logo = tk.Button(frame, text="Choisir un logo", command=choose_logo)
btn_logo.pack(pady=2)
label_logo = tk.Label(frame, text="Aucun logo sélectionné")
label_logo.pack()

# Taille QR
btn_qr_size = tk.Button(frame, text="Définir taille QR code", command=set_qr_size)
btn_qr_size.pack(pady=2)
label_qr_size = tk.Label(frame, text=f"Taille QR: {qr_size}px")
label_qr_size.pack()

# Taille logo
btn_logo_percent = tk.Button(frame, text="Définir taille logo (%)", command=set_logo_percent)
btn_logo_percent.pack(pady=2)
label_logo_percent = tk.Label(frame, text=f"Taille logo: {logo_percent}%")
label_logo_percent.pack()


# Générer
button = tk.Button(frame, text="Générer le QR Code", command=generate_qr)
button.pack(pady=10)

# Bouton Quitter
btn_quit = tk.Button(frame, text="Quitter", command=root.destroy, fg="white", bg="red")
btn_quit.pack(pady=5)

# Aperçu
label_img = tk.Label(frame)
label_img.pack()

root.mainloop()
