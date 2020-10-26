# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html

import plotly.graph_objects as go
from plotly.subplots import make_subplots

fig = make_subplots(rows=1, cols=2)
fig.add_trace(go.Scatter(y=[4, 2, 1], mode="lines"), row=1, col=1)
fig.add_trace(go.Bar(y=[2, 1, 3]), row=1, col=2)

fig2 = make_subplots(rows=1, cols=2)
fig2.add_trace(go.Scatter(y=[4, 2, 1], mode="lines"), row=1, col=1)
fig2.add_trace(go.Bar(y=[2, 1, 3]), row=1, col=2)

#fig.add_trace(go.Scatter(x=t1, y=y1, name="10 cycles sampled at 1KHz",mode='markers',
#                         marker=dict(color='Red',size=4)), row=2, col=1)
# fig.update_xaxes(title='Time (s)')

import plotly.graph_objects as go
import numpy as np

f = 30.76  #sinusoid frquencyf0
T = 1/f
tmin = 0
tmax = 1 #1 Second

dt0 = T/100  #frequency much higher than nyquist rate to simulate continuous-time signal.
dt1 = 1/1000 #1kHz sampling rate

#time data points with different sampling frequencies
t0 = np.arange(tmin,tmax,dt0)
t1 = np.arange(tmin,tmax,dt1)

# Sampling the sinusoid y = np.sin(2 pi f tx), where f is sampling frequency in Hz. tx - time scale.
y0 = np.sin(2*np.pi*f*t0)
y1 = np.sin(2*np.pi*f*t1)

#begin plotting of figure.
fig0 = go.Figure()
fig0.add_trace(go.Scatter(x=t0, y=y0, name="Continuous-Time Signal",mode='lines')) #mode=lines+markers+text
fig0.add_trace(go.Scatter(x=t1, y=y1, name="Signal Sampled at 1KHz",mode='markers',
                         marker=dict(color='Red',size=4)
                         )
              )
fig0.update_yaxes(title='Signal')
fig0.update_xaxes(title='Time (s)')
fig0.update_layout(title_text="Question 1: Sine wave at 30.76 hertz,being sampled at 1 kHz for 1 second")
#fig.show()







app = dash.Dash()
app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),
    html.Div(children='''Dash Framework: A web application framework for Python.'''),

    dcc.Graph(
        id='example-graph',
        animate=True,
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 12], 'type': 'line', 'name': 'Delhi'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'line', 'name': u'Mumbai'},
            ],

            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    ),

    dcc.Graph(
        id='example-grap',
        figure=fig
    ),

    dcc.Graph(
        id='example-gra',
        figure=fig2
    ),

    dcc.Graph(
        id='example-gr',
        figure=fig0
    ),
    dcc.Interval(
        id='graph-update',
        interval=1000,
        n_intervals=0
    ),

])

if __name__ == '__main__':

    app.run_server(debug=True, host="0.0.0.0", port="8080")