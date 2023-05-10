#                                                                               
#  Fracteur Copyright (c) 2023 LyFlow and Florely
#  This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
#  This is free software, and you are welcome to redistribute it under certain conditions; type `show c' for details.
#                                                                               


import time
import tkinter as tk
from tkinter import ttk, colorchooser

from program.fractal import fractalbase
from program.fractal.fractalbase import FractalType

root = None
app = None

entry_x, entry_y, entry_z = None, None, None
slider_iteration = None
sensibility_fractal_power_julia_c_frame, fractal_power_frame, fractal_c_frame = None, None, None
entry_cx, entry_cy = None, None
fractal_power_slider = None


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
        app.add_element_to_queue("downsampling")


def fractal_selected_event(event):
    from program.settings.settingsbase import fractal_settings

    fractal_selected = fractalbase.get_fractal_type_by_real_name(event.widget.get())
    if fractal_selected.name != fractal_settings.fractal_type:
        fractal_settings.fractal_type = fractal_selected.name
        fractal_settings.save()
        app.add_element_to_queue("fractal")
        update_fractal_type(fractal_selected.name)


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


def iteration_selected_event(event):
    from program.settings.settingsbase import fractal_settings

    new_iteration = event.widget.get()

    if new_iteration != fractal_settings.iteration:
        fractal_settings.iteration = event.widget.get()
        fractal_settings.save()

        app.add_element_to_queue("update_fractal")


def update_fractal_power(event):
    from program.settings.settingsbase import fractal_settings

    new_fractal_power = event.widget.get()

    if new_fractal_power != fractal_settings.fractal_power:
        fractal_settings.fractal_power = new_fractal_power
        fractal_settings.save()
        app.add_element_to_queue("update_fractal")


def teleport_position_event():
    app.fractal_manager.center = [float(entry_x.get()), float(entry_y.get())]
    app.fractal_manager.zoom = max(0.001, float(entry_z.get()))
    app.add_element_to_queue("update_fractal")


def update_iteration(fractal_type):
    from program.settings.settingsbase import fractal_settings

    if slider_iteration is None:
        return

    slider_iteration.set(fractal_settings.iteration)
    slider_iteration.config(from_=fractal_type.iteration_min, to=fractal_type.iteration_max)


def validate_float(msg, value):
    if value.count(".") > 1:
        return False

    if (msg == "-" and value[0] != "-") or value.count("-") > 1:
        return False

    check = " .-0123456789"
    for char in msg:
        if char not in check:
            return False
    return True


def update_c_julia_value(*args):
    from program.settings.settingsbase import fractal_settings

    def isBlank(myString):
        return not (myString and myString.strip())

    if isBlank(entry_cx.get()) or entry_cx.get() == "-":
        entry_cx.config(textvariable=tk.DoubleVar(value=0))

    if isBlank(entry_cy.get()) or entry_cy.get() == "-":
        entry_cy.config(textvariable=tk.DoubleVar(value=0))

    c = [float(entry_cx.get()), float(entry_cy.get())]

    if fractal_settings.c != c:
        fractal_settings.c = c
        fractal_settings.save()
        app.add_element_to_queue("update_fractal")


def update_c_entries():
    if entry_cx is None:
        return

    from program.settings.settingsbase import fractal_settings

    cx, cy = fractal_settings.c
    entry_cx.config(textvariable=tk.DoubleVar(value=cx))
    entry_cy.config(textvariable=tk.DoubleVar(value=cy))


