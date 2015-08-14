import os
import unicodecsv
import json
from BeautifulSoup import BeautifulSoup
import re
import urllib
import sys

template = {
	"@id": None,
	"@context": ["http://www.w3.org/ns/csvw",
        {"@language": "en",
        "dcterms":"http://purl.org/dc/terms/",
        "xsd": "http://www.w3.org/2001/XMLSchema#",
        "example": "http://www.example.org/"
        }],
    "delimiter": ",",    
    "@type": ["Table"],
    "tableSchema":{
    	"columns": [
    		{"name": "o-tmf",
    			"title": "o-tmf",
    			"dcterms:description": "Creator of origional file",
    			"dataType": "xsd:string",
    			"required": "true",
    			"propertyUrl": "example:o-tmf"
    		},
    		{"name": "creationtool",
    			"title": "creationtool",
    			"dcterms:description": "Tool used to create file",
    			"dataType": "xsd:string",
    			"required": "true",
    			"propertyUrl": "example:creationtool"
    		},
    		{"name": "creationtoolversion",
    			"title": "creationtoolversion",
    			"dcterms:description": "Version of the creation tool",
    			"dataType": "xsd:string",
    			"required": "true",
    			"propertyUrl": "example:creationtoolversion"
    		},
    		{"name": "segtype",
    			"title": "segtype",
    			"dcterms:description": "Type of the segment",
    			"dataType": "xsd:string",
    			"required": "true",
    			"propertyUrl": "example:segtype"
    		},
    		{"name": "datatype",
    			"title": "datatype",
    			"dcterms:description": "Type of the data",
    			"dataType": "xsd:string",
    			"required": "true",
    			"propertyUrl": "example:datatype"
    		},
    		{"name": "adminlang",
    			"title": "adminlang",
    			"dcterms:description": "Administrative language ",
    			"dataType": "xsd:string",
    			"required": "true",
    			"propertyUrl": "example:adminlang"
    		},
    		{"name": "srclang",
    			"title": "srclang",
    			"dcterms:description": "Source language",
    			"dataType": "xsd:string",
    			"required": "true",
    			"propertyUrl": "example:srclang"
    		},
	    	{"name": "prop",
	    		"title": "prop",
	    		"dcterms:description": "Document type",
	    		"dataType": "xsd:string",
	    		"required": "true",
	    		"propertyUrl": "example:prop"
	    		},
	    	{"name": "tuv",
	    		"title": "tuv",
	    		"dcterms:description": "Language of the segment",
	    		"dataType": "xsd:string",
	    		"required": "true",
	    		"propertyUrl": "example:tuv"
	    		},
	    	{"name": "seg",
	    		"title": "seg",
	    		"dcterms:description": "Sentences in various languages",
	    		"dataType": "xsd:string",
	    		"required": "true",
	    		"propertyUrl": "example:seg"
	    		},				
	],
	"primaryKey":["seg", "prop"]
    }
}

def TMXToCSVW(input, output = None):
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
	header = soup.find("header")

	#find all documents so we can iterate over them
	tus = soup.findAll("tu")
	
	csv_header = ("header.o-tmf", "header.creationtool", "header.creationtoolversion", "header.segtype", 
		"header.datatype", "header.adminlang", "header.srclang", "prop.type", "prop.value", 
		"lang", "seg")

	with open(csvName, "w") as f:
		writer = unicodecsv.writer(f, encoding="utf-8")
		writer.writerow(csv_header)
		
		otmf = header["o-tmf"]
		creationtool = header["creationtool"]
		creationtoolversion = header["creationtoolversion"]
		segtype = header["segtype"]
		datatype = header["datatype"]
		adminlang = header["adminlang"]
		srclang = header["srclang"]
		
		for tu in tus:
			prop = tu.find("prop")
			propType = prop["type"]
			propVal = prop.text
			for tuv in tu.findAll("tuv"):
				lang = tuv["lang"]
				seg = tuv.find("seg").text

				row = otmf, creationtool, creationtoolversion, segtype, datatype, \
					adminlang, srclang, propType, propVal, lang, seg
				writer.writerow(row)

	csvw = template
	head,tail = os.path.split(fileName)
	csvw["@id"] = "http://mt.peep.ie/download/{0}.csv".format(tail)			
	csvw["@url"] = "http://mt.peep.ie/download/{0}.csv".format(tail)
	csvw["tableSchema"]["aboutUrl"] = "http://mt.peep.ie/download/{0}.csv/row.{{_row}}".format(tail)


	with open(csvwName, "w") as f:
		json.dump(csvw, f, indent = 2)		

	return (csvName, csvwName)

if __name__ == "__main__":
	TMXToCSVW(sys.argv[1])