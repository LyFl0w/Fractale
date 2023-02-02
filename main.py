import numpy as np
import pygame

filtre = pygame.Color(0, 255, 0)
native_h, native_w = 500, 500
h, w = 400, 400
centre = [0, 0]
fps = 50
zoom = 1

pygame.init()
screen = pygame.display.set_mode((native_w, native_h))
clock = pygame.time.Clock()

def fractale_matrice(h, w, zoom=1.0, maxit=20, top_left_x=0, top_left_y=0,screen=screen):
    if maxit>0:
        pygame.draw.rect(screen,(255,255,255),(top_left_x+(w/3),top_left_y+(h/3),(h/3)*zoom,(w/3)*zoom),0)
        for i in range(3):
            for j in range(3):
                if (i,j)!=(1,1):
                    fractale_matrice(h/3,w/3,zoom,maxit-1,top_left_x+(w/3)*i,top_left_y+(h/3)*j,screen)

def zoom_at_cursor(zoom_factor):
    global zoom, centre
    zoom*=zoom_factor
    update(centre[0],centre[1])

def update(center_x, center_y):
    #screen.fill(0,0,0)
    mb = pygame.Surface((w,h))
    fractale_matrice(h,w,zoom=zoom,maxit=5,top_left_x=center_x,top_left_y=center_y,screen=mb)
    # Inversion de l'ordre des lignes de l'image de l'ensemble de Mandelbrot pour corriger la différence de coordonnées entre Pygame et NumPy
    screen.blit(pygame.transform.scale(mb, (native_w, native_h)), (0, 0))
    pygame.display.update()

def handle_mouse_movement():
    dx, dy = pygame.mouse.get_rel()
    if pygame.mouse.get_pressed()[0]:
        move(dx, dy)

def move(dx, dy):
    global centre
    speed = 1/zoom
    centre = [centre[0] + dx * speed, centre[1] + dy * speed]
    update(centre[0], centre[1])

update(centre[0],centre[1])
pygame.display.update()
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
