import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot(data: pd.DataFrame):
    # Extract data
    T = data['T']
    K = data['strike']
    IV = data['IV']

    # Setup plot
    fig = plt.figure(figsize = (14, 9))
    ax = fig.add_subplot(111, projection = '3d')
    surface = ax.plot_trisurf(T, K, IV, cmap = plt.cm.viridis, linewidth = 0.1)
    fig.colorbar(surface, shrink = 0.5, aspect = 5)

    ax.set_xlabel("Time to Expiration in Years")
    ax.set_ylabel("Strike Price")
    ax.set_zlabel("Implied Volatility")

    return fig
