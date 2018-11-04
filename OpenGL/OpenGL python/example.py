from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from OpenGL.GL.shaders import *
import random
from math import * # trigonometry
import pygame # just to get a display
import Image
import sys
import time
import numpy, math
from PIL import Image

name = 'OpenGL Python Scene'
CameraPosx = 0;
CameraPosy = 0;
CameraPosz = 20;
Orientx = 0.0;
Orienty = 0.0;
BoxList = None

print("Python OpenGL version: "+ str(OpenGL.__version__))

def createAndCompileShader(type,source):
	shader=glCreateShader(type)
	glShaderSource(shader,source)
	glCompileShader(shader)
	result=glGetShaderiv(shader,GL_COMPILE_STATUS)
	if (result!=1): # shader didn't compile
		raise Exception("Couldn't compile shader\nShader compilation Log:\n"+glGetShaderInfoLog(shader))
	return shader

def keyboard(key, x, y):
	global Orientx;
	global Orienty;
	#print("keyboard called with "+ key + ".")
	if key == 'w' and Orientx < 90:
		Orientx += 5
	if key == 's' and Orientx > -90:
		Orientx -= 5
	if key == 'a' and Orienty > -90:
		Orienty -= 5
	if key == 'd' and Orienty < 90:
		Orienty += 5
	if key == 'h':
		Orientx = 0
		Orienty = 0
	#print ("(" + str(Orientx) + ", " + str(Orienty) + ")")

def main():
	# build shader program
	#uDepth = glGetUniformLocation(program, "depth")
	#uRGB = glGetUniformLocation(program, "RGB")
	#aUV = glGetAttribLocation(program, "uV")
	# set background texture
	#rgb = Image.open(RGB)
	#rgbData = numpy.array(list(rgb.getdata()), numpy.uint8)
	#depth = Image.open(Depth)
	#depthData = numpy.array(list(depth.getdata()), numpy.uint8)
		 
	#RGBTexture = glGenTextures(1)
	#DepthTexture = glGenTextures(1)
	#glBindTexture(GL_TEXTURE_2D, RGBTexture)
	#glBindTexture(GL_TEXTURE_2D, DepthTexture)
	#glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
	#glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
	#glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, rgb.size[0], rgb.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, rgbData)
	#glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, depth.size[0], depth.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, depthData)

	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
	glutInitWindowSize(640,480)
	glutCreateWindow(name)
	glutKeyboardFunc(keyboard)
	glClearColor(0.,0.,0.,1.)
	glShadeModel(GL_SMOOTH)
	glEnable(GL_CULL_FACE)
	glEnable(GL_DEPTH_TEST)

	RGB = "rgb.jpg"
	Depth = "depth.jpg"
	vertex_shader=createAndCompileShader(GL_VERTEX_SHADER,"""
	#version 130
		void main()
		{
			gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
		}
	""");

	fragment_shader=createAndCompileShader(GL_FRAGMENT_SHADER,"""
	#version 130
		void main()
		{
			gl_FragColor = vec4(1,1,1,1.0);
		}
	""");
	program = glCreateProgram()
	glAttachShader(program,vertex_shader)
	glAttachShader(program,fragment_shader)
	glLinkProgram(program)
	#glDeleteShader(vertex_shader)
	#glDeleteShader(fragment_shader)
	try:
		glUseProgram(program)   
	except OpenGL.error.GLError:
		print glGetProgramInfoLog(program)
		raise
	glEnable(GL_LIGHTING)
	lightZeroPosition = [0.,0.,20.,1.]
	lightZeroColor = [1.8,1.0,0.8,1.0] #green tinged
	glLightfv(GL_LIGHT0, GL_POSITION, lightZeroPosition)
	glLightfv(GL_LIGHT0, GL_DIFFUSE, lightZeroColor)
	glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.1)
	glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
	glEnable(GL_LIGHT0)
	glUseProgram(program)
	makeList()
	glutDisplayFunc(display)
	glMatrixMode(GL_PROJECTION)
	gluPerspective(40.,1.,0.1,80.)
	glMatrixMode(GL_MODELVIEW)
	gluLookAt(CameraPosx,CameraPosy,CameraPosz, 0,0,0, 0,1,0)
	glPushMatrix()
	glutMainLoop()
	return
def makeList():
	global BoxList
	BoxList = glGenLists(1)
	glNewList(BoxList, GL_COMPILE)
	
	color = [1.0,1.,0.,1.]
	glMaterialfv(GL_FRONT_AND_BACK,GL_DIFFUSE,color)
	blockMultiplier = 1
	blockSize = 0.05
	offsetx = -16.125
	offsety = -12.5
	offsetz = -25
	glBegin(GL_QUADS)
	color = [1.0,1.,0.,1.]
	glMaterialfv(GL_FRONT_AND_BACK,GL_DIFFUSE,color)
	for i in range (0,640/blockMultiplier):
		for j in range (0,480/blockMultiplier):
			glVertex( i   * blockSize + offsetx,  j   * blockSize + offsety, 0 + offsetz)
			glVertex((i+1)* blockSize + offsetx,  j   * blockSize + offsety, 0 + offsetz)
			glVertex((i+1)* blockSize + offsetx, (j+1)* blockSize + offsety, 0 + offsetz)
			glVertex( i   * blockSize + offsetx, (j+1)* blockSize + offsety, 0 + offsetz)
	glEnd()
	
	glEndList();
def display():
	#print ("(" + str(Orientx) + ", " + str(Orienty) + ")")
	glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
	glPushMatrix()
	glRotate(Orientx,1,0,0)
	glRotate(Orienty,0,1,0)
	# Call the shader begin right before here
	glCallList(BoxList);
	# end to call to shader
	glPopMatrix()
	glutSwapBuffers()
	glutPostRedisplay();
	return

if __name__ == '__main__': main()
