#include <stdio.h>
#include <stdlib.h>
#include <vector>
#include <iomanip>
#include <sstream>

#include "display.hpp"
#include "include/glm/glm.hpp"
#include <MPILib/include/MPINetworkCode.hpp>

using namespace TwoDLib;
using namespace std::chrono;

Display* Display::disp = 0;

Display::Display(){
	lastTime = 0;
	delta = 0;
	num_frames = 0;
	start_time = duration_cast< milliseconds >(
    system_clock::now().time_since_epoch());
	rotator = 0.0f;
	_systems = vector<Ode2DSystem*>();
}

Display::~Display(){
	if (glutGetWindow()){
		Display::getInstance()->updateDisplay();
		glutDestroyWindow(glutGetWindow());
	}
	glutExit();
}

// The OpenGL display function, called as fast as possible.
void Display::display(void) {
	if (_systems.size() == 0)
		return;

	milliseconds real_time = duration_cast< milliseconds >(
    system_clock::now().time_since_epoch());
	milliseconds time_elapsed = real_time - start_time;

	// if (time_elapsed.count() % 10 != 0)
	// 	return;

	glClear(GL_COLOR_BUFFER_BIT);

	// **** used for 3D ****
	// glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
	// glPushMatrix();
	// glTranslatef(0, 0, -1);
	// glRotatef(rotator, 0, 1, 0);
	// glRotatef(rotator / 4, 0, 0, 1);

	glBegin(GL_QUADS);

	Mesh m = _systems[0]->MeshObject();

	LockMutex();

	double max = 0.0;
	for (int i=0; i<_systems[0]->Mass().size(); i++)
		if (max < log10(_systems[0]->Mass()[i] + 0.000006))
			max = log10(_systems[0]->Mass()[i] + 0.000006);

	double min = 1.0;
	for (int i=0; i<_systems[0]->Mass().size(); i++)
		if (log10(_systems[0]->Mass()[i] + 0.000006) < min)
			min = log10(_systems[0]->Mass()[i] + 0.000006);

	for(unsigned int i = 0; i<m.NrQuadrilateralStrips(); i++){
		for(unsigned int j = 0; j<m.NrCellsInStrip(i); j++) {
			Quadrilateral q = m.Quad(i,j);
			unsigned int idx = _systems[0]->Map(i,j);
			double mass = (log10(_systems[0]->Mass()[idx] + 0.000006) - min) / (max-min);
			vector<Point> ps = q.Points();

			glColor3f(mass, 0, 0);
			glVertex2f(2*(ps[0][0]-(mesh_min_v + ((mesh_max_v - mesh_min_v)/2.0)))/(mesh_max_v - mesh_min_v), 2*(ps[0][1]-(mesh_min_h + ((mesh_max_h - mesh_min_h)/2)))/(mesh_max_h - mesh_min_h));
			glVertex2f(2*(ps[1][0]-(mesh_min_v + ((mesh_max_v - mesh_min_v)/2.0)))/(mesh_max_v - mesh_min_v), 2*(ps[1][1]-(mesh_min_h + ((mesh_max_h - mesh_min_h)/2)))/(mesh_max_h - mesh_min_h));
			glVertex2f(2*(ps[2][0]-(mesh_min_v + ((mesh_max_v - mesh_min_v)/2.0)))/(mesh_max_v - mesh_min_v), 2*(ps[2][1]-(mesh_min_h + ((mesh_max_h - mesh_min_h)/2)))/(mesh_max_h - mesh_min_h));
			glVertex2f(2*(ps[3][0]-(mesh_min_v + ((mesh_max_v - mesh_min_v)/2.0)))/(mesh_max_v - mesh_min_v), 2*(ps[3][1]-(mesh_min_h + ((mesh_max_h - mesh_min_h)/2)))/(mesh_max_h - mesh_min_h));
		}
	}


	UnlockMutex();

	glEnd();

	// Print real time and sim time

	double sim_time = num_frames * m.TimeStep();

	glColor3f( 1.0, 1.0, 1.0 );
  glRasterPos2f(0.0, 0.9);
  int len, i;
	std::string t = std::string("Real Time (s) : ") + std::to_string( (int)floor((float)time_elapsed.count()/1000) )
	 + std::string("      Sim Time (s) : ") + std::to_string( sim_time / _systems.size() );
	const char* c_string = t.c_str();
  len = (int)strlen( c_string );
  for (i = 0; i < len; i++) {
    glutBitmapCharacter(GLUT_BITMAP_HELVETICA_10, c_string[i]);
  }

	double nice_min_h = (double)floor(mesh_min_h * 1) / 1.0;
	double nice_max_h = (double)ceil(mesh_max_h * 1) / 1.0;

	double nice_min_v = (double)floor(mesh_min_v * 0.01) / 0.01;
	double nice_max_v = (double)ceil(mesh_max_v * 0.01) / 0.01;

	double pos = 0;
	while(pos < nice_max_h){
		glColor3f( 1.0, 1.0, 1.0 );
	  glRasterPos2f(-1.0, 2*((pos - (mesh_min_h + ((mesh_max_h - mesh_min_h)/2.0)))/(mesh_max_h - mesh_min_h)));
		std::stringstream stream;
		stream << std::fixed << std:: setprecision(1) << pos;
		t = stream.str();
		c_string = t.c_str();
	  len = (int)strlen( c_string );
	  for (i = 0; i < len; i++) {
	    glutBitmapCharacter(GLUT_BITMAP_HELVETICA_10, c_string[i]);
	  }
		pos +=  (nice_max_h - nice_min_h) / 10;
	}
	pos = 0;
	while(pos > nice_min_h){
		glColor3f( 1.0, 1.0, 1.0 );
	  glRasterPos2f(-1.0, 2*((pos - (mesh_min_h + ((mesh_max_h - mesh_min_h)/2.0)))/(mesh_max_h - mesh_min_h)));
		std::stringstream stream;
		stream << std::fixed << std:: setprecision(1) << pos;
		t = stream.str();
		c_string = t.c_str();
	  len = (int)strlen( c_string );
	  for (i = 0; i < len; i++) {
	    glutBitmapCharacter(GLUT_BITMAP_HELVETICA_10, c_string[i]);
	  }
		pos -= (nice_max_h - nice_min_h) / 10;
	}

	pos = 0;
	while(pos < nice_max_v){
		glRasterPos2f(2*((pos - (mesh_min_v + ((mesh_max_v - mesh_min_v)/2.0)))/(mesh_max_v - mesh_min_v)), -1.0);
		std::stringstream stream2;
		stream2 << std::fixed << std:: setprecision(1) << pos;
		t = stream2.str();
		c_string = t.c_str();
		len = (int)strlen( c_string );
		for (i = 0; i < len; i++) {
			glutBitmapCharacter(GLUT_BITMAP_HELVETICA_10, c_string[i]);
		}
		pos += (nice_max_v - nice_min_v) / 10;
	}
	pos = 0;
	while(pos > nice_min_v){
		glRasterPos2f(2*((pos - (mesh_min_v + ((mesh_max_v - mesh_min_v)/2.0)))/(mesh_max_v - mesh_min_v)), -1.0);
		std::stringstream stream2;
		stream2 << std::fixed << std:: setprecision(1) << pos;
		t = stream2.str();
		c_string = t.c_str();
		len = (int)strlen( c_string );
		for (i = 0; i < len; i++) {
			glutBitmapCharacter(GLUT_BITMAP_HELVETICA_10, c_string[i]);
		}
		pos -= (nice_max_v - nice_min_v) / 10;
	}

	// **** used for 3D ****
	// glPopMatrix();
	glutSwapBuffers();
	glFlush();
}

