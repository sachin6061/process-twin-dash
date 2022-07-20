from dash import Dash, html, dcc, dash_table, callback, Input, Output, dependencies, callback_context
import pandas as pd
import base64

New_Req_df = pd.read_excel('GPRF Data_Plotly Dash UI.xlsx', sheet_name='New Requests')
cmpny_code = New_Req_df['Company Code'].unique()
New_Req_ = New_Req_df.shape[0]
New_Req_df['date'] = pd.to_datetime(New_Req_df['Document Date']).dt.strftime('%m/%Y')
uni_date = New_Req_df['date'].unique()

Disb_Team_df = pd.read_excel('GPRF Data_Plotly Dash UI.xlsx', sheet_name='Disbursement Team')
Disb_Team_df['date'] = pd.to_datetime(Disb_Team_df['Document Date']).dt.strftime('%m/%Y')
Disb_Team_ = Disb_Team_df.shape[0]

Approver_Team_df = pd.read_excel('GPRF Data_Plotly Dash UI.xlsx', sheet_name='Approver Team')
Approver_Team_df['date'] = pd.to_datetime(Approver_Team_df['Document Date']).dt.strftime('%m/%Y')
Approver_Team_ = Approver_Team_df.shape[0]

Coding_Team_df = pd.read_excel('GPRF Data_Plotly Dash UI.xlsx', sheet_name='Coding Team')
Coding_Team_df['date'] = pd.to_datetime(Coding_Team_df['Document Date']).dt.strftime('%m/%Y')
Coding_Team_ = Coding_Team_df.shape[0]

Invoice_Proce_Team_df = pd.read_excel('GPRF Data_Plotly Dash UI.xlsx', sheet_name='Invoice Processing Team')
Invoice_Proce_Team_ = Invoice_Proce_Team_df.shape[0]
Invoice_Proce_Team_df['date'] = pd.to_datetime(Invoice_Proce_Team_df['Document Date']).dt.strftime('%m/%Y')


def fnDropColumn(df):
    if 'date' in df.columns:
        return df.drop('date', axis=1)
    else:
        return df


def fnNewReqBtn(cmpny_wise, month_wise, df):
    if cmpny_wise is not None and month_wise is not None:
        new = df[df['Company Code'] == cmpny_wise]
        new = new[new['date'] == month_wise]
        new = fnDropColumn(new)
        data = new.to_dict("records")
        return data, [{"name": i, "id": i} for i in new.columns]
    elif month_wise is not None:
        new = df[df['date'] == month_wise]
        new = new[new['date'] == month_wise]
        new = fnDropColumn(new)
        data = new.to_dict("records")
        return data, [{"name": i, "id": i} for i in new.columns]
    elif cmpny_wise is not None:
        new = df[df['Company Code'] == cmpny_wise]
        new = fnDropColumn(new)
        data = new.to_dict("records")
        return data, [{"name": i, "id": i} for i in new.columns]
    else:
        new = df
        new = fnDropColumn(new)
        data = new.to_dict("records")
        return data, [{"name": i, "id": i} for i in new.columns]


@callback(
    [Output("datatable", "data"), Output('datatable', 'columns')],
    Input("cmpny_wise", "value"),
    Input("month_wise", "value"),
    Input("newReq", "n_clicks"),
    Input("invProTeam", "n_clicks"),
    Input("codTeam", "n_clicks"),
    Input("appTeam", "n_clicks"),
    Input("disAudTeam", "n_clicks"),
)
def update_tbl(cmpny_wise, month_wise, *args):
    trigger = callback_context.triggered[0]
    tr = trigger["prop_id"].split(".")[0]
    if tr == 'newReq':
        return fnNewReqBtn(cmpny_wise, month_wise, New_Req_df)
    elif tr == 'invProTeam':
        return fnNewReqBtn(cmpny_wise, month_wise, Invoice_Proce_Team_df)
    elif tr == 'codTeam':
        return fnNewReqBtn(cmpny_wise, month_wise, Coding_Team_df)
    elif tr == 'appTeam':
        return fnNewReqBtn(cmpny_wise, month_wise, Approver_Team_df)
    elif tr == 'disAudTeam':
        return fnNewReqBtn(cmpny_wise, month_wise, Disb_Team_df)
    elif cmpny_wise is not None and month_wise is not None:
        new = New_Req_df[New_Req_df['Company Code'] == cmpny_wise]
        new = new[new['date'] == month_wise]
        new = fnDropColumn(new)
        data = new.to_dict("records")
        return data, [{"name": i, "id": i} for i in new.columns]
    elif cmpny_wise is not None:
        new = New_Req_df[New_Req_df['Company Code'] == cmpny_wise]
        new = fnDropColumn(new)
        data = new.to_dict("records")
        return data, [{"name": i, "id": i} for i in new.columns]
    elif month_wise is not None:
        new = New_Req_df[New_Req_df['date'] == month_wise]
        new = fnDropColumn(new)
        data = new.to_dict("records")
        return data, [{"name": i, "id": i} for i in new.columns]

    else:
        new = Invoice_Proce_Team_df
        new = fnDropColumn(new)
        data = new.to_dict("records")
        return data, [{"name": i, "id": i} for i in new.columns]


app = Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.Header('Process Twin',
                    style={'text-align': 'center', "font-size": "3vw", 'width': '100%', 'padding': '20px'})
    ], style={'background-color': '#ffbf00', 'margin': '0px', 'padding': '0px',
              'box-size': 'border-box', 'display': 'flex'}),

    html.Div([html.H4('Ontime Payment 85',
                      style={'padding': '10px', 'margin': '5px', 'color': 'white', 'background-color': '#0066ff',
                             'border-radius': '15px', 'width': '20%'}),
              html.H4('Avg Time Per Invoice 2.56',
                      style={'padding': '10px', 'margin': '5px', 'color': 'white', 'background-color': '#a3a375',
                             'border-radius': '15px', 'width': '20%'}),
              html.H4('Avg Processing Time 5.56',
                      style={'padding': '10px', 'margin': '5px', 'color': 'white', 'background-color': '#a3a375',
                             'border-radius': '15px', 'width': '20%'})],
             style={'display': 'flex', 'flex-direction': 'row', 'justify-content': 'center', 'text-align': 'center',
                    "font-size": "1.2vw", 'margin': '0%', 'padding': '0%', 'box-size': 'border-box'}),

    html.Div(
        [html.Label('Select Company Code', style={'margin-top': '19px', "font-size": "1.1vw", 'font-weight': '100'}),
         dcc.Dropdown(cmpny_code, placeholder='Select Company Code', id='cmpny_wise',
                      style={'width': '300px', 'margin': '5px'}),
         html.Label('Select Month',
                    style={'margin-top': '19px', "font-size": "1.1vw", 'font-weight': '100', 'margin-left': '10px'}),
         dcc.Dropdown(uni_date, placeholder='Select Month', id='month_wise',
                      style={'width': '300px', 'margin': '5px'})],
        style={'display': 'flex', 'flex-direction': 'row', 'justify-content': 'center', 'text-align': 'center', }),

    # html.Div(
    #     [html.H5("New requests", style={'padding': '5px', 'margin': '5px', 'width': '20%'}),
    #      html.H5("Invoice Processing Team", style={'padding': '5px', 'margin': '5px', 'width': '20%'}),
    #      html.H5("Coding Team", style={'padding': '5px', 'margin': '5px', 'width': '20%'}),
    #      html.H5("Approver Team", style={'padding': '5px', 'margin': '5px', 'width': '20%'}),
    #      html.H5("Disbursement Audit Team", style={'padding': '5px', 'margin': '5px', 'width': '20%'})],
    #     style={'display': 'flex', 'flex-direction': 'row', "font-size": "1.2vw", 'text-align': 'center'}),

    html.Div(
        [html.Div(
            [html.Button("New requests - " + str(New_Req_), id='newReq',
                         style={'padding': '10px', 'background-color': '#ffbf00',
                                'border-radius': '5px', 'width': '100%',
                                "font-size": "1vw", 'font-weight': 'bold'})],
            style={'width': '20%', 'text-align': 'center', 'margin': '5px'}),
            html.Div(
                [html.Button("Invoice Processing Team - " + str(Invoice_Proce_Team_), id='invProTeam',
                             style={'padding': '10px', 'background-color': '#ffbf00',
                                    'border-radius': '5px', 'width': '100%', "font-size": "1vw",
                                    'font-weight': 'bold'})],
                style={'width': '20%', 'text-align': 'center', 'margin': '5px'}),
            html.Div(
                [html.Button("Coding Team - " + str(Coding_Team_), id='codTeam',
                             style={'padding': '10px', 'background-color': '#ffbf00',
                                    'border-radius': '5px', 'width': '100%', "font-size": "1vw",
                                    'font-weight': 'bold'})],
                style={'width': '20%', 'text-align': 'center', 'margin': '5px'}),
            html.Div([html.Button("Approver Team - " + str(Approver_Team_), id='appTeam',
                                  style={'padding': '10px', 'background-color': '#ffbf00',
                                         'border-radius': '5px', 'width': '100%', "font-size": "1vw",
                                         'font-weight': 'bold'})],
                     style={'width': '20%', 'text-align': 'center', 'margin': '5px'}),
            html.Div([html.Button("Disbursement Audit Team - " + str(Disb_Team_), id='disAudTeam',
                                  style={'padding': '10px', 'background-color': '#ffbf00',
                                         'border-radius': '5px', 'width': '100%', "font-size": "1vw",
                                         'font-weight': 'bold'})],
                     style={'width': '20%', 'text-align': 'center', 'margin': '5px'})
        ]
        , style={'display': 'flex', 'flex-direction': 'row', "font-size": "1.5vw"}),

    html.Div(html.Div(dash_table.DataTable(
        id='datatable',
        columns=[{"name": i, "id": i} for i in New_Req_df.columns],
        data=New_Req_df.to_dict('records'),
        style_table={
            'overflowY': 'scroll',
            'overflowX': 'scroll',
        },
        page_size=10,
        style_cell={'textAlign': 'center', 'background-color': '#f2f2f2'},
        style_header={'textAlign': 'center', 'background-color': '#ffbf00', "font-size": "1vw"},
        style_as_list_view=True,
        tooltip_delay=0,
        tooltip_duration=None
    ), style={'margin-top': '15px', }))
])

if __name__ == '__main__':
    app.run_server(debug=True)
