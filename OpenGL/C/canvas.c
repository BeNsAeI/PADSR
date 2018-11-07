/*
 * canvas.c -- An example of subwindows and event handling
 */

#include <GL/glut.h>

#define FRAME_W 42
#define FRAME_H 23

#define MIN_W 45
#define MIN_H 45

#define RUL_H 20

#define FONT			GLUT_BITMAP_8_BY_13
#define CHAR_W			8
#define CHAR_H			13
#define CHAR_DESCENT		3
#define LINE_SEP		2
#define CARRIAGE_RETURN		13
#define BACK_SPACE		8

int canW = 300, canH = 200;
int rulX0 = 0;
int pixsPer16th;
int triX0 = 50, triY0 = 50, triX1 = 75, triY1 = 75;
int squX0 = 100, squY0 = 50, squX1 = 150, squY1 = 100;
int movingSqu = 0, movingTri = 0;
int prevX, prevY;

int frameWin, rulerWin, canvasWin;

/* (from OpenGL Programming Guide, 2nd edition, page 601)
 If exact two-dimensional raterization is desired, you must
 carefully specify both the orthographic projection and the vertices
 of primitives that are to be rasterized.  The orthographic projection
 should be specified with integer coordinates, as shown in the
 following example:
      gluOrtho2D(0, width, 0, height);
 where width and height are the dimensions of the viewport.  Given
 this projection matrix, polygon vertices and pixel image positions
 should be placed at integer coordinates to rasterize predictably.
 For example, glRecti(0,0,1,1) reliably fills the lower left pixel of
 the viewport, and glRasterPos2i(0,0) reliably positions an unzoomed
 image at the lower left of the viewport.  Point vertices, line
 vertices, and bitmap positions should be placed at half-integer
 locations, however.  For example, a line drawn from (x1,0.5) to
 (x2,0.5) will be reliably rendered along the bottom row of pixels
 into the viewport, and a point drawn at (0.5,0.5) will reliably fill
 the same pixel as glRecti(0,0,1,1).

 An optimum compromise that allows all primitives to be specified at
 integer positions, while still ensuring predictable rasterization, is
 to translate x and y by 0.375, as shown in the following code
 fragment [reshapeCB()].  Such a translation keeps polygon and pixel
 image edges safely away from the centers of pixels, while moving line
 vertices close enough to the pixel centers.
*/
void reshapeCB(int w, int h)	/* generic 2D reshape callback */
{
  glViewport(0,0,w,h);
  glMatrixMode(GL_PROJECTION);
  glLoadIdentity();
  gluOrtho2D(0,w,0,h);
  glScalef(1.0,-1.0,1.0);	/* this flips the coordinate system so
				 that y increases going down the
				 screen (see below) */
  glTranslatef(0.0,-h,0.0);
  glMatrixMode(GL_MODELVIEW);
  glLoadIdentity();
  glTranslatef(0.375,0.375,0.0);/* so we can draw using integer
				   coordinates (see above) */
}
/*
 Note the flip of the y coordinate.  GLUT thinks the upper left hand
 corner of the screen or window is (0,0).  OpenGL, by default, thinks
 the lower left corner is (0,0).  This presents a problem when, for
 example, you compare the coordinates of a mouse event (from GLUT) with the
 coordinates of an OpenGL object.  The y coordinate flip makes OpenGL
 coordinates correspond to GLUT coordinates.
*/

/*-------------------- Frame ----------------------------*/
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

void displayFrameCB(void)
{
  glClear(GL_COLOR_BUFFER_BIT);
  
  glColor3f(0.0,0.0,0.0);
  emitString("What does this do?",10,CHAR_H);
  glutSwapBuffers();
}

void reshapeFrameCB(int tw, int th)
{
  int w,h;

  if( tw < MIN_W ) w = MIN_W; else w = tw;
  if( th < MIN_H ) h = MIN_H; else h = th;
  if( w != tw || h != th ) glutReshapeWindow(w,h);

  reshapeCB(w,h);

  /* reshape and position other windows */
  glutSetWindow(rulerWin);
  glutPositionWindow(FRAME_W,h-RUL_H);
  glutReshapeWindow(w-FRAME_W,RUL_H);

  canW = w-FRAME_W;
  canH = h-FRAME_H-RUL_H;
  glutSetWindow(canvasWin);
  glutPositionWindow(FRAME_W,FRAME_H);
  glutReshapeWindow(canW,canH);
}


void openFrameWindow(void)
{
  glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE);
  glutInitWindowSize(canW+FRAME_W,canH+FRAME_H+RUL_H);

  frameWin = glutCreateWindow("Draw");
  glClearColor(1,1,1,0);		/* set clear color to white */

  glutDisplayFunc(displayFrameCB);
  glutReshapeFunc(reshapeFrameCB);
}

