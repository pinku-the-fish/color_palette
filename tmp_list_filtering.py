import numpy as np
lst = [1, 2, 3, 4, 5, 6, 7, 8]
res = list(filter(lambda x: x % 3 == 0, lst))

print(res)
print(all(np.array(lst) < 10))