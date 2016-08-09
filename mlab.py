# import files
import sys
import os
#import urllib
import urllib.request # made a change here to get this to run on my desktop...for server, comment this out and uncomment the next line
import tarfile
import re
import shutil
import time


def parse(year, month, day):

	# initialize lists and sets
	nodelist = []
	ip_all = []
	trace_all = []
	ip_unique = set()
	trace_unique = set()
	edgeList = set()

	edgecount = 0

	# open files (works in layers)
	f = open("/home/jay/Desktop/Trace_01/mlab-nodes.txt", "r")
	for line in f:
		line = line.strip('\n')
		nodelist.append(line)
	f.close()

	for item in nodelist:

		try:
			url = "https://storage.googleapis.com/m-lab/paris-traceroute/" + year + "/" + month + "/" + day + "/" + year + month + day + "T000000Z-mlab1-" + item + "-paris-traceroute-0000.tgz"

			#print (url)

			#urllib.urlretrieve(url, "/home/jay/Desktop/Trace_01/mlab-temp/temp.tgz")  #I changed this to run on desktop. For server, uncomment the next line and comment out 63-68
			req = urllib.request.Request(url)
			with urllib.request.urlopen(req) as response:
				the_page = response.read()
			outfile = open("/home/jay/Desktop/Trace_01/mlab-temp/temp.tgz", "wb")
			outfile.write(the_page)
			outfile.close()


			tfile = tarfile.open("/home/jay/Desktop/Trace_01/mlab-temp/temp.tgz", "r:gz")
			tfile.extractall(path="/home/jay/Desktop/Trace_01/mlab-temp/")

			for l1_filename in os.listdir("/home/jay/Desktop/Trace_01/mlab-temp/" + year):
				for l2_filename in os.listdir("/home/jay/Desktop/Trace_01/mlab-temp/" + year + "/" + l1_filename):
					for l3_filename in os.listdir("/home/jay/Desktop/Trace_01/mlab-temp/" + year + "/" + l1_filename +'/' + l2_filename):
						for l4_filename in os.listdir("/home/jay/Desktop/Trace_01/mlab-temp/" + year + "/" + l1_filename +'/' + l2_filename + '/' + l3_filename):
							with open("/home/jay/Desktop/Trace_01/mlab-temp/" + year + "/" + l1_filename + "/" + l2_filename + "/" + l3_filename + "/" + l4_filename, "r") as f:

								# set variables, flags
								flag = 0
								hop = 1
								trace = []

								# iterate through inner file
								for line in f:

									# divide line into pieces
									line = line.split()

									# iterate through line to find line numbers
									for x in range(0, 31):

										try:
											# parse out src/dst on first pass
											if line[0] == 'traceroute' and flag == 0:
												flag = 1

												# src
												src = line[1]
												src = src.strip('[()')									
												src = src.split(':')
												src = src[0]

												# dst
												dst = line[3]
												dst = dst.strip('()],')
												dst = dst.split(':')
												dst = dst[0]

												# save src/dst
												ip_all.append(src + '\n')
												ip_all.append(dst + '\n')
												ip_unique.add(src + '\n')
												ip_unique.add(dst + '\n')

												# append to head of trace
												trace.append(src + ':' + dst + '\t')

											# catch each hop and strip extra characters
											if line[0] == str(x):
												if line[4] != None:
													address = line[4]
													address = address.strip('()')
													if ')' in address:
														head, sep, tail = address.separate(')')
														address = head

													# save ip's to appropriate list
													ip_all.append(address + '\n')
													ip_unique.add(address + '\n')

													# build string												
													#trace.append(address + '-' + str(hop))
													trace.append(address + ',' + str(hop) + '\t') # changed this to make parsing easier for Abdullah

													# increment hop count
													hop += 1
										except:
											pass	

								# convert trace to string
								trace = ' '.join(trace)
								trace_all.append(trace + '\n')

								# append string to running list
							
								trace_unique.add(trace + '\n')
		except:
			pass

		# delete downloaded files each time
		if os.path.exists("/home/jay/Desktop/Trace_01/mlab-temp/" + year):
			shutil.rmtree("/home/jay/Desktop/Trace_01/mlab-temp/" + year)

		if os.path.exists("/home/jay/Desktop/Trace_01/mlab-temp/temp.tgz"):
			os.remove("/home/jay/Desktop/Trace_01/mlab-temp/temp.tgz")


	# write data to files
	outfile = open("/home/jay/Desktop/Trace_01/MlabData/all_ip_" + month + "_" + day + "_" + year + ".txt", "w")
	for item in ip_all:
		outfile.write(item)
	outfile.close()

	outfile = open("/home/jay/Desktop/Trace_01/MlabData/all_trace_" + month + "_" + day + "_" + year + ".txt", "w")
	for item in trace_all:
		outfile.write(item)
	outfile.close()

	outfile = open("/home/jay/Desktop/Trace_01/MlabData/unique_ip_" + month + "_" + day + "_" + year + ".txt", "w")
	for item in ip_unique:
		outfile.write(item)
	outfile.close()

	outfile = open("/home/jay/Desktop/Trace_01/MlabData/unique_trace_" + month + "_" + day + "_" + year + ".txt", "w")
	for item in trace_unique:
		outfile.write(item)
	outfile.close()

	# get edges from unique trace list
	f = open("/home/jay/Desktop/Trace_01/MlabData/unique_trace_" + month + "_" + day + "_" + year + ".txt", "r")
	for item in f:

		# set list so it will reset
		trace = []

		# split trace and push to list
		for item in item.split():
			if ':' in item:
				pass
			else:
				#item = item.split('-')
				item = item.split(',') # changed this to make parsing easier for Abdullah
				trace.append(item[0])

		# find length of list
		length = len(trace)

		# set iterator variable so it will reset
		i = 0

		# iterate through trace list for pairs
		while i < length - 1:
			first = trace[i]
			second = trace[i+1]

			# add to edgeList set (unique values only)
			#edgeList.add(str(first) + ' ' + str(second)) # changed this to make parsing easier for Abdullah
			edgeList.add(str(first) + '\t' + str(second))
			i += 1


	# write edgeList to file
	out = open("/home/jay/Desktop/Trace_01/MlabData/unique_edge_" + month + "_" + day + "_" + year + ".txt", "w")
	for item in edgeList:
		out.write(item + '\n')

		item = item.split('\t')			

		if (('.' in item[0]) and ('.' in item[1])):
			edgecount += 1

	# close file
	f.close()
	out.close()

	# write stats
	outfile = open("/home/jay/Desktop/Trace_01/MlabData/stats_" + month + "_" + day + "_" + year + ".txt", "w")
	outfile.write("Total IP: " + str(len(ip_all)) + '\n')
	outfile.write("Unique IP: " + str(len(ip_unique)) + '\n')
	outfile.write("Total Trace: " + str(len(trace_all)) + '\n')
	outfile.write("Unique Trace: " + str(len(trace_unique)) + '\n')
	outfile.write("Unique Edge: " + str(edgecount) + '\n')
	outfile.close()

	# clear lists
	del ip_all
	del trace_all
	del ip_unique
	del trace_unique
	del edgeList



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
	os.system("./mlab_tracecount " + year + ' ' + month + ' ' + day)

	# ip count
	os.system("./mlab_ipcount " + year + ' ' + month + ' ' + day)

	# for log file
	end = time.time()

	with open("log.txt", "a") as f:
		f.write("M-Lab:" + '\t' + "Start-Time-" + month + '_' + day + '_' + year + '\t' + "Runtime (minutes)-" + str((end - start)/60) + '\n')


if __name__ == '__main__':
  main(sys.argv)
