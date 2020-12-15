import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import dash_table
import base64
import plotly.graph_objs as go

app = dash.Dash(__name__)
server = app.server

app.title = 'C-DOT Covid Meter'

dw_data = pd.read_excel('cdot_covid_data.xlsx',parse_dates=True, sheet_name='Date-wise')

df_groupby_block = dw_data.groupby(['Block'],as_index=False).count()

df1 = df_groupby_block[['Block', 'Total Cases']]

df2_raw = dw_data.sort_values(['Staff No.'])
df2= df2_raw[['Staff No.', 'Staff Name', 'Block']]


df3 = dw_data.groupby(['Date'],as_index=False).count()


fig = px.bar(df3, x="Date", y="Total Cases", color='Total Cases', orientation='v', height=600,
             title='Trend of Covid Cases', color_discrete_sequence = px.colors.cyclical.IceFire)

fig.update_layout(font=dict(
                    family="Courier New, monospace",
                    size=18))

app.layout = html.Div(children=[

    html.H1(children=['C-DoT Delhi Covid Meter'], className = 'header_title'),

    html.Div(children=['''Last Updated on 15th Dec 2020, 10:00 AM IST'''], className = 'header_time'),

    html.Div(children=[
        
        html.Div(children=[], className = 'row1col1'),

        html.Div(children=[
            html.Div(children=[''' EMPLOYEES '''], className = 'row1col2_title'),
            
            html.Div(children=[''' 568 '''], className = 'row1col2_data')
        ],className = 'row1col2'),

        html.Div(children=[
            html.Div(children=['''TOTAL CASES'''], className = 'row1col3_title'),
            
            html.Div(children=[''' 53 '''], className = 'row1col3_data')
        ], className = 'row1col3'),
        
        html.Div(children=[], className = 'row1col4'),

    ], className = 'container1'),

    html.Div(children=[

        html.Div(children = [], className = 'row2col1'),

        html.Div(children = [

            dcc.Tabs(id="tabs", children = [
                dcc.Tab(label='Block Wise List', children = [
                    html.Div(children = [
                        dash_table.DataTable(
                            id='block_table',
                            style_cell={'textAlign': 'center', 'width' : '50%'},
                            style_header={ 'backgroundColor': '#EEEEEE', 'fontWeight': 'bold'},
                            #style_table={ 'height' : '600px'},
                            columns=[{"name" :i, "id" :i} for i in df1.columns],
                            #fixed_rows={'headers': True},
                            data=df1.to_dict('records'),
                        )
                    ])
                ]),
            
                dcc.Tab(label='Staff Wise List', children = [
                    html.Div(children = [
                        dash_table.DataTable(
                            id='staff_table',
                            style_cell={'textAlign': 'center' },
                            style_cell_conditional=[ 
                                {'if': {'column_id': 'Staff No.'}, 'width': '30%'},
                                {'if': {'column_id': 'Staff Name'}, 'width': '50%'},
                                {'if': {'column_id': 'Block'}, 'width': '20%'},
                            ],
                            #fixed_rows={'headers': True},
                            style_header={ 'backgroundColor': '#EEEEEE', 'fontWeight': 'bold' },
                            style_table={ 'height' : '520px', 'overflowY': 'scroll'},
                            columns=[{"name" :i, "id" :i} for i in df2.columns],
                            data=df2.to_dict('records'),
                        )
                    ])
                ])
                ], style={
                    'height': '6vh',
                    'background-color': '#66ff66',
                    'font-weight' : 'bold',
                    'font-size' : '20px'
                })
        ], className = 'row2col2'),

        html.Div(children = [], className = 'row2col3')
    ], className = 'container2'),

    html.Div( children = [
        dcc.Graph( id = "g2", figure=fig)
    ]),

    html.Div( ' @ Copyright. All Rights Reserved', className = 'footer')
    
    ], style={'textAlign': 'center'})

if __name__ == '__main__':
    #app.Flask(debug=False,port=8080,host='0.0.0.0')
    #app.run(debug=False)
    app.run_server(debug=False)
