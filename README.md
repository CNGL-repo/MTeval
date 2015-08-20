# MTeval
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

Running runserver.py will run the service.  