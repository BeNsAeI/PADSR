all:
	clear
	g++ simpleC-NN.cpp network.cpp -std=c++11 -o out
	./out
debug:
	clear
	g++ simpleC-NN.cpp network.cpp -g -Wall -DDEBUG -std=c++11 -o out
	gdb out
	clear
