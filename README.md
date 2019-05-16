This project is writen in Python3 and subject to simulate a address book system using Python Flask and elasticsearch.

The flask server is in *addr_book_flask.py* have 5 endpoints (APIs):

`GET /contact?pageSize={}&page={}&query={}`: Query documents. This endpoint will providing a listing of all contacts, or it 
will use query parameter to search database

`POST /contact`: post documents on database, will return failure is contact already exsited

`GET /contact/{name}`: get one documents with the provided unique name

`PUT /contact/{name}`: edit one documents with the provided unique name and information

`DELETE /contact/{name}`: delete one documnets with the provided unique name and information
Note: the above three api will return failure if the name is not found in the database

When the unique name is provided for POST and GET/PUT/DELETE, it will be convert to 8 bit integer using hash function, this
number is then become the unique id for the document. It is a simplified emplementation, but also have its constrains. When
the database become bigger in size, the hash function may produce non-unique value for different input string. Thus, may
cause error. One way to avoid this is to keep a log for used id and constantly check the log file when adding new documents.
