#include <iostream>
#include <filesystem>
#include <fstream>
using namespace std;

void createFile() {
	ofstream MyFile("test.txt");
	MyFile << "This is a test file created via outfile stream\n";
	MyFile.close();
}

int main() {
	createFile();
	return 0;
}
