from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import OpenGL.GL.shaders
import random
import math
import pygame  # just to get a display
import sys
import time
import numpy
import math
from PIL import Image
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from Integration.Video_To_Depthmap.video_converter import VideoConverter

name = 'OpenGL Python Scene'
CameraPosx = 0
CameraPosy = 0
CameraPosz = 45
Orientx = 0.0
Orienty = 45.0
multiplier = 5.0
uMultiplier = None
BoxList = None
rgb = None
depth = None
rgbData = None
depthData = None
converter = None
frame_and_depth_map_gen = None
uRGB = None
uDepth = None

print("Python OpenGL version: " + str(OpenGL.__version__))


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

def run_opengl(input_video, low, step, fast, nn):
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(640, 480)
    glutCreateWindow(name)
    glutKeyboardFunc(keyboard)
    glClearColor(0., 0., 0., 1.)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)

    vertex_shader = createAndCompileShader(GL_VERTEX_SHADER, """
	#version 130
	uniform sampler2D depth;
	uniform float uMultiplier;
	out vec2 vST; // texture coords
	out vec3 vN; // normal vector
	out vec3 vL; // vector from point to light
	out vec3 vE; // vector from point to eye
	const vec3 LIGHTPOSITION = vec3( 5., 5., 0. );
	const float PI = 3.14159265;
	const float AMP = 0.2;
	const float W = 2.;

	void
	main( )
	{
		vST = gl_MultiTexCoord0.st;
		vec3 vert = gl_Vertex.xyz;
		vert.z = texture2D(depth, vST).r * uMultiplier;
		vec4 ECposition = gl_ModelViewMatrix * gl_Vertex;
		vec3 aLocalNormal = gl_Normal;
		vN = normalize( gl_NormalMatrix * aLocalNormal ); // normal vector
		vN.z = vN.z + vert.z;
		vL = LIGHTPOSITION - ECposition.xyz; // vector from the point
		// to the light position
		vE = vec3( 0., 0., 0. ) - ECposition.xyz; // vector from the point
		// to the eye position
		gl_Position = gl_ModelViewProjectionMatrix * vec4(vert,1);
	}
	""")

    fragment_shader = createAndCompileShader(GL_FRAGMENT_SHADER, """
	#version 130
	uniform sampler2D RGB;
	uniform float uKa, uKd, uKs; // coefficients of each type of lighting
	uniform float uShininess; // specular exponent
	in vec2 vST; // texture cords
	in vec3 vN; // normal vector
	in vec3 vL; // vector from point to light
	in vec3 vE; // vector from point to eye
	void
	main( )
	{
		vec3 myColor = texture2D(RGB, vST).rgb;
		vec3 Normal = normalize(vN);
		vec3 Light = normalize(vL);
		vec3 Eye = normalize(vE);
		vec3 ambient = uKa * myColor;
		float d = max( dot(Normal,Light), 0. ); // only do diffuse if the light can see the point
		vec3 diffuse = uKd * d * myColor;
		float s = 0.;
		if( dot(Normal,Light) > 0. ) // only do specular if the light can see the point
		{
			vec3 ref = normalize( reflect( -Light, Normal ) );
			s = pow( max( dot(Eye,ref),0. ), uShininess );
		}
		vec3 specular = uKs * s * vec3(1,1,1);
		gl_FragColor = vec4( ambient + diffuse + specular, 1. );
	}
	""")
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
    global rgb
    global depth
    global rgbData
    global depthData
    global converter
    global frame_and_depth_map_gen

    converter = VideoConverter(input_video, low, step, fast, nn)
    frame_and_depth_map_gen = converter.get_frame_and_depth_map()

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
    global Depth
    global rgb
    global rgbData
    global depth
    global depthData
    global converter
    global frame_and_depth_map_gen

    try:
        depthData, rgbData = next(frame_and_depth_map_gen)
    except StopIteration:
        frame_and_depth_map_gen = converter.get_frame_and_depth_map()
        depthData, rgbData = next(frame_and_depth_map_gen)

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
    run_opengl(os.path.dirname(os.path.abspath(__file__))+"/../Video_To_Depthmap/test.mp4", True, 1, False)
