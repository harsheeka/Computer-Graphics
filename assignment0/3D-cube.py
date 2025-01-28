import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
import pyrr

#vertex shader source code
vertex_src = """
layout(location = 0) in vec3 a_position;
uniform mat4 rotation;
void main()
{
    gl_Position = rotation * vec4(a_position, 1.0);
}
"""

#fragment shader source code
fragment_src = """
out vec4 out_color;
void main()
{
    out_color = vec4(1.0, 0.0, 0.0, 1.0); // Red
}
"""

def window_resize(window, width, height):    #function for window sizing
    glViewport(0, 0, width, height)


if not glfw.init():       #initialise glfw
    raise Exception("GLFW initialization failed!")

window = glfw.create_window(800, 600, "Rotating 3D Cube", None, None) #creating a glfw window
if not window:
    glfw.terminate()
    raise Exception("GLFW window creation failed!")

glfw.set_window_pos(window, 100, 100)   #setting up window's position
glfw.make_context_current(window)
glfw.set_window_size_callback(window, window_resize)

#cube vertices
vertices = [
    # Front face
    -0.5, -0.5,  0.5,
     0.5, -0.5,  0.5,
     0.5,  0.5,  0.5,
    -0.5,  0.5,  0.5,
    # Back face
    -0.5, -0.5, -0.5,
     0.5, -0.5, -0.5,
     0.5,  0.5, -0.5,
    -0.5,  0.5, -0.5
]

#indices for cube
indices = [
    # Front face
    0, 1, 2, 2, 3, 0,
    # Back face
    4, 5, 6, 6, 7, 4,
    # Left face
    4, 0, 3, 3, 7, 4,
    # Right face
    1, 5, 6, 6, 2, 1,
    # Top face
    3, 2, 6, 6, 7, 3,
    # Bottom face
    4, 5, 1, 1, 0, 4
]

vertices = np.array(vertices, dtype=np.float32)
indices = np.array(indices, dtype=np.uint32)

#compiling shaders
shader = compileProgram(
    compileShader(vertex_src, GL_VERTEX_SHADER),
    compileShader(fragment_src, GL_FRAGMENT_SHADER)
)

VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

EBO = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)


glEnableVertexAttribArray(0)    #position attribute
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))

glUseProgram(shader)

#setting the background color and enabling depth testing
glClearColor(0.1, 0.1, 0.1, 1.0)
glEnable(GL_DEPTH_TEST)

#uniform location for rotation
rotation_loc = glGetUniformLocation(shader, "rotation")


while not glfw.window_should_close(window):     #main loop starts here
    glfw.poll_events()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

#creating rotation matrices
    rot_x = pyrr.Matrix44.from_x_rotation(0.5 * glfw.get_time())
    rot_y = pyrr.Matrix44.from_y_rotation(0.8 * glfw.get_time())
    rotation = pyrr.matrix44.multiply(rot_x, rot_y)

    glUniformMatrix4fv(rotation_loc, 1, GL_FALSE, rotation)

    glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None) #draw the cube

    glfw.swap_buffers(window)  #swap the buffers

glfw.terminate()   
