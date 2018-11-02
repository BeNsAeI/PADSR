from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys

name = 'OpenGL Python Teapot'
CameraPosx = 0;
CameraPosy = 0;
CameraPosz = 20;
Orientx = 0.0;
Orienty = 0.0;
BoxList = None

def keyboard(key, x, y):
	global Orientx;
	global Orienty;
	print("keyboard called with "+ key + ".")
	if key == 'w' and Orientx < 90:
		Orientx += 5
	if key == 's' and Orientx > -90:
		Orientx -= 5
	if key == 'a' and Orienty > -90:
		Orienty -= 5
	if key == 'd' and Orienty < 90:
		Orienty += 5
	print ("(" + str(Orientx) + ", " + str(Orienty) + ")")

def main():
	
	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
	glutInitWindowSize(640,480)
	glutCreateWindow(name)
	glutKeyboardFunc(keyboard)
	glClearColor(0.,0.,0.,1.)
	glShadeModel(GL_SMOOTH)
	glEnable(GL_CULL_FACE)
	glEnable(GL_DEPTH_TEST)
	glEnable(GL_LIGHTING)
	lightZeroPosition = [0.,0.,20.,1.]
	lightZeroColor = [1.8,1.0,0.8,1.0] #green tinged
	glLightfv(GL_LIGHT0, GL_POSITION, lightZeroPosition)
	glLightfv(GL_LIGHT0, GL_DIFFUSE, lightZeroColor)
	glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.1)
	glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
	glEnable(GL_LIGHT0)
	makeList()
	glutDisplayFunc(display)
	glMatrixMode(GL_PROJECTION)
	gluPerspective(40.,1.,1.,40.)
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
	blockMultiplier = 2
	blockSize = 0.05
	offsetx = -8
	offsety = -6.5
	offsetz = -3
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
	print ("(" + str(Orientx) + ", " + str(Orienty) + ")")
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
