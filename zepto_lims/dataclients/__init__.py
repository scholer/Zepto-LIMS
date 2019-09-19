# Copyright 2019, Rasmus Sorensen <rasmusscholer@gmail.com>
"""

This package contains various data clients.

Data clients are responsible for making the data available for CRUD operations
via some means.

Data clients does not have any concept of the model domain, e.g. 'tubes' or
'boxes. - That is the job of the consumer, e.g. a TubeTracker class.

Data clients also do not care about how the data is stored - that is the job of
a `datastore` class.

For instance, the InternalDfClient initializes a CsvDfStore,
which reads and saves csv data from disk, and makes it available
in the form of a pandas DataFrame.

As such, the data-clients are mostly just thin wrappers to the datastore.
They are used mostly to make it easier to plug in different kinds of data stores,
e.g. switch from local csv files to a SQL database.

The data clients does not currently make any attempt of abstracting the CRUD API,
simply because of how different you would work with a DataFrame vs
an SQL database vs an object database.

Thus, the consuming object should be "matched" on the CRUD API side of things,
e.g. the InternalDfClient should be used by the TubeTrackerDf, which expects to
receive data in the form of pandas DataFrames, and performs CRUD operations using
the pandas.DataFrame API.


Note: There are also data-servers, which are created to serve as an abstraction link
to data stored on other machines/servers.
(This is still on the drawing board - no data-servers have yet been implemented.)

"""
