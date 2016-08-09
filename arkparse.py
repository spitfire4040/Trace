# import files
import sys
import os
import os.path
import urllib
import gzip
from requests.auth import HTTPBasicAuth
import requests
import time


# initialize node list
nodelist = []


def parse(year, month, day):

	edgecount = 0

	# open nodelist file
	f = open("/home/jay/Trace/ark_nodes.txt", "r")

	# read nodes into list
	for item in f:
		nodelist.append(item)
	f.close()

	# re-initialize variables each time (clear)
	trace = []

	all_trace = []
	unique_trace = set()

	all_ip = []
	unique_ip = set()

	edgeList = set()

	src = ''
	dst = ''
	hop = ''
	ip = ''
	addr = ''

	starCounter = 1
	count = 1

	# check for directories and create if necessary
	if not os.path.exists("/home/jay/Desktop/Trace_01/ArkData"):
		os.makedirs("/home/jay/Desktop/Trace_01/ArkData")

	if not os.path.exists("/home/jay/Desktop/Trace_01/ark-temp"):
		os.makedirs("/home/jay/Desktop/Trace_01/ark-temp")

	# open files for write
	out1 = open("/home/jay/Desktop/Trace_01/ArkData/all_trace_" + month + '_' + day + '_' + year + ".txt", "w")
	out2 = open("/home/jay/Desktop/Trace_01/ArkData/unique_trace_" + month + '_' + day + '_' + year + ".txt", "w")
	out3 = open("/home/jay/Desktop/Trace_01/ArkData/all_ip_" + month + '_' + day + '_' + year + ".txt", "w")
	out4 = open("/home/jay/Desktop/Trace_01/ArkData/unique_ip_" + month + '_' + day + '_' + year + ".txt", "w")
	out5 = open("/home/jay/Desktop/Trace_01/ArkData/unique_edge_" + month + '_' + day + '_' + year + ".txt", "w")
	out6 = open("/home/jay/Desktop/Trace_01/ArkData/stats_" + month + '_' + day + '_' + year + ".txt", "w")

	# iterate through each team
	for x in range(1, 4):

		# cycle through each file for team/day
		for item in nodelist:

			# remove carriage return
			item = item.strip('\n')

			# retrieve file			
			filename = "https://topo-data.caida.org/team-probing/list-7.allpref24/team-" + str(x) + "/daily/" + year + "/cycle-" + year + month + day + "/daily.l7.t1.c004642." + year + month + day + "." + item + ".warts.gz"

			# fetch file with requests
			r = requests.get(filename, auth=("jthom@cse.unr.edu", "sherdnig3544"))

			# open file for write
			f = open("/home/jay/Desktop/Trace_01/ark-temp/temp.gz", "wb")
			for chunk in r.iter_content(chunk_size=512 * 1024):
				if chunk:
					f.write(chunk)
			f.close()

			# use scamper to convert to text file
			os.system("zcat /home/jay/Desktop/Trace_01/ark-temp/temp.gz | sc_warts2text > /home/jay/Desktop/Trace_01/ark-temp/warts.txt")

			# open textfile for read
			f = open("/home/jay/Desktop/Trace_01/ark-temp/warts.txt", "r")

			try:
				# iterate through each line
				for line in f:

					# split line into pieces
					line = line.split()

					# build trace string (line not traceroute)
					if line[0] != 'traceroute':
						hop = line[0]
						ip = line[1]

						if ip == '*':
							ip = '0'

						#addr = ip + '-' + hop + ' ' # changed this to make it easier for Abdullah to parse in C
						addr = ip + ',' + hop + '\t'						
						trace.append(addr)
						all_ip.append(ip)
						unique_ip.add(ip)

					# reset and append running list each time line == traceroute
					if line[0] == 'traceroute':

						# get values for src, dst
						src = line[2]
						dst = line[4]

						if src == '*':
							src = '0'

						if dst == '*':
							dst = '0'

						all_ip.append(src)
						all_ip.append(dst)
						unique_ip.add(src)
						unique_ip.add(dst)

						# check for empty list and append if good
						if not trace:
							pass
						else:

							# eliminate trailing '*'s
							while '0' in trace[-1]:
								del(trace[-1])

							# convert list to string
							trace = ''.join(trace)

							# append string to running lists
							all_trace.append(trace)
							unique_trace.add(trace)

						# reset trace
						trace = []

						# append src, dst to new trace
						#trace.append(src + ':' + dst + ' ') # changed this to make it easier for Abdullah to parse in C
						trace.append(src + ':' + dst + '\t')						

			except:
				pass

			# once more at end to catch last trace
			try:
				# eliminate trailing '*'s
				while '0' in trace[-1]:
					del(trace[-1])

				# convert list to string
				trace = ''.join(trace)

				# append string to running lists
				all_trace.append(trace)
				unique_trace.add(trace)
			except:
				pass

			f.close()

			#except:
				#print ("url does not exist")



	# find edges...
	# iterate through unique traces
	for item in unique_trace:

		# set list so it will reset
		trace = []

		# split trace and push to list
		#for item in item.split(): # changed this to make it easier for Abdullah to parse in C
		for item in item.split('\t'):		
			if (':' in item):
				pass
			else:
				#item = item.split('-') # changed this to make it easier for Abdullah to parse in C
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
			#edgeList.add(str(first) + ' ' + str(second)) # changed this to make it easier for Abdullah to parse in C
			edgeList.add(str(first) + '\t' + str(second))			
			i += 1


	# write all_trace to file
	for item in all_trace:
		out1.write(item)
		out1.write('\n')

	# write unique_trace to file
	for item in unique_trace:
		out2.write(item)
		out2.write('\n')

	# write all_ip to file
	for item in all_ip:
		out3.write(item)
		out3.write('\n')

	# write unique_ip to file
	for item in unique_ip:
		out4.write(item)
		out4.write('\n')

	# write edgelist to file
	for item in edgeList:
		out5.write(item)
		out5.write('\n')

		item = item.split('\t')			

		if (('.' in item[0]) and ('.' in item[1])):
			edgecount += 1

	# write stats
	out6.write("Total IP: " + str(len(all_ip)) + '\n')
	out6.write("Unique IP: " + str(len(unique_ip)) + '\n')
	out6.write("Total Trace: " + str(len(all_trace)) + '\n')
	out6.write("Unique Trace: " + str(len(unique_trace)) + '\n')
	out6.write("Unique Edge: " + str(edgecount) + '\n')

	# close files
	out1.close()
	out2.close()
	out3.close()
	out4.close()
	out5.close()
	out6.close()


def main(argv):

	# get day from command line args
	year = sys.argv[1]
	month = sys.argv[2]
	day = sys.argv[3]
	
	start = time.time()

	# run parse
	parse(year, month, day)

	# trace count
	os.system("./ark_tracecount " + year + ' ' + month + ' ' + day)

	# ip count
	os.system("./ark_ipcount " + year + ' ' + month + ' ' + day)

	end = time.time()

	with open("log.txt", "a") as f:
		f.write("Ark:" + '\t' + "Start-Time-" + month + '_' + day + '_' + year + '\t' + "Runtime (minutes)-" + str((end - start)/60) + '\n')



if __name__ == '__main__':
  main(sys.argv)
