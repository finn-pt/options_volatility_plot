import pandas as pd
import plotly.graph_objects as plt

def plot(data: pd.DataFrame):
    """
    Generates a 3d plot compatible with streamlit

    Paramters:
        data (pd.DataFrame) - the data to be plotted

    Returns: fig - a 3d plot which can be interacted with in streamlit
    """
    fig = plt.Figure(
        data = [plt.Mesh3d(x = data["T"], y = data["strike"], 
        z = data["IV"], opacity = 0.85, intensity = data["IV"], 
        colorscale = "Viridis")]
        )

    fig.update_layout(
        scene=dict(
            xaxis_title = "Time to Expiration (Years)",
            yaxis_title = "Strike Price ($)",
            zaxis_title = "Implied Volatility"
        )
    )
    return fig
