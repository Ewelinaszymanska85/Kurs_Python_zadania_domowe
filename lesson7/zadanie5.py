from functools import reduce


liczby = [ 1, 2, 3, 4, 5] 

iloczyn = reduce(lambda x, y: x * y, liczby) 

print(iloczyn) 