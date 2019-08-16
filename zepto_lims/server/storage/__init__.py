"""

We have the following objects:

* Tubes
* Boxes

Tubes have the following attributes:

* tube_id - this is just a unique integer for internal control.
* box_id - binds a tube to
* date
* sampleid - sample identifier; a string e.g. "RS123a12".
* sampledesc - sampe description.
* notes - a single text field with further notes.


We initially reserve the following special boxes (these could also be boolean fields or a status enum)?

* Discarted - The tube has been deliberately thrown out.
* Consumed - Tubes that have been fully consumed.
* Lost - Tubes that are currently lost, but where you haven't knowingly discated the tube.


I would like to implement the following data stores:

* CSV - because having local text files is great for revisioning and grep'ing.
* Database - for faster performance.

Databases could be:

* SQL-based, e.g. postgres, firebird, or sqlite (suitable for small deployments).
* Document-based, e.g MongoDB or Couchbase. Cassandra is definitely overkill.
* Key-value databases, e.g. Redis.
* EdgeDB - uses GraphQL as native query language.


Server APIs could be:

* Internal - each client directly accessing the database.
* REST - returning JSON data
* GraphQL



"""
