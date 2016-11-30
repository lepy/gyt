import gyt
import gyt.folder
# print(gyt.__file__)
import os
import pandas as pd

modulepath = os.path.dirname(__file__)

def test_folder():
    # if os.path.exists(gyt.folder.Folder.CONTENTFILEPATH):
    #     os.remove(gyt.folder.Folder.CONTENTFILEPATH)

    foldername = "project0815"
    projectpath = os.path.join(modulepath, foldername)
    f = gyt.folder.Folder(name=foldername, path=projectpath)
    f.import_files(projectpath)
    # print(f)
    # print(f.ls())
    # print("!", f.load().columns)
    print("!", f.content)
    assert f.name == foldername, f.name

def test_dump():
    dfdict = {'c37181811ebf400a9bd3e213c6e78870': {'hash': '55b84a9d317184fe61224bfb4a060fb0', 'mod': False, 'name': 'bigdata.dat'}, '4286d30ad3d64372a894c54b1701fb7b': {'hash': '5eb63bbbe01eeed093cb22bb8f5acdc3', 'mod': False, 'name': 'README'}}
    df = pd.DataFrame.from_dict(dfdict, orient="index")
    df.index.name = "idx"
    print(df)

if __name__ == '__main__':
    test_folder()
    #test_dump()