void Display::scene(int width, int height)
{
	// **** used for 3D ****
	// if (height == 0)
	// {
	// 	height = 1;
	// }

	// glViewport(0, 0, width, height);
	// glMatrixMode(GL_PROJECTION);
	// glLoadIdentity();
  //
	// gluPerspective(45.0f, (GLfloat)width / (GLfloat)height, 0.1f, 100.0f);
  //
	// glMatrixMode(GL_MODELVIEW);
	// glLoadIdentity();

	glViewport(0, 0, width, height);
	glLoadIdentity();
}

void Display::init() const {
	// **** used for 3D ****
	//gluPerspective(45, 1, 2, 10);
	//glEnable(GL_DEPTH_TEST);
	glClearColor(0.0f, 0.0f, 0.0f, 0.0f);
}

void Display::update() {
}

void Display::updateDisplay() {
	num_frames++;
	int time;
	time = glutGet(GLUT_ELAPSED_TIME);
	delta = time - lastTime;
	lastTime = time;
	//Sleep(50);
	glutPostRedisplay();
	glutMainLoopEvent();
}

void Display::shutdown() const {
	glutExit();
	// Nice new line if we quit early.
	std::cout << "\n";
}

void Display::animate() const{

	char* arv[] = {"Miind"};
	int count = 1;
	glutInit(&count, arv);
	glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGBA);
	glutInitWindowSize(500, 500);
	glutInitWindowPosition(0, 0);
	glutCreateWindow("Miind2D");
	glutDisplayFunc(Display::stat_display);
	glutReshapeFunc(Display::stat_scene);
	glutIdleFunc(Display::stat_update);
	atexit(Display::stat_shutdown);

	glutSetOption(GLUT_ACTION_ON_WINDOW_CLOSE, GLUT_ACTION_CONTINUE_EXECUTION);

	init();
}

void Display::stat_runthreaded() {
	Display::getInstance()->animate();
	while((Display::getInstance()->close_display) && !(*Display::getInstance()->close_display)){
		if(!glutGetWindow()){
			glutExit();
			break;
		}

		Display::getInstance()->updateDisplay();
	}
}

void Display::processDraw(void) {
}
