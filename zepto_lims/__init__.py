# Copyright 2019, Rasmus Sorensen <rasmusscholer@gmail.com>
"""

Transport layer - parts, overview:


* The data is stored by a `datastore` object.
    This handles data persistence.

* The server takes the data from the `datastore` object and makes it available to dataclients.
    There are two ways to serve the data:
    * By HTTP (REST/GraphQL) - if the server is on a different machine (or a separate process).
    * Using an internal server-client.

* The client is responsible for retrieving data from the server and make it available to
    the parent application. The client does not perform any logic, only data transport.

* The `app(s)` are responsible for all logic, but not connected to how to retrieve data
    (other than asking the client for the data).
    The app decides which client to use and how to configure it.







"""
