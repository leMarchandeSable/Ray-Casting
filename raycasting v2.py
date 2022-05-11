import pygame
import numpy as np
import os
import time


class Border:
    def __init__(self, x1, y1, x2, y2):
        self.a = np.array([x1, y1])
        self.b = np.array([x2, y2])

    def show(self):
        pygame.draw.line(surface, blanc, self.a, self.b, 2)


class Ray:
    def __init__(self, x, y, angle):
        self.start = np.array([x, y])

        # angle en degre et dir un vecteur unitaire
        self.angle = angle
        self.dir = np.array([np.cos(np.pi * self.angle / 180),
                             np.sin(np.pi * self.angle / 180)])

        self.end = self.start
        self.dist = -1

    def show(self):
        # on modifie la couleur de rayon en fonction de la distance a un mur
        color = [255, 255, 255]
        if self.dist < 100:
            color[1] = 0
            color[2] = 0
        if self.dist < 200:
            color[1] = 0

        pygame.draw.line(surface, color, self.start, self.end, 1)

    def intersect(self, wall):
        # returne vrai si le rayon coupe wall
        # si oui calcule la distance a la particule et les coord du point d'intersection
        x1 = wall.a[0]
        y1 = wall.a[1]
        x2 = wall.b[0]
        y2 = wall.b[1]
        x3 = self.start[0]
        y3 = self.start[1]
        x4 = self.start[0] + self.dir[0]
        y4 = self.start[1] + self.dir[1]

        D = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

        # si D = 0 les 2 droites sont parallele
        if D == 0:
            return False

        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / D
        u = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / D

        if 0 < t < 1 and u > 0:
            px = x1 + t * (x2 - x1)
            py = y1 + t * (y2 - y1)

            self.end = np.array([px, py])
            self.dist = np.sqrt(np.sum((self.start - self.end)**2))
            return True
        else:
            return False


class Particle:
    def __init__(self, x, y):
        # coord de la souris
        self.x = x
        self.y = y

        # parametre des rayons
        self.n = 90

        # initialisation des objets rayons
        self.rays = []
        self.update([])                     # on initialise sans mur

    def creat_ray(self):
        return [Ray(self.x, self.y, i) for i in range(0, 360, 360 // self.n)]

    def update(self, walls):
        # on actualise les rayons avec la position actuelle la souris
        self.rays = self.creat_ray()

        # pour chaque rayon on regarde s'il coupe un mur
        # si oui on cherche le point d'intersection le plus proche de la particule
        for ray in self.rays:

            # on cherche la distance minimal entre x, y et le point d'intersection
            # on initialsie les constante avec des conditions impossible
            closest = ray.start
            dist = -1
            for wall in walls:
                if ray.intersect(wall):
                    # condition minimal
                    if ray.dist < dist or dist == -1:
                        dist = ray.dist
                        closest = ray.end
            # une fois trouvé on garde que le point d'intersection le plus proche ray.end
            ray.dist = dist
            ray.end = closest

    def show(self):
        # affichage des rayons
        for ray in self.rays:
            ray.show()

    def run(self):
        launched = 1
        while launched:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    launched = 0

            surface.fill(noir)

            # position de la souris
            x, y = pygame.mouse.get_pos()
            self.x, self.y = x, y

            self.update(walls)      # actualisation et calcule des points d'intersection
            self.show()             # affichage des rayons

            # affichage des murs
            for wall in walls:
                wall.show()

            pygame.display.flip()
            # save(surface, "3")
            # clock.tick(60)


def save(surface, doc_name):

    path = 'C:/Users/simon/Documents/IPSA/A2/python/Pygame/raycating/'

    if doc_name not in os.listdir(path):
        os.mkdir(doc_name)
    else:
        os.chdir(path + doc_name)
        pygame.image.save(surface, str(round(time.time(), 1)) + ".jpg")


# ----------------------------------------------------------------------------------------------------------------------
# initialisation constante + environnement
H = 400
L = 800
blanc = (255, 255, 255)
noir = (0, 0, 0)

# mur exterieur
walls = [Border(0, 0, 0, H),
         Border(0, H, L, H),
         Border(L, H, L, 0),
         Border(L, 0, 0, 0)]
# obstacle
[walls.append(Border(np.random.random() * L,
                     np.random.random() * H,
                     np.random.random() * L,
                     np.random.random() * H)) for i in range(5)]


# initialisation fenetre
pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("Raycasting")
surface = pygame.display.set_mode((L, H))

# ----------------------------------------------------------------------------------------------------------------------
player = Particle(L // 2, H // 2)
player.run()


