=====================================
articleone Requirements Documentation
=====================================

The purpose of this document is to detail the requirements for 
the articleone module. This is an initial take to help with 
planning. There may be additional requirements or non-required 
features added in the future.


Purpose
-------
The purposes of the articleone module are:

* To parse data pulled from the sites of the U.S. legislative 
  branch (hence Article 1) for use in Python scripts,
* To continue my exploration with the Python language


Functional Requirements
-----------------------
The following are the functional requirements for articleone: 

1. articleone can parse the list of current U.S. senators found here:
   https://www.senate.gov/general/contact_information/senators_cfm.xml
2. articleone can parse the list of current U.S representatives 
   found here: 
   https://www.house.gov/representatives


Technical Requirements
----------------------
The following are the technical requirements for articleone:

1. articleone is a Python module.
2. articleone will use the aiohttp module for HTTP.
3. articleone will use descriptors to handle validation.
4. articleone will normalize all strings to UTF-8, NFC


Design Discussion
-----------------
The first thing to work through is the data model. If I'm going to 
go get data, I need somewhere to put it. The pattern I'm going to 
use here is going to be based on the pattern in *Fluent Python*. 
The technical requirements here can be seen in the test cases in 
the tests/test_model module.