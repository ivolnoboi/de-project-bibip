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
        raise NotImplementedError

    # Задание 3. Доступные к продаже
    def get_cars(self, status: CarStatus) -> list[Car]:
        raise NotImplementedError

    # Задание 4. Детальная информация
    def get_car_info(self, vin: str) -> CarFullInfo | None:
        raise NotImplementedError

    # Задание 5. Обновление ключевого поля
    def update_vin(self, vin: str, new_vin: str) -> Car:
        raise NotImplementedError

    # Задание 6. Удаление продажи
    def revert_sale(self, sales_number: str) -> Car:
        raise NotImplementedError

    # Задание 7. Самые продаваемые модели
    def top_models_by_sales(self) -> list[ModelSaleStats]:
        raise NotImplementedError
