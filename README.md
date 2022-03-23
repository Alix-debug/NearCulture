# 📖 **NearCulture**

This project is made within the Web data mining and semantic course in Year 4 (Data science and artificial intelligence major) at ESILV - Engineering school.


Made by Alix Petitcol, Françoise Ruch and Marine Sublet.

## Table of content

- 📝 [Project Description and Requirements](#-project-requirements)
- ⚙️ [Set Up](#-set-up)
- 💻 [Used Technologies](#-used-technologies)
  1. Fuseki as TripleStore
  2. Python Flask application
- 👩‍💻 [Application](#-application)
  1.  Data Preprocessing and import
  2.  Ontology with Protégé
  3.  Querying the triplestore

## 🎯 Project requirements

### Minimal requirements

· Setup a triplestore. The simplest is to use Apache Jena Fuseki.

· Define or reuse a vocabulary for describing bicycle-sharing stations and their availability using Protégé.

· Convert static data about monuments and libraries into RDF, and load the resulting data to the triplestore. You can simply generate an RDF file that you load manually to the triplestore, or add the RDF programmatically using SPARQL Update queries.

· Make an application that will allow one to select a city (in a list or on a map) and get the corresponding museums/libraries. There resulting list should be available in HTML with RDFa. You may also make the data available in RDF (Turtle, RDF/XML, or JSON-LD) based on content negotiation.

· While the real time data may be generated on the fly, static data should be extracted from the triplestore using a SPARQL query.

## 📝 Set Up

You can test this project in local using the following steps :

1. First download and unzip the NearCulture project folder that contains the flask application, the museums and libraries open data and their .ttl associated files.

2. You will detect the presence of an apache-jena-fuseki-3.0.9.zip in the extracted folder. You need to unzip it and run the fuseki-server.bat
Then, you will be able to run your fuseki triplestore at the following address : http://localhost:3030/.

3. fill the database using the given .ttl files in the "import" folder. Name the databases respectively Museums, Libraries, Trips, Travelers.  

## 💻 Used Technologies

### 1. Fuseki as TripleStore

Apache Jena Fuseki is a SPARQL server. It can run as a operating system service, as a Java web application (WAR file), and as a standalone server. It provides security (using Apache Shiro) and has a user interface for server monitoring and administration.
In our case, we use it as a standalone server in order to query the server with SPARQL queries.

### 2. Python Flask application

We chose to implement a flask application to interact with our Fuseki triplestore. Flask is quick and easy to learn, so it was perfect regarding the project's deadline.

## 👩‍💻 Application

### 1. Data Preprocessing and import

We have retrieve the CSV dataset provided in the project requirement.
In order to insert them into the Fuseki triplestore we had to transform them into rdf files.
First we converted the files into pandas dataframes to clean them and select the information we wanted to keep : The name, address (region, city and street address), url (link to the offical website of the POI), longitude and latitude. 

Then we wrote an output JSON_LD file. However, this data format was not allowed in Fuseki triplestore. Thus, we finally convert the JSON_LD file into a Turtle file, using an online converter.


Here is an instance of the processing code we have implement in python to prepare the Library JSON_LD file :

```PYTHON
import pandas as pd

#load museum and library files
from google.colab import files 
uploaded = files.upload()

#for library 
data = pd.read_csv('HigherEducationLibrary.csv', sep=';', on_bad_lines='skip')

data=data[['id','nomlong','adresse_adresse','com_nom','geo','internet_web']]

#data cleaning
data.dropna(inplace=True)
data.reset_index(inplace=True)
data.drop('index',axis=1,inplace=True)

#create the longitude and latitude columns and insert values
data["latitude"]=float(0.0)
data["longitude"]=float(0.0)
for i in range(0,len(data.geo)):
  tab=data.geo[i].split(',')
  data["latitude"][i] = tab[0]
  data["longitude"][i] = tab[1]

data.drop('geo',axis=1,inplace=True)

#create the JSON_LD output file
outfile = open("script_JSONLD_libraries.json", 'w')

outfile.write('{\n"@context": "http://schema.org/",\n"@graph":[\n\n')
for i in range(0, len(data)):
    outline= '{\n"@type": "Library",\n'+'"identifier" : '+'"'+data.iloc[i]["id"]+'",'+"\n"+'"name" : '+'"'+data.iloc[i]["nomlong"]+'",'+"\n"+ '"address":{\n"@type": "PostalAddress",\n''     "addressLocality" :'+'"'+ data.iloc[i]["com_nom"]+'",'+"\n     "+'"streetAddress" : '+'"'+data.iloc[i]["adresse_adresse"]+'"'+"\n     },\n"+'"url" : '+'"'+data.iloc[i]["internet_web"]+'",'+"\n"+'"latitude" : '+'"'+str(data.iloc[i]["latitude"])+'",'+"\n"+'"longitude" : '+'"'+str(data.iloc[i]["longitude"])+'"'+"},\n"
    outfile.write(outline)
outfile.write('\n]\n\n}')
outfile.close()
```


### 2. Ontology with Protégé

In order to create our own ontology, we have created all our entities - POI (libraries - Museums), the trips and the travelers - using protégé. Then, because the owl format that was containing our ontology was not supported for the upload step in the fuseki triplestore we have convert the ontology in a .ttl file using an online converter.

### 3. Querying the triplestore

To set museums and libraries datasets in the triplestore we have reused the Schema.org vocabuary. We have also set our own vocubulary based on our ontology. Here are the queries we have implemented for this project. 

1/List the instances of the geolocated POI :

We have chosen to display the list of the POI : museums, using the follwing query, but also the libraries and the travalers.
We return multiple information about the name, the localisation of the POI and its latitude and longitude.


```SPARQL

	PREFIX schema: <http://schema.org/>
	PREFIX sc: <http://purl.org/science/owl/sciencecommons/>
	PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

	SELECT ?identifier ?name ?longitude ?latitude WHERE {
		?Instance 
		rdf:type schema:Museum; schema:name ?name; 			       
								schema:identifier ?identifier;
								schema:longitude ?longitude;
								schema:latitude ?latitude;
		} LIMIT 100

```

2/List the name of all Museums For each one, display its city.

This query is described in the Museum tab of the navigation bar. 
We proposed at least 9 different located areas for each POI, however we can easily add new location item in the html code.

```SPARQL
PREFIX schema: <http://schema.org/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT ?i ?name ?url ?r ?s ?lat ?long
WHERE
  {
  	?b0 schema:identifier ?i .
  	?b0 schema:name ?name .	
    ?b0 schema:address ?b1 .
  	?b1 schema:addressLocality ?r .
  	?b1 schema:addressRegion "{region}" .
    ?b1 schema:streetAddress ?s.
  	?b0 schema:url ?url .
  	?b0 schema:latitude ?lat .
    ?b0 schema:longitude ?long .
 
  }LIMIT 100

```
In this query the {region} is replaced by the city the user specified.

3/List the name of trips that have Paris as destination.

```SPARQL
PREFIX schema: <http://schema.org/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX : <http://www.semanticweb.org/protegee>


SELECT ?description ?itinerary ?name WHERE { ?Instance rdf:type :trip; :description ?description; :itinerary ?itinerary; :name ?name; :name "Trip in Paris" . }
```

4/List the name of travellers older than X years.

We decided to implement an ASK query that returns True or False depending on the traveler's age. If the traveler is older than an age, chosen in the list, it returns true.
```SPARQL
"prefix :      <http://www.semanticweb.org/protegee> 

		ASK WHERE{?Instance :age ?age FILTER (?age >"""+region+""")}

```


#### Propose 5 SPARQL queries:
a.	A query that contains at least 2 Optional Graph Patterns :

```SPARQL
PREFIX schema: <http://schema.org/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX sc: <http://purl.org/science/owl/sciencecommons/>
PREFIX ex: <http://example.org/>

SELECT ?name ?id ?url ?long ?lat WHERE {?Instance rdf:type schema:Library;schema:name ?name; schema:identifier ?id . OPTIONAL {?Instance schema:url ?url . } OPTIONAL {?Instance schema:longitude ?long; schema:latitude ?lat .}} LIMIT 100
```

This query is accessible at the ... tab in the nav bar.

b.	A query that contains at least 2 alternatives and conjunctions. 
Our query returns names of both people and trips.

```SPARQL
PREFIX schema: <http://schema.org/>
	PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
	PREFIX ex: <http://example.org/>
	PREFIX sc: <http://purl.org/science/owl/sciencecommons/>
	PREFIX owl: <http://www.w3.org/2002/07/owl#>
	PREFIX : <http://www.semanticweb.org/protegee>


	SELECT ?description WHERE { { ?Instance rdf:type :trip. ?Instance :description ?description . }
	UNION
	{ ?Instance rdf:type :traveler. ?Instance :familyName ?description . }
	}
```
This query is accessible at the ... tab in the nav bar.

c.	A query that contains a CONSTRUCT query form
Our query returns a new schema with all museums' names.

```SPARQL
PREFIX schema: <http://schema.org/>
PREFIX sc: <http://purl.org/science/owl/sciencecommons/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

CONSTRUCT{ ?x schema:Museum ?name} WHERE {?x schema:name ?name}
```
This query is accessible at the ... tab in the nav bar.

d.	A query that contains an ASK query form 

```SPARQL
"prefix :      <http://www.semanticweb.org/protegee> 

		ASK WHERE{?Instance :age ?age FILTER (?age >"""+region+""")}
```
This query is accessible at the ... tab in the nav bar.

e.	A query that contains a DESCRIBE query for (export) : described the data in rdf 
Query that exports all the libraries :

```SPARQL
PREFIX schema: <http://schema.org/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ex: <http://example.org/>
PREFIX sc: <http://purl.org/science/owl/sciencecommons/>

DESCRIBE ?Instance WHERE {?Instance rdf:type schema:Library; schema:name ?x}

```
This query is accessible at the ... tab in the nav bar.


