import os
import csv
from BeautifulSoup import BeautifulSoup
import re

# class SGMLToCSV:
# 	def __init__(self, input = None, output = None):
# 		self.input = input
# 		self.output = output
# 		if input != None:
# 			self.convert(input, output)

# 	def convert(self, input, output):
# 		outName = output
# 		#if output is empty, use the same input name with a different extension
# 		if output == None:
# 			outName = "{0}.csv".format(os.path.splitext(input)[0])

# 		#make a soup with the input sgml
# 		soup = BeautifulSoup(open(input))

# 		#get the first line
# 		#Note: not using any of this information for the csv..
# 		meta = soup.srcset

# 		#find all documents so we can iterate over them
# 		docs = soup.findAll("doc")
		

# 		header = ("docId", "segId", "segContents")
# 		with open(output, "w") as f:
# 			writer = csv.writer(f)
# 			writer.writerow(header)

# 			for doc in docs:
# 				docId = doc["docid"]
# 				for seg in doc.findAll("seg"):
# 					segId = seg["id"]
# 					segText = seg.string

# 					row = docId, segId, segText
# 					writer.writerow(row)

# #testing
# if __name__ == "__main__":
# 	con = SGMLToCSV(input = "test.sgm", output = "out.csv")

def SGMLToCSV(input, output = None):
	outName = output
	#if output is empty, use the same input name with a different extension
	if output == None:
		outName = "{0}.csv".format(os.path.splitext(input)[0])

	#make a soup with the input sgml
	soup = BeautifulSoup(open(input))

	#get the first line
	#Note: not using any of this information for the csv..
	meta = soup.srcset

	#find all documents so we can iterate over them
	docs = soup.findAll("doc")
	

	header = ("docId", "segId", "segContents", "sysid", "genre", "origlang")
	with open(outName, "w") as f:
		writer = csv.writer(f)
		writer.writerow(header)

		for doc in docs:
			docId = doc["docid"]
			sysid = doc["sysid"]
			genre = doc["genre"]
			origlang = doc["origlang"]
			for seg in doc.findAll("seg"):
				segId = seg["id"]
				segText = seg.string

				row = docId, segId, segText, sysid, genre, origlang
				writer.writerow(row)