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


position = 0, 0
native_h, native_w = 600, 600
h, w = 400, 400
fps = 5
zoom = 1

pygame.init()
screen = pygame.display.set_mode((native_w, native_h))
clock = pygame.time.Clock()


def update(center_x, center_y):
    mb = fractale_matrice(h, w, zoom, center_x=center_x, center_y=center_y, fractal_power=10, maxit=100)
    # Inversion de l'ordre des lignes de l'image de l'ensemble de Mandelbrot pour corriger la différence de coordonnées entre Pygame et NumPy
    mb = np.flipud(mb)
    mb_surface = pygame.surfarray.make_surface(mb)
    pygame.surfarray.blit_array(mb_surface, mb)
    screen.blit(pygame.transform.scale(mb_surface, (native_w, native_h)), (0, 0))
    pygame.draw.circle(screen, (255, 0, 0), pygame.mouse.get_pos(), 10)
    pygame.draw.circle(screen, (255, 0, 0), (native_w / 2, native_h / 2), 10)
    pygame.display.update()


def zoom_at_cursor(zoom_factor):
    global zoom, position
    mouse_x, mouse_y = pygame.mouse.get_pos()
    rel_x = ((mouse_x / native_w) * 3.8 - 2)
    rel_y = -((mouse_y / native_h) * 2.8 - 1.4)
    center_x, center_y = position
    zoom *= zoom_factor
    if zoom < 1:
        zoom = 1
    elif zoom > 100:
        zoom = 100
    center_x += rel_x
    center_y += rel_y
    position = center_x, center_y
    update(center_x, center_y)


def move(dx, dy):
    global position
    speed = 0.01
    position = (position[0] + dx * speed, position[1] + dy * speed)
    update(position[0], -position[1])


def handle_mouse_movement():
    dx, dy = pygame.mouse.get_rel()
    if pygame.mouse.get_pressed()[0]:
        move(dx, dy)


update(0, 0)

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
