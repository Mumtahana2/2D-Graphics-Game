from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time

W_Width, W_Height = 500, 500
points = []
frozen = False
blink = False
last_blink_time = time.time()

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = [random.random(), random.random(), random.random()]
        self.dx = random.choice([-1, 1]) * random.uniform(0.5, 1.0)
        self.dy = random.choice([-1, 1]) * random.uniform(0.5, 1.0)
        self.speed = 1.0

    def move(self):
        if not frozen:
            self.x += self.dx * self.speed
            self.y += self.dy * self.speed

            # Bounce off walls
            if self.x <= 0 or self.x >= W_Width:
                self.dx *= -1
            if self.y <= 0 or self.y >= W_Height:
                self.dy *= -1

    def draw(self):
        global blink, last_blink_time
        current_time = time.time()
        if blink and (current_time - last_blink_time) >= 0.5:
            glColor3f(0, 0, 0)  # make it invisible
            if (current_time - last_blink_time) >= 1.0:
                last_blink_time = current_time
        else:
            glColor3f(*self.color)

        glPointSize(7)
        glBegin(GL_POINTS)
        glVertex2f(self.x, self.y)
        glEnd()

def add_point(x, y):
    points.append(Point(x, W_Height - y))

def draw_points():
    for point in points:
        point.draw()

def move_points():
    for point in points:
        point.move()

def increase_speed():
    for point in points:
        point.speed *= 1.1

def decrease_speed():
    for point in points:
        point.speed *= 0.9

def toggle_freeze():
    global frozen
    frozen = not frozen

def toggle_blink():
    global blink
    blink = not blink

def iterate():
    glViewport(0, 0, W_Width, W_Height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, W_Width, 0.0, W_Height, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def showScreen():
    glClearColor(0.0, 0.0, 0.0, 1.0)  # background black
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    draw_points()
    glutSwapBuffers()

def animate():
    glutPostRedisplay()
    move_points()

def mouse_click(button, state, x, y):
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        add_point(x, y)  # add new point at mouse click
    elif button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        toggle_blink()

def special_keys(key, x, y):
    if key == GLUT_KEY_UP:
        increase_speed()
    elif key == GLUT_KEY_DOWN:
        decrease_speed()

def keyboard(key, x, y):
    if key == b' ':
        toggle_freeze()

# -----------------------------
# Main program starts here
# -----------------------------
glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(100, 100)
wind = glutCreateWindow(b"Amazing Box")

# Register callbacks
glutDisplayFunc(showScreen)
glutIdleFunc(animate)
glutMouseFunc(mouse_click)
glutSpecialFunc(special_keys)   # for arrow keys
glutKeyboardFunc(keyboard)      # for normal keys

# Spawn a few points initially
for _ in range(5):
    points.append(Point(random.randint(0, W_Width), random.randint(0, W_Height)))

glutMainLoop()
