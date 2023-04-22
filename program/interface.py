import tkinter as tk
from tkinter import ttk, colorchooser

from program.fractal import fractalbase

root = None
app = None


def screen_size_selected_event(event):
    from program.settings.settingsbase import screen_settings

    screen_size = list(map(int, event.widget.get().split("x")))
    if screen_settings.get_native_size() != screen_size:
        screen_settings.set_native_size(screen_size)
        app.add_element_to_queue("screen_size")


def downsampling_selected_event(event):
    from program.settings.settingsbase import screen_settings

    downsampling_value = event.widget.get() / 100
    if screen_settings.get_generation_size_optimization() != downsampling_value:
        screen_settings.set_generation_size_optimization(downsampling_value)
        app.add_element_to_queue("update_fractal")


def fractal_selected_event(event):
    from program.settings.settingsbase import fractal_settings

    fractal_selected = fractalbase.get_fractal_type_by_real_name(event.widget.get())
    if fractal_selected.name != fractal_settings.fractal_type:
        fractal_settings.fractal_type = fractal_selected.name
        fractal_settings.save()
        app.add_element_to_queue("fractal")


def sensibility_selected_event(event):
    from program.settings.settingsbase import screen_settings

    sensibility_value = event.widget.get()
    if screen_settings.sensibility != sensibility_value:
        screen_settings.sensibility = sensibility_value
        screen_settings.save()


def filter_color_selected_event():
    from program.settings.settingsbase import screen_settings

    color = colorchooser.askcolor(title="Choisissez une couleur", color=tuple(screen_settings.filter))

    if not color[1]:
        return

    rgb_color_value = color[0]
    if screen_settings.filter != rgb_color_value:
        screen_settings.filter = rgb_color_value
        screen_settings.save()
        app.add_element_to_queue("update_fractal")


def screenshot():
    app.add_element_to_queue("screenshot")


def kill_thread():
    global root
    if root is not None:
        root.quit()
        root = None


def run(app_):
    from program.settings.settingsbase import screen_settings, fractal_settings

    global root, app
    app = app_

    def update_parameters_value():
        screen_size_var.set('x'.join(map(str, screen_settings.get_native_size())))
        slider_generation_optimization.set(screen_settings.get_generation_size_optimization() * 100)
        variable_var.set(fractalbase.get_fractal_by_name(fractal_settings.fractal_type).real_name)
        slider_sensibility.set(screen_settings.sensibility)
        filter_status_button.config(text="Désactiver" if screen_settings.display_filter else "Activer")
        cursor_status_button.config(text="Désactiver le curseur" if screen_settings.display_cursor else "Activer le curseur")

    def reset_settings():
        screen_settings.reset_settings()
        fractal_settings.reset_settings()

        # Update Interface
        update_parameters_value()

        # Update PyGame
        app.add_element_to_queue("screen_size")
        app.add_element_to_queue("fractal")

    def display_filter_event():
        filter_status = not screen_settings.display_filter
        screen_settings.display_filter = filter_status
        screen_settings.save()

        app.add_element_to_queue("update_fractal")

        filter_status_button.config(text="Désactiver" if filter_status else "Activer")

    def display_cursor_event():
        cursor_status = not screen_settings.display_cursor
        screen_settings.display_cursor = cursor_status
        screen_settings.save()

        app.add_element_to_queue("update_fractal")

        cursor_status_button.config(text="Désactiver le curseur" if cursor_status else "Activer le curseur")

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
    screen_size_options = [
        "640x480",
        "800x600",
        "800x800",
        "1024x768",
        "1280x720",
        "1366x768",
        "1600x900",
        "1920x1080",
        "2560x1440",
    ]

    screen_size_var = tk.StringVar()
    screen_size_combobox = ttk.Combobox(fenetre_frame, textvariable=screen_size_var, values=screen_size_options,
                                        state='readonly')
    screen_size_combobox.bind("<<ComboboxSelected>>", screen_size_selected_event)
    screen_size_combobox.pack()

    fenetre_frame.pack(ipady=10)

    # Cadre pour le slider d'optimsation de rendu

    downsampling_frame = ttk.Frame(options_frame)

    # Titre
    label = tk.Label(downsampling_frame, text="Détail Graphique")
    label.pack()

    # Slider
    slider_generation_optimization = tk.Scale(downsampling_frame, from_=1, to=100, resolution=1, orient=tk.HORIZONTAL,
                                              length=150)
    slider_generation_optimization.pack()

    # Ajout d'un gestionnaire d'événement pour détecter le relâchement du curseur du slider
    slider_generation_optimization.bind("<ButtonRelease-3>", downsampling_selected_event)
    slider_generation_optimization.bind("<ButtonRelease-1>", downsampling_selected_event)

    downsampling_frame.pack(ipady=10)

    # Cadre pour le type de fractal

    fractal_frame = ttk.Frame(options_frame)

    # Titre
    label = tk.Label(fractal_frame, text="Fractale")
    label.pack()

    # Liste déroulante pour choisir la variable d'énumération
    variable_options = [fractals.real_name for fractals in fractalbase.FractalType]
    variable_var = tk.StringVar()
    variable_combobox = ttk.Combobox(fractal_frame, textvariable=variable_var, values=variable_options,
                                     state='readonly')
    variable_combobox.bind("<<ComboboxSelected>>", fractal_selected_event)
    variable_combobox.pack()

    fractal_frame.pack(ipady=10)

    # Cadre pour le slider de sensibilité

    sensibility_frame = ttk.Frame(options_frame)

    # Titre
    label = tk.Label(sensibility_frame, text="Sensibilité")
    label.pack()

    # Slider
    slider_sensibility = tk.Scale(sensibility_frame, from_=0, to=10, resolution=0.1, orient=tk.HORIZONTAL, length=150)
    slider_sensibility.pack()

    # Ajout d'un gestionnaire d'événement pour détecter le relâchement du curseur du slider
    slider_sensibility.bind("<ButtonRelease-3>", sensibility_selected_event)
    slider_sensibility.bind("<ButtonRelease-1>", sensibility_selected_event)

    sensibility_frame.pack(ipady=10)

    # Bouton pour réinitialiser les paramètres
    reset_button = ttk.Button(options_frame, text="Réinitialisation des Paramètres", command=reset_settings)
    reset_button.pack(pady=10, ipadx=5)

    # Cadre droit pour les utilitaires
    utilities_frame = ttk.LabelFrame(root, text="Utilitaires")
    utilities_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    # Bouton pour capturer un screenshot
    screenshot_button = ttk.Button(utilities_frame, text="Capture d'écran", command=screenshot)
    screenshot_button.pack(pady=10, ipadx=5)

    filter_frame = ttk.LabelFrame(utilities_frame, text="Filtre")

    # Bouton pour la couleur du filtre

    filter_button = ttk.Button(filter_frame, text="Couleur", command=filter_color_selected_event)
    filter_button.pack(side=tk.LEFT, padx=10, ipadx=5)

    # Bouton pour activer/désactiver le filtre
    filter_status_button = ttk.Button(filter_frame, command=display_filter_event)
    filter_status_button.pack(side=tk.LEFT, padx=10, ipadx=5)

    filter_frame.pack(pady=10, ipady=10)

    # Bouton pour activer/désactiver le curseur
    cursor_status_button = ttk.Button(utilities_frame, command=display_cursor_event)
    cursor_status_button.pack(padx=10, ipadx=5, pady=10)

    # Définition des poids des colonnes pour qu'elles s'adaptent à la fenêtre
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

    update_parameters_value()

    # Lancement de la boucle principale
    root.mainloop()

    root = None
