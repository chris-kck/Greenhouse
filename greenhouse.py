
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
#obj.activate_actuator(15,1)
#time.sleep(3)
#obj.activate_actuator(15,0)

def now():
    return datetime.datetime.now().strftime("%X")

X = deque(maxlen = 20)
X.append(1)

Y = deque(maxlen = 20)
Y.append(1)

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        dcc.Graph(id = 'live-graph', animate = True),
        dcc.Interval(
            id = 'graph-update',
            interval = 1000,
            n_intervals = 0
        ),
    ]
)

@app.callback(
    Output('live-graph', 'figure'),
    [ Input('graph-update', 'n_intervals') ]
)

def update_graph_scatter(n):
    X.append(X[-1]+1)
    Y.append(Y[-1]+Y[-1] * random.uniform(-0.1,0.1))

    data = plotly.graph_objs.Scatter(
        x=list(X),
        y=list(Y),
        name='Scatter',
        mode= 'lines+markers'
    )

    return {'data': [data],
            'layout' : go.Layout(xaxis=dict(range=[min(X),max(X)]),yaxis = dict(range = [min(Y),max(Y)]),)}

if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port=8080)

