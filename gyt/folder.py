"""Project folder"""

import pandas as pd
import uuid
import os
import hashlib
import logging

class Folder(object):
    """emulate a Folder"""
    _columns = ["name", "mod", "hash"]
    CONTENTFILEPATH = ".content"

    def __init__(self, *args, **kwargs):
        self.path = kwargs.get("path") or os.getcwd()
        self._content = pd.DataFrame(columns=self._columns)
        self.load()

        self._metadata = kwargs.get("metadata") or {}
        try:
            self.uuid = uuid.UUID(kwargs.get("uuid"))
        except:
            self.uuid = uuid.uuid4()
        self.name = kwargs.get("name") or "N.N."

    @property
    def content(self):
        return self._content

    def import_files(self, path):
        self.get_content(path)
        self.dump()

    def get_hash(self, filepath):
        if os.path.exists(filepath):
            BLOCKSIZE = 65536
            hasher = hashlib.md5()
            with open(filepath, 'rb') as afile:
                buf = afile.read(BLOCKSIZE)
                while len(buf) > 0:
                    hasher.update(buf)
                    buf = afile.read(BLOCKSIZE)
            return hasher.hexdigest()

    def __str__(self):
        return "(f:%s)" % self.name

    def __repr__(self):
        return "(f:%s)" % self.name

    def ls(self, *args, **kwargs):
        """list dir"""
        return self._content

    def get_content(self, path):
        content = self.content
        df0 = pd.DataFrame(columns=self._columns)
        if path is None:
            return
        elif os.path.exists(path) and os.path.isdir(path):
            filenames = os.listdir(path)
            dfdict = {}
            for filename in filenames:
                if filename == self.CONTENTFILEPATH:
                    continue
                hash = self.get_hash(os.path.join(path, filename))
                if filename not in content.name:
                    dfdict[uuid.uuid4()] = {"name":filename, "mod":False, "hash":hash}
                elif filename not in content.name:
                    print("file '%s' exist" % filename)
                    file_row = content[content.hash==hash]
                    print(file_row)

            df = pd.DataFrame.from_dict(dfdict, orient="index")
            print(df)
            print(content)
            self._content = content.append(df)

    def dump(self):
        """dump content"""
        self._content.to_csv(os.path.join(self.CONTENTFILEPATH))

    def load(self):
        """load content"""
        if os.path.exists(self.CONTENTFILEPATH):
            self._content = pd.read_csv(self.CONTENTFILEPATH)
        return self._content

if __name__ == '__main__':
    os.remove(Folder.CONTENTFILEPATH)
    f = Folder(name="root", path=os.getcwd())
    f.import_files(os.getcwd())
    print(f)
    print(f.ls())