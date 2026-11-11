# A deliberately broken solution - nine of the ten rules fire here.
# Rule 2 needs a file with no function at all; see no_function.py.


def um_even_digits(times):
    total = 0
    times = int(input())          # rule 3 (parameter overwritten) + rule 4 (input)
    while times > 0:
        times, r = divmod(times, 10)
        if r % 2 == 0:
            total = r + total
    print("the answer is", total)  # rule 6 (stray print) + rule 7 (print with commas)
    return total


def average(nums, weights):        # rule 5: weights is never read
    return sum(nums) / len(nums)


def mean(nums):
    return round(sum(nums) / len(nums), 2)   # rule 8: trailing zeros are lost


class Counter:
    def __init__(self, name):
        name = name                # rule 10: self.name is never assigned
        return name                # rule 9: __init__ must return None
