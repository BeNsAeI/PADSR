#include <iostream>
#include <cstring>
#include <string.h>
#include <vector>
#include <cmath>
#include <math.h>
#include "network.h"
#include "data.h"
#include "const.h"
#include "color.h"

using std::cin;
using std::cout;
using std::endl;
using std::string;
using std::vector;

int main(int argc, char ** argv)
{
	printf(ANSI_COLOR_CYAN "Listing Parameters: \n" ANSI_COLOR_RESET);
	printf("Data sizes are: X: (%dx%d), Y: (%dx1), W: (%dx1).\n",(int)Y.size(), (int)X.size()/(int)Y.size(), (int)Y.size(), (int)W.size());
	int xRows = (int)Y.size();
	int xCols = (int)X.size()/(int)Y.size();
	int yRows = (int)Y.size();
	int yCols = 1;
	int wRows = (int)W.size();
	int wCols = 1;
	printf(ANSI_COLOR_BLUE "Number of cycles: " ANSI_COLOR_YELLOW "%d.\n", CYCLE);
	printf(ANSI_COLOR_BLUE "Bar modulus value: " ANSI_COLOR_YELLOW "%d.\n", BAR);
	printf(ANSI_COLOR_BLUE "Number of decimal places shown in prints: " ANSI_COLOR_YELLOW "%d\n", ND);
	#ifdef DEBUG
		printf(ANSI_COLOR_RED "Mode: Debug.\n" ANSI_COLOR_RESET);
	#endif
	printf(ANSI_COLOR_YELLOW "_ _ _ _ _ _ _ _\n\n" ANSI_COLOR_RESET);
	printf(ANSI_COLOR_CYAN "Setting up the Network...\n" ANSI_COLOR_RESET);
	Network * myNetwork = new Network();
	printf(ANSI_COLOR_CYAN "Listing Data: \n" ANSI_COLOR_RESET);
	printf(ANSI_COLOR_MAGENTA "X: \n" ANSI_COLOR_RESET);
	myNetwork->print_W(X,Y.size(),X.size()/Y.size());
	printf(ANSI_COLOR_MAGENTA "True Label y: \n" ANSI_COLOR_RESET);
	myNetwork->print_W(Y,Y.size(),1);
	printf(ANSI_COLOR_MAGENTA "initial Weights: \n" ANSI_COLOR_RESET);
	myNetwork->print_W(W,W.size(),1);
	printf(ANSI_COLOR_YELLOW "_ _ _ _ _ _ _ _\n\n" ANSI_COLOR_RESET);
	printf(ANSI_COLOR_CYAN "Training...\n" ANSI_COLOR_RESET);

	for (unsigned i = 0; i != CYCLE; ++i) {
		vector<float> pred = myNetwork->sigmoid(myNetwork->dot(X, W, xRows, xCols, yCols ) );
		vector<float> pred_error = Y - pred;
		vector<float> pred_delta = pred_error * myNetwork->sigmoid_d(pred);
		#ifdef DEBUF
			myNetwork->print_W(X, xRows, xCols);
			std::cout << std::endl;
			myNetwork->print_W(myNetwork->transpose( &X[0], xCols, xRows),xCols,xRows);
			std::cout << std::endl;
			myNetwork->print_W(X, xRows, xCols);
		#endif
		vector<float> W_delta = myNetwork->dot(myNetwork->transpose( &X[0], xCols, xRows), pred_delta, xCols, xRows, yCols);
		W = W + W_delta;
		if (i % CYCLE/BAR == 0)
			printf(ANSI_COLOR_MAGENTA "#" ANSI_COLOR_RESET);
		if (i == CYCLE - 1)
		{
			printf("\n");
			printf(ANSI_COLOR_CYAN "Printing:" ANSI_COLOR_YELLOW " >> True lable Y" ANSI_COLOR_BLUE " -> " ANSI_COLOR_YELLOW "Prediction" ANSI_COLOR_CYAN ": \n" ANSI_COLOR_RESET);
			myNetwork->print ( Y, pred, Y.size(), 1 );
			printf(ANSI_COLOR_CYAN "Printing:" ANSI_COLOR_YELLOW " >> " ANSI_COLOR_BLUE "Wights" ANSI_COLOR_CYAN ": \n" ANSI_COLOR_RESET);
			myNetwork->print_W( W, W.size(), 1 );
		}
	};

	printf(ANSI_COLOR_CYAN "Training Done.\n" ANSI_COLOR_RESET);
	printf(ANSI_COLOR_CYAN "Test 1: " ANSI_COLOR_RESET);
	float predicted1 = myNetwork->sigmoid(myNetwork->dot(test0, W, 1, 4, wCols ) )[0];
	if (roundf (predicted1 * powf(10,float(ND)-1)) / powf(10,float(ND)-1) == 0 )
		printf(ANSI_COLOR_GREEN "Passed! (%.*f)\n" ANSI_COLOR_RESET, ND, predicted1);
	else
		printf(ANSI_COLOR_RED "Failed! (%.*f)\n" ANSI_COLOR_RESET, ND, predicted1);
	printf(ANSI_COLOR_CYAN "Test 2: " ANSI_COLOR_RESET);
	float predicted2 = myNetwork->sigmoid(myNetwork->dot(test1, W, 1, 4, wCols ) )[0];
	if (roundf (predicted2 * powf(10,float(ND)-1)) / powf(10,float(ND)-1) == 1)
		printf(ANSI_COLOR_GREEN "Passed! (%.*f)\n" ANSI_COLOR_RESET, ND, predicted2);
	else
		printf(ANSI_COLOR_RED "Failed! (%.*f)\n" ANSI_COLOR_RESET, ND, predicted2);
	printf(ANSI_COLOR_YELLOW "_ _ _ _ _ _ _ _\n\n" ANSI_COLOR_RESET);
	printf(ANSI_COLOR_CYAN "Cleaning Up...\n" ANSI_COLOR_RESET);
	delete(myNetwork);
	printf(ANSI_COLOR_GREEN "Done.\n" ANSI_COLOR_RESET);
	return 0;
}
