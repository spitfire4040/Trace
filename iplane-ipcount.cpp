
// header files
#include <iostream>
#include <fstream>
#include <string>
#include <map>
#include <set>
#include <sstream>

using namespace std;

// main function
int main()
{
	// initialize variables
	ifstream fin1, fin2;
	string ip1, ip2, ip3, ip4, inFileName1, inFileName2, outFileName, num, temp;
	ofstream fout;
	stringstream ss;
	int i, j, counter1, counter2, tracecount = 0;
	u_long num1, num2;

	// initialize sets and iterators
	set<string> unique_ip;
	set<string>::iterator unique_ip_iterator;
	multiset<string> all_ip;
	multiset<string>::iterator all_ip_iterator;

	// set file name
	// set file name
	inFileName1 = "/home/jay/Trace/iPlaneData/unique_ip.txt"; // unique_ip
	inFileName2 = "/home/jay/Trace/iPlaneData/all_ip.txt"; // all_ip
	outFileName = "/home/jay/Trace/iPlaneData/ipcount.txt"; // ipcount

	// open files
	fin1.open(inFileName1);
	fin2.open(inFileName2);
	fout.open(outFileName);

	// read unique ips into set
	while (fin1.good())
	{
		fin1 >> temp;
		all_ip.insert(temp);
	}

	// read all ips into multiset
	while (fin2.good())
	{
		fin2 >> temp;
		unique_ip.insert(temp);
	}

	// iterate through each value in the unique map and see how many are in the multimap
	for (unique_ip_iterator = unique_ip.begin(); unique_ip_iterator != unique_ip.end(); unique_ip_iterator++)
	{
		temp = *unique_ip_iterator;
		num1 = all_ip.count(temp);
		fout << num1 << ' ' << temp << endl;
	}

	// close files
	fin1.close();
	fin2.close();
	fout.close();

	// clear sets
	unique_ip.clear();
	all_ip.clear();


	// end program
	return 0;
}
