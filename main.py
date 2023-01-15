import pygame
import numpy as np


def fractale_matrice(h, w, zoom=1.0, maxit=20, center_x=0, center_y=0, fractal_type='Mandelbrot', fractal_power=2):
    x, y = np.mgrid[-1.4:1.4:h * 1j, -2:0.8:w * 1j]
    x = (x - center_x) / zoom
    y = (y - center_y) / zoom
    c = x + y * 1j
    z = c
    diverge = np.zeros((h, w), dtype=bool)
    divtime = np.full((h, w), maxit, dtype=int)

    if fractal_type == 'Julia':
        fractale = -0.835 - 0.2321j
    elif fractal_type == 'Mandelbrot':
        fractale = c
    else:
        raise ValueError("La valeur de fractal_type doit être 'Mandelbrot' ou 'Julia'.")

    for i in range(maxit):
        z = z ** fractal_power + fractale
        diverge = np.logical_or(diverge, z * np.conj(z) > 2 ** 2)
        divtime[np.logical_and(diverge, divtime == maxit)] = i
        z[diverge] = 2

    return divtime



native_h, native_w = 400, 400
h, w = 400, 400
centre=[200,200]
fps = 100
zoom = 1

pygame.init()
screen = pygame.display.set_mode((native_w, native_h))
clock = pygame.time.Clock()


def update(center_x, center_y):
    mb = fractale_matrice(h, w, zoom, center_x=(center_x/native_w)*3.8-2, center_y=(center_y/native_h )*2.8-1.4, fractal_power=10, maxit=100)
    # Inversion de l'ordre des lignes de l'image de l'ensemble de Mandelbrot pour corriger la différence de coordonnées entre Pygame et NumPy
    mb = np.flipud(mb)
    mb_surface = pygame.surfarray.make_surface(mb)
    pygame.surfarray.blit_array(mb_surface, mb)
    screen.blit(pygame.transform.scale(mb_surface, (native_w, native_h)), (0, 0))
    pygame.draw.circle(screen, (255, 255, 0), pygame.mouse.get_pos(), 10)
    pygame.draw.circle(screen, (255, 255, 0), (native_w / 2, native_h / 2), 10)
    pygame.display.update()


def zoom_at_cursor(zoom_factor):
    global zoom,centre
    #prend les coordonnées du curseur 
    mouse_x, mouse_y = pygame.mouse.get_pos()
    print("souris",mouse_x,mouse_y)
    print("centre",centre)
    #transforme les coordonnées en natif 
    #mouse_x=(mouse_x/(native_w/w))
    #mouse_y=(mouse_y/(native_h/h))
    print("deplacement",(mouse_y-centre[1])*0.75,(mouse_x-centre[0])*0.75)
    centre=[centre[0]+((mouse_x-centre[0])*0.2) , centre[1]+((mouse_y-centre[1])*0.2)]
    mouse_x, mouse_y = pygame.mouse.get_pos()
    # Calculate the offset of the cursor from the current center
    offset_x = (mouse_x - centre[0]) / zoom
    offset_y = (mouse_y - centre[1]) / zoom
    # Update the center to keep the cursor in the same position
    centre[0] += offset_x * (zoom_factor - 1)
    centre[1] += offset_y * (zoom_factor - 1)
    zoom*=zoom_factor
    print(centre)
    update(centre[0],centre[1  ])
    #


def move(dx, dy):
    global centre
    speed = 1
    centre = [centre[0] - dx * speed, centre[1] + dy * speed]
    print("mouvement souris",centre[0],centre[1])
    update(centre[0], centre[1])


def handle_mouse_movement():
    dx, dy = pygame.mouse.get_rel()
    if pygame.mouse.get_pressed()[0]:
        move(dx, dy)


update((2/3.8)*native_h, 1.4/5*native_w)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                zoom_at_cursor(1.1)
            elif event.button == 5:
                zoom_at_cursor(0.9)
        elif event.type == pygame.MOUSEMOTION:
            handle_mouse_movement()

    clock.tick(fps)

pygame.quit()
