import numpy as np
import pygame
import math
filtre = pygame.Color(0, 255, 0)
native_h, native_w = 500, 500
h, w = 400, 400
dim_screen=[400,400]
diff=[h/2,w/2]
fps = 50


centre = [h//3, 0]
zoom = 9
maxit=6

pygame.init()
screen = pygame.display.set_mode((native_w, native_h))
clock = pygame.time.Clock()

def verifier_presence(centre_screen,h_screen,w_screen,centre_carre,h_carre,w_carre):
    for i in [0]:
        for j in [0]:
            #print()
            #if centre_carre[0]<0 and centre_carre[1]<0:
                #print(centre_screen)
                #print(centre_screen[0]-(w_screen/2),centre_carre[0]+(w_carre/2)*i,centre_screen[0]+(w_screen/2)," ", centre_screen[1]-(h_screen/2),centre_carre[1]+(h_carre/2)*j,centre_screen[1]+(h_screen/2))
            if centre_screen[0]-(w_screen/2)<=centre_carre[0]+(w_carre/2)*i<=centre_screen[0]+(w_screen/2) or centre_screen[1]-(h_screen/2)<=centre_carre[1]+(h_carre/2)*j<=centre_screen[1]+(h_screen/2):
                return True 
    return False

def fractale_matrice(h_carre, w_carre, zoom=1.0, maxit=maxit, x=0, y=0,screen=screen,distance=False):
    a=0
    next_distance=False
    if distance==True:
        if math.sqrt((x)**2+(y)**2)<=w:
            distance=False
            next_distance=True
    if maxit>0:
        if distance==False:
            a+=1
            pygame.draw.rect(screen,(255,255,255),( ((x-(h_carre/3/2))*zoom+diff[0]),((y-(w_carre/3/2))*zoom+diff[1]),int((w_carre/3)*zoom ),int((h_carre/3)*zoom)),0)
            for i in [-1,0,1]:
                for j in [-1,0,1]:
                    if (i,j)!=(0,0):
                        #if verifier_presence((centre[0],centre[1]),dim_screen[1],dim_screen[0],(x+(w_carre/3)*i,y+(h_carre/3)*j),h_carre/3,w_carre/3)==True:
                        a+=fractale_matrice(h_carre/3,w_carre/3,zoom,maxit-1,x+(w_carre/3)*i,y+(h_carre/3)*j,screen,next_distance)
    return a

def zoom_at_cursor(zoom_factor):
    global zoom, centre,co_screen,dim_screen
    zoom*=zoom_factor
    dim_screen=[w/zoom,h/zoom]
    #print(zoom)
    #print(dim_screen)
    update(centre[0],centre[1])


def position_cube(center_x,center_y,cube_x,cube_y,largeur):
    if center_x-cube_x>=largeur/2:
        x=1
    elif center_x-cube_x<=-largeur/2:
        x=-1
    else:
        x=0
    if center_y-cube_y>=largeur:
        y=1
    elif center_y-cube_y<=-largeur:
        y=-1
    else:
        y=0
    return [x,y]


def infini(center_x,center_y):
    global zoom,centre,maxit,pos_cube
    mb = pygame.Surface((w,h))
    pos_cube=position_cube(center_x,center_y,0,0,h/3)
    bloc=position_cube(center_x,center_y,pos_cube[0]*h/3,pos_cube[1]*h/3,h/9)
    """if zoom<=2:
        zoom*=3
        maxit=5
        center_x=(h/3)*bloc[0]+(center_x-(pos_cube[0]*(h/3)+bloc[0]*(h/9)))*3
        center_y=(h/3)*bloc[1]+(center_y-(pos_cube[1]*(h/3)+bloc[1]*(h/9)))*3"""
    if zoom>=9:
        zoom/=3
        maxit=5
        #print("-------------------------")
        #print("téléportation")
        #print("--------------------------")
        #center_x=(h/3)*bloc[0]+(center_x-(pos_cube[0]*(h/3)+bloc[0]*(h/9)))*3
        #center_y=(h/3)*bloc[1]+(center_y-(pos_cube[1]*(h/3)+bloc[1]*(h/9)))*3
        center_x=(h/3)*bloc[0]+(center_x-(pos_cube[0]*(h/3)+bloc[0]*(h/9)))*3
        center_y=(h/3)*bloc[1]+(center_y-(pos_cube[1]*(h/3)+bloc[1]*(h/9)))*3
    if abs(center_x) > diff[0]: 
        if center_x>0:
            center_x-=w
        else:
            center_x+=w
    if abs(center_y) > diff[1]: 
        if center_y>0:
            center_y-=h
        else:
            center_y+=h

    #print("case",pos_cube)
    #print("bloc",bloc)
    return [center_x,center_y]

def update(center_x, center_y):
    global centre
    #screen.fill(0,0,0)
    mb = pygame.Surface((w,h))
    #print("-------------------------")
    centre=infini(center_x,center_y)
    fractale_matrice(h,w,zoom=zoom,maxit=maxit,x=-centre[0],y=centre[1],screen=mb)
    for i in range(-1,2):
        for y in range(-1,2):
            fractale_matrice(h,w,zoom=zoom,maxit=maxit,x=-centre[0]+i*h,y=centre[1]+y*w,screen=mb,distance=True)
    # Inversion de l'ordre des lignes de l'image de l'ensemble de Mandelbrot pour corriger la différence de coordonnées entre Pygame et NumPy
    screen.blit(pygame.transform.scale(mb, (native_w, native_h)), (0, 0))

    #print("co",centre[0],centre[1])
    #print("zoom",zoom)
    
    pygame.display.update()

def handle_mouse_movement():
    dx, dy = pygame.mouse.get_rel()
    if pygame.mouse.get_pressed()[0]:
        move(dx, dy)

def move(dx, dy):
    global centre
    speed = 1/zoom
    
    #if -133<=centre[0] - dx * speed<=133 and -133<=centre[1] + dy * speed<=133:
    centre = [centre[0] - dx * speed, centre[1] + dy * speed]
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
