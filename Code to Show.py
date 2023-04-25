#!/usr/bin/env python3

Testing Code:
	
TESTING ON other dataset:
curl -X GET 'http://localhost:5000/another.json'
curl -X PUT 'http://localhost:5000/another/477.json' -d '{"name": "Veronica", "age": 40}'
curl -X DELETE 'http://localhost:5000/another/477.json'



GET:

curl -X GET 'http://localhost:5000/users.json?orderBy="age"'
curl -X GET 'http://localhost:5000/users.json?orderBy="age"&limitToFirst=3'
curl -X GET 'http://localhost:5000/users.json?orderBy="age"&limitToLast=3'
curl -X GET 'http://localhost:5000/users.json?orderBy="age"&startAt=20'
curl -X GET 'http://localhost:5000/users.json?orderBy="age"&endAt=30'
curl -X GET 'http://localhost:5000/users.json?orderBy="age"&startAt=20&&endAt=30'
curl -X GET 'http://localhost:5000/users.json?orderBy="age"&startAt=20&&endAt=30&limitToFirst=1'
curl -X GET 'http://localhost:5000/users.json?orderBy="name"&equalTo="Selena"'



PATCH:

curl -X PATCH 'http://localhost:5000/users/300.json' -d '{"name": "Ryan", "age": 15}'



PUT:
	
curl -X PUT 'http://localhost:5000/users/301.json' -d '{"name": "Jimy", "age": 40}'


POST:
curl -X POST 'http://localhost:5000/another.json' -d '{"name": "Veronica", "age": 40}'


DELETE:

curl -X DELETE 'http://localhost:5000/users/300.json'


