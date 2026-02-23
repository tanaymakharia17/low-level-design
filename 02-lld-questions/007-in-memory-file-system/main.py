"""

Requirements:
1. Create directory on a path
2. Create a file on a path
3. Remove a directory
4. Remove a file
5. Read a file
6. list all files

Classes and blueprint:
AbstractFileSystem abc, for the composite system

An file abstract class for types of file - txt, .py file, .cpp file (this will inherit the file abstract class)
A class of directory which will inherit the abstract file system
"""


from abc import ABC, abstractmethod
from enum import Enum




class AbstractFileSystem(ABC):
    @abstractmethod
    def ls(self, path=None): pass

    @abstractmethod
    def rm(self): pass

    @abstractmethod
    def get_name(self): pass




class FileTypeEnum(Enum):
    TXT = 1
    PY = 2
    CPP = 3

class AbstractFile(AbstractFileSystem):
    name: str
    type: FileTypeEnum


    def __init__(self, name):
        self.name = name
        

    @abstractmethod
    def read(self): pass

    def ls(self):
        print(self.name)

    def rm(self):
        print(f"Removing File {self.name}")
    
    def get_name(self):
        return self.name

    


class PythonFile(AbstractFile):
    data: str

    def __init__(self, name, data):
        super().__init__(name)
        self.data = data
        self.type = FileTypeEnum.PY

    def read(self):
        print(f"This is a python File. Data: {self.data}")


class TXTFile(AbstractFile):
    data: str

    def __init__(self, name, data):
        super().__init__(name)
        self.data = data
        self.type = FileTypeEnum.TXT

    def read(self):
        print(f"This is a txt File. Data: {self.data}")


class CppFile(AbstractFile):
    data: str

    def __init__(self, name, data):
        super().__init__(name)
        self.data = data
        self.type = FileTypeEnum.CPP

    def read(self):
        print(f"This is a cpp File. Data: {self.data}")


class Directory(AbstractFileSystem):
    name: str
    file_sys_list: list[AbstractFileSystem]

    def __init__(self, name):
        self.name = name
        self.file_sys_list = []
    
    def get_name(self):
        return self.name
    
    def add(self, file_sys):
        self.file_sys_list.append(file_sys)
    
    def rm_child(self, name):
        file_obj = self.get_child(name) 
        if file_obj:
            file_obj.rm()
            self.file_sys_list.remove(file_obj)
    
    def get_child(self, name):
        for file_obj in self.file_sys_list:
            if file_obj.get_name() == name:
                return file_obj
        return None

    def ls(self):
        childs = [child_obj.get_name() for child_obj in self.file_sys_list]
        print(childs)

    
    def rm(self):
        print(f"Deleting Dir: {self.name}")
        for file_obj in self.file_sys_list:
            file_obj.rm()
        self.file_sys_list = []



class FileSysController:

    root_dir: Directory = Directory("")


    def rm(self, path: str):
        path_list = path.strip('/').split('/')
        curr = self.root_dir
        for file_sys_name in path_list[:-1]:
            child = curr.get_child(file_sys_name)
            if child:
                curr = child

        
        curr.rm_child(path_list[-1])

    def ls(self, path):
        path_list = path.strip('/').split('/')
        curr = self.root_dir
        for file_sys_name in path_list:
            child = curr.get_child(file_sys_name)
            if child:
                curr = child

        
        curr.ls()
    
    def create(self, path, obj: AbstractFileSystem):
        path_list = path.strip('/').split('/')
        curr = self.root_dir
        for file_sys_name in path_list:
            child = curr.get_child(file_sys_name)
            if child:
                curr = child

        
        curr.add(obj)
    

    def read(self, path):
        path_list = path.strip('/').split('/')
        curr = self.root_dir
        for file_sys_name in path_list[:-1]:
            child = curr.get_child(file_sys_name)
            if child:
                curr = child

        file_name = path_list[-1]
        file_obj: AbstractFile = curr.get_child(file_name)
        file_obj.read()




fs = FileSysController()

fs.create("/projects", Directory("projects"))
fs.create("/projects/app.py", PythonFile("app.py", "print('hi')"))
fs.create("/projects/readme.txt", TXTFile("readme.txt", "Docs here"))

fs.ls("/projects")        # Output: ['app.py', 'readme.txt']
fs.read("/projects/app.py")  # Output: This is a python File. Data: print('hi')

fs.rm("/projects/readme.txt")
fs.ls("/projects")        # Output: ['app.py']