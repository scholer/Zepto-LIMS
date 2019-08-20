# Copyright 2019, Rasmus Sorensen <rasmusscholer@gmail.com>
"""

The server takes the data from the `datastore` object and makes it available to clients.
There are two ways to serve the data:
* By HTTP (REST/GraphQL) - if the server is on a different machine (or a separate process).
* Using an internal server-client.

This module contains the BaseServer class, which contains all logic common to the
different server implementations.


"""