def update_fractal_type(fractal_name):
    global fractal_power_frame, fractal_c_frame, sensibility_fractal_power_julia_c_frame, entry_cx, entry_cy

    if sensibility_fractal_power_julia_c_frame is None:
        return

    from program.settings.settingsbase import fractal_settings

    if fractal_name == FractalType.MANDELBROT.name:
        fractal_power_frame = ttk.Frame(sensibility_fractal_power_julia_c_frame)

        # Titre
        label_power = tk.Label(fractal_power_frame, text="Puissance de la Fractale")
        label_power.pack()

        # Slider
        fractal_power_slider = tk.Scale(fractal_power_frame, from_=2, to=50, resolution=1, orient=tk.HORIZONTAL,
                                        length=150)
        fractal_power_slider.set(fractal_settings.fractal_power)
        fractal_power_slider.pack()

        # Ajout d'un gestionnaire d'événement pour détecter le relâchement du curseur du slider
        fractal_power_slider.bind("<ButtonRelease-3>", update_fractal_power)
        fractal_power_slider.bind("<ButtonRelease-1>", update_fractal_power)

        fractal_power_frame.grid(row=0, column=1, sticky=tk.W, padx=5)

        fractal_power_slider.set(fractal_settings.fractal_power)
    elif fractal_power_frame is not None:
        fractal_power_frame.destroy()

    if fractal_name == FractalType.JULIA.name:

        fractal_c_frame = ttk.Frame(sensibility_fractal_power_julia_c_frame)

        # Titre
        label_c = tk.Label(fractal_c_frame, text="Valeur donnée de C")
        label_c.pack(pady=8)

        position_c_frame = ttk.Frame(fractal_c_frame)

        # Fonction de validation enregistrée pour les zones de saisie
        float_validation_c = fractal_c_frame.register(validate_float)

        # Zone de saisie pour x
        label_cx = tk.Label(position_c_frame, text="c = ")
        label_cx.grid(row=0, column=0, sticky=tk.W)
        entry_cx = tk.Entry(position_c_frame, validate="key",
                            validatecommand=(float_validation_c, "%S", "%P"), width=15)
        entry_cx.grid(row=0, column=1, sticky=tk.W, pady=2)

        entry_cy = tk.Entry(position_c_frame, validate="key",
                            validatecommand=(float_validation_c, "%S", "%P"), width=15)
        entry_cy.grid(row=0, column=2, sticky=tk.W, pady=2)

        # Zone de saisie pour y
        label_cy = tk.Label(position_c_frame, text="i")
        label_cy.grid(row=0, column=3, sticky=tk.W)

        entry_cx.bind('<KeyRelease>', update_c_julia_value)
        entry_cy.bind('<KeyRelease>', update_c_julia_value)

        update_c_entries()

        position_c_frame.pack(pady=12)

        fractal_c_frame.grid(row=0, column=1, sticky=tk.W, padx=5)

    elif fractal_c_frame is not None:
        fractal_c_frame.destroy()


def kill_thread():
    global root
    if root is not None:
        root.quit()
        root = None


