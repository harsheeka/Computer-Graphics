import numpy as np
import glfw
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.arrays import vbo


def draw_grass():
    #green grass using a rectangle (QUAD)
    glColor3f(0.0, 1.0, 0.0)  #green color for grass
    glBegin(GL_QUADS)
    glVertex2f(-1.0, -1.0)  #Bottom-left
    glVertex2f(1.0, -1.0)   #Bottom-right
    glVertex2f(1.0, -0.4)   #Top-right
    glVertex2f(-1.0, -0.4)  #Top-left
    glEnd()


def draw_river():
    #blue river as a horizontal rectangle
    glColor3f(0.0, 0.0, 1.0)  #Blue color for river
    glBegin(GL_QUADS)
    glVertex2f(-1.0, -0.4)  #Bottom-left of river
    glVertex2f(1.0, -0.4)   #Bottom-right of river
    glVertex2f(1.0, 0.0)    #Top-right of river
    glVertex2f(-1.0, 0.0)   #Top-left of river
    glEnd()


def draw_mountains():
    #two brown triangles representing mountains
    glColor3f(0.6, 0.3, 0.1)  #Brown color for mountains
    
    #Left mountain
    glBegin(GL_TRIANGLES)
    glVertex2f(-1.0, 0.0)   #Bottom-left of mountain
    glVertex2f(-0.5, 0.8)   #Top of mountain
    glVertex2f(0.0, 0.0)   #Bottom-right of mountain
    glEnd()
    
    #Right mountain
    glBegin(GL_TRIANGLES)
    glVertex2f(0.0, 0.0)    #Bottom-left of mountain
    glVertex2f(0.5, 0.8)    #Top of mountain
    glVertex2f(1.0, 0.0)    #Bottom-right of mountain
    glEnd()


def draw_sunset():
    num_segments = 100
    angle_step = 2 * np.pi / num_segments
    radius = 0.4  #radius of the sun(this will be the size of the visible part)
    vertices = []
    colors = []

    #positioning the sun at the intersection point of the mountains (so that its in centor)
    sun_center_x = 0.0
    sun_center_y = 0.0 

    #calculing the angle between the two mountain peaks to find out how much sun should be visible 
    left_peak = (-0.5, 0.8)
    right_peak = (0.5, 0.8)

    left_angle = np.arctan2(left_peak[1] - sun_center_y, left_peak[0] - sun_center_x)
    right_angle = np.arctan2(right_peak[1] - sun_center_y, right_peak[0] - sun_center_x)
    
    if left_angle >= right_angle:
        left_angle, right_angle = right_angle, left_angle  #ensure left_angle < right_angle
    
    #creating vertices for the arc of the sun
    for i in range(num_segments):
        angle = left_angle + (right_angle - left_angle) * (i / num_segments)
        x = sun_center_x + radius * np.cos(angle)
        y = sun_center_y + radius * np.sin(angle)
        vertices.append((x, y))

        #sun gradient colors
        r = 1.0 - (i / num_segments) * 0.5  #from yellow-orange to red
        g = 0.5  
        b = 0.0  

        colors.append((r, g, b))

    vertices = np.array(vertices, dtype=np.float32)
    colors = np.array(colors, dtype=np.float32)

    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(sun_center_x, sun_center_y)  #center of the sun at the intersection
    for i in range(num_segments):
        glColor3fv(colors[i])  #apply color for this vertex
        glVertex2fv(vertices[i])  #apply position for this vertex
    glEnd()


def render_scene():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    #the grass
    draw_grass()
    #the river
    draw_river()
    #the mountains
    draw_mountains()
    #the sunset inside the V shape
    draw_sunset()
    glFlush()


def main():
    if not glfw.init():
        return
    
    window = glfw.create_window(800, 600, "2D Scenery: Grass, River, Mountains, and Sunset", None, None)
    if not window:
        glfw.terminate()
        return
    
    glfw.make_context_current(window)
    
    #background color to light blue (for the sky)
    glClearColor(0.53, 0.81, 0.98, 1.0)
    
    while not glfw.window_should_close(window):
        render_scene()
        
        glfw.swap_buffers(window)
        glfw.poll_events()
    
    glfw.terminate()


if __name__ == "__main__":
    main()
