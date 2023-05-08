#
#  Fracteur Copyright (c) 2023 LyFlow and Florely
#  This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
#  This is free software, and you are welcome to redistribute it under certain conditions; type `show c' for details.
#

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np


def pyramide_division(sommet, hauteur, largeur, maxit):
    if maxit > 0:
        millieu_haut_1 = [sommet[0] + largeur / 4, sommet[1] + largeur / 4, sommet[2] - hauteur / 2]
        millieu_haut_2 = [sommet[0] + largeur / 4, sommet[1] - largeur / 4, sommet[2] - hauteur / 2]
        millieu_haut_3 = [sommet[0] - largeur / 4, sommet[1] + largeur / 4, sommet[2] - hauteur / 2]
        millieu_haut_4 = [sommet[0] - largeur / 4, sommet[1] - largeur / 4, sommet[2] - hauteur / 2]
        if maxit == 1:
            coins_bas_1 = [sommet[0] + largeur / 2, sommet[1] + largeur / 2, sommet[2] - hauteur]
            coins_bas_2 = [sommet[0] + largeur / 2, sommet[1] - largeur / 2, sommet[2] - hauteur]
            coins_bas_3 = [sommet[0] - largeur / 2, sommet[1] + largeur / 2, sommet[2] - hauteur]
            coins_bas_4 = [sommet[0] - largeur / 2, sommet[1] - largeur / 2, sommet[2] - hauteur]

            milleu_bas_1 = [sommet[0] + largeur / 2, sommet[1], sommet[2] - hauteur]
            milleu_bas_2 = [sommet[0], sommet[1] - largeur / 2, sommet[2] - hauteur]
            milleu_bas_3 = [sommet[0], sommet[1] + largeur / 2, sommet[2] - hauteur]
            milleu_bas_4 = [sommet[0] - largeur / 2, sommet[1], sommet[2] - hauteur]

            centre_bas = [sommet[0], sommet[1], sommet[2] - hauteur]
            liste_polygone = [  # [coins_bas_1,coins_bas_2,coins_bas_3,coins_bas_4],
                [millieu_haut_1, coins_bas_1, milleu_bas_1],
                [millieu_haut_1, coins_bas_1, milleu_bas_3],
                [millieu_haut_1, centre_bas, milleu_bas_1],
                [millieu_haut_1, centre_bas, milleu_bas_3],
                [coins_bas_1, milleu_bas_3, centre_bas, milleu_bas_1],

                [millieu_haut_3, coins_bas_3, milleu_bas_4],
                [millieu_haut_3, coins_bas_3, milleu_bas_3],
                [millieu_haut_3, centre_bas, milleu_bas_4],
                [millieu_haut_3, centre_bas, milleu_bas_3],
                [coins_bas_3, milleu_bas_3, centre_bas, milleu_bas_4],

                [millieu_haut_4, coins_bas_4, milleu_bas_4],
                [millieu_haut_4, coins_bas_4, milleu_bas_2],
                [millieu_haut_4, centre_bas, milleu_bas_4],
                [millieu_haut_4, centre_bas, milleu_bas_2],
                [coins_bas_4, milleu_bas_4, centre_bas, milleu_bas_2],

                [millieu_haut_2, coins_bas_2, milleu_bas_1],
                [millieu_haut_2, coins_bas_2, milleu_bas_2],
                [millieu_haut_2, centre_bas, milleu_bas_1],
                [millieu_haut_2, centre_bas, milleu_bas_2],
                [coins_bas_2, milleu_bas_2, centre_bas, milleu_bas_1],

                [millieu_haut_1, millieu_haut_2, sommet],
                [millieu_haut_2, millieu_haut_4, sommet],
                [millieu_haut_3, millieu_haut_1, sommet],
                [millieu_haut_4, millieu_haut_3, sommet],
                [millieu_haut_1, millieu_haut_3, millieu_haut_4, millieu_haut_2]
            ]
            return liste_polygone
        else:
            return pyramide_division(sommet, hauteur / 2, largeur / 2, maxit - 1) + pyramide_division(millieu_haut_1,
                                                                                                      hauteur / 2,
                                                                                                      largeur / 2,
                                                                                                      maxit - 1) + pyramide_division(
                millieu_haut_2, hauteur / 2, largeur / 2, maxit - 1) + pyramide_division(millieu_haut_3, hauteur / 2,
                                                                                         largeur / 2,
                                                                                         maxit - 1) + pyramide_division(
                millieu_haut_4, hauteur / 2, largeur / 2, maxit - 1)


def run(app):
    app.matplotlib_running = True

    import warnings
    warnings.filterwarnings("ignore")

    hauteur = 2
    largeur = 2
    maxit = 3

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # vertices of a pyramid
    v = np.array([[-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1], [0, 0, 1]])
    ax.scatter3D(v[:, 0], v[:, 1], v[:, 2])

    # generate list of sides' polygons of our pyramid
    verts = [[v[0], v[1], v[4]], [v[0], v[3], v[4]],
             [v[2], v[1], v[4]], [v[2], v[3], v[4]], [v[0], v[1], v[2], v[3]]]
    if maxit > 1:
        verts = pyramide_division(v[4], hauteur, largeur, maxit)
    # plot sides
    ax.add_collection3d(Poly3DCollection(verts,
                                         facecolors='cyan', linewidths=1, edgecolors='r', alpha=.25))

    plt.show()
    app.matplotlib_running = False
