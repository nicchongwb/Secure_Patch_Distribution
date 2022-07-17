#include <iostream>
#include <filesystem>
#include <fstream>
using namespace std;

void createFile() {
	ofstream MyFile("test.txt");
	MyFile << "This is a test files\n";
	MyFile.close();
}

int main() {
	createFile();
	return 0;
}
