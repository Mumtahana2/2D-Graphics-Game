from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

W_Width, W_Height = 500, 500
num_raindrops = 50
raindrops = []
rain_angle = 0
background_color = [0.0, 0.0, 0.0]  # Start with a dark background

class Raindrop:
    def __init__(self):
        self.x = random.uniform(0, 500)
        self.y = random.uniform(250, 500)
        self.speed = random.uniform(0.1, 0.5)

def initialize_raindrops():
    global raindrops
    raindrops = [Raindrop() for _ in range(num_raindrops)]

def draw_raindrops():
    global raindrops
    glPointSize(5)
    glBegin(GL_POINTS)
    for raindrop in raindrops:
        glVertex2f(raindrop.x, raindrop.y)
    glEnd()

def draw_points():
    glPointSize(5)
    glBegin(GL_POINTS)
    glVertex2f(150, 100)
    glVertex2f(350, 100)
    glVertex2f(150, 250)
    glVertex2f(350, 250)
    glEnd()

def draw_lines():
    glPointSize(5)
    glBegin(GL_LINES)
    glVertex2f(150, 100)
    glVertex2f(350, 100)
    glVertex2f(150, 100)
    glVertex2f(150, 250)
    glVertex2f(350, 100)
    glVertex2f(350, 250)
    glEnd()

def draw_triangle():
    glBegin(GL_LINE_LOOP)
    glColor3f(1.0, 1.0, 1.0)
    glVertex2d(100, 250)
    glVertex2d(400, 250)
    glVertex2d(250, 350)
    glEnd()

def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def showScreen():
    global background_color
    glClearColor(background_color[0], background_color[1], background_color[2], 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    glColor3f(1.0, 1.0, 1.0)  # Set drawing color to white
    draw_points()
    draw_lines()
    draw_triangle()
    draw_raindrops()
    glutSwapBuffers()

def animate():
    glutPostRedisplay()
    global raindrops, rain_angle
    for raindrop in raindrops:
        raindrop.y -= raindrop.speed
        raindrop.x += rain_angle
        if raindrop.y < 0:
            raindrop.x = random.uniform(0, 500)
            raindrop.y = random.uniform(250, 500)
        if raindrop.x < 0 or raindrop.x > 500:
            raindrop.x = random.uniform(0, 500)
            raindrop.y = random.uniform(250, 500)

def keyPressed(*args):
    global rain_angle, background_color
    if args[0] == GLUT_KEY_LEFT:
        rain_angle -= 0.01
    elif args[0] == GLUT_KEY_RIGHT:
        rain_angle += 0.01
    elif args[0] == b'd':  # Gradually change background from dark to light
        background_color = [min(c + 0.01, 1.0) for c in background_color]
    elif args[0] == b'n':  # Gradually change background from light to dark
        background_color = [max(c - 0.01, 0.0) for c in background_color]

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500, 500)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"OpenGL Coding Practice")
initialize_raindrops()
glutDisplayFunc(showScreen)
glutIdleFunc(animate)
glutSpecialFunc(keyPressed)  # Register special key presses for arrow keys
glutKeyboardFunc(keyPressed)  # Register regular key presses
glutMainLoop()
