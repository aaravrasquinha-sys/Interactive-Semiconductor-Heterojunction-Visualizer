import plotly.graph_objects as go
import numpy as np
from dash import Dash, dcc, html, Input, Output

# Initialize the Dash app
app = Dash(__name__)

# Generate x-axis values for two regions of the heterojunction
x_values_region1 = np.linspace(0, 1, 100)
x_values_region2 = np.linspace(1, 2, 100)

# Smooth transition function
def smooth_transition(x, y_start, y_end):
    """Creates a smooth transition between two points with a slight curve."""
    return y_start + (y_end - y_start) * (1 - np.cos(np.pi * x)) / 2

# Dash layout
app.layout = html.Div([
    html.Div([
        html.H2("Heterojunction Energy Band Diagram"),
        html.Label("Voltage Level (V)"),
        dcc.Slider(id='voltage-slider', min=0, max=2, step=0.1, value=1,
                   marks={i: f'{i}V' for i in np.arange(0, 2.1, 0.5)}),
        html.Label("Doping Concentration"),
        dcc.Slider(id='doping-slider', min=1, max=3, step=0.1, value=1.5,
                   marks={i: f'{i}' for i in np.arange(1, 3.1, 0.5)}),
    ], style={'width': '20%', 'display': 'inline-block', 'padding': '20px'}),

    html.Div([
        dcc.Graph(id='band-diagram')
    ], style={'width': '75%', 'display': 'inline-block', 'padding': '20px'})
])

# Callback to update the graph based on the slider values
@app.callback(
    Output('band-diagram', 'figure'),
    [Input('voltage-slider', 'value'),
     Input('doping-slider', 'value')]
)
def update_graph(voltage, doping):
    # Adjusted conduction and valence bands with doping and voltage
    conduction_band_region1 = smooth_transition(x_values_region1, 1.5, 1.5 + doping * 0.2 + voltage * 0.1)
    conduction_band_region2 = smooth_transition(x_values_region2 - 1, 1.5 + doping * 0.2 + voltage * 0.1, 1.8 + doping * 0.2 + voltage * 0.1)

    valence_band_region1 = smooth_transition(x_values_region1, 0.5, 0.5 + doping * 0.1 + voltage * 0.05)
    valence_band_region2 = smooth_transition(x_values_region2 - 1, 0.5 + doping * 0.1 + voltage * 0.05, 0.7 + doping * 0.1 + voltage * 0.05)

    fermi_level_region1 = np.ones_like(x_values_region1) * (1.15 + voltage * 0.05)
    fermi_level_region2 = np.ones_like(x_values_region2) * (1.25 + voltage * 0.05)

    # Create the figure
    fig = go.Figure()

    # Plot for conduction band
    fig.add_trace(go.Scatter(x=x_values_region1, y=conduction_band_region1,
                             mode='lines', name='Conduction Band (Region 1)', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=x_values_region2, y=conduction_band_region2,
                             mode='lines', name='Conduction Band (Region 2)', line=dict(color='blue')))

    # Plot for valence band
    fig.add_trace(go.Scatter(x=x_values_region1, y=valence_band_region1,
                             mode='lines', name='Valence Band (Region 1)', line=dict(color='red')))
    fig.add_trace(go.Scatter(x=x_values_region2, y=valence_band_region2,
                             mode='lines', name='Valence Band (Region 2)', line=dict(color='red')))

    # Plot for Fermi level
    fig.add_trace(go.Scatter(x=np.concatenate([x_values_region1, x_values_region2]),
                             y=np.concatenate([fermi_level_region1, fermi_level_region2]),
                             mode='lines', name='Fermi Level', line=dict(color='green', dash='dash')))

    # Layout adjustments
    fig.update_layout(
        title="Energy Band Diagram with Interactive Controls",
        xaxis_title="Position",
        yaxis_title="Energy (eV)",
        legend=dict(x=0.7, y=1.0),
        xaxis=dict(range=[0, 2]),
        yaxis=dict(range=[0, 3])
    )

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
