all:
	clear
	g++ simpleC-NN.cpp network.cpp -o out
	./out
debug:
	clear
	g++ simpleC-NN.cpp network.cpp -g -Wall -DDEBUG -o out
	gdb out
	clear
