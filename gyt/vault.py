import uuid
import os
import sys
import hashlib
import logging
import pandas as pd

class Blob(object):
    """emulate a Folder"""

    def __init__(self, **kwargs):
        self._metadata = kwargs.get("metadata") or {}
        try:
            self._uuid = uuid.UUID(kwargs.get("uuid"))
        except:
            self._uuid = uuid.uuid4()
        self._name = kwargs.get("name") or "N.N."
        self._data = None

    def _get_name(self):
        return self._data
    def _set_name(self, value):
        self._data = value
    name = property(fget=_get_name, fset=_set_name, doc="blob name")

    @property
    def uuid(self):
        """blob uuid in hex format (50d4a50f9d89497da0dba40c5a1b4ec3)"""
        return self._uuid.hex

    def _get_data(self):
        return self._data
    def _set_data(self, value):
        self._data = value
    data = property(fget=_get_data, fset=_set_data, doc="raw blob data")

    def get_hash(self, filepath):
        """calculate hash"""
        if os.path.exists(filepath):
            BLOCKSIZE = 65536
            hasher = hashlib.md5()
            with open(filepath, 'rb') as afile:
                buf = afile.read(BLOCKSIZE)
                while len(buf) > 0:
                    hasher.update(buf)
                    buf = afile.read(BLOCKSIZE)
            return hasher.hexdigest()

    def dump(self, filepath):
        with open(filepath, "w") as fh:
            fh.write(self._data)

    def load(self, filepath):
        with open(filepath, "rs") as fh:
            self._data = fh.read()

    def __str__(self):
        return "(b:{})".format(self.uuid)

    def __repr__(self):
        return "(b:{})".format(self.uuid)

class Vault(object):
    """data vault"""
    def __init__(self, rootpath):
        self.rootpath = None
        try:
            os.makedirs(os.path.dirname(rootpath), exist_ok=True)
            self.rootpath = rootpath
        except OSError as exp:
            logging.error("Vault Error: {}".format(exp))
            raise exp
        logging.info("create vault {}".format(self.rootpath))

        self.df_blobs = pd.DataFrame(columns=["uuid", "hash", "name"])

    def set_blob(self, blob):
        """store blob in vault"""
        path = os.path.join(self.rootpath, 'objects', blob.uuid[:2], blob.uuid[-2:]) + os.sep
        print("create vault {}".format(path))
        logging.info("create vault {}".format(path))
        try:
            if not os.path.exists(path):
                # os.makedirs(os.path.dirname(path), exist_ok=True)
                os.makedirs(os.path.dirname(path), exist_ok=True)
        except OSError as exp:
            logging.error("Vault Error: {}".format(exp))
            raise exp
        filepath = os.path.join(path, blob.uuid)
        blob.dump(filepath)


if __name__ == '__main__':
    logging.StreamHandler(sys.stdout)
    blob = Blob(name="test", uuid="50d4a50f9d89497da0dba40c5a1b4ec3")
    blob.data = "123"
    print(blob)

    vault = Vault(rootpath="/tmp/vault")
    vault.set_blob(blob)