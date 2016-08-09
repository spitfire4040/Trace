# import headers
import sys
import os
import urllib
#import urllib.request # made a change here to get this to run on my desktop...for server, comment this out and uncomment the next line
import gzip
import time


def parse(year, month, day):

	# initialize variables
	hop = 1
	flag = False
	src = ''
	dst = ''
	count = 1
	edgecount = 0

	# initialize variables
	trace = []
	all_trace = []
	all_ip = []
	unique_trace = set()
	unique_ip = set()
	edgelist = set()

	# open nodelist
	f = open("testnodelist.txt", "r")

	# iterate through each line in nodelist
	for line in f:

		try:

			# retrieve file **I changed this to run on desktop. For server, uncomment the next line and comment out 63-68
			urllib.urlretrieve("http://iplane.cs.washington.edu/data/iplane_logs/" + year + "/" + month + "/" + day + "/" + line, "/home/jay/Desktop/Trace_01/iplane-temp/temp.gz")
			#req = urllib.request.Request("http://iplane.cs.washington.edu/data/iplane_logs/" + year + "/" + month + "/" + day + "/" + line)
			#with urllib.request.urlopen(req) as response:
				#the_page = response.read()
			#outfile = open("/home/jay/Desktop/Trace_01/iplane-temp/temp.gz", "wb")
			#outfile.write(the_page)
			#outfile.close()

			# open in and out files for .gz processing
			with gzip.open("/home/jay/Desktop/Trace_01/iplane-temp/temp.gz", "rb") as in_file:
				s = in_file.read()

			with open("/home/jay/Desktop/Trace_01/iplane-temp/temp.out", "w") as out_file:
				out_file.write(s)

			# call c code to stream file to text > temp.txt
			os.system("./iplane /home/jay/Desktop/Trace_01/iplane-temp/temp.out > /home/jay/Desktop/Trace_01/iplane-temp/temp.txt")

			# build list of traces for each day
			infile = open("/home/jay/Desktop/Trace_01/iplane-temp/temp.txt", "r")

			# iterate through lines of f
			for line in infile:
				line = line.split()

				# if 'destination', write and reset
				if (line[0] == "destination:"):
					dst = line[1]

					# add to ip lists
					all_ip.append(dst)
					unique_ip.add(dst)

					# get rid of empty line
					if trace != None:

						# add to trace lists
						all_trace.append(''.join(trace))
						unique_trace.add(''.join(trace))

					# reset lists and flag
					trace = []
					hop = 1
					flag = False
				else:
					if line[1] == "0.0.0.0":
						addr = '0'

					else:
						addr = line[1]					

					# print src:dst on first pass
					if (flag == False):
						trace.append(addr + ':' + dst + '\t')
						trace.append(addr + ',' + str(hop) + '\t')
						flag = True
						hop += 1

					else:
						trace.append(addr + ',' + str(hop) + '\t')

						# add to ip lists
						all_ip.append(addr)
						unique_ip.add(addr)

						# increment hop		
						hop += 1
		except:
			pass



	# close nodelist				
	f.close()


	# find edges...
	# iterate through unique traces
	for item in unique_trace:

		# set list so it will reset
		trace = []

		# split trace and push to list
		for item in item.split():
			if (':' in item):
				pass
			else:
				item = item.split(',')
				trace.append(item[0])

		# find length of list
		length = len(trace)

		# set iterator variable so it will reset
		i = 0

		# iterate through trace list for pairs
		while i < length - 1:
			first = trace[i]
			second = trace[i+1]

			# set incrementing value for 0's
			if first == '0' and second == '0':
				# don't count 0 - 0
				pass

			else:

				if first == '0':
					first = count
					count += 1

				if second == '0':
					second = count
					count += 1

			# add to edgeList set (unique values only)
			edgelist.add(str(first) + '\t' + str(second))
			i += 1

	# open all_trace file
	with open("/home/jay/Desktop/Trace_01/iPlaneData/all_trace_" + month + '_' + day + '_' + year + ".txt", "w") as f:

		# write list to file
		for item in all_trace:
			if not item:
				pass
			else:
				f.write(item + '\n')


	# open all_ip file
	with open("/home/jay/Desktop/Trace_01/iPlaneData/all_ip_" + month + '_' + day + '_' + year + ".txt", "w") as f:

		# write list to file
		for item in all_ip:
			if not item:
				pass
			else:
				f.write(item + '\n')


	# open unique_trace file
	with open("/home/jay/Desktop/Trace_01/iPlaneData/unique_trace_" + month + '_' + day + '_' + year + ".txt", "w") as f:

		# write list to file
		for item in unique_trace:
			if not item:
				pass
			else:
				f.write(item + '\n')


	# open unique_ip file
	with open("/home/jay/Desktop/Trace_01/iPlaneData/unique_ip_" + month + '_' + day + '_' + year + ".txt", "w") as f:

		# write list to file
		for item in unique_ip:
			if not item:
				pass
			else:
				f.write(item + '\n')


	# open unique_edge file
	with open("/home/jay/Desktop/Trace_01/iPlaneData/unique_edge_" + month + '_' + day + '_' + year + ".txt", "w") as f:

		# write list to file
		for item in edgelist:
			if not item:
				pass
			else:
				f.write(item + '\n')

		item = item.split('\t')			

		if (('.' in item[0]) and ('.' in item[1])):
			edgecount += 1

	# open stats file
	with open("/home/jay/Desktop/Trace_01/iPlaneData/stats_" + month + '_' + day + '_' + year + ".txt", "w") as f:
		# write stats
		f.write("Total IP: " + str(len(all_ip)) + '\n')
		f.write("Unique IP: " + str(len(unique_ip)) + '\n')
		f.write("Total Trace: " + str(len(all_trace)) + '\n')
		f.write("Unique Trace: " + str(edgecount) + '\n')
		f.write("Unique Edge: " + str(len(edgecount)) + '\n')



def main(argv):
	# get day from command line args
	year = sys.argv[1]
	month = sys.argv[2]
	day = sys.argv[3]

	# for log file
	start = time.time()

	# run parse
	parse(year, month, day)

	# trace count
	os.system("./iplane_tracecount " + year + ' ' + month + ' ' + day)

	# ip count
	os.system("./iplane_ipcount " + year + ' ' + month + ' ' + day)

	# for log file
	end = time.time()

	with open("log.txt", "a") as f:
		f.write("iPlane:" + '\t' + "Start-Time-" + month + '_' + day + '_' + year + '\t' + "Runtime (minutes)-" + str((end - start)/60) + '\n')


if __name__ == '__main__':
  main(sys.argv)
