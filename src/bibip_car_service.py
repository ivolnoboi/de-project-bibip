from datetime import datetime
from decimal import Decimal
import os
from models import Car, CarFullInfo, CarStatus, Model, ModelSaleStats, Sale, DatabaseRecord as db


class CarService:

    def __find_car_by_vin(self, vin: str, root_dir_path: str) -> tuple[Car, int] | None:
        '''Find a car record by vin in a table and create a car object.\n
        Returns: car object and it's index in table cars.txt.'''
        line_number: int | None = None
        with open(root_dir_path + "/cars_index.txt", "r") as f:
            while True:
                line = f.readline()
                if not line:  # if it's end of file
                    return None
                if vin in line:  # if record is found
                    line_number = int(line.strip().split(';')[1])
                    break

        with open(root_dir_path + "/cars.txt", "r") as f:
            f.seek(line_number * (self.__record_len + self.__ws_size))
            val = f.read(self.__record_len)
            return Car.make_object(val), line_number
        return None

    def __find_model_by_id(self, model_id: str, root_dir_path: str) -> Model | None:
        line_number: int | None = None
        with open(root_dir_path + "/models_index.txt", "r") as f:
            while True:
                line = f.readline()
                if not line:  # if it's end of file
                    return None
                model_index, model_record_num = line.strip().split(';')
                if model_index == model_id:  # if it's found
                    line_number = int(model_record_num)
                    break

        with open(root_dir_path + "/models.txt", "r") as f:
            f.seek(line_number * (self.__record_len + self.__ws_size))
            val = f.read(self.__record_len)
            return Model.make_object(val)
        return None

    def __find_sale_by_car_vin(self, car_vin: str, root_dir_path: str) -> Sale | None:
        '''Find a sale record by vin in a table and create a car object.'''
        line_number: int | None = None
        with open(root_dir_path + "/sales_index.txt", "r") as f:
            while True:
                line = f.readline()
                if not line:  # if it's end of file
                    return None
                if car_vin in line:  # if record is found
                    line_number = int(line.strip().split(';')[1])
                    break

        with open(root_dir_path + "/sales.txt", "r") as f:
            f.seek(line_number * (self.__record_len + self.__ws_size))
            val = f.read(self.__record_len)
            return Sale.make_object(val)
        return None

    def __init__(self, root_directory_path: str) -> None:
        self.root_directory_path = root_directory_path
        # length of records in the database
        self.__record_len = 500
        self.__index_record_len = 30
        # size of whitespace (depends on operating system)
        self.__ws_size = 2 if os.name == 'nt' else 1
        # database initialization (creating tables)
        open(self.root_directory_path + "/models.txt", "a").close()
        open(self.root_directory_path + "/models_index.txt", 'a').close()
        open(self.root_directory_path + "/cars.txt", "a").close()
        open(self.root_directory_path + "/cars_index.txt", 'a').close()
        open(self.root_directory_path + "/sales.txt", "a").close()
        open(self.root_directory_path + "/sales_index.txt", 'a').close()

    # Task 1. Adding a model to the models table.
    def add_model(self, model: Model) -> Model:
        '''Add a model to the models table.'''
        result_str = model.make_record(self.__record_len)
        with open(self.root_directory_path + "/models.txt", "a") as f:
            f.write(result_str)

        with open(self.root_directory_path + "/models_index.txt", "r+") as f:
            arr = f.readlines()
            new_index = len(arr)
            temp_arr = [(int(i.strip().split(';')[0]), int(
                i.strip().split(';')[1])) for i in arr]
            temp_arr.append((model.id, new_index))
            temp_arr = sorted(temp_arr, key=lambda x: x[0])
            arr = [db.make_record(self.__index_record_len, i[0], i[1]) for i in temp_arr]
            f.seek(0)
            f.writelines(arr)

        return model

    # Task 1. Adding a car to the cars table.
    def add_car(self, car: Car) -> Car:
        '''Add a car to the cars table.'''
        result_str = car.make_record(self.__record_len)
        with open(self.root_directory_path + "/cars.txt", "a") as f:
            f.write(result_str)

        with open(self.root_directory_path + "/cars_index.txt", "r+") as f:
            arr = f.readlines()
            new_index = len(arr)
            arr.append(db.make_record(self.__index_record_len, car.vin, new_index))
            arr = sorted(arr)
            f.seek(0)
            f.writelines(arr)

        return car

    # Task 2. Save sale.
    def sell_car(self, sale: Sale) -> Car:
        '''Save a sale record to the sales table.'''
        result_str = sale.make_record(self.__record_len)
        with open(self.root_directory_path + "/sales.txt", "a") as f:
            f.write(result_str)

        with open(self.root_directory_path + "/sales_index.txt", "r+") as f:
            arr = f.readlines()
            new_index = len(arr)
            temp_arr = [i.strip().split(';') for i in arr]
            temp_arr.append([sale.car_vin, str(new_index)])
            temp_arr = sorted(temp_arr, key=lambda x: x[0])
            arr = [db.make_record(self.__index_record_len, i[0], i[1]) for i in temp_arr]
            f.seek(0)
            f.writelines(arr)

        car_index = self.__find_car_by_vin(sale.car_vin, self.root_directory_path)
        if car_index:
            car, index_num = car_index
            car.status = CarStatus('sold')
            with open(self.root_directory_path + "/cars.txt", "r+") as f:
                f.seek(index_num * (self.__record_len + self.__ws_size))
                line_to_write = car.make_record(self.__record_len)
                f.write(line_to_write)
        return car

    # Task 3. Cars available for sale.
    def get_cars(self, status: CarStatus) -> list[Car]:
        '''Get all the cars available for sale.'''
        available_cars = []
        with open(self.root_directory_path + "/cars.txt", 'r') as f:
            while True:
                line = f.readline()
                if not line:  # if it's end of file
                    break
                if status in line:
                    car = Car.make_object(line)
                    available_cars.append(car)
        return available_cars

    # Task 4. Detailed information.
    def get_car_info(self, vin: str) -> CarFullInfo | None:
        '''Get detailed information about a car by vin.'''
        sales_date: datetime | None = None
        sales_cost: Decimal | None = None

        # looking for a car
        car_index = self.__find_car_by_vin(vin, self.root_directory_path)
        if not car_index:  # if the car is not found
            return None

        car, _ = car_index
        # looking for a model name and brand
        model = self.__find_model_by_id(str(car.model), self.root_directory_path)
        if not model:  # if the model is not found
            return None

        # looking for a sale if exists
        if car.status == CarStatus.sold:
            sale = self.__find_sale_by_car_vin(vin, self.root_directory_path)
            if sale:
                sales_date = sale.sales_date
                sales_cost = sale.cost

        return CarFullInfo(
            vin=vin,
            car_model_name=model.name,
            car_model_brand=model.brand,
            price=car.price,
            date_start=car.date_start,
            status=car.status,
            sales_date=sales_date,
            sales_cost=sales_cost,
        )

    # Task 5. Updating key field.
    def update_vin(self, vin: str, new_vin: str) -> Car:
        '''Update a vin number.'''
        # find a car
        car_index = self.__find_car_by_vin(vin, self.root_directory_path)
        if car_index:
            car, car_line = car_index

        # recalculating indexes
        with open(self.root_directory_path + "/cars_index.txt", "r+") as f:
            arr = f.readlines()
            index, _ = [(i, v) for i, v in enumerate(arr) if f'{car.vin};{car_line}' in v][0]
            arr[index] = db.make_record(self.__index_record_len, new_vin, car_line)
            arr = sorted(arr)
            f.seek(0)
            f.writelines(arr)

        with open(self.root_directory_path + "/cars.txt", "r+") as f:
            f.seek(car_line * (self.__record_len + self.__ws_size))
            car.vin = new_vin
            line_to_write = car.make_record(self.__record_len)
            f.write(line_to_write)
        return car

    # Task 6. Removing sale.
    def revert_sale(self, sales_number: str) -> Car:
        '''Remove a sale record from sales.txt.'''
        # removing record from index file and find the number of the
        # line in sales.txt (line_number)
        line_number = -1
        with open(self.root_directory_path + "/sales_index.txt", "r+") as f:
            arr = f.readlines()
            vin = sales_number.split('#')[1]
            # sale_ind is the number of the line to remove in sales_index.txt
            sale_ind, sale_line = [(i, v)
                                   for i, v in enumerate(arr) if vin in v][0]
            # line_number is the number of the line to remove in sale.txt
            line_number = int(sale_line.strip().split(';')[1])
            # writing to the file
            first_arr = arr[:sale_ind]
            second_arr = []
            # recalculating indexes
            for elem in arr[sale_ind + 1:]:
                vin, ind = elem.strip().split(';')
                second_arr.append(db.make_record(self.__index_record_len, vin, int(ind) - 1))
            arr = first_arr + second_arr
            f.seek(0)
            f.writelines(arr)
            f.truncate()

        # removing a record from sales.txt
        cur_line = line_number + 1
        with open(self.root_directory_path + "/sales.txt", "r+") as f:
            while True:
                f.seek(cur_line * (self.__record_len + self.__ws_size))
                line = f.read(self.__record_len)
                if not line:
                    break
                f.seek((cur_line - 1) * (self.__record_len + self.__ws_size))
                f.write(line)
                cur_line += 1
            f.seek((cur_line - 1) * (self.__record_len + self.__ws_size))
            f.truncate()

        # finding a car and changing status to available
        car_index = self.__find_car_by_vin(vin, self.root_directory_path)
        if car_index:
            car, index_num = car_index
            car.status = CarStatus('available')
            with open(self.root_directory_path + "/cars.txt", "r+") as f:
                f.seek(index_num * (self.__record_len + self.__ws_size))
                line_to_write = car.make_record(self.__record_len)
                f.write(line_to_write)
        return car

    # Task 7. Top 3 best selling models.
    def top_models_by_sales(self) -> list[ModelSaleStats]:
        '''Find top 3 models by amount of sales.'''
        model_sales_dict: dict[str, int] = {}

        # getting all sold cars and adding models and their sales count
        # to the dictionary
        with open(self.root_directory_path + "/sales.txt", "r") as f:
            while True:
                line = f.readline()
                if not line:
                    break
                # extracting vin number
                sale_line = line.strip().split(';')
                car_vin = sale_line[1]

                # looking for a car
                car_index = self.__find_car_by_vin(car_vin, self.root_directory_path)
                if car_index:
                    car_model = str(car_index[0].model)
                    # adding to the dictionary
                    model_sales_dict[car_model] = model_sales_dict[car_model] + \
                        1 if car_model in model_sales_dict else 1

        # sorting models by count of sales
        top_3_models = sorted(model_sales_dict.items(),
                              key=lambda x: x[1], reverse=True)[:3]

        model_sale_stats: list[ModelSaleStats] = []

        # joining with the models table to get name and brand of a model
        for model_id, count in top_3_models:
            line_number = -1
            with open(self.root_directory_path + "/models_index.txt", "r") as f:
                while True:
                    line = f.readline()
                    if not line:
                        break
                    # model_line is the number of the line in models.txt
                    model_index, model_line = [i for i in line.strip().split(';')]
                    if model_index == model_id:
                        line_number = int(model_line)
                        break

            with open(self.root_directory_path + "/models.txt", "r") as f:
                f.seek(line_number * (self.__record_len + self.__ws_size))
                val = f.read(self.__record_len)
                index, model_name, model_brand = val.strip().split(';')
                model_sale_stats.append(
                    ModelSaleStats(
                        car_model_name=model_name,
                        brand=model_brand,
                        sales_number=count
                    )
                )
        print('model_sale_stats = ', model_sale_stats)

        return model_sale_stats
