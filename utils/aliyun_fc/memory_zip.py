#!/usr/bin/python3
# -*- coding: utf-8 -*-

from io import BytesIO
from zipfile import ZipFile


class MemoryZip:
    """A class for creating a zip file in memory."""
    def __init__(self):
        #BytesIO works for Python3. StringIO probably needed for Python2.
        self.memory=BytesIO()

    def append(self, filename, contents):
        """Appends a new file to the zip."""
        with ZipFile(self.memory, 'a') as zf:
            zf.writestr(filename, contents)

    def append_mult(self, *args):
        """Appends multiple files to the zip. args should be tuples of the
        form (filename, contents)."""
        for filename, contents in args:
            self.append(filename, contents)

    def read(self):
        """Reads the zip, allowing it to be saved to file."""
        #If StringIO used, getvalue() probably needs to be reaplced
        #with a combination of seek(0) and read().
        return self.memory.getvalue()

    def save(self, filepath):
        """Saves the zip to file."""
        with open(filepath, 'wb') as file:
            file.write(self.read())