# DSCI551- Project: Firebase Emulsion


## RESTful API Testing Code:
	

### GET:

Our API supports GET function so that user can retrive the data from our mongodb database,Our get function supports the filter functions
order by, limit to first&Last, startat end at, equal to also if we are using orderby the API will create an index in our mongodb data base to help sort the datas

curl -X GET 'http://localhost:5000/users.json'

curl -X GET 'http://localhost:5000/users.json?orderBy="$key"'

curl -X GET 'http://localhost:5000/users.json?orderBy="age"'

curl -X GET 'http://localhost:5000/users.json?orderBy="age"&limitToFirst=3'

curl -X GET 'http://localhost:5000/users.json?orderBy="age"&limitToLast=3'

curl -X GET 'http://localhost:5000/users.json?orderBy="age"&startAt=20'

curl -X GET 'http://localhost:5000/users.json?orderBy="age"&endAt=30'

curl -X GET 'http://localhost:5000/users.json?orderBy="age"&startAt=20&&endAt=30'

curl -X GET 'http://localhost:5000/users.json?orderBy="age"&startAt=20&&endAt=30&limitToFirst=1'

curl -X GET 'http://localhost:5000/users.json?orderBy="name"&equalTo="Selina"'

curl -X GET 'http://localhost:5000/users.json?orderBy="age"&equalTo="45"'




### PATCH:

PATCH function is to update with the id that we input

curl -X PATCH 'http://localhost:5000/users/300.json' -d '{"name": "Ryan", "age": 15}'

Also, ifthe id does not exists, such as 301 it will create a new user

curl -X PATCH 'http://localhost:5000/users/301.json' -d '{"name": "Jason", "age": 15}'



### PUT:
PUT will replace or create a new one

curl -X PUT 'http://localhost:5000/users/301.json' -d '{"name": "Jimy", "age": 40}'

curl -X PUT 'http://localhost:5000/users/302.json' -d '{"name": "Jimywang", "age": 45}'



### POST:
POST will create a new one into the database

curl -X POST 'http://localhost:5000/users.json' -d '{"_id":23, "name": "Victoria", "age": 40}'




### DELETE:
DELETE function deletes the data for the id we put 

curl -X DELETE 'http://localhost:5000/users/300.json'

curl -X GET 'http://localhost:5000/users.json'


### TESTING ON other dataset:

curl -X GET 'http://localhost:5000/another.json'

curl -X PUT 'http://localhost:5000/another/477.json' -d '{"name": "Veronica", "age": 40}'

curl -X DELETE 'http://localhost:5000/another/477.json'


## WEB APP

To run the web app please run the **RESTful API.py** first and then run **Index.HTML**

The web app is showing a realtime syncing of the user database, and it's able to support Find, Create, Update, and Delete function of the database 
