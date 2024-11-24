from datetime import datetime
from decimal import Decimal
from models import Car, CarFullInfo, CarStatus, Model, ModelSaleStats, Sale


class CarService:
    def __init__(self, root_directory_path: str) -> None:
        self.root_directory_path = root_directory_path

    # Задание 1. Сохранение автомобилей и моделей
    def add_model(self, model: Model) -> Model:
        result_str = f'{model.id};{model.name};{model.brand}'.ljust(500) + '\n'
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
        result_str = f'{car.vin};{car.model};{car.price};{car.date_start};{car.status}'.ljust(500) + '\n'
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

    # Задание 3. Доступные к продаже
    def get_cars(self, status: CarStatus) -> list[Car]:
        available_cars = []
        with open(self.root_directory_path + "/cars.txt", 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                if status in line:
                    car_params = line.strip().split(';')
                    car = Car(
                        vin=car_params[0],
                        model=int(car_params[1]),
                        price=Decimal(car_params[2]),
                        date_start=datetime.strptime(car_params[3], '%Y-%m-%d %X'),
                        status=status,
                    )
                    available_cars.append(car)
        return available_cars

    # Задание 4. Детальная информация
    def get_car_info(self, vin: str) -> CarFullInfo | None:
        model_name: str = None
        model_brand: str = None
        price: Decimal = None
        date_start: datetime = None
        status: CarStatus = None
        sales_date: datetime = None
        sales_cost: Decimal = None
        model: int = None
        # find a car
        line_number = -1
        with open(self.root_directory_path + "/cars_index.txt", "r+") as f:
            arr = f.readlines()
            temp_arr2 = [i for i in arr if vin in i]
            if len(temp_arr2) == 0:
                return None
            line_number = int(temp_arr2[0].strip().split(';')[1])
        
        with open(self.root_directory_path + "/cars.txt", "r") as f:
            f.seek(line_number * 501)
            val = f.read(500)
            car = val.strip().split(';')
            model=int(car[1])
            price=Decimal(car[2])
            date_start=datetime.strptime(car[3], '%Y-%m-%d %X')
            status=car[4]

        line_number = -1
        with open(self.root_directory_path + "/models_index.txt", "r") as f:
            while True:
                line = f.readline()
                if not line:
                    break
                model_index, line_number = [int(i) for i in line.strip().split(';')]
                if model_index == model:
                    break

        with open(self.root_directory_path + "/models.txt", "r") as f:
            f.seek(line_number * 501)
            val = f.read(500)
            index, model_name, model_brand = val.strip().split(';')
        
        if status == CarStatus.sold:
            line_number = -1
            with open(self.root_directory_path + "/sales_index.txt", "r") as f:
                arr = f.readlines()
                temp_arr2 = [i for i in arr if vin in i]
                line_number = int(temp_arr2[0].strip().split(';')[1])
        
            with open(self.root_directory_path + "/sales.txt", "r") as f:
                f.seek(line_number * 501)
                val = f.read(500)
                sale = val.strip().split(';')
                sales_date = datetime.strptime(sale[2], '%Y-%m-%d %X')
                sales_cost = Decimal(sale[3])

        return CarFullInfo(
            vin=vin,
            car_model_name=model_name,
            car_model_brand=model_brand,
            price=price,
            date_start=date_start,
            status=status,
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
