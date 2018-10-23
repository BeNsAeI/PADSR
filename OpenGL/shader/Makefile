main:		main.cpp
#		g++ -o out  main.cpp glslprogram.cpp -DGLEW_STATIC -lGL  -lGLU  /usr/lib/libglut.so  -lm
#		./out
		make glew
install:
		sudo apt-get install build-essential libgl1-mesa-dev
		sudo apt-get install libglew-dev libsdl2-dev libsdl2-image-dev libglm-dev libfreetype6-dev
		sudo apt install mesa-utils
		glxinfo | grep OpenGL
		pkg-config --libs --static glew
glew:
		g++ -o out  main.cpp glslprogram.cpp -DGLEW_STATIC -lGL  -lGLU -lglut  -lm -lGLEW -lGLU -lm -lGL -lm -lpthread -ldl -ldrm -lXdamage -lXfixes -lX11-xcb -lxcb-glx -lxcb-dri2 -lXxf86vm -lXext -lX11 -lpthread -lxcb -lXau -lXdmcp
		./out
main2:		main-myOwn-View-Point.cpp
		g++ -o out  main-myOwn-View-Point.cpp  -lGL  -lGLU  /usr/lib/libglut.so  -lm
		./out
sample:		sample.cpp
		g++ -o sample  sample.cpp  -lGL  -lGLU  /usr/lib/libglut.so  -lm
