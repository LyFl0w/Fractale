import tkinter as tk
from tkinter import ttk


# Fonction pour le bouton screenshot
def capture_screenshot():
    print("Screenshot effectué !")


# Fonction pour le bouton reset
def reset_parametres():
    print("Paramètres réinitialisés!")


def on_combobox_selected(event):
    selected_item = event.widget.get()
    print("Variable sélectionnée :", selected_item)


def update_value(event):
    print(f"Valeur sélectionnée : {event.widget.get()}")


# Création de la fenêtre
root = tk.Tk()
root.title("Paramètres")
root.geometry("680x380")
root.resizable(False, False)

# Cadre gauche pour les options
options_frame = ttk.LabelFrame(root, text="Options")
options_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")


# Cadre pour les paramètres de la taille de fenetre
fenetre_frame = ttk.Frame(options_frame)

# Titre
label = tk.Label(fenetre_frame, text="Taille de fenêtre")
label.pack()

# Liste déroulante pour choisir la taille de la fenêtre
taille_options = [
    "640x480",
    "800x600",
    "1024x768",
    "1280x720",
    "1366x768",
    "1600x900",
    "1920x1080",
    "2560x1440",
]

taille_var = tk.StringVar()
taille_combobox = ttk.Combobox(fenetre_frame, textvariable=taille_var, values=taille_options, state='readonly')
taille_var.set(taille_options[0])
taille_combobox.bind("<<ComboboxSelected>>", on_combobox_selected)
taille_combobox.pack()

fenetre_frame.pack(ipady=10)


# Cadre pour le type de fractale

fractale_frame = ttk.Frame(options_frame)

# Titre
label = tk.Label(fractale_frame, text="Fractale")
label.pack()

# Liste déroulante pour choisir la variable d'énumération
variable_options = ["Sponge Cube", "Triangle"]
variable_var = tk.StringVar()
variable_var.set(variable_options[0])
variable_combobox = ttk.Combobox(fractale_frame, textvariable=variable_var, values=variable_options, state='readonly')
variable_combobox.bind("<<ComboboxSelected>>", on_combobox_selected)
variable_combobox.pack()

fractale_frame.pack(ipady=10)


# Cadre pour le slider de sensibilité

sensibilite_frame = ttk.Frame(options_frame)

# Titre
label = tk.Label(sensibilite_frame, text="Sensibilité")
label.pack()

# Slider
slider_sensibilite = tk.Scale(sensibilite_frame, from_=0, to=10, resolution=0.1, orient=tk.HORIZONTAL, length=150)
slider_sensibilite.set(5)
slider_sensibilite.pack()

# Ajout d'un gestionnaire d'événement pour détecter le relâchement du curseur du slider
slider_sensibilite.bind("<ButtonRelease-3>", update_value)
slider_sensibilite.bind("<ButtonRelease-1>", update_value)

sensibilite_frame.pack(ipady=10)


# Cadre pour le slider pour la puissance du zoom

zoom_frame = ttk.Frame(options_frame)

# Titre
label = tk.Label(zoom_frame, text="Puissance du zoom")
label.pack()

# Slider
slider_zoom = tk.Scale(zoom_frame, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL, length=150)
slider_zoom.set(0.5)
slider_zoom.pack()

# Ajout d'un gestionnaire d'événement pour détecter le relâchement du curseur du slider
slider_zoom.bind("<ButtonRelease-3>", update_value)
slider_zoom.bind("<ButtonRelease-1>", update_value)

zoom_frame.pack(ipady=10)


# Bouton pour réinitialiser les paramètres
reset_button = ttk.Button(options_frame, text="Reset Paramètres", command=reset_parametres)
reset_button.pack(pady=10)


# Cadre droit pour les utilitaires
utilitaires_frame = ttk.LabelFrame(root, text="Utilitaires")
utilitaires_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# Bouton pour capturer un screenshot
screenshot_button = ttk.Button(utilitaires_frame, text="Capture d'écran", command=capture_screenshot)
screenshot_button.pack(pady=10)

# Définition des poids des colonnes pour qu'elles s'adaptent à la fenêtre
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)


# Lancement de la boucle principale
root.mainloop()