def run(app_):
    from program.settings.settingsbase import screen_settings, fractal_settings

    global root, app, entry_x, entry_y, entry_z, slider_iteration, sensibility_fractal_power_julia_c_frame, \
        fractal_power_frame, fractal_c_frame, entry_cx, entry_cy, fractal_power_slider
    app = app_

    def update_position_entries():
        entry_x.config(textvariable=tk.DoubleVar(value=app.fractal_manager.center[0]))
        entry_y.config(textvariable=tk.DoubleVar(value=app.fractal_manager.center[1]))
        entry_z.config(textvariable=tk.DoubleVar(value=app.fractal_manager.zoom))

    def update_parameters_value():
        screen_size_var.set('x'.join(map(str, screen_settings.get_native_size())))
        slider_generation_optimization.set(screen_settings.get_generation_size_optimization() * 100)
        variable_var.set(fractalbase.get_fractal_by_name(fractal_settings.fractal_type).real_name)
        slider_sensibility.set(screen_settings.sensibility)
        filter_status_button.config(text="Désactiver" if screen_settings.display_filter else "Activer")
        cursor_status_button.config(
            text="Désactiver le curseur" if screen_settings.display_cursor else "Activer le curseur")

        fractal_type = fractalbase.get_fractal_by_name(fractal_settings.fractal_type)
        slider_iteration.config(from_=fractal_type.iteration_min, to=fractal_type.iteration_max)
        slider_iteration.set(fractal_settings.iteration)

        if fractal_power_slider is not None:
            fractal_power_slider.set(fractal_settings.fractal_power)

    def reset_settings():
        fractal_settings.reset_settings()
        screen_settings.reset_settings()

        # Update Interface
        update_parameters_value()

        update_fractal_type(fractal_settings.fractal_type)

        # Update PyGame
        app.add_element_to_queue("fractal")
        app.add_element_to_queue("screen_size")

        time.sleep(1)

        update_position_entries()

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
    options_fenetre_frame = ttk.Frame(options_frame)

    fenetre_frame = ttk.Frame(options_fenetre_frame)

    # Titre
    label = tk.Label(fenetre_frame, text="Taille de fenêtre")
    label.pack(ipady=8)

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
    screen_size_combobox.pack(pady=10)

    fenetre_frame.grid(row=0, column=0, sticky=tk.W, padx=5)

    # Cadre pour le slider d'optimsation de rendu

    downsampling_frame = ttk.Frame(options_fenetre_frame)

    # Titre
    label = tk.Label(downsampling_frame, text="Détail Graphique")
    label.pack()

    # Slider
    slider_generation_optimization = tk.Scale(downsampling_frame, from_=1, to=250, resolution=1, orient=tk.HORIZONTAL,
                                              length=150)
    slider_generation_optimization.pack()

    # Ajout d'un gestionnaire d'événement pour détecter le relâchement du curseur du slider
    slider_generation_optimization.bind("<ButtonRelease-3>", downsampling_selected_event)
    slider_generation_optimization.bind("<ButtonRelease-1>", downsampling_selected_event)

    downsampling_frame.grid(row=0, column=1, sticky=tk.W, padx=5)

    options_fenetre_frame.pack(ipady=10)

    fractal_options_frame = ttk.Frame(options_frame)

    # Cadre pour le type de fractal

    fractal_frame = ttk.Frame(fractal_options_frame)

    # Titre
    label = tk.Label(fractal_frame, text="Fractale")
    label.pack(ipady=8)

    # Liste déroulante pour choisir la variable d'énumération
    variable_options = [fractals.real_name for fractals in fractalbase.FractalType]
    variable_var = tk.StringVar()
    variable_combobox = ttk.Combobox(fractal_frame, textvariable=variable_var, values=variable_options,
                                     state='readonly')
    variable_combobox.bind("<<ComboboxSelected>>", fractal_selected_event)
    variable_combobox.pack(pady=10)

    fractal_frame.grid(row=0, column=0, sticky=tk.W, padx=5)

    # Cadre pour le slider d'iteration

    iteration_frame = ttk.Frame(fractal_options_frame)

    # Titre
    label = tk.Label(iteration_frame, text="Iteration")
    label.pack()

    # Slider
    slider_iteration = tk.Scale(iteration_frame, resolution=1, orient=tk.HORIZONTAL, length=150)
    slider_iteration.pack()

    # Ajout d'un gestionnaire d'événement pour détecter le relâchement du curseur du slider
    slider_iteration.bind("<ButtonRelease-3>", iteration_selected_event)
    slider_iteration.bind("<ButtonRelease-1>", iteration_selected_event)

    iteration_frame.grid(row=0, column=1, sticky=tk.W, padx=5)

    fractal_options_frame.pack(ipady=10)

    # Cadre pour le slider de sensibilité et fractal power

    sensibility_fractal_power_julia_c_frame = ttk.Frame(options_frame)

    # Cadre pour le slider de sensibilité

    sensibility_frame = ttk.Frame(sensibility_fractal_power_julia_c_frame)

    # Titre
    label = tk.Label(sensibility_frame, text="Sensibilité")
    label.pack()

    # Slider
    slider_sensibility = tk.Scale(sensibility_frame, from_=0, to=10, resolution=0.1, orient=tk.HORIZONTAL, length=150)
    slider_sensibility.pack()

    # Ajout d'un gestionnaire d'événement pour détecter le relâchement du curseur du slider
    slider_sensibility.bind("<ButtonRelease-3>", sensibility_selected_event)
    slider_sensibility.bind("<ButtonRelease-1>", sensibility_selected_event)

    sensibility_frame.grid(row=0, column=0, sticky=tk.W, padx=5)

    # Cadre pour le slider de fractal power
    fractal_type = app.fractal_manager.get_fractal_type()

    if fractal_type == FractalType.MANDELBROT:
        fractal_power_frame = ttk.Frame(sensibility_fractal_power_julia_c_frame)

        # Titre
        label_power = tk.Label(fractal_power_frame, text="Puissance de la Fractale")
        label_power.pack()

        # Slider
        fractal_power_slider = tk.Scale(fractal_power_frame, from_=2, to=50, resolution=1, orient=tk.HORIZONTAL,
                                        length=150)
        fractal_power_slider.pack()

        # Ajout d'un gestionnaire d'événement pour détecter le relâchement du curseur du slider
        fractal_power_slider.bind("<ButtonRelease-3>", update_fractal_power)
        fractal_power_slider.bind("<ButtonRelease-1>", update_fractal_power)

        fractal_power_frame.grid(row=0, column=1, sticky=tk.W, padx=5)

    elif fractal_type == FractalType.JULIA:

        fractal_c_frame = ttk.Frame(sensibility_fractal_power_julia_c_frame)

        # Titre
        label_c = tk.Label(fractal_c_frame, text="Valeur donnée de C")
        label_c.pack(pady=8)

        position_c_frame = ttk.Frame(fractal_c_frame)

        # Fonction de validation enregistrée pour les zones de saisie
        float_validation_c = fractal_c_frame.register(validate_float)

        # Zone de saisie pour x
        label_cx = tk.Label(position_c_frame, text="c = ")
        label_cx.grid(row=0, column=0, sticky=tk.W)
        entry_cx = tk.Entry(position_c_frame, validate="key",
                            validatecommand=(float_validation_c, "%S", "%P"), width=15)
        entry_cx.grid(row=0, column=1, sticky=tk.W, pady=2)

        entry_cy = tk.Entry(position_c_frame, validate="key",
                            validatecommand=(float_validation_c, "%S", "%P"), width=15)
        entry_cy.grid(row=0, column=2, sticky=tk.W, pady=2)

        # Zone de saisie pour y
        label_cy = tk.Label(position_c_frame, text="i")
        label_cy.grid(row=0, column=3, sticky=tk.W)

        entry_cx.bind('<KeyRelease>', update_c_julia_value)
        entry_cy.bind('<KeyRelease>', update_c_julia_value)

        update_c_entries()

        position_c_frame.pack(pady=12)

        fractal_c_frame.grid(row=0, column=1, sticky=tk.W, padx=5)

    sensibility_fractal_power_julia_c_frame.pack()

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

    # Cadre droit pour les coordonnées
    position_frame = ttk.LabelFrame(utilities_frame, text="Position")

    position_selection_frame = ttk.Frame(position_frame)

    # Fonction de validation enregistrée pour les zones de saisie
    float_validation = position_selection_frame.register(validate_float)

    # Zone de saisie pour x
    label_x = tk.Label(position_selection_frame, text="Coordonnée x :")
    label_x.grid(row=0, column=0, sticky=tk.W, padx=5)
    entry_x = tk.Entry(position_selection_frame, validate="key",
                       validatecommand=(float_validation, "%S", "%P"))
    entry_x.grid(row=0, column=1, sticky=tk.W, pady=2)

    # Zone de saisie pour y
    label_y = tk.Label(position_selection_frame, text="Coordonnée y :")
    label_y.grid(row=1, column=0, sticky=tk.W, padx=5)
    entry_y = tk.Entry(position_selection_frame, validate="key",
                       validatecommand=(float_validation, "%S", "%P"))
    entry_y.grid(row=1, column=1, sticky=tk.W, pady=2)

    # Zone de saisie pour z
    label_z = tk.Label(position_selection_frame, text="Coordonnée z :")
    label_z.grid(row=2, column=0, sticky=tk.W, padx=5)
    entry_z = tk.Entry(position_selection_frame, validate="key",
                       validatecommand=(float_validation, "%S", "%P"))
    entry_z.grid(row=2, column=1, sticky=tk.W, pady=2)

    update_position_entries()

    position_selection_frame.pack()

    go_position_button = tk.Button(position_frame, text="Go", padx=10, command=teleport_position_event)
    go_position_button.pack(pady=5)

    position_frame.pack()

    # Définition des poids des colonnes pour qu'elles s'adaptent à la fenêtre
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

    update_parameters_value()

    # Lancement de la boucle principale
    root.mainloop()

    root = None
    entry_x, entry_y, entry_z = None, None, None
    slider_iteration = None
    sensibility_fractal_power_julia_c_frame, fractal_power_frame, fractal_power_slider, fractal_c_frame = None, None, None, None
    entry_cx, entry_cy = None, None
