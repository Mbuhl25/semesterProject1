import time

iterations = 1000000000  # 1 milliard, 100 mio, 10 mio iterationer
sum = 0

start = time.perf_counter()  # starttid i sekunder med høj opløsning

for i in range(iterations):
    sum += i

end = time.perf_counter()  # sluttid
elapsed = end - start

print("Elapsed time:", elapsed, "seconds")
print("Sum:", sum)