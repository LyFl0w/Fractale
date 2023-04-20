import sys
import threading
import tkinter as tk
from tkinter import ttk
from fractal import fractal
from settings.settings import screen_settings

root = None


def screen_size_selected_event(event):
    screen_size = list(map(int, event.widget.get().split("x")))
    if screen_settings.get_native_size() != screen_size:
        screen_settings.set_native_size(screen_size)


def downspampling_selected_event(event):
    downspampling_value = event.widget.get() / 100
    if screen_settings.get_generation_size_optimization() != downspampling_value:
        screen_settings.set_generation_size_optimization(downspampling_value)


def fractal_selected_event(event):
    fractal_selected = fractal.get_fractal_type_by_real_name(event.widget.get())
    print(fractal_selected.name)


# Fonction pour le bouton reset
def reset_parametres():
    screen_settings.reset_settings()


# Fonction pour le bouton screenshot
def capture_screenshot():
    print("Screenshot effectué !")


def on_combobox_selected(event):
    selected_item = event.widget.get()
    print("Variable sélectionnée :", selected_item)


def update_value(event):
    print(f"Valeur sélectionnée : {event.widget.get()}")


def kill_thread():
    global root
    if root is not None:
        root.quit()
        root = None


def run():
    global root
    print("run interface")
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

    # Cadre pour le slider d'optimsation de rendu

    downsampling_frame = ttk.Frame(options_frame)

    # Titre
    label = tk.Label(downsampling_frame, text="Détail Graphique")
    label.pack()

    # Slider
    slider_sensibilite = tk.Scale(downsampling_frame, from_=1, to=100, resolution=1, orient=tk.HORIZONTAL, length=150)
    slider_sensibilite.set(100)
    slider_sensibilite.pack()

    # Ajout d'un gestionnaire d'événement pour détecter le relâchement du curseur du slider
    slider_sensibilite.bind("<ButtonRelease-3>", update_value)
    slider_sensibilite.bind("<ButtonRelease-1>", update_value)

    downsampling_frame.pack(ipady=10)

    # Cadre pour le type de fractal

    fractal_frame = ttk.Frame(options_frame)

    # Titre
    label = tk.Label(fractal_frame, text="Fractale")
    label.pack()

    # Liste déroulante pour choisir la variable d'énumération
    variable_options = [fractals.real_name for fractals in fractal.FractalType]
    variable_var = tk.StringVar()
    variable_var.set(variable_options[0])
    variable_combobox = ttk.Combobox(fractal_frame, textvariable=variable_var, values=variable_options,
                                     state='readonly')
    variable_combobox.bind("<<ComboboxSelected>>", fractal_selected_event)
    variable_combobox.pack()

    fractal_frame.pack(ipady=10)

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

    # Bouton pour réinitialiser les paramètres
    reset_button = ttk.Button(options_frame, text="Réinitialisation des Paramètres", command=reset_parametres)
    reset_button.pack(pady=10, ipadx=5)

    # Cadre droit pour les utilitaires
    utilitaires_frame = ttk.LabelFrame(root, text="Utilitaires")
    utilitaires_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    # Bouton pour capturer un screenshot
    screenshot_button = ttk.Button(utilitaires_frame, text="Capture d'écran", command=capture_screenshot)
    screenshot_button.pack(pady=10, ipadx=5)

    # Définition des poids des colonnes pour qu'elles s'adaptent à la fenêtre
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

    print(threading.get_ident())

    # Lancement de la boucle principale
    root.mainloop()

    root = None
