## URL shortener API

Shortenes the provided url and stores in a database.
Shortened URL are unique and subsequent request for same url will result the already computed key.

Later revisions:
 - Caching requests
 - adding expiration date on each request
 - removing expired results and returning error response
 
 
 Before running the application configure `CONNSTR` variable in `db\__init__.py` to connect to your database