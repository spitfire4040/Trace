// header files
#include <iostream>
#include <fstream>
#include <string>
#include <map>
#include <set>
#include <sstream>

using namespace std;

// main function
int main(int argc, char *argv[])
{
	// initialize variables
	ifstream fin1, fin2;
	string inFileName1, inFileName2, outFileName, temp, start_time;
	ofstream fout;
	stringstream ss;
	long int num1, length1, length2;

	// initialize command line variables
	start_time = argv[1];

	// initialize sets and iterators
	set<string> unique_trace;
	set<string>::iterator unique_trace_iterator;
	multiset<string> all_trace;
	multiset<string>::iterator all_trace_iterator;

	// set file name
	inFileName1 = "/home/jay/Desktop/Trace_01/RipeData/unique_trace_" + start_time + ".txt"; // unique_trace
	inFileName2 = "/home/jay/Desktop/Trace_01/RipeData/all_trace_" + start_time + ".txt"; // all_trace
	outFileName = "/home/jay/Desktop/Trace_01/RipeData/tracecount_" + start_time + ".txt"; // trace_count

	// open files
	fin1.open(inFileName1);
	fin2.open(inFileName2);
	fout.open(outFileName);

	// read unique traces into set
	while (fin1.good())
	{
		getline(fin1,temp);
		unique_trace.insert(temp);
	}

	// read all traces into multiset
	while (fin2.good())
	{
		getline(fin2,temp);
		all_trace.insert(temp);
	}

	while (fin2.good())
	{
		getline(fin2, temp);
		cout << "blah blah" << endl;
		cout << temp << endl;
	}

	// iterate through each value in the unique map and see how many are in the multimap
	for (unique_trace_iterator = unique_trace.begin(); unique_trace_iterator != unique_trace.end(); unique_trace_iterator++)
	{
		temp = *unique_trace_iterator;
		num1 = all_trace.count(temp);
		fout << num1 << '\t' << temp << endl;
	}

	// close files
	fin1.close();
	fin2.close();
	fout.close();

	// clear sets
	unique_trace.clear();
	all_trace.clear();

	// end program
	return 0;
}
