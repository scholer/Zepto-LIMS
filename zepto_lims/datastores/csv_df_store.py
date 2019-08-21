# Copyright 2019, Rasmus Sorensen <rasmusscholer@gmail.com>
"""

This module uses pandas DataFrame to read and write data to/from disk, stored in CSV format.

This is basically just a simple "proof-of-principle" data store.
It is probably more viable in the long run to use an actual database,
e.g. sqlite, postgres, mongodb, edgedb, or similar.

If you need to keep a text-representation of the data (e.g. for git revision control)
or just simple inspection, you can just make an automatic data export,
e.g. every time the database is flushed or the app closes (or by manual user request).

However, having a simple CSV file as the main data store does have the
advantage that you can update fields manually, or even add new columns,
and the changes are reflected in the primary data.

Of course, you could also just keep these two things ("tube location" and "additional tube info")
in two different tables, or even in entirely different storage methods.
You could have tube-location in a postgres database, and the additional tube info in
an Excel or Google spreadsheet.
You could even have a method to automatically update the "external" data source (Excel, Google)
with the tube location. However, that might be confusing if you try to update the location
in the external data source (because we also look for "removed tubes", and the internal data
wouldn't know if the external data has been fixed. As always, it is always better to have ONE
source of truth.


"""

from pathlib import Path
import pandas as pd
from datetime import datetime


class CsvDfStore:

    def __init__(self, config):

        self.config = config if config is not None else {}
        self.table_cache = {}
        # Uh, instead of setting a lot of config-defined attributes, it is probably best
        # to just use self.config.get(key, default) to get config values.
        # self.datastore_autoflush = config.get('datastore_autoflush')
        # self.sort_before_save = config.get('datastore_sort_before_save')
        # self.sort_on_update = config.get('datastore_sort_on_update')

    @property
    def datastore_root_dir(self):
        return Path(self.config.get('datastore_root_dir'))

    def get_table_filepath(self, table: str):
        filename = table + ".csv"
        filepath = self.datastore_root_dir / filename
        return filepath

    def to_disk(self, df, filename):
        """ Save DataFrame to disk (applying final sorting, etc, if specified by config). """
        if self.config.get('datastore_sort_before_save'):
            df.sort_values(
                by=self.config.get('datastore_sort_by_columns'),
                ascending=self.config.get('datastore_sort_ascending', True),
            )
        df.to_csv(filename)

    def load_table(self, table: str):
        """ Load table from disk. """
        return pd.read_csv(self.get_table_filepath(table))

    def save_table(self, table: str):
        """ Save table to disk.
        OBS: The table name must be loaded into memory (cached).
        If you want to just make sure the table is saved *if* it has been loaded,
        use `save_table_if_loaded`.
        """
        df = self.table_cache[table]
        self.to_disk(df, self.get_table_filepath(table))

    def save_table_if_loaded(self, table: str):
        """ Save table to disk. OBS: The table name must be loaded into memory (cached). """
        try:
            df = self.table_cache[table]
        except KeyError:
            print(f"Table '{table}' is not loaded/cached.")
        else:
            self.to_disk(df, self.get_table_filepath(table))

    def export_table(self, table: str, folder=None, filename=None):
        if folder is None:
            folder = self.config.get('datastore_last_export_folder', '.')
        else:
            self.config['datastore_last_export_folder'] = str(folder)
        if filename is None:
            filename = table + '.csv'
        filepath = Path(folder) / Path(filename)
        df = self.get_table(table)
        df.to_csv(filepath)

    def backup_export_table(self, table: str, folder=None, filename=None):
        """ Export a backup of the given table to a file on disk.
        `backup_export_table` differs from `export_table` in that it uses different config keys,
            datastore_backup_export_folder
            datastore_backup_export_filename
        and that it allows for the folder and filename to contain formatting variables,
        (e.g. `date` and `table`).
        If folder doesn't exist (after string format), it and all its parents will be created.
        """
        if folder is None:
            folder = self.config.get('datastore_backup_export_folder', '.')
        if filename is None:
            filename = self.config.get('datastore_backup_export_filename',
                                       '{table}_backup-{date:%Y%m%d-%H%%M%S}.csv')
        now = datetime.now()
        folder = folder.format(date=now, now=now, datetime=now)
        filename = filename.format(date=now, now=now, datetime=now)
        folder, filename = Path(folder), Path(filename)
        if not folder.exists():
            print("Creating folder:", folder)
            folder.mkdir(parents=True)
        self.export_table(table, folder=folder, filename=filename)

    def get_table(self, table: str) -> pd.DataFrame:
        if table not in self.table_cache:
            self.table_cache[table] = self.load_table(table)
        return self.table_cache[table]

    def set_table(self, table: str, df: pd.DataFrame, *, flush=None):
        """ Set a specific table, overwriting the current content. """
        self.table_cache[table] = df
        if flush is None:
            flush = self.config.get('datastore_autoflush')
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

    def append_row(self, table, row, *, flush=None, resort=None):
        """ Append a single row to the table. """
        df = self.get_table(table)
        df.append(row)
        if self.config.get('datastore_sort_on_update'):
            df.sort_values(
                by=self.config.get('datastore_sort_by_columns'),
                ascending=self.config.get('datastore_sort_ascending', True),
            )
        self.set_table(table, df, flush=flush)
        return df

    def append_rows(self, table, rows, *, flush=None):
        """ Append multiple rows to table. """
        df = self.get_table(table)
        df.append(rows)
        if self.config.get('datastore_sort_on_update'):
            df.sort_values(
                by=self.config.get('datastore_sort_by_columns'),
                ascending=self.config.get('datastore_sort_ascending', True),
            )
        self.set_table(table, df, flush=flush)
        return df
