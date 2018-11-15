#include <iostream>
#include <cstring>
#include <string.h>
#include <vector>
#include "network.h"
#include "const.h"

using std::cin;
using std::cout;
using std::endl;
using std::string;
using std::vector;

int main(int argc, char ** argv)
{
	Network * myNetwork = new Network();
	for (unsigned i = 0; i != 50; ++i) {
		vector<float> pred = myNetwork->sigmoid(myNetwork->dot(X, W, 4, 4, 1 ) );
		vector<float> pred_error = y - pred;
		vector<float> pred_delta = pred_error * myNetwork->sigmoid_d(pred);
		vector<float> W_delta = myNetwork->dot(myNetwork->transpose( &X[0], 4, 4 ), pred_delta, 4, 4, 1);
		W = W + W_delta;
		if (i == 49){
			myNetwork->print ( pred, 4, 1 );
		}
	};
	return 0;
}
