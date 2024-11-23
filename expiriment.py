from decimal import Decimal
from datetime import datetime
from src.models import Car, CarStatus


def create_line(car: Car) -> str:
    result_str = f'{car.vin};{car.model};{car.price};{car.date_start};{car.status}'.ljust(500) + '\n'
    with open("data.txt", "a") as f:
        f.write(result_str)
    
    with open("index.txt", "r+") as f:
        arr = f.readlines()
        new_index = len(arr)
        arr.append(f'{car.vin};{new_index}'.ljust(30) + '\n')
        arr = sorted(arr)
        f.seek(0)
        f.writelines(arr)
        print(arr)


    print(result_str)
    return result_str


create_line(Car(
            vin="5N1AR2MM4DC605882",
            model=4,
            price=Decimal("3200"),
            date_start=datetime(2024, 7, 15),
            status=CarStatus.available,
        ))


# arr = [1,2,3,4,5,7,8,9]
# i = 0
# number = 6
# while number > arr[i] and i < len(arr):
#     i += 1
# print(i)
# arr.insert(i, number)
# print(arr)

arr = [['aaa', 3], ['ccc', 2], ['bbb', 1]]
print(sorted(arr, key=lambda x: x[1]))
print(int('56'))
