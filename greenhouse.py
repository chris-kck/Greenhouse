
import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html

import plotly
import plotly.graph_objs as go
from plotly.subplots import make_subplots

from collections import deque
import datetime
from smartagro import *

obj = smart.SmartAgro()

def now():
    return datetime.datetime.now().strftime("%c")


X = deque(maxlen=20)
X.append(0)

Y0 = deque(maxlen=20)
Y1 = deque(maxlen=20)
Y2 = deque(maxlen=20)
Y3 = deque(maxlen=20)
Y2.append(1)
Y3.append(1)

app = dash.Dash(__name__)

# title='Real-time Monitoring',
app.layout = html.Div(

    [html.H1(children='SmartAgro API Demonstrator', style={'text-align': 'center'}),
     html.Br(),
     html.H2(children="Last Updated:", style={'text-align': 'center'}),
     html.Div(id='time', style={'text-align': 'center'}),
     dcc.RadioItems(
         id='fan',
         options=[
             {'label': 'Turn Fan ON', 'value': 1},
             {'label': 'Turn Fan OFF', 'value': 0}
         ],
         value=0
     ),
     dcc.Dropdown(
         id='sensor-dropdown', style={'width': '200px'},
         options=[
             {'label': 'Moisture', 'value': 0},
             {'label': 'Light', 'value': 1},
             {'label': 'Temperature', 'value': 2},
             {'label': 'Humidity', 'value': 3}
         ],
         value=0
     ),
     html.Div(id='output', style={'visibility': 'hidden'}),
     dcc.Graph(id='live-graph', animate=True),
     dcc.Graph(id='zero', animate=True),
     html.Div(id="0", style={'width': '49%', 'display': 'inline-block', 'text-align': 'center', 'font-size': '25px', 'font-weight': 'bold'}),
     html.Div(id="1", style={'width': '49%', 'display': 'inline-block', 'text-align': 'center', 'font-size': '25px', 'font-weight': 'bold'}),

     dcc.Graph(id='one', animate=True),
     html.Div(id="2", style={'width': '49%', 'display': 'inline-block', 'text-align': 'center', 'font-size': '25px', 'font-weight': 'bold'}),
     html.Div(id="3", style={'width': '49%', 'display': 'inline-block', 'text-align': 'center', 'font-size': '25px', 'font-weight': 'bold'}),
     dcc.Interval(id='graph-update', interval=5000, n_intervals=0),
     ]
)


@app.callback(
    Output('live-graph', 'figure'),
    Output('zero', 'figure'),
    Output('one', 'figure'),
    Output('time', 'children'),
    Output('0', 'children'),
    Output('1', 'children'),
    Output('2', 'children'),
    Output('3', 'children'),
    [Input('graph-update', 'n_intervals'), Input('sensor-dropdown', 'value')]
)
def update_graph_scatter(n, sensor):
    X.append(X[-1] + 5)
    readings = obj.read_all()
    Y0.append(readings[0])  # moisture
    Y1.append(readings[1])  # light
    Y2.append(readings[2] if readings[2] != 0 else Y2[-1])  # temp
    Y3.append(readings[3] if readings[3] != 0 else Y3[-1])  # humidity

    fig = make_subplots(rows=1, cols=2)
    fig.add_trace(go.Scatter(x=list(X), y=list(Y0), mode="lines+markers", name="Moisture"), row=1, col=1, )
    fig.add_trace(go.Scatter(x=list(X), y=list(Y1), mode="lines+markers", name="Light"), row=1, col=2, )
    fig.update_layout(xaxis=dict(range=[min(X), max(X)]), )  # if u dnt add it autoscales
    fig.update_yaxes(title_text="Moisture %", row=1, col=1, range=[0, 100])
    fig.update_yaxes(title_text="Light %", row=1, col=2, range=[0, 100])
    fig.update_xaxes(title_text="Elapsed Time (s)", range=[min(X), max(X)])  # for both axes

    fig2 = make_subplots(rows=1, cols=2)
    fig2.add_trace(go.Scatter(x=list(X), y=list(Y2), mode="lines+markers", name="Temperature"), row=1, col=1, )
    fig2.add_trace(go.Scatter(x=list(X), y=list(Y3), mode="lines+markers", name="Humidity"), row=1, col=2, )
    fig2.update_layout(xaxis=dict(range=[min(X), max(X)]))
    fig2.update_yaxes(title_text="Temperature °C", row=1, col=1, range=[0, 40])
    fig2.update_yaxes(title_text="Humidity %", row=1, col=2, range=[0, 100])
    fig2.update_xaxes(title_text="Elapsed Time (s)", range=[min(X), max(X)])

    Y = [Y0, Y1, Y2, Y3]
    data = plotly.graph_objs.Scatter(x=list(X), y=list(Y[sensor]), name='Scatter', mode='lines+markers')
    fig0 = {'data': [data], 'layout': go.Layout(xaxis=dict(range=[min(X), max(X)]),
                                                yaxis=dict(range=[min(Y[sensor]), max(Y[sensor])]), )}
    y0 = f"Moisture: {Y0[-1]} %"
    y1 = f"Light Intensity: {Y1[-1]} %"
    y2 = f"Temperature: {Y2[-1]} °C"
    y3 = f"Humidity: {Y3[-1]} %"
    return fig0, fig, fig2, now(), y0, y1, y2, y3


@app.callback(Output('output', 'children'),
              [Input('fan', 'value')])
def update_output_1(value):
    obj.activate_actuator(15, value)
    return value

    return {'data': [data],
            'layout' : go.Layout(xaxis=dict(range=[min(X), max(X)]),yaxis = dict(range = [min(Y0),max(Y0)]),)}, fig, fig2

if __name__ == '__main__':
    try:
        app.run_server(host="0.0.0.0", port=8080)
    except KeyboardInterrupt:
        obj.cleanup()
        print("Exiting")