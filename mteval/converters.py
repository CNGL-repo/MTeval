import os
import csv
import json
from BeautifulSoup import BeautifulSoup
import re
import urllib

template = {
	"@id": None,
	"@context": ["http://www.w3.org/ns/csvw",
        {
        "terms":"http://mt.peep.ie/terms/",
        "@language": "en",
        "dcterms":"http://purl.org/dc/terms/",
        "xsd": "http://www.w3.org/2001/XMLSchema#",
        }],
    "delimiter": ",",    
    "@type":["Table"],

    "tableSchema":{
    	"columns": [
    		{
	    		"name": "docId",
	    		"title": "docId",
	    		"dcterms:description": "Id of the document",
	    		"datatype": "xsd:string",
	    		"required": "true",
	    		"propertyUrl": "terms:docId"
    		},
	    	{
		    	"name": "segId",
	    		"title": "segId",
	    		"dcterms:description": "Id of the segment",
	    		"datatype": "xsd:integer",
	    		"required": "true",
	    		"propertyUrl": "terms:segId"
	    	},
	    	{
	    		"name": "segContents",
	    		"title": "segContents",
	    		"dcterms:description": "Content of the segment",
	    		"datatype": "xsd:string",
	    		"required": "true",
	    		"propertyUrl": "terms:segContents"
	    	},
	    	{
	    		"name": "sysid",
	    		"title": "sysid",
	    		"dcterms:description": "Id of the system",
	    		"datatype": "xsd:string",
	    		"required": "true",
	    		"propertyUrl": "terms:sysid"
	    	},
	    	{
	    		"name": "genre",
	    		"title": "genre",
	    		"dcterms:description": "genre of the source",
	    		"datatype": "xsd:string",
	    		"required": "true",
	    		"propertyUrl": "terms:genre"
	    	},
	    	{
	    		"name": "origlang",
	    		"title": "origlang",
	    		"dcterms:description": "Language of the source content",
	    		"datatype": "xsd:string",
	    		"required": "true",
	    		"propertyUrl": "terms:origlang"
	    	},				
	],
	"primaryKey":["sysid", "docId"]
    }
}


def SGMLToCSVW(input, output = None):
	csvName = output
	csvwName = output
	fileName = os.path.splitext(input)[0]
	#if output is empty, use the same input name with a different extension
	if output == None:
		csvName = "{0}.csv".format(fileName)
		csvwName = "{0}.csv.csvw".format(fileName)

	#make a soup with the input sgml
	soup = BeautifulSoup(open(input))

	#get the first line
	#Note: not using any of this information for the csv..
	meta = soup.srcset

	#find all documents so we can iterate over them
	docs = soup.findAll("doc")
	


	header = ("docId", "segId", "segContents", "sysid", "genre", "origlang")
	with open(csvName, "w") as f:
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

	csvw = template
	head,tail = os.path.split(fileName)
	csvw["@id"] = "http://mt.peep.ie/download/{0}.csv".format(tail)			
	csvw["@url"] = "http://mt.peep.ie/download/{0}.csv".format(tail)
	csvw["tableSchema"]["aboutUrl"] = "http://mt.peep.ie/download/{0}.csv/row.{{_row}}".format(tail)


	with open(csvwName, "w") as f:
		json.dump(csvw, f, indent = 2)		

	return (csvName, csvwName)