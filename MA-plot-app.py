#!/usr/bin/env python3
# this is modified from https://dash.plotly.com/interactive-graphing
from dash import Dash, dcc, html, Input, Output, callback, dash_table, no_update
import plotly.express as px
import json,sys
import pandas as pd
import numpy as np

USE_EXAMPLE_DATA = True

# columns to show
columns_to_show_in_table = [ 'WBID', 'geneName', 'stage',
    'log_baseMean', 'log2FoldChange', 'lfcSE',
   # 'stat_enriched','stat_depleted','stat_equal',
    'padj_enriched', 'padj_depleted','padj_equal',
    'outcome_01','outcome_05']

# get Williams et al's data
if USE_EXAMPLE_DATA:
    print("Using example data", file=sys.stderr)
    df = pd.read_csv('example-data/subset.data-for-MA-plot-app.csv.gz', compression="gzip")
else:
    print("Database connection not supported.", file=sys.stderr)
    sys.exit(1)

# add a column
df['log_baseMean'] = np.log(df.baseMean)
df['outcome_01'] = df['outcome_01'].fillna('not significant') 
df['outcome_05'] = df['outcome_05'].fillna('not significant') 
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', 'styles.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

def generate_table(df, geneNames, max_rows=50):
    if not geneNames:
        return None
    dataframe = df.loc[df['WBID'].isin(geneNames)]
    return dataframe.to_dict("records")


styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

fig = px.scatter(df, x="log_baseMean", 
                 y="log2FoldChange", 
                 color="outcome_01", 
                 custom_data=["WBID"],
                 title="MA plot of ELT-2-GFP enriched sorted cells in the embryo")
fig.update_layout(clickmode='event+select')
fig.update_traces(marker_size=5, hoverinfo="none", hovertemplate=None)

@callback(
    Output("graph-tooltip", "show"),
    Output("graph-tooltip", "bbox"),
    Output("graph-tooltip", "children"),
    Input("basic-interactions", "hoverData"),
)
def display_hover(hoverData):
    if hoverData is None:
        return False, no_update, no_update
    pt = hoverData["points"][0]
    bbox = pt["bbox"]
    wbid = pt["customdata"].pop()

    df_row = df.loc[df['WBID'] == wbid]
    geneName = df_row.iloc[0]['geneName']
    WBID = df_row.iloc[0]['WBID']
    log2FC = df_row.iloc[0]['log2FoldChange']
    outcome_01 = df_row.iloc[0]['outcome_01']
    outcome_05 = df_row.iloc[0]['outcome_05']
    children = [
        html.Div([
            #html.Img(src=img_src, style={"width": "100%"}),
            html.P(f"{geneName} : {WBID}", 
                   style={"color": "darkblue", 
                          "overflow-wrap": "break-word"}),
            html.P(f"outcome at .01: {outcome_01}"),
            html.P(f"outcome at .05: {outcome_05}"),
        ], style={'white-space': 'normal'}) # 'width': '200px', 
    ]

    return True, bbox, children

app.layout = html.Div([
    html.H1(children='Interactive MA-plot for RNA-seq from Williams et al. 2023'),
    html.Div([
        html.P(children=["This is a plot of overall gene abundance (log_baseMean) against differential expression (log2FoldChange) of genes in the ",
            html.I(children="C. elegans"),
            " embryonic intestinal cells (cell-sorted). The data are from ",
            html.A(children="Williams et al. 2023", 
                    href="https://pubmed.ncbi.nlm.nih.gov/37183501/", 
                    target="_new"),
        html.P(" ", style = {'margin-bottom': '30px'}) # to space the graph down
                ])]),
    dcc.Graph(
        id='basic-interactions',
        figure=fig, 
        clear_on_unhover=True
    ),

    dcc.Tooltip(id="graph-tooltip"),


    html.Div([
        html.H4(children='Selected data'),
        dash_table.DataTable(
            #fixed_columns = {'headers': True, 'data': 3},
            columns=[ { 'name':i, 'id': i} for i in columns_to_show_in_table],
            id='table-data')
    ]),
    html.Hr(),
    html.H4(children='Debug info'),
    html.P(children="Show json object returned dynamically by selecting, clicking, hovering or zooming."),
    html.Div(className='row', children=[
        html.Div([
            dcc.Markdown("""
                **Hover Data**

                Mouse over values in the graph.
            """),
            html.Pre(id='hover-data', style=styles['pre'])
        ], className='three columns'),

        html.Div([
            dcc.Markdown("""
                **Click Data**

                Click on points in the graph.
            """),
            html.Pre(id='click-data', style=styles['pre']),
        ], className='three columns'),

        html.Div([
            dcc.Markdown("""
                **Selection Data**

                Choose the lasso or rectangle tool in the graph's menu
                bar and then select points in the graph.

                Note that if `layout.clickmode = 'event+select'`, selection data also
                accumulates (or un-accumulates) selected data if you hold down the shift
                button while clicking.
            """),
            html.Pre(id='selected-data', style=styles['pre']),
        ], className='three columns'),

        html.Div([
            dcc.Markdown("""
                **Zoom and Relayout Data**

                Click and drag on the graph to zoom or click on the zoom
                buttons in the graph's menu bar.
                Clicking on legend items will also fire
                this event.
            """),
            html.Pre(id='relayout-data', style=styles['pre']),
        ], className='three columns')
    ])
])

@callback(
    Output('hover-data', 'children'),
    Input('basic-interactions', 'hoverData'))
def display_hover_data(hoverData):
    return json.dumps(hoverData, indent=2)


@callback(
    Output('click-data', 'children'),
    Input('basic-interactions', 'clickData'))
def display_click_data(clickData):
    return json.dumps(clickData, indent=2)


@callback(
    Output('selected-data', 'children'),
    Input('basic-interactions', 'selectedData'))
def display_selected_data(selectedData):
    return json.dumps(selectedData, indent=2)

@callback(
    Output('table-data', 'data'),
    Input('basic-interactions', 'selectedData'))
def showtable_selected_data(selectedData):
    geneNames = None
    #print(selectedData, file=sys.stderr)
    if selectedData:
        geneNames = [record['customdata'].pop() for record in selectedData['points']]

    return generate_table(df, geneNames, max_rows=50)

""" @callback(
    Output('relayout-data', 'children'),
    Input('basic-interactions', 'reLayoutData'))
def display_relayout_data(relayoutData):
    return json.dumps(relayoutData, indent=2)

 """
if __name__ == '__main__':
    app.run(debug=True)
