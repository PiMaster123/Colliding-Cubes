import pygame
from pygame.locals import *
import random
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import os
import sys

display = (1080, 800)

board = [[[0 for i in range(4)] for j in range(4)] for k in range(10)]


# Make the border
def border():
    # Make vertices
    vertices = [
        (4, -4, -4),
        (4, 4, -4),
        (-4, 4, -4),
        (-4, -4, -4),
        (4, -4, 4),
        (4, 4, 4),
        (-4, -4, 4),
        (-4, 4, 4)
    ]

    # Connect edges
    edges = [
        (0, 1),
        (0, 3),
        (0, 4),
        (2, 1),
        (2, 3),
        (2, 7),
        (6, 3),
        (6, 4),
        (6, 7),
        (5, 1),
        (5, 4),
        (5, 7)
    ]
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()


# simple 1 x 1
def player(x, y, z):
    vertices = [
        (x, y, z),
        (x, y, z+1),
        (x, y+1, z),
        (x, y+1, z+1),
        (x+1, y, z),
        (x+1, y, z+1),
        (x+1, y+1, z),
        (x+1, y+1, z+1)
    ]

    edges = [
        (0, 1),
        (0, 2),
        (2, 3),
        (1, 3),
        (4, 5),
        (4, 6),
        (6, 7),
        (5, 7),
        (3, 7),
        (2, 6),
        (0, 4),
        (1, 5),
    ]

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()


def drawfood(x, y, z):

    vertices = [
        (x, y, z),
        (x, y, z + 0.5),
        (x, y + 0.5, z),
        (x, y + 0.5, z + 0.5),
        (x + 0.5, y, z),
        (x + 0.5, y, z + 0.5),
        (x + 0.5, y + 0.5, z),
        (x + 0.5, y + 0.5, z + 0.5)
    ]

    edges = [
        (0, 1),
        (0, 2),
        (2, 3),
        (1, 3),
        (4, 5),
        (4, 6),
        (6, 7),
        (5, 7),
        (3, 7),
        (2, 6),
        (0, 4),
        (1, 5),
    ]

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()


def main():

    dx = random.uniform(-0.01, 0.01)
    dy = random.uniform(-0.01, 0.01)
    dz = random.uniform(-0.01, 0.01)

    foodx = random.uniform(-4, 3.5) + dx
    foody = random.uniform(-4, 3.5) + dy
    foodz = random.uniform(-4, 3.5) + dz

    x = 1
    y = 1
    z = 1

    pygame.init()
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    clock = pygame.time.Clock()

    score = 0
    high = 0
    angle = 0

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0, 0, -15)

    while True:
        foodx += dx
        foody += dy
        foodz += dz

        if foodx < -4 or foodx > 3.5:
            dx *= -1

        if foody < -4 or foody > 3.5:
            dy *= -1

        if foodz < -4 or foodz > 3.5:
            dz *= -1

        ticks = pygame.time.get_ticks()
        sec = 60 - math.floor(ticks/1000)
        if sec < 0:
            sec, dx, dy, dz = 0, 0, 0, 0

        timeGood = sec > 0

        if abs(x - foodx) < 0.5 and abs(y - foody) < 0.5 and abs(z - foodz) < 0.5:
            score += 1
            foodx = random.uniform(-4, 3.5)
            foody = random.uniform(-4, 3.5)
            foodz = random.uniform(-4, 3.5)

            dx = random.uniform(-0.01, 0.01)
            dy = random.uniform(-0.01, 0.01)
            dz = random.uniform(-0.01, 0.01)

        rotateAngle = 0
        rotateX = 0
        rotateY = 0
        rotateZ = 0

        angleMod = angle % 360

        pygame.display.set_caption(f'Time Remaining: {sec}        Score: {score}')

        # Python Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT] and timeGood:
            rotateAngle = 1
            rotateY = -1
            angle -= 1
            print(angle)

        if pressed[pygame.K_RIGHT] and timeGood:
            rotateAngle = 1
            rotateY = 1
            angle += 1
            print(angle)

        # The first sector
        if 0 <= angleMod < 45 or 315 <= angleMod < 360:
            if pressed[pygame.K_s] and z < 3 and timeGood:
                z += 0.1
            if pressed[pygame.K_w] and z > -4 and timeGood:
                z -= 0.1

            if pressed[pygame.K_d] and x < 3 and timeGood:
                x += 0.1
            if pressed[pygame.K_a] and x > -4 and timeGood:
                x -= 0.1

        # The second sector
        if 45 <= angleMod < 135:
            if pressed[pygame.K_s] and x > -4 and timeGood:
                x -= 0.1
            if pressed[pygame.K_w] and x < 3 and timeGood:
                x += 0.1

            if pressed[pygame.K_d] and z < 3 and timeGood:
                z += 0.1
            if pressed[pygame.K_a] and z > -4 and timeGood:
                z -= 0.1

        # The third sector
        if 135 <= angleMod < 225:
            if pressed[pygame.K_s] and z > -4 and timeGood:
                z -= 0.1
            if pressed[pygame.K_w] and z < 3 and timeGood:
                z += 0.1

            if pressed[pygame.K_d] and x > -4 and timeGood:
                x -= 0.1
            if pressed[pygame.K_a] and x < 3 and timeGood:
                x += 0.1

        # The fourth sector
        if 225 <= angleMod < 315:
            if pressed[pygame.K_s] and x < 3 and timeGood:
                x += 0.1
            if pressed[pygame.K_w] and x > -4 and timeGood:
                x -= 0.1

            if pressed[pygame.K_d] and z > -4 and timeGood:
                z -= 0.1
            if pressed[pygame.K_a] and z < 3 and timeGood:
                z += 0.1

        if pressed[pygame.K_UP] and y < 3 and timeGood:
            y += 0.1
        if pressed[pygame.K_DOWN] and y > -4 and timeGood:
            y -= 0.1

        if not timeGood and pressed[pygame.K_r]:
            if score >= high:
                high = score
                os.execl(sys.executable, sys.executable, *sys.argv)

        glRotatef(rotateAngle, rotateX, rotateY, rotateZ)

        glClear(GL_COLOR_BUFFER_BIT)
        glClear(GL_DEPTH_BUFFER_BIT)

        drawfood(foodx, foody, foodz)
        player(x, y, z)
        border()
        pygame.display.flip()
        clock.tick(60)


main()
