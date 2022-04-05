from itertools import count
from nis import cat
from mock_data import catalog


def lower_than(price):
    return sum([1 if x['price'] < price else 0 for x in catalog])
    # return len([x for x in catalog if x['price'] < price])

print(lower_than(2))
print(lower_than(5))
print(lower_than(12))
print(lower_than(20))