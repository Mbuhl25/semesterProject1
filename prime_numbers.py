def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

def get_primes(n):
    primes = []
    for i in range(2, n + 1):  # ← added missing colon here
        if is_prime(i):
            primes.append(i)
    return primes

if __name__ == "__main__":
    n = int(input("Find primes up to: "))
    print(get_primes(n))
