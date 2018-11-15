#include <iostream>
#include <vector>
#include "network.h"
#include <math.h>
#include <cmath>
Network::Network()
{
	#ifdef DEBUG
	std::cout << "Contructor for Network was called" << std::endl;
	#endif
}

std::vector<float> Network::dot(const std::vector<float>& m1, const std::vector<float>& m2, const int m1_rows, const int m1_columns, const int m2_columns)
{
	std::vector<float> output (m1_rows*m2_columns);
	
	for( int row = 0; row != m1_rows; ++row ) {
		for( int col = 0; col != m2_columns; ++col ) {
			output[ row * m2_columns + col ] = 0.f;
			for( int k = 0; k != m1_columns; ++k ) {
				output[ row * m2_columns + col ] += m1[ row * m1_columns + k ] * m2[ k * m2_columns + col ];
			}
		}
	}
	return output;
}
std::vector<float> Network::sigmoid (const std::vector<float>& m1)
{
	const unsigned long VECTOR_SIZE = m1.size();
	std::vector<float> output (VECTOR_SIZE);
	for( unsigned i = 0; i != VECTOR_SIZE; ++i ) {
		output[ i ] = 1 / (1 + exp(-m1[ i ]));
	}
	return output;
}
std::vector<float> Network::sigmoid_d (const std::vector<float>& m1)
{
	const unsigned long VECTOR_SIZE = m1.size();
	std::vector<float> output (VECTOR_SIZE);
	for( unsigned i = 0; i != VECTOR_SIZE; ++i ) {
		output[ i ] = m1[ i ] * (1 - m1[ i ]);
	}
	return output;
}
std::vector<float> Network::transpose (float *m, const int C, const int R)
{
	std::vector<float> mT (C*R);
	for(int n = 0; n!=C*R; n++) {
		int i = n/C;
		int j = n%C;
		mT[n] = m[R*j + i];
	}
	return mT;
}
void Network::print(const std::vector<float>& m, int n_rows, int n_columns)
{
	for( int i = 0; i != n_rows; ++i ) {
		for( int j = 0; j != n_columns; ++j ) {
			std::cout << m[ i * n_columns + j ] << " ";
		}
		std::cout << '\n';
	}
	std::cout << std::endl;
}
std::vector<float> operator-(const std::vector<float>& m1, const std::vector<float>& m2)
{
	const unsigned long VECTOR_SIZE = m1.size();
	std::vector<float> difference (VECTOR_SIZE);
	for (unsigned i = 0; i != VECTOR_SIZE; ++i){
 	   difference[i] = m1[i] - m2[i];
	};
	return difference;
}
std::vector<float> operator*(const std::vector<float>& m1, const std::vector<float>& m2)
{
	const unsigned long VECTOR_SIZE = m1.size();
	std::vector<float> product (VECTOR_SIZE);
	for (unsigned i = 0; i != VECTOR_SIZE; ++i){
		product[i] = m1[i] * m2[i];
	};
	return product;
}
std::vector<float> operator+(const std::vector<float>& m1, const std::vector<float>& m2)
{
	const unsigned long VECTOR_SIZE = m1.size();
	std::vector<float> sum (VECTOR_SIZE);
	for (unsigned i = 0; i != VECTOR_SIZE; ++i){
		sum[i] = m1[i] + m2[i];
	};
	return sum;
}
