#ifndef NETWORK
#define NETWORK
#include <vector>

class Network{
public:
	Network();
	std::vector<float> dot (const std::vector<float>& m1, const std::vector<float>& m2, const int m1_rows, const int m1_columns, const int m2_columns);
	std::vector<float> sigmoid (const std::vector<float>& m1);
	std::vector<float> sigmoid_d (const std::vector<float>& m1);
	std::vector<float> transpose (float *m, const int C, const int R);
	void print(const std::vector<float>& m, int n_rows, int n_columns);
};

std::vector<float> operator-(const std::vector<float>& m1, const std::vector<float>& m2);
std::vector<float> operator*(const std::vector<float>& m1, const std::vector<float>& m2);
std::vector<float> operator+(const std::vector<float>& m1, const std::vector<float>& m2);

#endif
