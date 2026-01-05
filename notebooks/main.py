import marimo

app = marimo.App()

@app.cell
def _():
    import numpy as np
    import pandas as pd
    return np, pd

@app.cell
def _(np):
    x = np.linspace(0, 10, 200)
    y = np.sin(x)
    y
    return x, y

@app.cell
def _(x, y):
    import matplotlib.pyplot as plt
    plt.plot(x, y)
    plt.title("Sine Wave")
    plt.show()
