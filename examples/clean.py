# A correct solution - every rule passes.

def sum_even_digits(n):
    total = 0
    while n > 0:
        n, r = divmod(n, 10)
        if r % 2 == 0:
            total = total + r
    return total


def mean(nums):
    # fixed decimals belong in an f-string, not in round()
    return f"{sum(nums) / len(nums):.2f}"


class Rectangle:
    def __init__(self, w, h):
        self.w = w
        self.h = h

    def area(self):
        return self.w * self.h
