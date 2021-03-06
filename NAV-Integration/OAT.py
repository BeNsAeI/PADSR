#Obstacle Avoidance Test
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import time
import sys
import numpy as np
import math

name = 'ball_glut'
frame_rate = 60.0
time_frame = 1.0
time_step = time_frame / frame_rate
Time = 0.0
sphere_count = 50
sphere_poly = 16
sphere_mass = 5
sphere_radious = 0.25
spring_activation_radious = sphere_radious * 8
from random import randint
start_coordinate = [randint(-13, 13),randint(-13, 13)]
destination = [randint(-13, 13),randint(-13, 13)]
print ("Task is to go from (" + str(start_coordinate[0]) + ", " + str(start_coordinate[1]) + ") to (" + str(destination[0]) + ", " + str(destination[1])+ ").")
sphere_coord = [start_coordinate[0], start_coordinate[1], 0]
variance = 25.0
rand_sphere_coords = []
raw_force = 15
dynamic_force = 1
global_k = 1.50
destination_threshold = sphere_radious * 2
path = []
halt_threshold = 1

def main():
	#setting up obstacles:
	global rand_sphere_coords
	rand_sphere_coords = np.random.rand(sphere_count,3)
	for i in rand_sphere_coords:
		i[0] = i[0] * variance - variance/2
		i[1] = i[1] * variance - variance/2
		i[2] = spring_activation_radious
	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
	glutInitWindowSize(800,600)
	glutCreateWindow(name)

	glClearColor(0.,0.,0.,1.)
	glShadeModel(GL_SMOOTH)
	glEnable(GL_CULL_FACE)
	glEnable(GL_DEPTH_TEST)
	glEnable(GL_LIGHTING)
	lightZeroPosition = [10.,4.,10.,1.]
	lightZeroColor = [0.8,1.0,0.8,1.0] #green tinged
	glLightfv(GL_LIGHT0, GL_POSITION, lightZeroPosition)
	glLightfv(GL_LIGHT0, GL_DIFFUSE, lightZeroColor)
	glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.1)
	glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
	glEnable(GL_LIGHT0)
	global Time
	Time = time.time()
	glutDisplayFunc(display)
	glMatrixMode(GL_PROJECTION)
	gluPerspective(40.,1.,10.,40.)
	glMatrixMode(GL_MODELVIEW)
	gluLookAt(0,0,40,0,0,0,0,1,0)
	glPushMatrix()
	glutMainLoop()
	return
def sphere_force():
	return raw_force * dynamic_force
def vector(destination):
	global sphere_coord
	if math.sqrt( (destination[0]-sphere_coord[0])**2 + (destination[1]-sphere_coord[1])**2 ) < destination_threshold:
		vector_x = 0
		vector_y = 0
		print ("Done!")
		exit(0)
	else:
		R = math.sqrt( (destination[0]-sphere_coord[0])**2 + (destination[1]-sphere_coord[1])**2 )
		vector_x = (destination[0] - sphere_coord[0])/(R) * sphere_force()
		vector_y = (destination[1] - sphere_coord[1])/(R) * sphere_force()

	return vector_x, vector_y

