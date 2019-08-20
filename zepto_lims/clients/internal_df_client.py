# Copyright 2019, Rasmus Sorensen <rasmusscholer@gmail.com>
"""




"""

from zepto_lims.datastores.csv_df_store import CsvDfStore


class InternalDfClient:
    """
    This is a client that:
    * Retrieves data directly from a PandasCsvDataStore.
    * Hands off the data as a pandas DataFrame.


    """

    def __init__(self, config):
        self.datastore = CsvDfStore(config)

    def get_table(self, table):
        return self.datastore.get_table(table)

    def set_table(self, table, df):
        self.datastore.set_table(table, df)
