# Import Header Files
import sys
import os
import os.path
import urllib
import string
from pymongo import MongoClient
import collections
from ripe.atlas.sagan import TracerouteResult

start_time = 0

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

def trace():
	# global variables
	global start_time

	traceCount3 = 0
	ipCount3 = 0
	srcCount3 = 0
	dstCount3 = 0
	privateIP = 0
	edgeCount = 0
	target = 0

	uniqueTrace = set()
	uniqueIP = set()
	uniqueSrc = set()
	uniqueDst = set()
	uniqueEdge = set()

	nodeList = []
	with open("RipeNodeList") as f:
		for line in f:
			for word in line.split():
				nodeList.append(word)

	for line in open("start_time.txt"):
		if line.strip():
			start_time = int(line)
	end_time = start_time + 86400

	for node in nodeList:
		traceCount1 = 0
		srcCount1 = 0
		dstCount1 = 0
		ipCount1 = 0
		traceCount2 = 0
		srcCount2 = 0
		dstCount2 = 0
		ipCount2 = 0
		flag = 0
		privateIP = 0
		edgeCount1 = 0

		if not os.path.exists("/home/jthom/Trace/RipeData/" + str(start_time) + "/all_nodes"):
			os.makedirs("/home/jthom/Trace/RipeData/" + str(start_time) + "/all_nodes")

		if not os.path.exists("/home/jthom/Trace/RipeData/" + str(start_time) + "/per_node/" + node):
			os.makedirs("/home/jthom/Trace/RipeData/" + str(start_time) + "/per_node/" + node)

		# open working files
		of1 = open("traceList.txt", "w")
		of2 = open("ipList.txt", "w")
		of3 = open("src.txt", "w")
		of4 = open("dst.txt", "w")
		of5 = open("/home/jthom/Trace/RipeData/" + str(start_time) + "/per_node/" + node + "/stats.txt", "w")		
		of6 = open("/home/jthom/Trace/RipeData/" + str(start_time) + "/per_node/" + node + "/trace.txt", "w")
		of7 = open("/home/jthom/Trace/RipeData/" + str(start_time) + "/per_node/" + node + "/ip.txt", "w")
		of8 = open("/home/jthom/Trace/RipeData/" + str(start_time) + "/per_node/" + node + "/src.txt", "w")
		of9 = open("/home/jthom/Trace/RipeData/" + str(start_time) + "/per_node/" + node + "/dst.txt", "w")
		of10 = open("/home/jthom/Trace/RipeData/" + str(start_time) + "/per_node/" + node + "/traceCount.txt", "w")
		of11 = open("/home/jthom/Trace/RipeData/" + str(start_time) + "/per_node/" + node + "/edgeList.txt", "w")
		of15 = open("/home/jthom/Trace/RipeData/" + str(start_time) + "/per_node/" + node + "/ipCount.txt", "w")
		ofx = open("/home/jthom/Trace/RipeData/" + str(start_time) + "/all_nodes/stats.txt", "w")	

		try:
			# download page from internet and store in filesystem
			urllib.urlretrieve("https://atlas.ripe.net/api/v2/measurements/" + node + "/results?start=" + str(start_time) + "&stop=" + str(end_time) + "&format=json", "/home/jthom/Trace/ripe.json")

			try:
				# Import file to db
				os.system("mongoimport --db RipeNode --collection mapping --type json --file ripe.json --jsonArray")
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
					srcList = []
					dstList = []

					flag = 0
					ip = my_result.ip_path
					if(my_result.is_success == 1):
						#newLine.append(my_result.source_address)
						source = my_result.source_address
						destination = my_result.destination_address
						srcList.append(my_result.source_address)
						dstList.append(my_result.destination_address)
						for x in ip:
							sublist = x
							for y in sublist:
								while flag == 0:
									if(y == None):
										newLine.append('0')
									else:
										newLine.append(y)
									flag = 1
							flag = 0
					else:
						pass

					# write parsed data to file
					# trace strings and ip addresses
					of1.write(source + ':' + destination + ' ')
					hop = 1
					for address in newLine:
						of1.write(address + '-' + str(hop))
						of2.write(address)
						of1.write(' ')
						of2.write('\n')
						ipCount1 += 1
						hop += 1
					if (len(newLine) != 0):
						of1.write('\n')
						traceCount1 += 1
					
					# source ip addresses
					for address in srcList:
						of3.write(address)
						of3.write('\n')
						srcCount1 += 1

					# destination ip addresses
					for address in dstList:
						of4.write(address)
						of4.write('\n')
						dstCount1 += 1
					
			except:
				print "Could not process document"

		except:
			of5.write("ERROR -- Could not download node " + node)		

		# Close files
		of1.close()
		of2.close()
		of3.close()
		of4.close()

		# write per node data to file

		# Unique Traces
		with open("traceList.txt", "r") as f:
		    trace = []
		    for line in f:
		    	if line not in trace:
		        	trace.append(line)
		        uniqueTrace.add(line)
		f.close()

		for item in trace:
			of6.write(item)
			traceCount2 += 1
		of6.close()

		# Trace Counts
		# initialize variables
		allTraceList = []
		uniqueTraceList = []
		uniqueIpList = []

		# open traceList file
		with open("traceList.txt", "r") as f:
			for line in f:

				# make list of traces
				allTraceList.append(line)
				if line not in uniqueTraceList:

					# make list of unique traces
					uniqueTraceList.append(line)
		f.close()

		# for each unique trace, count number of occurances in total list
		for item in uniqueTraceList:
			num = allTraceList.count(item)

			# write count and trace to new file
			of10.write(str(num) + " " + item)

		# close file
		of10.close()

		# ip counts
		with open("ipList.txt", "r") as f:

			# create lists for all and unique
		    ips = []
		    uips = set()

		    # fill both lists
		    for item in f:
		        ips.append(item)
		        uips.add(item)

		# compare unique to all and count all
		for item in uips:
			num = ips.count(item)

			# write out to file
			of15.write(str(num) + " " + item)

		# close files
		of15.close()
		f.close()		

		# initialize lists
		edgeList = set()
		starCounter = 1
		count = 1

		for item in uniqueTraceList:

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

				# add to edgeList set (unique values only)
				edgeList.add(str(first) + ' ' + str(second))
				uniqueEdge.add(str(first) + ' ' + str(second))
				i += 1

		# write edgeList to file
		for item in edgeList:
			of11.write(item + '\n')
			edgeCount1 += 1

		# close file
		of11.close()

		# Unique IPs
		with open("ipList.txt", "r") as f:
		    ip = []
		    for line in f:
		    	if line not in ip:
		        	ip.append(line)
		        uniqueIP.add(line)
		f.close()
		#for item in ip:
		for item in uniqueIP:
			of7.write(item)
			if (('10.0' in item) or ('192.168' in item) or ('172.16' in item)):
				privateIP += 1
			ipCount2 += 1
		of7.close()

		# Unique Source IPs
		with open("src.txt", "r") as f:
		    src = []
		    for line in f:
		    	if line not in src:
		        	src.append(line)
		        uniqueSrc.add(line)
		f.close()
		for item in src:
			of8.write(item)
			srcCount2 += 1
		of8.close()

		# Unique Destination IPs
		with open("dst.txt", "r") as f:
		    dst = []
		    for line in f:
		    	if line not in dst:
		        	dst.append(line)
		        uniqueDst.add(line)
		f.close()
		for item in dst:
			of9.write(item)
			dstCount2 += 1
		of9.close()

		# Drop Collection
		result = db.mapping.drop()

		# write individual node totals to file
		of5.write("Node: " + node + '\n')
		of5.write("Total Traces: " + str(traceCount1) + '\n')
		of5.write("Total IPs: " + str(ipCount1) + '\n')
		of5.write("Total Source IPs: " + str(srcCount1) + '\n')
		of5.write("Total Destination IPs: " + str(dstCount1) + '\n')
		of5.write("Unique Traces: " + str(traceCount2) + '\n')
		of5.write("Unique IPs: " + str(ipCount2) + '\n')
		of5.write("Private IPs: " + str(privateIP) + '\n')
		of5.write("Unique Source IPs: " + str(srcCount2) + '\n')
		of5.write("Unique Destination IPs: " + str(dstCount2) + '\n')
		of5.write("Unique Edges: " + str(edgeCount1) + '\n')
		of5.write("*************************************" + '\n')
		of5.close()

	# Write Totals To File

	# unique traces
	of11 = open("/home/jthom/Trace/RipeData/" + str(start_time) + "/all_nodes/traces.txt", "w")
	for item in uniqueTrace:
		of11.write(item)
		traceCount3 += 1
	of11.close()

	# unique ip addresses
	of12 = open("/home/jthom/Trace/RipeData/" + str(start_time) + "/all_nodes/ips.txt", "w")
	for item in uniqueIP:
		of12.write(item)
		ipCount3 += 1
	of12.close()

	# unique source ip addresses
	of13 = open("/home/jthom/Trace/RipeData/" + str(start_time) + "/all_nodes/src.txt", "w")
	for item in uniqueSrc:
		of13.write(item)
		srcCount3 += 1
	of13.close()

	# unique destination ip addresses
	of14 = open("/home/jthom/Trace/RipeData/" + str(start_time) + "/all_nodes/dst.txt", "w")
	for item in uniqueDst:
		of14.write(item)
		dstCount3 += 1
	of14.close()

	# unique edges (w/o '0's counted)
	of15 = open("/home/jthom/Trace/RipeData/" + str(start_time) + "/all_nodes/edges.txt", "w")
	for item in uniqueEdge:
		of15.write(item + '\n')
		item = item.split(' ')

		if (('.' in item[0]) and ('.' in item[1])):
			edgeCount += 1
	of15.close()

	# write totals to file
	ofx.write("Total Unique Traces: " + str(traceCount3) + '\n')
	ofx.write("Total Unique IPs: " + str(ipCount3) + '\n')
	ofx.write("Total Unique Source IPs: " + str(srcCount3) + '\n')
	ofx.write("Total Unique Destination IPs: " + str(dstCount3) + '\n')
	ofx.write("Total Unique Edges: " + str(edgeCount) + '\n')
	ofx.close()

	# update start_time.txt
	f = open("start_time.txt", "w")
	f.write(str(end_time))
	f.close()


def main():
	# iterate through days
	for x in range(1, 2): # from 1 to number of days you want + 1
		trace()


if __name__ == '__main__':		
	main()