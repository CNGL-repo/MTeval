import os
import csv
import json
from BeautifulSoup import BeautifulSoup
import re


template = {
	"@id": None,
	"@context": ["http://www.w3.org/ns/csvw",
        {"@language": "en",
        "dcterms":"http://purl.org/dc/terms/",
        "xsd": "http://www.w3.org/2001/XMLSchema#",
        }],
    "delimiter": ",",    
    "tableSchema":{
    	"columns": [
    		{"name": "docId",
    		"title": "docId",
    		"dcterms:description": "Id of the document",
    		"dataType": "xsd:string",
    		"required": "true"
    		},
	    	{"name": "segId",
	    		"title": "segId",
	    		"dcterms:description": "Id of the segment",
	    		"dataType": "xsd:integer",
	    		"required": "true"
	    		},
	    	{"name": "segContents",
	    		"title": "segContents",
	    		"dcterms:description": "Content of the segment",
	    		"dataType": "xsd:string",
	    		"required": "true"
	    		},
	    	{"name": "sysid",
	    		"title": "sysid",
	    		"dcterms:description": "Id of the system",
	    		"dataType": "xsd:string",
	    		"required": "true"
	    		},
	    	{"name": "genre",
	    		"title": "genre",
	    		"dcterms:description": "genre of the source",
	    		"dataType": "xsd:string",
	    		"required": "true"
	    		},
	    	{"name": "origlang",
	    		"title": "origlang",
	    		"dcterms:description": "Language of the source content",
	    		"dataType": "xsd:string",
	    		"required": "true"
	    		},				
	],
	"primaryKey":["sysid", "docId"]
    }
}
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

def SGMLToCSVW(input, output = None):
	csvName = output
	csvwName = output
	fileName = os.path.splitext(input)[0]
	#if output is empty, use the same input name with a different extension
	if output == None:
		csvName = "{0}.csv".format(fileName)
		csvwName = "{0}.csvw".format(fileName)

	#make a soup with the input sgml
	soup = BeautifulSoup(open(input))

	#get the first line
	#Note: not using any of this information for the csv..
	meta = soup.srcset

	#find all documents so we can iterate over them
	docs = soup.findAll("doc")
	

	header = ("docId", "segId", "segContents")
	with open(csvName, "w") as f:
		writer = csv.writer(f)
		writer.writerow(header)

		for doc in docs:
			docId = doc["docid"]
			for seg in doc.findAll("seg"):
				segId = seg["id"]
				segText = seg.string

				row = docId, segId, segText
				writer.writerow(row)

	csvw = template
	head,tail = os.path.split(fileName)
	csvw["@id"] = "http://mt.peep.ie/download/{0}.csv".format(tail)			
	csvw["@url"] = "http://mt.peep.ie/download/{0}.csv".format(tail)

	with open(csvwName, "w") as f:
		json.dump(csvw, f, indent = 2)


