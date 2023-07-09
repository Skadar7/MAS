import matplotlib.pyplot as plt
import numpy as np


def func(x1, x2):
    return 10 * x1 ** 2 + 3 * x1 * x2 + x2 ** 2 + 10 * x2


def visualize(history):
    x1 = np.linspace(-10, 10, 100)
    x2 = np.linspace(-10, 10, 100)

    X1, X2 = np.meshgrid(x1, x2)

    Z = func(X1, X2)

    fig = plt.figure(figsize=plt.figaspect(0.5))
    ax = fig.add_subplot(1, 2, 1)
    _, _, Z_P = zip(*history)
    ax.plot(Z_P)
    ax.set_title('Optimization process')
    ax.set_ylabel('f(X)')
    ax.set_xlabel('X')
    ax = fig.add_subplot(1, 2, 2, projection='3d')
    ax.plot_surface(X1, X2, Z, rstride=1, cstride=1, cmap='jet', edgecolor='none')
    x1_p, x2_p, z_p = zip(*history)
    ax.plot(x1_p, x2_p, z_p, color='red')
    ax.scatter(x1_p, x2_p, z_p, color='black')
    ax.set_title('3d plot')
    plt.show()