# A script with no function at all - rule 2 fires.

total = 0
for n in range(1, 11):
    if n % 2 == 0:
        total = total + n

print(total)
