# Copyright 2019, Rasmus Sorensen <rasmusscholer@gmail.com>
"""

This module uses pandas DataFrame to read and write data to/from disk, stored in CSV format.


"""

from pathlib import Path
import pandas as pd


class CsvDfStore:

    def __init__(self, config):

        self.config = config if config is not None else {}
        self.table_cache = {}
        self.datastore_root_dir = Path(config.get('datastore_root_dir'))
        self.datastore_autoflush = config.get('datastore_autoflush')

    def get_table_filepath(self, table: str):
        filename = table + ".csv"
        filepath = self.datastore_root_dir / filename
        return filepath

    def load_table(self, table: str):
        return pd.read_csv(self.get_table_filepath(table))

    def save_table(self, table: str):
        df = self.table_cache[table]
        df.to_csv(self.get_table_filepath(table))

    def get_table(self, table: str) -> pd.DataFrame:
        if table not in self.table_cache:
            self.table_cache[table] = self.load_table(table)
        return self.table_cache[table]

    def set_table(self, table: str, df: pd.DataFrame, flush=None):
        """ Set a specific table, overwriting the current content. """
        self.table_cache[table] = df
        if flush is None:
            flush = self.datastore_autoflush
        if flush:
            self.save_table(table)

    def update_table(self, table: str, data: pd.DataFrame):
        """ Update a table with the given data, updating
        Initially, this should probably be only implemented on the client side,
        then just do a complete overwrite of the existing dataframe.
        Having this feature in the datastore is only really worth it when
        we have sufficiently large tables that only sending partial table data
        is worth it (and even then, obviously only for HTTP server communication.
        """
        pass


