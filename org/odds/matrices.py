import numpy as np
import scipy.linalg as lin
import matplotlib.pyplot as plt
from kivy.utils import interpolate


def do_one():
    A = np.array([[1, 2], [3, 4]])
    print(A)

    b = np.array([3, 17])
    print(b)

    x = lin.solve(A, b)
    print(x)

    np.allclose(A @ x, b)

def do_matrices():
    A1 = np.random.random((1000, 1000))
    print(A1[:10])
    b1 = np.random.random(1000)
    print(b1[:10])

    try:
        solution = lin.solve(A1, b1)
        print(solution[:10])
    except lin.LinAlgError:
        print("matrix is singular or ill-conditioned")
        return

    # plot it
    plt.figure(figsize=(6, 6))
    plt.imshow(A1, cmap='viridis', interpolation='nearest')
    plt.colorbar(label="matrix values")
    plt.title("1000 x 1000 random matrix A")
    plt.show()

    # plot the solution vector
    plt.figure(figsize=(8, 4))
    plt.bar(range(len(solution)), solution, color='blue')
    plt.xlabel('index')
    plt.ylabel('solution values')
    plt.title('solution vector x')
    plt.show()

def do_matrices2():
    A = np.random.rand(5, 5)
    b = np.random.rand(5)
    try:
        x = lin.solve(A, b)
    except lin.LinAlgError:
        print("singular or unsolvable matrix")
        x = None

    fig, ax = plt.subplots(figsize=(8, 6))

    cax = ax.imshow(A, cmap='coolwarm', interpolation='nearest')
    plt.colorbar(cax, ax=ax, label="matrix values")
    ax.set_title("matrix and solution comparison")
    ax.set_xlabel("columns")
    ax.set_ylabel("rows")

    ax2 = ax.twinx()

    indices = np.arange(len(b))

    if x is not None:
        ax2.plot(indices, b, marker='o')

def main():
    plt.style.use('ggplot')

    do_matrices2()

if __name__ == "__main__":
    main()