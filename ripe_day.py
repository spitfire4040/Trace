# Import Header Files
import sys
import os
import os.path
import urllib
import string
from pymongo import MongoClient
import collections
from ripe.atlas.sagan import TracerouteResult
import time


# convert ip string to integer value
def ip2int(addr):                                                               
	return struct.unpack("!I", socket.inet_aton(addr))[0]                       

# convert integer value to ip string
def int2ip(addr):                                                               
	return socket.inet_ntoa(struct.pack("!I", addr)) 

def convert(data):
    if isinstance(data, basestring):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data

def trace(start_time):

	# set end time
	end_time = str(int(start_time) + 86400)

	# initialize data structures
	uniqueTrace = set()
	uniqueIP = set()
	uniqueEdge = set()
	allTrace = []
	allIP = []
	nodeList = []

	# initialize edge count
	edgecount = 0

	# open node list
	with open("RipeNodeList") as f:
		for line in f:
			for word in line.split():
				nodeList.append(word)

	# iterate through each of 195 nodes
	for node in nodeList:

		# open working files
		with open("/home/jthom/Trace/ripe-temp/traceList.txt", "w") as f:

			try:
				# download page from internet and store in filesystem
				urllib.urlretrieve("https://atlas.ripe.net/api/v2/measurements/" + node + "/results?start=" + str(start_time) + "&stop=" + str(end_time) + "&format=json", "/home/jthom/Trace/ripe-temp/ripe.json")

				try:
					# Import file to db
					os.system("mongoimport --db RipeNode --collection mapping --type json --file /home/jthom/Trace/ripe-temp/ripe.json --jsonArray")
				except:
					print "Error--problem loading data to MongoDB"

				# Create client 
				client = MongoClient()

				# Assign the local variable db to the database named primer
				db = client.RipeNode

				# Access collection object
				db.mapping

				# Create object variable for later use
				coll = db.mapping
				index_i = 0
				index_j = 1

				# iterate through all documents in a collection
				cursor = coll.find()#[index_i:index_j]

				# use mongo to parse data
				try:
					for post in coll.find():
						record = convert(post)

						my_result = TracerouteResult.get(record)

						newLine = []

						flag = 0
						ip = my_result.ip_path
						if(my_result.is_success == 1):

							# set value of source and destination
							source = my_result.source_address
							destination = my_result.destination_address

							# push src and dst to ip lists
							allIP.append(source)
							allIP.append(destination)
							uniqueIP.add(source)
							uniqueIP.add(destination)

							# get all addresses
							for x in ip:
								sublist = x
								for y in sublist:
									while flag == 0:
										if(y == None):
											newLine.append('0')
										else:
											newLine.append(y)
											allIP.append(y)
											uniqueIP.add(y)
										flag = 1
								flag = 0
						else:
							pass

						# write parsed data to file
						f.write(source + ':' + destination + ' ')
						hop = 1
						for address in newLine:
							f.write(address + '-' + str(hop))
							f.write(' ')
							hop += 1

						# end line
						if (len(newLine) != 0):
							f.write('\n')
						
				except:
					pass

			except:
				pass		


		# write per node data to file

		# Unique Traces
		with open("/home/jthom/Trace/ripe-temp/traceList.txt", "r") as f:
		    trace = []
		    for line in f:
		    	#if line not in trace:
		        	#trace.append(line)
		        uniqueTrace.add(line)
		        allTrace.append(line)

		# get edges
		#edgeList = set()
		starCounter = 1
		count = 1

		for item in uniqueTrace:

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
				if first == '0':
					first = count
					count += 1
				if second == '0':
					second = count
					count += 1

				uniqueEdge.add(str(first) + ' ' + str(second))
				i += 1

		# Drop Collection
		result = db.mapping.drop()

	# all traces
	with open("/home/jthom/Trace/RipeData/all_trace.txt", "w") as f:
		for item in allTrace:
			f.write(item)

	# all ips
	with open("/home/jthom/Trace/RipeData/all_ip.txt", "w") as f:
		for item in allIP:
			f.write(item + '\n')

	# unique traces
	with open("/home/jthom/Trace/RipeData/unique_trace.txt", "w") as f:
		for item in uniqueTrace:
			f.write(item)

	# unique ip addresses
	with open("/home/jthom/Trace/RipeData/unique_ip.txt", "w") as f:
		for item in uniqueIP:
			f.write(item + '\n')

	# unique edges (w/o '0's counted)
	with open("/home/jthom/Trace/RipeData/unique_edge.txt", "w") as f:
		for item in uniqueEdge:
			f.write(item + '\n')
			item = item.split(' ')

			if (('.' in item[0]) and ('.' in item[1])):
				edgecount += 1

	# write totals to file
	with open("/home/jthom/Trace/RipeData/stats.txt", "w") as f:
		f.write("Total IPs: " + str(len(allIP)) + '\n')
		f.write("Total Traces: " + str(len(allTrace)) + '\n')
		f.write("Total Unique IPs: " + str(len(uniqueIP)) + '\n')
		f.write("Total Unique Traces: " + str(len(uniqueTrace)) + '\n')
		f.write("Total Unique Edges: " + str(edgecount) + '\n')


# main function
def main(argv):

	start = time.time()
	# call trace
	start_time = sys.argv[1]
	trace(start_time)

        # trace count
        os.system("./ripe_tracecount")

        # ip count
        os.system("./ripe_ipcount")

	end = time.time()
	
	with open("log.txt", "a") as f:
		f.write("Ripe Runtime: " + str(end - start) + '\n')


# initiate program
if __name__ == '__main__':		
	main(sys.argv)
