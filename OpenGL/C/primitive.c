/*
 * primitive.c -- Show off the different geometric primitives in OpenGL
 */

#include <GL/glut.h>

#define FONT			GLUT_BITMAP_8_BY_13
#define CHAR_W			8
#define CHAR_H			13
#define CHAR_DESCENT		3
#define LINE_SEP		2
#define CARRIAGE_RETURN		13
#define BACK_SPACE		8

/* emitString(s, x, y) -- displays string s at location x,y  */
void emitString(char *s, int tx, int ty)
{
  int x,y;

  x = tx;
  y = ty;
  while( *s ) {
    if( *s == CARRIAGE_RETURN ) {
      x = tx;
      y += CHAR_H + LINE_SEP;
    } else {
      glRasterPos2i(x,y);
      glutBitmapCharacter(FONT,*s);
      x += CHAR_W;
   }
    ++s;
  }
}

void displayCB(void)		/* function called whenever redisplay needed */
{
  glClear(GL_COLOR_BUFFER_BIT);		/* clear the display */
  glColor3f(1.0, 1.0, 1.0);		/* set current color to white */

  glLoadIdentity();			/* start with the identity matrix */
  gluOrtho2D(0,500,0,420);		/* how object is mapped to window */
  glMatrixMode(GL_MODELVIEW);		/* move the model around */

#define VERTEX_LIST \
  glVertex2i(20,60);\
  glVertex2i(80,80);\
  glVertex2i(40,40);\
  glVertex2i(60,20);\
  glVertex2i(0,0)

  glTranslatef(43,320,0);	/* translate model to appropriate point */
  glBegin(GL_POINTS);
  VERTEX_LIST;
  glEnd();
  emitString("GL_POINTS",-20,-15);

  glTranslatef(0,-100,0);	/* translations are cumulative */
  glBegin(GL_LINES);
  VERTEX_LIST;
  glEnd();
  emitString("GL_LINES",-20,-15);

  glTranslatef(166,0,0);
  glBegin(GL_LINE_STRIP);
  VERTEX_LIST;
  glEnd();
  emitString("GL_LINE_STRIP",-20,-15);

  glTranslatef(166,0,0);
  glBegin(GL_LINE_LOOP);
  VERTEX_LIST;
  glEnd();
  emitString("GL_LINE_LOOP",-20,-15);

  glTranslatef(-320,-100,0);
  glBegin(GL_TRIANGLES);
  VERTEX_LIST;
  glEnd();
  emitString("GL_TRIANGLES",-20,-15);

  glTranslatef(166,0,0);
  glBegin(GL_TRIANGLE_STRIP);
  VERTEX_LIST;
  glEnd();
  emitString("GL_TRIANGLE_STRIP",-20,-15);

  glTranslatef(166,0,0);
  glBegin(GL_TRIANGLE_FAN);
  VERTEX_LIST;
  glEnd();
  emitString("GL_TRIANGLE_FAN",-20,-15);

  glTranslatef(-320,-100,0);
  glBegin(GL_QUADS);
  VERTEX_LIST;
  glEnd();
  emitString("GL_QUADS",-20,-15);

  glTranslatef(166,0,0);
  glBegin(GL_QUAD_STRIP);
  VERTEX_LIST;
  glEnd();
  emitString("GL_QUAD_STRIP",-20,-15);

  glTranslatef(166,0,0);
  glBegin(GL_POLYGON);
  VERTEX_LIST;
  glEnd();
  emitString("GL_POLYGON",-20,-15);



  glFlush();
}

void keyCB(unsigned char key, int x, int y)	/* called on key press */
{
  if( key == 'q' ) exit(0);
}


int main(int argc, char *argv[])
{
  int win;

  glutInit(&argc, argv);		/* initialize GLUT system */

  glutInitDisplayMode(GLUT_RGB);
  glutInitWindowSize(500,420);		/* width=500pixels height=420pixels */
  win = glutCreateWindow("Primitives");	/* create window */

  /* from this point on the current window is win */

  glClearColor(0.0,0.0,0.0,0.0);	/* set background to black */
  glutDisplayFunc(displayCB);		/* set window's display callback */
  glutKeyboardFunc(keyCB);		/* set window's key callback */

  glutMainLoop();			/* start processing events... */

  /* execution never reaches this point */

  return 0;
}
