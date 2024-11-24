# from decimal import Decimal
# from datetime import datetime
from datetime import datetime
from decimal import Decimal
from src.models import Car, CarStatus
from os import rename, remove


arr = ['aaaaaa', 'bbb', 'ccccccc', 'dddddd', 'eeee', 'fffffff']
with open('data.txt', 'w') as f:
    for i in arr:
        f.write(i.ljust(20) + '\n')

# line_to_del = 3
# with open('exp.txt', 'r') as rf:
#     with open('exp2.txt', 'w') as wf:
#         counter = 0
#         while True:
#             line = rf.readline()
#             if not line:
#                 break
#             counter += 1
#             if counter == line_to_del:
#                 continue
#             wf.write(line)
# remove('exp.txt')
# rename('exp2.txt', 'exp.txt')

# line_to_remove = 2
# cur_line = 3
# with open("data.txt", "r+") as f:
#     while True:
#         f.seek(cur_line * 22)
#         line = f.read(21)
#         if not line:
#             break
#         f.seek((cur_line - 1) * 22)
#         f.write(line)
#         cur_line += 1
#     f.seek((cur_line - 1) * 22)
#     f.truncate()

    with open("data.txt", "r") as f:
        f.seek(None * 20)
        val = f.read(20)