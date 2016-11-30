"""Project folder"""

import pandas as pd
import uuid
import os
import hashlib
import logging

class Folder(object):
    """emulate a Folder"""
    _columns = ["name", "mod", "hash"]
    CONTENTFILEPATH = ".gyt"

    def __init__(self, *args, **kwargs):
        self.path = kwargs.get("path") or os.getcwd()
        self._content = pd.DataFrame(columns=self._columns)
        self._content.index.name = 'idx'
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
        df0.index.name = "idx"
        if path is None:
            return
        elif os.path.exists(path) and os.path.isdir(path):
            filenames = os.listdir(path)
            dfdict = {}
            for filename in filenames:
                if filename == self.CONTENTFILEPATH:
                    continue
                hash = self.get_hash(os.path.join(path, filename))
                print("!!!", filename, hash, any(content.name.isin([filename])))
                if not any(content.name.isin([filename])):
                    print("newfile")
                    dfdict[uuid.uuid4().hex] = {"name":filename, "mod":False, "hash":hash}
                elif filename not in content.name:
                    file_row = content[content.hash==hash]
                    print("file '%s' exist" % filename, file_row.to_dict())
                    # dfdict[file_row.idx]
                    #print("row", file_row.to_dict())

            df = pd.DataFrame.from_dict(dfdict, orient="index")
            df.index.name = "idx"
            #print(dfdict)
            # print(df)
            # print(content)
            self._content = pd.concat([self._content, df])[self._columns]
            #self._content.update(df)

    def dump(self):
        """dump content"""
        self._content.to_csv(os.path.join(self.CONTENTFILEPATH), index_label="idx")

    def load(self):
        """load content"""
        if os.path.exists(self.CONTENTFILEPATH):
            df = pd.read_csv(self.CONTENTFILEPATH)
            df.index = df["idx"]
            # print("!!", df.head())
            # print(df.index)
            self._content = df[self._columns]
        return self._content

if __name__ == '__main__':
    os.remove(Folder.CONTENTFILEPATH)
    f = Folder(name="root", path=os.getcwd())
    f.import_files(os.getcwd())
    print(f)
    print(f.ls())
