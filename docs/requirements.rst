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
the following modules:

* tests/test_model
* tests/test_validators
* tests/test_common
* tests/test_senate

Next up is the design for the HTTP client to pull the data. I'm 
not really calling APIs here. I'm more or less just scraping. So, 
I probably don't need anything super complex here. I also don't 
have to worry about authentication. There is an implementation of 
a asynchronous HTTP client in *Fluent Python*, so maybe I can start 
with that?

Seriously, if you haven't read *Fluent Python* by Luciano Ramalho, 
you should.

Anyway, that pattern is probably more complex than I need to start 
with, so I'll just go with the client example from the aiohttp site 
for now. Look for the detailed requirements here:

* tests/test_http

Since I'm writing this starting from the data model rather than 
from the connection, it's probably worth walking through the steps 
involved in the connection to figure out how to break it down into 
functions. Those steps are:

1. Make the connection to senate.gov
2. Get the XML file
3. Parse the XML file
4. Build the Senator objects

That probably breaks down into the functions:

1. http.fetch
2. senate._fetch_senate_xml
3. common.parse_xml
4. senate.Senator.from_xml

This will all need to be asynchronous in order for it to matter 
that I'm using aiohttp here. Though, the asynchronicity here isn't 
all that useful since the senate.xml file is just one HTTP call. 
But I probably want it to be able to go get the House information 
while it's waiting on the call for senate.xml.