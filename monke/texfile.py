import os

class Texfile:
    def  __init__(self, name: str, path: str=""):
        self.name = f'{name}.tex'
        self.path = path
        self.path_with_name = f'{self.path}{self.name}'
        self.objects: list[str] = []
    
    def clear(self):
        file = open(self.path_with_name, "w")
        file.close()
        
    def add(self, text: str):
        if text not in self.objects:
            self.objects.append(text)
        
    def make(self):
        with open(self.path_with_name, "w") as file:
            for object in self.objects:
                file.write(object)
        
    def delete_object(self, obj: str):
        for object in self.objects:
            if object == obj:
                self.objects.remove(obj)
                return
            
    
    def delete(self):
        global in_dir
        
        if self.path != "":
            os.chdir(self.path)
            
        files = os.listdir()
        for file in files:
            if file == self.name:     
                os.remove(self.name)