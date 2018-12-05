import tempfile
import os

class File:
    """
    This class was created for testing special methods. 
    It creates a file-like object that allows you to effectively 
    iterate through lines of text. The addition operator is also 
    redefined to create a new object and file with the data from 
    both previous files and then return this object.
    """

    def __init__(self, path):
        self.path = path 
        # атрибут, запоминающий позицию для чтения в файла
        self.current_position = 0 

        # если файл не существует, то он создается 
        # для избежания проблем с чтением
        if not os.path.exists(self.path):
            open(self.path, 'w').close()

    def __str__(self):
        return self.path

    def __add__(self, obj):
        # файла создается в папке Temp 
        # название всегда одинаковое, но можно заморочиться с уникальным
        new_path = os.path.join(tempfile.gettempdir(), 'new_file.txt')
        # создает новый объект с только что созданным путем 
        new_file = type(self)(new_path)
        new_file.write(self.read() + obj.read())
        
        return new_file

    def __iter__(self):
        return self

    def __next__(self):
        with open(self.path, 'r') as f:
            # ищет текущую позицию и начинает с нее
            f.seek(self.current_position)
            
            line = f.readline()
            # если достигнут конец файла, позиция в файле
            # возвращается к нулю
            if line == '':
                self.current_position = 0
                raise StopIteration('EOF')
            
            # перед выходом из текущей итерации 
            # сохраняется текущая позиция
            self.current_position = f.tell()    
            return line

    def write(self, content):
        with open(self.path, 'w') as f: 
            return f.write(content)

    def read(self):
        with open(self.path, 'r') as f:
            return f.read()


