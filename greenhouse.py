
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
    [
        dcc.Graph(id = 'live-graph', animate = True),
        dcc.Graph(id='zero', animate = True),
        dcc.Graph(id='one', animate = True),
        dcc.Interval(
            id = 'graph-update',
            interval = 5000,
            n_intervals = 0
        ),
    ]
)

@app.callback(
    Output('live-graph', 'figure'),
    Output('zero', 'figure'),
    Output('one', 'figure'),
    [ Input('graph-update', 'n_intervals') ]
)

def update_graph_scatter(n):
    X.append(X[-1]+5)
    readings = obj.read_all()
    Y0.append(readings[0])  # moisture
    Y1.append(readings[1])  # light
    Y2.append(readings[2])  # temp
    Y3.append(readings[3])  # humidity

    data = plotly.graph_objs.Scatter(
        x=list(X),
        y=list(Y0),
        name='Scatter',
        mode= 'lines+markers'
    )

    fig = make_subplots(rows=1, cols=2)
    fig.add_trace(go.Scatter(x=list(X), y=list(Y0), mode="lines+markers", name="Moisture"), row=1, col=1, )
    fig.add_trace(go.Scatter(x=list(X), y=list(Y1), mode="lines+markers", name="Light"), row=1, col=2, )
    fig.update_layout(xaxis=dict(range=[min(X), max(X)]),
                      yaxis = dict(range = [min(Y0),max(Y0)])
                      )
    fig.update_yaxes(title_text="Moisture %", row=1, col=1)
    fig.update_yaxes(title_text="Light %", row=1, col=2)
    fig.update_xaxes(title_text="Elapsed Time (s)")

    fig2 = make_subplots(rows=1, cols=2)
    fig2.add_trace(go.Scatter(x=list(X), y=list(Y2), mode="lines+markers",  name="Temperature"), row=1, col=1,)
    fig2.add_trace(go.Scatter(x=list(X), y=list(Y3), mode="lines+markers",  name="Humidity"), row=1, col=2,)
    fig2.update_layout(xaxis=dict(range=[min(X), max(X)]),
                       yaxis = dict(range = [min(Y2),max(Y2)])
                       )
    fig2.update_yaxes(title_text="Temperature °C", row=1, col=1)
    fig2.update_yaxes(title_text="Humidity %", row=1, col=2)
    fig2.update_xaxes(title_text="Elapsed Time (s)")

    return {'data': [data],
            'layout' : go.Layout(xaxis=dict(range=[min(X), max(X)]),yaxis = dict(range = [min(Y0),max(Y0)]),)}, fig, fig2

if __name__ == '__main__':
    try:
        app.run_server(host="0.0.0.0", port=8080)
    except KeyboardInterrupt:
        obj.cleanup()
        print("Exiting")