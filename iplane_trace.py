# import headers
import sys
import os
import urllib
import gzip
import time


# get day from command line args
year = sys.argv[1]
month = sys.argv[2]
day = sys.argv[3]

#print 'year: ', year
#print 'month: ', month
#print 'day: ', day


def parse():

	# global variables
	global year, month, day

	# initialize variables
	hop = 1
	flag = False
	src = ''
	dst = ''

	# initialize variables
	trace = []
	all_trace = []
	all_ip = []
	unique_trace = set()
	unique_ip = set()
	edgelist = set()

	# open nodelist
	f = open("nodelist.txt", "r")

	# iterate through each line in nodelist
	for line in f:

		try:

			# retrieve file
			urllib.urlretrieve("http://iplane.cs.washington.edu/data/iplane_logs/" + year + "/" + month + "/" + day + "/" + line, "/home/jthom/Trace/iplane-temp/temp.gz")

			#print "http://iplane.cs.washington.edu/data/iplane_logs/" + year + "/" + month + "/" + day + "/" + line

			# open in and out files for .gz processing
			with gzip.open("/home/jthom/Trace/iplane-temp/temp.gz", "rb") as in_file:
				s = in_file.read()

			with open("/home/jthom/Trace/iplane-temp/temp.out", "w") as out_file:
				out_file.write(s)

			# call c code to stream file to text > temp.txt
			os.system("./iplane /home/jthom/Trace/iplane-temp/temp.out > /home/jthom/Trace/iplane-temp/temp.txt")

			# build list of traces for each day
			infile = open("/home/jthom/Trace/iplane-temp/temp.txt", "r")

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
						trace.append(addr + ':' + dst + ' ')
						trace.append(addr + '-' + str(hop) + ' ')
						flag = True
						hop += 1

					else:
						trace.append(addr + '-' + str(hop) + ' ')

						# add to ip lists
						all_ip.append(addr)
						unique_ip.add(addr)

						# increment hop		
						hop += 1
		except:
			#print "No Such File"
			#print ' '
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
				item = item.split('-')
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
			if first == '*' and second == '*':
				# don't count * - *
				pass

			else:

				if first == '*':
					first = count
					count += 1

				if second == '*':
					second = count
					count += 1

			# add to edgeList set (unique values only)
			edgelist.add(str(first) + ' ' + str(second))
			i += 1

	# open all_trace file
	with open("/home/jthom/Trace/iPlaneData/all_trace.txt", "w") as f:

		# write list to file
		for item in all_trace:
			if not item:
				pass
			else:
				f.write(item + '\n')


	# open all_ip file
	with open("/home/jthom/Trace/iPlaneData/all_ip.txt", "w") as f:

		# write list to file
		for item in all_ip:
			if not item:
				pass
			else:
				f.write(item + '\n')


	# open unique_trace file
	with open("/home/jthom/Trace/iPlaneData/unique_trace.txt", "w") as f:

		# write list to file
		for item in unique_trace:
			if not item:
				pass
			else:
				f.write(item + '\n')


	# open unique_ip file
	with open("/home/jthom/Trace/iPlaneData/unique_ip.txt", "w") as f:

		# write list to file
		for item in unique_ip:
			if not item:
				pass
			else:
				f.write(item + '\n')


	# open unique_edge file
	with open("/home/jthom/Trace/iPlaneData/unique_edge.txt", "w") as f:

		# write list to file
		for item in edgelist:
			if not item:
				pass
			else:
				f.write(item + '\n')

	# open stats file
	with open("/home/jthom/Trace/iPlaneData/stats.txt", "w") as f:
		# write stats
		f.write("Total IP: " + str(len(all_ip)) + '\n')
		f.write("Unique IP: " + str(len(unique_ip)) + '\n')
		f.write("Total Trace: " + str(len(all_trace)) + '\n')
		f.write("Unique Trace: " + str(len(unique_trace)) + '\n')
		f.write("Unique Edge: " + str(len(edgelist)) + '\n')



def main(argv):

	start = time.time()

	# run parse
	parse()

	# trace count
	os.system("./iplane_tracecount")

	# ip count
	os.system("./iplane_ipcount")

	end = time.time()

	with open("log.txt", "a") as f:
		f.write("iPlane Runtime: " + str(end - start) + '\n')


if __name__ == '__main__':
  main(sys.argv)
