from datetime import datetime
from decimal import Decimal
from models import Car, CarFullInfo, CarStatus, Model, ModelSaleStats, Sale


def make_car_record(car: Car) -> str:
    '''Make a string from a car object for inserting into a table.'''
    return f'{car.vin};{car.model};{car.price};{car.date_start};{car.status}'.ljust(500) + '\n'


def make_car_object(record: str) -> Car:
    '''Make a car object from a record from a table.'''
    car = record.strip().split(';')
    return Car(
        vin=car[0],
        model=int(car[1]),
        price=Decimal(car[2]),
        date_start=datetime.strptime(car[3], '%Y-%m-%d %X'),
        status=CarStatus(car[4])
    )


def make_model_record(model: Model) -> str:
    '''Make a string from a model object for inserting into a table.'''
    return f'{model.id};{model.name};{model.brand}'.ljust(500) + '\n'


def make_model_object(record: str) -> Model:
    '''Make a model object from a record from a table.'''
    model = record.strip().split(';')
    return Model(
        id=int(model[0]),
        name=model[1],
        brand=model[2]
    )


def make_sale_object(record: str) -> Sale:
    '''Make a sale object from a table's record.'''
    sale = record.strip().split(';')
    return Sale(
        sales_number=sale[0],
        car_vin=sale[1],
        sales_date=datetime.strptime(sale[2], '%Y-%m-%d %X'),
        cost=Decimal(sale[3])
    )


def find_car_by_vin(vin: str, root_dir_path: str) -> Car | None:
    '''Find a car record by vin in a table and create a car object.'''
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
        f.seek(line_number * 502)
        val = f.read(501)
        return make_car_object(val)
    return None


def find_model_by_id(model_id: str, root_dir_path: str) -> Model | None:
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
        f.seek(line_number * 502)
        val = f.read(501)
        return make_model_object(val)
    return None


def find_sale_by_car_vin(car_vin: str, root_dir_path: str) -> Sale | None:
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
        f.seek(line_number * 502)
        val = f.read(501)
        return make_sale_object(val)
    return None


