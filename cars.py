"""
The script that receives the input csv-table with cars 
and the output list of the objects-cars. Each type of car 
has its own required attributes and methods. In the case 
of absence of some required attributes or incorrect data in the table, 
the row of the table is skipped and the object is not created.
"""

import csv
import os.path
import sys


class CarBase:
    """Base class with common attributes and method"""

    def __init__(self, brand, photo_file_name, carrying):
        self.brand = brand 
        self.photo_file_name = photo_file_name
        self.carrying = float(carrying)

    def get_photo_file_ext(self):
        """Returns the vehicle photo extension"""
        _, ext = os.path.splitext(self.photo_file_name)
        return ext



class Car(CarBase):
    """Passenger car class"""
    
    def __init__(self, brand, passenger_seats_count, photo_file_name, carrying):
        
        self.car_type = "car"
        
        # если аргументы не равны пустым строкам - инициализация,
        # в ином случае бросается исключение; в других классах аналогичный принцип
        if passenger_seats_count and brand and carrying and photo_file_name: 
            self.passenger_seats_count = int(passenger_seats_count)
            super().__init__(brand, photo_file_name, carrying)
        else:
            raise AttributeError



class Truck(CarBase):
    """Truck class"""

    def __init__(self, brand, photo_file_name, body_whl, carrying):
        
        self.car_type = "truck"
        
        if body_whl and brand and photo_file_name and carrying:
            # раскладываем строку размеров на отдельные атрибуты длины
            # высоты и ширины, из которых вычисляется объем в методе класса
            body_lst = body_whl.split('x')
            self.body_length, self.body_width, self.body_height = map(float, body_lst)
            super().__init__(brand, photo_file_name, carrying)
        elif brand and photo_file_name and carrying:
            self.body_length, self.body_width, self.body_height = .0, .0, .0
            super().__init__(brand, photo_file_name, carrying)
        else:
            raise AttributeError


    def get_body_volume(self):
        """Returns the volume of the cargo part in cubic meters"""
        return self.body_length * self.body_height * self.body_width



class SpecMachine(CarBase):
    """Special equipment class"""

    def __init__(self, brand, photo_file_name, carrying, extra):
        
        self.car_type = "spec_machine"
        
        if extra and brand and carrying and photo_file_name:
            self.extra = extra
            super().__init__(brand, photo_file_name, carrying)
        else:
            raise AttributeError
            



def get_car_list(csv_filename):
    """Returns from the source csv-table a list of car objects"""
    
    # индексирование в будущем списке, для упрощенного чтения
    indx_car_type = 0
    indx_brand = 1
    indx_seats_count = 2
    indx_photo_name = 3
    indx_body_whl = 4
    indx_carrying = 5
    indx_extra = 6

    # открывает файл без контекстного менеджера, т. к.
    # это увеличает глубину отступов
    csv_fd = open(csv_filename)
    reader = csv.reader(csv_fd, delimiter=';')
    
    #пропускаем заголовок csv
    next(reader)
    
    # будущий список объектов
    car_list = []
    
    # пробегаемся по созданному csv-объекту
    for row in reader:
        car = None
        
        try:
            # проверяем каждую строку на принадлежность на соотвествие имеющимся классам
            if row[indx_car_type] == "car":
                car = Car(row[indx_brand], row[indx_seats_count], row[indx_photo_name], row[indx_carrying])
            
            elif row[indx_car_type] == "truck":
                car = Truck(row[indx_brand], row[indx_photo_name], row[indx_body_whl], row[indx_carrying])
            
            elif row[indx_car_type] == "spec_machine":
                car = SpecMachine(row[indx_brand], row[indx_photo_name], row[indx_carrying], row[indx_extra])
            
            # в случае пустой строки пропускаем ее
            else:
                continue
            
            car_list.append(car)
        
        # пропуск строки, если числовые данные некорректны или 
        # инициализатор класса поднял AttributeError из-за наличия атрибутов в виде пустых строк
        except (IndexError, AttributeError, ValueError):
            continue
    
    csv_fd.close()

    return car_list

if __name__ == '__main__':
    get_car_list(sys.argv[1])
