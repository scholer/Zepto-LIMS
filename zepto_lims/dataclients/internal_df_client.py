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
        # Initialize config-defined data-store. For now, we just always use the CsvDfStore.
        self.datastore = CsvDfStore(config)

    def get_table(self, table):
        return self.datastore.get_table(table)

    def set_table(self, table, df, *, flush):
        self.datastore.set_table(table, df, flush=flush)

    def append_row(self, table, row):
        self.datastore.append_row(table, row)
