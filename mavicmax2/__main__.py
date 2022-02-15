import sys

from mavicmax2.mavicmax2 import fib

if __name__ == "__main__":
    n = int(sys.argv[1])
    print(fib(n))