/*--------------------- Ruler ------------------------------*/
void displayRulerCB(void)
{
  GLfloat x;
  int m,w;

  glClear(GL_COLOR_BUFFER_BIT);

  glColor3f(0.0,0.0,0.0);
  w = glutGet(GLUT_WINDOW_WIDTH);	/* get the width of the
					   rulerWin */
  glBegin(GL_LINES);
  for( m=1+rulX0/pixsPer16th,x=(float)m*pixsPer16th-rulX0;
       x<w;
       x += pixsPer16th,++m ) {
    glVertex2f(x,0.0);
    glVertex2f(x,4.0);
  }
  glEnd();

  glutSwapBuffers();
}

void mouseRulerCB(int mousebutton, int state, int x, int y)
{
  if( state == GLUT_DOWN ) {
    prevX = x;
  }
}

void motionRulerCB(int x, int y)
{
  rulX0 = rulX0+prevX-x;
  prevX = x;
  if( rulX0 < 0 ) rulX0 = 0;
  glutPostRedisplay();
}

void openRulerWindow(void)
{
  rulerWin = glutCreateSubWindow(frameWin,FRAME_W,
				  glutGet(GLUT_WINDOW_HEIGHT)-RUL_H,
				  glutGet(GLUT_WINDOW_WIDTH)-FRAME_W,
				  RUL_H);
  glClearColor(0,1,0,0);
  glutDisplayFunc(displayRulerCB);
  glutReshapeFunc(reshapeCB);
  glutMouseFunc(mouseRulerCB);
  glutMotionFunc(motionRulerCB);
}

 


/*---------------------- Canvas ----------------------------*/
void displayCanvasCB(void)
{
  glClear(GL_COLOR_BUFFER_BIT);

  /* draw triangle */
  glColor3f(1,0,0);
  glBegin(GL_POLYGON);
  glVertex2i((triX0+triX1)/2,triY0);
  glVertex2i(triX0,triY1);
  glVertex2i(triX1,triY1);
  glEnd();

    /* draw square */
  glColor3f(0,0,1);
  glBegin(GL_LINE_LOOP);
  glVertex2i(squX0,squY0);
  glVertex2i(squX0,squY1);
  glVertex2i(squX1,squY1);
  glVertex2i(squX1,squY0);
  glEnd();

  glutSwapBuffers();		/* <----- VERY IMPORTANT */
  /* All drawing commands in a double buffered window go to the
     undisplayed buffer.  glutSwapBuffers() displays this buffer. */
}

void keyCanvasCB(unsigned char key, int x, int y)
{
  if( key == 'q' || key == 'Q' ) exit(0);
}


void mouseCanvasCB(int mousebutton, int state, int x, int y)
{
  if( state == GLUT_UP ) {	/* mouse button released */
    prevX = x; prevY = y;		/* set the start position for moves */
    if( triX0 <= x && x <= triX1 &&
	triY0 <= y && y <= triY1 ) {	/* inside triangle bounding box */
      movingTri = 1-movingTri;		/* toggle move */
    }
    if( squX0 <= x && x <= squX1 &&
	squY0 <= y && y <= squY1 ) {	/* inside square bounding box */
      movingSqu = 1-movingSqu;
    }
  }
}

/* passiveMotionCanvasCB is called whenever the mouse moves in the
   canvas window */
void passiveMotionCanvasCB(int x, int y)
{
  int deltax, deltay;

  if( movingTri || movingSqu ) {
    if( movingTri ) {
      deltax = x-prevX;
      deltay = y-prevY;
      if( triX0 + deltax < 0 ) deltax = -triX0;
      if( triY0 + deltay < 0 ) deltay = -triY0;
      triX0 += deltax; triY0 += deltay;
      triX1 += deltax; triY1 += deltay;
    }
    if( movingSqu ) {
      deltax = x-prevX;
      deltay = y-prevY;
      if( squX0 + deltax < 0 ) deltax = -squX0;
      if( squY0 + deltay < 0 ) deltay = -squY0;
      squX0 += deltax; squY0 += deltay;
      squX1 += deltax; squY1 += deltay;
    }
    prevX = x;  prevY = y;
    glutPostRedisplay();	/* <-------- force a display event */
  }
}

void openCanvasWindow(void)
{
  canvasWin = glutCreateSubWindow(frameWin,FRAME_W,FRAME_H,canW,canH);
  glClearColor(1,1,0,0);
  glutDisplayFunc(displayCanvasCB);	/* required */
  glutReshapeFunc(reshapeCB);
  glutKeyboardFunc(keyCanvasCB);
  glutMouseFunc(mouseCanvasCB);
  glutPassiveMotionFunc(passiveMotionCanvasCB);
}

int main(int argc, char *argv[])
{
  int scrW,scrWmm;

  glutInit(&argc, argv);		/* initialize GLUT system */

  /* calculate pixels per 16th of an inch */
  scrW = glutGet(GLUT_SCREEN_WIDTH);
  scrWmm = glutGet(GLUT_SCREEN_WIDTH_MM);
  if( scrW == 0 || scrWmm == 0 ) pixsPer16th=89.0/16.0;
  else pixsPer16th = (scrW*25.4)/(scrWmm*16.0);

  openFrameWindow();		/* frameWin is the parent window */
  openRulerWindow();		/* rulerWin is a subwindow of frameWin */
  openCanvasWindow();		/* canvasWin is a subwindow of frameWin */

  glutMainLoop();
  return 0;
}

