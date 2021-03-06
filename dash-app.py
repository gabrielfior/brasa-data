import itertools
import json

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import pandas as pd
from dash.dependencies import Input, Output
import os
import flask
from random import shuffle
import numpy as np

####
from utils import excel_cols

server = flask.Flask(__name__)
server.secret_key = os.environ.get('secret_key', str(np.random.randint(0, 1000000)))
app = dash.Dash(__name__, server=server)
####

n_rows = 10000
list_excel_cols = list(itertools.islice(excel_cols(), n_rows))
list_excel_cols_shuffled = list(itertools.islice(excel_cols(), n_rows))
shuffle(list_excel_cols_shuffled)
df_rows = pd.DataFrame({
    'index': np.arange(n_rows),
    'x': list_excel_cols,
    'y': np.random.randint(0, 100, n_rows),
})

app.layout = html.Div([
    html.H4('Editable DataTable'),
    html.H6('%d rows' % n_rows),
    dt.DataTable(
        rows=df_rows.to_dict('records'),
        columns=sorted(df_rows.columns),
        editable=True,
        id='editable-table'
    ),
    html.Div([
        #html.Pre(id='output', className='two columns'),
        html.Div(
            dcc.Graph(
                id='graph',
                style={
                    'overflow-x': 'wordwrap'
                }
            ),
            className='ten columns'
        )], className='row')
], className='container')

'''
@app.callback(
    Output('output', 'children'),
    [Input('editable-table', 'rows')])
def update_selected_row_indices(rows):
    return json.dumps(rows, indent=2)
'''

@app.callback(
    Output('graph', 'figure'),
    [Input('editable-table', 'rows')])
def update_figure(rows):
    dff = pd.DataFrame(rows)
    return {
        'data': [{
            'x': dff['x'],
            'y': dff['y'],
            'index': dff['index']
        }],
        'layout': {
            'margin': {'l': 10, 'r': 0, 't': 10, 'b': 20}
        }
    }


app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

if __name__ == '__main__':
    app.server.run(debug=True, threaded=True)
