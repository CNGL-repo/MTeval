# MTeval
##Description
Platform to organise MT Shared Tasks and automatically process the submissions

An admin account is generated the first time the service is run.
Admin accounts can organise shared tasks(competitions) and post test and training
data for them.
Admin accounts can also approve teams and remove teams.

Users can register teams. Teams are verified by admin approval and email
verification.
Teams can submit submissions in an SGML format to competitions.
Upon submission the SGML is added to the upload folder in MTEval.
From this file a CSV and CSVW are created.
From the CSVW a RDF is created.
These are all stored in the upload folder also.
Files are named by using the teamname and date of submission.
Any number of attempts can be submitted.

When using on a new server the cfg file must be changed so the appropriate path 
is used for file uploading and storage.

The service uses MongoDB through Pymongo. 

##Starting MTEval
* Start 4Store (see below)
* Ensure the configuration file (mteval/config.cfg) is correct
* Start MTEval from the root directory
  - python runserver.py 
* The server should now be running on port 5005

##Starting 4Store
4Store is used as a persistent triple store for MTEval. It **must** be started before submissions are uploaded, and before SPARQL queries can be run

###Start the 4store database
4s-backend mteval
###Start the SPARQL server
4s-httpd -H 127.0.0.1 -p 8989 mteval

##Submissions
Submissions are available at:
/comps/submissions

They can be restricted by competition by giving the parameter competition:
/comps/submissions?competition=XXX

SPARQL queries can be given at:
/comps/submissions/sparql