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

1. articleone can return information about U.S. members of 
   Congress from the @unitedstates project on GitHub


Technical Requirements
----------------------
The following are the technical requirements for articleone:

1. articleone is a Python module.
2. articleone will use descriptors to handle validation.
3. articleone will normalize all strings to UTF-8, NFC


Design Discussion
-----------------
The following are my thoughts as I work through the design. There 
is no guarantee this is coherent or useful.


Data Model
~~~~~~~~~~
The first thing to work through is the data model. If I'm going to 
go get data, I need somewhere to put it. The pattern I'm going to 
use here is going to be based on the pattern in *Fluent Python*. 
The technical requirements here can be seen in the test cases in 
the following modules:

* tests/test_model
* tests/test_validators
* tests/test_common
* tests/test_senate


Connection: Initial Thoughts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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

The mainline for this will be senate.get_senators.


Connection: Asynchronicity
~~~~~~~~~~~~~~~~~~~~~~~~~~
The above plan doesn't really work if this is asynchronous. I 
can't just call http.fetch and have it get the data. I have 
to create the event loop, add fetch to the loop, and watch for 
the event signalling that fetch is complete. And I have to do 
all that in a way that doesn't block anything.

So, maybe I better start the design from the event loop and 
build from there. I suppose this means that I really need a 
mainline here to manage the event loop. And all of this is 
sounding like a lot of infrastructure for what is, right now 
at least, two HTTP calls. Maybe this is not the project to 
play with aiohttp on. So, let's keep it with requests for now.

Asynchronous HTTP call feature is cancelled.


Connection: Redesign
~~~~~~~~~~~~~~~~~~~~
The pattern with requests is much easier. It doesn't change much 
from my initial-thoughts design:

1. http.get
2. senate._get_senate_xml
3. common.parse_xml
4. senate.Senator.from_xml

Is 2 really necessary? I'm not sure when I'd ever need to make 
a call to get senate.xml separate from the call to get all the 
senator.Senator objects. Also, I can just call the mainline 
for this senate.senators. Though, may want to look at ways to 
handle caching for that, making it act more like a property 
than a function. Maybe.

Anyway, the steps inside senator.senators are:

1. http.get
2. common.parse_xml
3. senate.Senator.from_xml

Since the trusted objects are in common and the data going to 
parse_xml is not trusted, I may want to think about moving it 
out of common. I have to parse HTML for the House, so having 
it outside of senate still seems good. Maybe a utility module?


Interface: CLI
~~~~~~~~~~~~~~
I could implement the status updates with a coroutine, but I'm 
not certain why that would be better than a class. So, I think 
I'll try it with a class this time. See the specific requirements 
for the cli.Status object in tests/test_cli.


Roadblock: Switching from senate.gov
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Instead of pointing directly to the senate.gov site, I'm switching 
to using the information provided by the @unitedstates project 
on GitHub. I could access this data through Propublica's Congress 
API, but that requires signing up for an API key, which I'd have to 
keep secret. While I may change my mind in the future, for now I'm 
just going to go to @unitedstates.

This means a pretty substantial redesign of the connection client 
modules. The senate module will be removed and replaced with a 
unitedstates module for connecting to the @unitedstates project. 
Both Senate and House information will be retrieved from there. 
That probably means that I won't need separate Senator and 
Representative objects. The distinction will just be an attribute 
of the common.Member object.

The initial plan for the contents of unitedstates.py:

* senators
* representatives
* members

The functional requirements above will be updated with this change

The URL for the information is:
https://theunitedstates.io/congress-legislators/legislators-current.json