"""
Calculator
File System
"""

from abc import ABC, abstractmethod


class FileSystem(ABC):

    @abstractmethod
    def ls(self, space=0): pass


class File(FileSystem):
    __name = None
    def __init__(self, name):
        self.__name = name
    
    def ls(self, space=0):
        indent = "    " * space
        print(f"{indent}- {self.__name}")


class Directory(FileSystem):
    __name = None
    __fileSystemList = None

    def __init__(self, name):
        self.__name = name
        self.__fileSystemList = []

    def add(self, fileSysObj: FileSystem):
        self.__fileSystemList.append(fileSysObj)
    
    def ls(self, space=0):
        indent = "    " * space
        print(f"{indent}[{self.__name}/]")
        for fileSysObj in self.__fileSystemList:
            fileSysObj.ls(space+1)




if __name__ == '__main__':
    # Creating files
    f_readme = File("readme.txt")
    f_data1 = File("data.csv")
    f_data2 = File("data.csv")           # duplicate name
    f_image1 = File("image.png")
    f_image2 = File("logo.png")
    f_note = File("notes.txt")
    f_script = File("script.py")
    f_secret = File(".env")              # hidden-style file

    # Creating directory structure
    root = Directory("root")
    dir_docs = Directory("documents")
    dir_images = Directory("images")
    dir_scripts = Directory("scripts")
    dir_empty = Directory("empty_dir")   # intentionally empty
    dir_archives = Directory("archives")
    dir_2023 = Directory("2023")
    dir_2024 = Directory("2024")

    # Assembling the structure
    root.add(f_readme)                      # root/
    root.add(dir_docs)                      # root/documents/
    root.add(dir_images)                    # root/images/
    root.add(dir_scripts)                   # root/scripts/
    root.add(dir_empty)                    # root/empty_dir/

    dir_docs.add(f_data1)                   # documents/data.csv
    dir_docs.add(f_note)                    # documents/notes.txt
    dir_docs.add(dir_archives)              # documents/archives/

    dir_images.add(f_image1)                # images/image.png
    dir_images.add(f_image2)                # images/logo.png

    dir_scripts.add(f_script)               # scripts/script.py
    dir_scripts.add(f_secret)               # scripts/.env

    dir_archives.add(dir_2023)              # documents/archives/2023/
    dir_archives.add(dir_2024)              # documents/archives/2024/
    dir_2023.add(f_data2)                   # documents/archives/2023/data.csv (same name as earlier!)

    # Final listing
    root.ls()