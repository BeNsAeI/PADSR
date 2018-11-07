from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from OpenGL.GL.shaders import *
import random
from math import *  # trigonometry
import pygame  # just to get a display
import sys
import time
import numpy
import math
from PIL import Image
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Video_To_Depthmap/')))
from video_converter_2 import VideoConverter2
from Shader import ShaderProcessor
import cv2

name = 'OpenGL Python Scene'
CameraPosx = 0
CameraPosy = 0
CameraPosz = 45
Orientx = 0.0
Orienty = 45.0
multiplier = 10.0
uMultiplier = None
BoxList = None
uRGB = None
uDepth = None

print("Python OpenGL version: " + str(OpenGL.__version__))

converter = VideoConverter2()
frameList, depthmapList = converter.convert_video("test.mp4", "out.pm4", True, False, 1, True)

frameList_iter = iter(frameList)
depthmapList_iter = iter(depthmapList)

def getNextFrame(list_iter):
    try:
        return list_iter.next()
    except StopIteration:
        return None

def createAndCompileShader(type, source):
    shader = glCreateShader(type)
    glShaderSource(shader, source)
    glCompileShader(shader)
    result = glGetShaderiv(shader, GL_COMPILE_STATUS)
    if (result != 1):  # shader didn't compile
        raise Exception(
            "Couldn't compile shader\nShader compilation Log:\n"+glGetShaderInfoLog(shader))
    return shader


def keyboard(key, x, y):
    global Orientx
    global Orienty
    global multiplier
    #print("keyboard called with "+ key + ".")
    if key == 'w' and Orientx < 90:
        Orientx += 1
    if key == 's' and Orientx > -90:
        Orientx -= 1
    if key == 'a' and Orienty > -90:
        Orienty -= 1
    if key == 'd' and Orienty < 90:
        Orienty += 1
    if key == 'h':
        Orientx = 0
        Orienty = 0
    if key == '=' and multiplier < 20:
        multiplier += 0.25
    if key == "-" and multiplier > -20:
        multiplier -= 0.25
    #print ("(" + str(Orientx) + ", " + str(Orienty) + ")")


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(640, 480)
    glutCreateWindow(name)
    glutKeyboardFunc(keyboard)
    glClearColor(0., 0., 0., 1.)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)

    shaderProcessor = ShaderProcessor()
    vertex_shader = shaderProcessor.createVertexShader()
    fragment_shader = shaderProcessor.createFragmentShader()

    program = glCreateProgram()
    glAttachShader(program, vertex_shader)
    glAttachShader(program, fragment_shader)
    glLinkProgram(program)
    # glDeleteShader(vertex_shader)
    # glDeleteShader(fragment_shader)
    try:
        glUseProgram(program)
    except OpenGL.error.GLError:
        print glGetProgramInfoLog(program)
        raise
    global uRGB
    global uDepth
    uDepth = glGetUniformLocation(program, "depth")
    uRGB = glGetUniformLocation(program, "RGB")
    global uMultiplier
    uMultiplier = glGetUniformLocation(program, "uMultiplier")
    uKa = glGetUniformLocation(program, "uKa")
    uKd = glGetUniformLocation(program, "uKd")
    uKs = glGetUniformLocation(program, "uKs")
    uShininess = glGetUniformLocation(program, "uShininess")

    if uKa < 0 or uKd < 0 or uKs < 0 or uShininess < 0:
        print "Error finding float lighting values."
    #	exit(1)
    if uDepth < 0 or uRGB < 0:
        print "Error finding sampler texture declearqations."
        print ("Values -> uRGB: " + str(uRGB) + ", uDepth:" + str(uDepth))
    #	exit(1)

    glUniform1f(uMultiplier, 0)
    glUniform1f(uKa, 0.25)
    glUniform1f(uKd, 0.5)
    glUniform1f(uKs, 0.25)
    glUniform1f(uShininess, 1)

    # set background texture
    global RGB
    global Depth
    global rgb
    global depth
    global rgbData
    global depthData


    glEnable(GL_LIGHTING)
    lightZeroPosition = [0., 0., 20., 1.]
    lightZeroColor = [1.8, 1.0, 0.8, 1.0]  # green tinged
    glLightfv(GL_LIGHT0, GL_POSITION, lightZeroPosition)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightZeroColor)
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.1)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
    glEnable(GL_LIGHT0)
    glUseProgram(program)
    makeList()
    glutDisplayFunc(display)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(40., 1., 0.1, 80.)
    glMatrixMode(GL_MODELVIEW)
    gluLookAt(CameraPosx, CameraPosy, CameraPosz, 0, 0, 0, 0, 1, 0)
    glPushMatrix()
    glutMainLoop()
    return


def makeList():
    global BoxList
    BoxList = glGenLists(1)
    glNewList(BoxList, GL_COMPILE)

    color = [1.0, 1., 0., 1.]
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, color)
    blockMultiplier = 1
    blockSize = 0.05
    offsetx = -16.125
    offsety = -12.5
    offsetz = 0
    glRotatef(180, 0, 0, 1)
    glBegin(GL_QUADS)
    color = [1.0, 1., 0., 1.]
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, color)

    for i in range(0, 640/blockMultiplier):
        for j in range(0, 480/blockMultiplier):
            glMultiTexCoord2f(0, (float(i))/(641), (float(j))/(481))
            glVertex(i * blockSize + offsetx,  j *
                     blockSize + offsety, 0 + offsetz)
            glMultiTexCoord2f(0, (float(i+1))/(641), (float(j))/(481))
            glVertex((i+1) * blockSize + offsetx,  j *
                     blockSize + offsety, 0 + offsetz)
            glMultiTexCoord2f(0, (float(i+1))/(641), (float(j+1))/(481))
            glVertex((i+1) * blockSize + offsetx, (j+1)
                     * blockSize + offsety, 0 + offsetz)
            glMultiTexCoord2f(0, (float(i))/(641), (float(j+1))/(481))
            glVertex(i * blockSize + offsetx, (j+1) *
                     blockSize + offsety, 0 + offsetz)

    glEnd()

    glEndList()


def display():
    global multiplier
    global uMultiplier
    global RGB
    global Depth
    global rgb
    global depth

    rgbData = getNextFrame(frameList_iter)
    depthData = getNextFrame(depthmapList_iter)
    if depthData is None:
        return
    depthData = cv2.cvtColor(depthData,cv2.COLOR_GRAY2RGB)

    glEnable(GL_TEXTURE_2D)
    glActiveTexture(GL_TEXTURE0)
    RGBTexture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, RGBTexture)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB,
                 rgbData.shape[1], rgbData.shape[0], 0, GL_RGB, GL_UNSIGNED_BYTE, rgbData)

    glActiveTexture(GL_TEXTURE1)
    DepthTexture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, DepthTexture)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB,
                 depthData.shape[1], depthData.shape[0], 0, GL_RGB, GL_UNSIGNED_BYTE, depthData)

    glUniform1i(uRGB, 0)
    glUniform1i(uDepth, 1)

    glUniform1f(uMultiplier, multiplier)
    #print ("(" + str(Orientx) + ", " + str(Orienty) + ")")
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glPushMatrix()
    glRotate(Orientx, 1, 0, 0)
    glRotate(Orienty, 0, 1, 0)
    # Call the shader begin right before here
    glCallList(BoxList)
    # end to call to shader
    glPopMatrix()
    glutSwapBuffers()
    glutPostRedisplay()
    return


if __name__ == '__main__':
    main()
