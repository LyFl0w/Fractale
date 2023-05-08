#
#  Fracteur Copyright (c) 2023 LyFlow and Florely
#  This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
#  This is free software, and you are welcome to redistribute it under certain conditions; type `show c' for details.
#

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np


def cube_division(sommet, hauteur, largeur, profondeur, maxit):
    if maxit > 0:
        liste_polygone = []
        for i in range(3):
            for y in range(3):
                for z in range(3):
                    sommet_carre = [sommet[0] - (hauteur / 3) * i, sommet[1] - (hauteur / 3) * y,
                                    sommet[2] - (hauteur / 3) * z]
                    if [i, y, z].count(1) < 2:
                        if maxit == 1:
                            v = np.array([[sommet[0] - largeur, sommet[1] - hauteur, sommet[2] - profondeur],
                                          [sommet[0] - largeur, sommet[1] - hauteur, sommet[2]],
                                          [sommet[0], sommet[1] - hauteur, sommet[2] - profondeur],
                                          [sommet[0], sommet[1] - hauteur, sommet[2]],
                                          [sommet[0], sommet[1], sommet[2] - profondeur],
                                          [sommet[0], sommet[1], sommet[2]],
                                          [sommet[0] - largeur, sommet[1], sommet[2]],
                                          [sommet[0] - largeur, sommet[1], sommet[2] - profondeur]])
                            liste_polygone = liste_polygone + [[v[0], v[1], v[3], v[2]], [v[2], v[3], v[5], v[4]],
                                                               [v[4], v[5], v[6], v[7]], [v[6], v[7], v[0], v[1]],
                                                               [v[0], v[2], v[4], v[7]], [v[1], v[3], v[5], v[6]]]
                        else:
                            liste_polygone += cube_division(sommet_carre, hauteur / 3, largeur / 3, profondeur / 3,
                                                            maxit - 1)
        return liste_polygone


def run(app):
    app.matplotlib_running = True

    import warnings
    warnings.filterwarnings("ignore")

    hauteur = 2
    largeur = 2
    profondeur = 2
    maxit = 3
    sommet = [1, 1, 1]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # vertices of a pyramid
    v = np.array([[sommet[0] - largeur, sommet[1] - hauteur, sommet[2] - profondeur],
                  [sommet[0] - largeur, sommet[1] - hauteur, sommet[2]],
                  [sommet[0], sommet[1] - hauteur, sommet[2] - profondeur], [sommet[0], sommet[1] - hauteur, sommet[2]],
                  [sommet[0], sommet[1], sommet[2] - profondeur], [sommet[0], sommet[1], sommet[2]],
                  [sommet[0] - largeur, sommet[1], sommet[2]],
                  [sommet[0] - largeur, sommet[1], sommet[2] - profondeur]])
    ax.scatter3D(v[:, 0], v[:, 1], v[:, 2])

    # generate list of sides' polygons of our pyramid
    verts = [[v[0], v[1], v[3], v[2]], [v[2], v[3], v[5], v[4]], [v[4], v[5], v[6], v[7]], [v[6], v[7], v[0], v[1]],
             [v[0], v[2], v[4], v[7]], [v[1], v[3], v[5], v[6]]]
    if maxit > 1:
        verts = cube_division(sommet, hauteur, largeur, profondeur, maxit)
    # plot sides
    ax.add_collection3d(Poly3DCollection(verts,
                                         facecolors='cyan', linewidths=1, edgecolors='r', alpha=.25))

    plt.show()
    app.matplotlib_running = False
