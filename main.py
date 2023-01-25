import numpy as np
import pygame

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

    return np.fliplr(np.flipud(divtime))


native_h, native_w = 600, 500
h, w = 200,200
centre=[0,0]
fps = 50
zoom = 1

pygame.init()
screen = pygame.display.set_mode((native_w, native_h))
clock = pygame.time.Clock()

def update(center_x, center_y):
    mb = fractale_matrice(h, w, zoom, center_x=(center_x/native_w)*3.8, center_y=(center_y/native_h )*2.8, fractal_power=2, maxit=100)
    # Inversion de l'ordre des lignes de l'image de l'ensemble de Mandelbrot pour corriger la différence de coordonnées entre Pygame et NumPy
    mb = np.flipud(mb)
    mb_surface = pygame.surfarray.make_surface(mb)
    pygame.surfarray.blit_array(mb_surface, mb)
    screen.blit(pygame.transform.scale(mb_surface, (native_w, native_h)), (0, 0))
    pygame.draw.circle(screen, (255, 255, 0), pygame.mouse.get_pos(), 10)
    pygame.draw.circle(screen, (255, 255, 0), (native_w / 2, native_h / 2), 10)
    pygame.display.update()

def zoom_at_cursor(factor):
    global zoom, centre
    cursor_x, cursor_y = pygame.mouse.get_pos()
    cursor_x_fractale = (cursor_x/native_w)*3.8
    cursor_y_fractale = (cursor_y/native_h)*2.8
    centre[0] += (cursor_x_fractale - centre[0]) * (1 - factor)
    centre[1] += (cursor_y_fractale - centre[1]) * (1 - factor)
    zoom *= factor
    update(centre[0], centre[1])

def move(dx, dy):
    global centre
    speed = 1
    centre = [centre[0] + dx * speed, centre[1] - dy * speed]
    print("mouvement souris",centre[0],centre[1])
    update(centre[0], centre[1])


def handle_mouse_movement():
    dx, dy = pygame.mouse.get_rel()
    if pygame.mouse.get_pressed()[0]:
        move(dx, dy)


update(centre[0],centre[1])

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