class CarService:
    def __init__(self, root_directory_path: str) -> None:
        self.root_directory_path = root_directory_path

    # Задание 1. Сохранение автомобилей и моделей
    def add_model(self, model: Model) -> Model:
        result_str = make_model_record(model)
        with open(self.root_directory_path + "/models.txt", "a") as f:
            f.write(result_str)

        f = open(self.root_directory_path + "/models_index.txt", 'a')
        f.close()
        with open(self.root_directory_path + "/models_index.txt", "r+") as f:
            arr = f.readlines()
            new_index = len(arr)
            temp_arr = [[int(i.strip().split(';')[0]), int(i.strip().split(';')[1])] for i in arr]
            temp_arr.append([model.id, new_index])
            temp_arr = sorted(temp_arr, key=lambda x: x[0])
            arr = [f'{i[0]};{i[1]}'.ljust(30) + '\n' for i in temp_arr]
            f.seek(0)
            f.writelines(arr)

        return model

    # Задание 1. Сохранение автомобилей и моделей
    def add_car(self, car: Car) -> Car:
        result_str = make_car_record(car)
        with open(self.root_directory_path + "/cars.txt", "a") as f:
            f.write(result_str)

        f = open(self.root_directory_path + "/cars_index.txt", 'a')
        f.close()
        with open(self.root_directory_path + "/cars_index.txt", "r+") as f:
            arr = f.readlines()
            new_index = len(arr)
            arr.append(f'{car.vin};{new_index}'.ljust(30) + '\n')
            arr = sorted(arr)
            f.seek(0)
            f.writelines(arr)

        return car

    # Задание 2. Сохранение продаж.
    def sell_car(self, sale: Sale) -> Car:
        result_str = f'{sale.sales_number};{sale.car_vin};{sale.sales_date};{sale.cost}'.ljust(500) + '\n'
        with open(self.root_directory_path + "/sales.txt", "a") as f:
            f.write(result_str)
    
        f = open(self.root_directory_path + "/sales_index.txt", 'a')
        f.close()
        with open(self.root_directory_path + "/sales_index.txt", "r+") as f:
            arr = f.readlines()
            new_index = len(arr)
            temp_arr = [i.strip().split(';') for i in arr]
            temp_arr.append([sale.car_vin, str(new_index)])
            temp_arr = sorted(temp_arr, key=lambda x: x[0])
            arr = [f'{i[0]};{i[1]}'.ljust(30) + '\n' for i in temp_arr]
            f.seek(0)
            f.writelines(arr)
        
        # find a car
        line_number = -1
        with open(self.root_directory_path + "/cars_index.txt", "r+") as f:
            arr = f.readlines()
            temp_arr2 = [i for i in arr if sale.car_vin in i]
            line_number = int(temp_arr2[0].strip().split(';')[1])
        
        final_car = Car(vin='', model=-1, price=Decimal('0'), date_start=datetime.now(), status=CarStatus.sold)
        with open(self.root_directory_path + "/cars.txt", "r+") as f:
            f.seek(line_number * 501)
            val = f.read(500)
            car = val.strip().split(';')
            final_car = Car(
                vin=car[0],
                model=int(car[1]),
                price=Decimal(car[2]),
                date_start=datetime.strptime(car[3], '%Y-%m-%d %X'),
                status=CarStatus.sold,
            )
            f.seek(line_number * 502)
            line_to_write = f'{final_car.vin};{final_car.model};{final_car.price};{final_car.date_start};{final_car.status}'.ljust(500) + '\n'
            f.write(line_to_write)
        return final_car

    # Task 3. Cars available for sale.
    def get_cars(self, status: CarStatus) -> list[Car]:
        available_cars = []
        with open(self.root_directory_path + "/cars.txt", 'r') as f:
            while True:
                line = f.readline()
                if not line:  # if it's end of file
                    break
                if status in line:
                    car = make_car_object(line)
                    available_cars.append(car)
        return available_cars

    # Task 4. Detailed information.
    def get_car_info(self, vin: str) -> CarFullInfo | None:
        '''Get detailed information about a car by vin.'''
        sales_date: datetime | None = None
        sales_cost: Decimal | None = None

        # looking for a car
        car = find_car_by_vin(vin, self.root_directory_path)
        if not car:  # if the car is not found
            return None

        # looking for a model name and brand
        model = find_model_by_id(str(car.model), self.root_directory_path)
        if not model:  # if the model is not found
            return None

        # looking for a sale if exists
        if car.status == CarStatus.sold:
            sale = find_sale_by_car_vin(vin, self.root_directory_path)
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

    # Задание 5. Обновление ключевого поля
    def update_vin(self, vin: str, new_vin: str) -> Car:
        # find a car
        line_number = -1
        with open(self.root_directory_path + "/cars_index.txt", "r+") as f:
            arr = f.readlines()
            temp_arr2 = [(i, v) for i, v in enumerate(arr) if vin in v]
            arr_index = temp_arr2[0][0] # what if out of range
            line_number = int(temp_arr2[0][1].strip().split(';')[1])
            # writing to file
            arr[arr_index] = f'{new_vin};{line_number}'.ljust(30) + '\n'
            arr = sorted(arr)
            f.seek(0)
            f.writelines(arr)
        
        final_car = Car(vin='', model=-1, price=Decimal('0'), date_start=datetime.now(), status=CarStatus.sold)
        with open(self.root_directory_path + "/cars.txt", "r+") as f:
            f.seek(line_number * 501)
            val = f.read(500)
            car = val.strip().split(';')
            final_car = Car(
                vin=new_vin,
                model=int(car[1]),
                price=Decimal(car[2]),
                date_start=datetime.strptime(car[3], '%Y-%m-%d %X'),
                status=CarStatus(car[4]),
            )
            f.seek(line_number * 502)
            line_to_write = f'{final_car.vin};{final_car.model};{final_car.price};{final_car.date_start};{final_car.status}'.ljust(500) + '\n'
            f.write(line_to_write)
        return final_car

    # Задание 6. Удаление продажи
    def revert_sale(self, sales_number: str) -> Car:
        # removing record from index file and find a line in sales.txt (line_number)
        line_number = -1
        with open(self.root_directory_path + "/sales_index.txt", "r+") as f:
            arr = f.readlines()
            vin = sales_number.split('#')[1]
            # sale_ind is a number of line to remove in sales_index.txt
            sale_ind, sale_line = [(i, v) for i, v in enumerate(arr) if vin in v][0]
            # line_number is a number of line to remove in sale.txt
            line_number = int(sale_line.strip().split(';')[1])
            # writing to file
            first_arr = arr[:sale_ind]
            second_arr = []
            # recalculating indexes
            for elem in arr[sale_ind + 1:]:
                vin, ind = elem.strip().split(';')
                second_arr.append(f'{vin};{int(ind) - 1}'.ljust(30) + '\n')
            arr = first_arr + second_arr
            f.seek(0)
            f.writelines(arr)
            f.truncate()
        
        # removing a record from sales.txt
        cur_line = line_number + 1
        with open(self.root_directory_path + "/sales.txt", "r+") as f:
            while True:
                f.seek(cur_line * 502)
                line = f.read(501)
                if not line:
                    break
                f.seek((cur_line - 1) * 502)
                f.write(line)
                cur_line += 1
            f.seek((cur_line - 1) * 502)
            f.truncate()

        # finding a line number of a car
        line_number = -1
        vin = sales_number.split('#')[1]
        with open(self.root_directory_path + "/cars_index.txt", "r+") as f:
            arr = f.readlines()
            temp_arr2 = [(i, v) for i, v in enumerate(arr) if vin in v]
            line_number = int(temp_arr2[0][1].strip().split(';')[1])
        
        with open(self.root_directory_path + "/cars.txt", "r+") as f:
            f.seek(line_number * 502)
            val = f.read(501)
            car = val.strip().split(';')
            final_car = Car(
                vin=car[0],
                model=int(car[1]),
                price=Decimal(car[2]),
                date_start=datetime.strptime(car[3], '%Y-%m-%d %X'),
                status=CarStatus(car[4]),
            )
            f.seek(line_number * 502)
            line_to_write = f'{final_car.vin};{final_car.model};{final_car.price};{final_car.date_start};{'available'}'.ljust(500) + '\n'
            f.write(line_to_write)
        return final_car

    # Задание 7. Самые продаваемые модели
    def top_models_by_sales(self) -> list[ModelSaleStats]:
        model_sales_dict: dict[str, int] = {}
        with open(self.root_directory_path + "/sales.txt", "r") as f:
            while True:
                line = f.readline()
                if not line:
                    break
                # write function get_sale_from_table
                sale_line = line.strip().split(';')
                car_vin = sale_line[1]
        
                # use function get_car_by_vin
                # find a car
                line_number = -1
                with open(self.root_directory_path + "/cars_index.txt", "r") as f_ci:
                    arr = f_ci.readlines()
                    temp_arr2 = [i for i in arr if car_vin in i]
                    line_number = int(temp_arr2[0].strip().split(';')[1])
        
                with open(self.root_directory_path + "/cars.txt", "r+") as f_c:
                    f_c.seek(line_number * 502)
                    val = f_c.read(501)
                    model = val.strip().split(';')[1]
                    # adding to the dictionary
                    model_sales_dict[model] = model_sales_dict[model] + 1 if model in model_sales_dict else 1
        
        print('model_sales_dict = ', model_sales_dict)
        top_3_models = sorted(model_sales_dict.items(), key=lambda x: x[1], reverse=True)[:3]
        model_sale_stats: list[ModelSaleStats] = []
        print('top_3_models = ', top_3_models)
        for model_id, count in top_3_models:
            line_number = -1
            with open(self.root_directory_path + "/models_index.txt", "r") as f:
                while True:
                    line = f.readline()
                    if not line:
                        break
                    # model_line is a number of line in models.txt
                    model_index, model_line = [i for i in line.strip().split(';')]
                    if model_index == model_id:
                        line_number = int(model_line)
                        break
                print(line_number)

            with open(self.root_directory_path + "/models.txt", "r") as f:
                f.seek(line_number * 502)
                val = f.read(501)
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
