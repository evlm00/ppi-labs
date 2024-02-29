import numpy as np
from matplotlib import pyplot as plt

def func_py(x: list[float]) -> list[float]:
    """
    Calculate function values for passed array of arguments
    """
    return [ t/(t**2 + 1) for t in x ]

def tabulate_py(a: float, b: float, n: int) -> dict[float]:
    x = [ a + x*(b - a)/n for x in range(n) ]
    y = func_py(x)
    return x, y

def tabulate_np(a: float, b: float, n: int) -> np.ndarray:
    x = np.linspace(a, b, n)
    y = x / (x**2 + 1)
    return x, y

def test_tabulation(f, a, b, n, axis):
    res = f(a, b, n)

    axis.plot(res[0], res[1])
    axis.grid()

def main():
    a, b, n = 0, 1, 1000

    fig, (ax1, ax2) = plt.subplots(2, 1)
    res = test_tabulation(tabulate_py, a, b, n, ax1)
    res = test_tabulation(tabulate_np, a, b, n, ax2)
    plt.show()


if __name__ == '__main__':
    main()