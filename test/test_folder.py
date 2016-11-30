import gyt
import gyt.folder
print(gyt.__file__)
import os

modulepath = os.path.dirname(__file__)

def test_folder():
    # if os.path.exists(gyt.folder.Folder.CONTENTFILEPATH):
    #     os.remove(gyt.folder.Folder.CONTENTFILEPATH)

    foldername = "project0815"
    projectpath = os.path.join(modulepath, foldername)
    f = gyt.folder.Folder(name=foldername, path=projectpath)
    f.import_files(projectpath)
    print(f)
    print(f.ls())
    assert f.name == foldername, f.name

if __name__ == '__main__':
    test_folder()