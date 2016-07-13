# import files
import sys
import os
import urllib
import tarfile
import re
import shutil

# get day from command line args
year = sys.argv[1]
month = sys.argv[2]
day = sys.argv[3]

def parse():
	global year, month, day

	# initialize lists and sets
	nodelist = []
	ip_all = []
	trace_all = []
	ip_unique = set()
	trace_unique = set()
	edgeList = set()

	# open files (works in layers)
	f = open("/home/jthom/Trace/mlab-nodes.txt", "r")
	for line in f:
		line = line.strip('\n')
		nodelist.append(line)
	f.close()

	for item in nodelist:

		try:

			url = "https://storage.googleapis.com/m-lab/paris-traceroute/" + year + "/" + month + "/" + day + "/" + year + month + day + "T000000Z-mlab1-" + item + "-paris-traceroute-0000.tgz"

			print (url)

			urllib.urlretrieve(url, "/home/jthom/Trace/mlab-temp/temp.tgz")
			tfile = tarfile.open("/home/jthom/Trace/mlab-temp/temp.tgz", "r:gz")
			tfile.extractall(path="/home/jthom/Trace/mlab-temp/")

			for l1_filename in os.listdir("/home/jthom/Trace/mlab-temp/" + year):
				for l2_filename in os.listdir("/home/jthom/Trace/mlab-temp/" + year + "/" + l1_filename):
					for l3_filename in os.listdir("/home/jthom/Trace/mlab-temp/" + year + "/" + l1_filename +'/' + l2_filename):
						for l4_filename in os.listdir("/home/jthom/Trace/mlab-temp/" + year + "/" + l1_filename +'/' + l2_filename + '/' + l3_filename):
							with open("/home/jthom/Trace/mlab-temp/" + year + "/" + l1_filename + "/" + l2_filename + "/" + l3_filename + "/" + l4_filename, "r") as f:

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
												trace.append(src + ':' + dst)

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
													trace.append(address + '-' + str(hop))

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
		if os.path.exists("/home/jthom/Trace/mlab-temp/" + year):
			shutil.rmtree("/home/jthom/Trace/mlab-temp/" + year)

		if os.path.exists("/home/jthom/Trace/mlab-temp/temp.tgz"):
			os.remove("/home/jthom/Trace/mlab-temp/temp.tgz")


	# write data to files
	outfile = open("/home/jthom/Trace/MlabData/all_ip.txt", "w")
	for item in ip_all:
		outfile.write(item)
	outfile.close()

	outfile = open("/home/jthom/Trace/MlabData/all_trace.txt", "w")
	for item in trace_all:
		outfile.write(item)
	outfile.close()

	outfile = open("/home/jthom/Trace/MlabData/unique_ip.txt", "w")
	for item in ip_unique:
		outfile.write(item)
	outfile.close()

	outfile = open("/home/jthom/Trace/MlabData/unique_trace.txt", "w")
	for item in trace_unique:
		outfile.write(item)
	outfile.close()

	# get edges from unique trace list
	f = open("/home/jthom/Trace/MlabData/unique_trace.txt", "r")
	for item in f:

		# set list so it will reset
		trace = []

		# split trace and push to list
		for item in item.split():
			if ':' in item:
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

			# add to edgeList set (unique values only)
			edgeList.add(str(first) + ' ' + str(second))
			i += 1


	# write edgeList to file
	out = open("/home/jthom/Trace/MlabData/unique_edge.txt", "w")
	for item in edgeList:
		out.write(item + '\n')

	# close file
	f.close()
	out.close()

	# write stats
	outfile = open("/home/jthom/Trace/MlabData/stats.txt", "w")
	outfile.write("Total IP: " + str(len(ip_all)) + '\n')
	outfile.write("Unique IP: " + str(len(ip_unique)) + '\n')
	outfile.write("Total Trace: " + str(len(trace_all)) + '\n')
	outfile.write("Unique Trace: " + str(len(trace_unique)) + '\n')
	outfile.write("Unique Edge: " + str(len(edgeList)) + '\n')
	outfile.close()

	# clear lists
	del ip_all
	del trace_all
	del ip_unique
	del trace_unique
	del edgeList



def main(argv):
	# run parse
	parse()

	# trace count
	os.system("./mlab-tracecount")

	# ip count
	os.system("./mlab-ipcount")


if __name__ == '__main__':
  main(sys.argv)