def spring(destination):
	global dynamic_force
	nearby_spheres = []
	for i in rand_sphere_coords:
		if math.sqrt( (i[0]-sphere_coord[0])**2 + (i[1]-sphere_coord[1])**2 ) < spring_activation_radious * 2:
			nearby_spheres.append([i[0],i[1],i[2]])
	force = 0
	force_x = vector(destination)[0]
	force_y = vector(destination)[1]
	for i in range(0,len(nearby_spheres)-1):
		if abs(nearby_spheres[i][0] - nearby_spheres[i+1][0]) < spring_activation_radious/2 and\
		abs(nearby_spheres[i][1] - nearby_spheres[i+1][1]) < spring_activation_radious/2:
			nearby_spheres[i][2] = nearby_spheres[i][2] + \
								   math.sqrt( abs(nearby_spheres[i][0] - nearby_spheres[i+1][0]) ** 2 + abs(nearby_spheres[i][1] - nearby_spheres[i+1][1]) ** 2)/2
			nearby_spheres[i+1][2] = nearby_spheres[i][2]
			nearby_spheres[i][0] = (nearby_spheres[i][0] + nearby_spheres[i+1][0])/2
			nearby_spheres[i+1][0] = nearby_spheres[i][0]
			nearby_spheres[i][1] = (nearby_spheres[i][1] + nearby_spheres[i+1][1])/2
			nearby_spheres[i+1][1] = nearby_spheres[i][1]

	for i in nearby_spheres:
		#if math.sqrt( (i[0]-sphere_coord[0])**2 + (i[1]-sphere_coord[1])**2 ) < spring_activation_radious:
			glPushMatrix()
			color = [0.0625,0.0625,0.0625,1]
			glMaterialfv(GL_FRONT,GL_DIFFUSE,color)
			glTranslatef(i[0], i[1], 0)
			glutWireSphere(i[2],sphere_poly/2,sphere_poly/2)
			glPopMatrix()
			k = global_k
			R = math.sqrt( (i[0]-sphere_coord[0])**2 + (i[1]-sphere_coord[1])**2 )
			if i[0] != sphere_coord[0]:
				d_x = abs(i[2] * sphere_coord[0])/R - abs(i[0] - sphere_coord[0])
				d_y = abs(i[2] * sphere_coord[1])/R - abs(i[1] - sphere_coord[1])
			force_x -= (i[0] - sphere_coord[0])/R * (k * d_x)
			force_y -= (i[1] - sphere_coord[1])/R * (k * d_y)
	if (abs(force_x) < halt_threshold and abs(force_y) < halt_threshold):
		#print("Forces increasing: <" + str(force_x,) + ", " + str(force_y) + ">")
		dynamic_force += 0.1
	if (abs(force_x) > raw_force or abs(force_y) > raw_force):
		#print("Forces decreasing: <" + str(force_x,) + ", " + str(force_y) + ">")
		dynamic_force = 1
	return force_x, force_y

def sphere_speed(destination):
	return (spring(destination)[0] / sphere_mass), (spring(destination)[1] / sphere_mass)

def update(time):
	global sphere_speed
	global path
	path.append([sphere_coord[0],sphere_coord[1]])
	sphere_coord[0] += sphere_speed(destination)[0] * time
	sphere_coord[1] += sphere_speed(destination)[1] * time

def animate():
	global Time
	new_time = time.time()
	if new_time < Time:
		Time = new_time
		return
	if abs(new_time - Time) > time_step:
		update(new_time - Time)
		Time = new_time

def display():
	glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
	animate()

	glPushMatrix()
	color = [0.0, 1.0, 0.0,1]
	glMaterialfv(GL_FRONT,GL_DIFFUSE,color)
	glTranslatef(start_coordinate[0], start_coordinate[1], 0)
	glutWireSphere(sphere_radious*2,sphere_poly/4,sphere_poly/4)
	glPopMatrix()

	glPushMatrix()
	color = [1.0, 0.0, 0.0,1]
	glMaterialfv(GL_FRONT,GL_DIFFUSE,color)
	glTranslatef(destination[0], destination[1], 0)
	glutWireSphere(sphere_radious*2,sphere_poly/4,sphere_poly/4)
	glPopMatrix()

	glPushMatrix()
	color = [0.0, 1.0, 0.0, 1.0]
	glMaterialfv(GL_FRONT,GL_DIFFUSE,color)
	glTranslatef(sphere_coord[0], sphere_coord[1],sphere_coord[2])
	glutSolidSphere(sphere_radious,sphere_poly,sphere_poly)
	glPopMatrix()

	for i in rand_sphere_coords:
		glPushMatrix()
		color = [1.0,0.5,0.5,1.0]
		glMaterialfv(GL_FRONT,GL_DIFFUSE,color)
		glTranslatef(i[0], i[1], 0)
		glutSolidSphere(sphere_radious,sphere_poly,sphere_poly)
		glPopMatrix()

	glPushMatrix()
	glLineWidth(5)
	glBegin(GL_LINES)
	glColor3f(1.0, 1.0, 1.0)
	for i in path:
		glVertex3f(i[0], i[1], 1.0)
	glEnd()
	glLineWidth(1)
	glPopMatrix()

	glutSwapBuffers()
	glutPostRedisplay()
	return

if __name__ == '__main__': main()
