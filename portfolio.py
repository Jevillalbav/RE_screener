#pip install -r requirements.txt

import pandas as pd 
import numpy as np
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

data_model_a = pd.read_csv("data_model.csv", index_col = 0, parse_dates=True)
forecasts_database_a = pd.read_csv("forecasts_database.csv", index_col = 0, parse_dates=True)
expected_irr_a = pd.read_csv("expected_irr.csv", index_col = 0, parse_dates=True)
irr_real_a = pd.read_csv("irr_real.csv", index_col = 0, parse_dates=True)
complete_irr_a = pd.read_csv("complete_irr.csv", index_col = 0, parse_dates=True)
leverage_a = pd.read_csv("leverage.csv", index_col = 0, parse_dates=True)
conjunto_submarkets = complete_irr_a['name'].copy().values.tolist()
categories_options = [{'label': x, 'value': x} for x in conjunto_submarkets]


################################################################################################################################
fig = go.Figure()
fig.update_layout(xaxis_title="Date", 
                  
    xaxis = dict(  domain=[0.05, 0.98],
                                                    title="Date",
                                                    titlefont=dict(color="black"),
                                                    tickfont=dict(color="black"),
                                                    showgrid=False,dtick='M12', 
                                                    ticks="outside", tickcolor="black")
    ,
    yaxis=dict(title="Price - USD" #+ data_model_f['yax'].unique()[0]
               ,titlefont=dict(color="black",size = 20),
                                    tickfont=dict(color="black"), tickformat = '$,.0f', 
                                    showgrid=False,position=0.04) #overlaying="y",
                                    #range=[0,int((data_model_f['price'].max()*1.2)/100)*100],
                                    #dtick=int((data_model_f['price'].max()*1.2)/100)*5)
                                    #gridcolor='white',
                                    #gridwidth=0.5
                                    
    ,
    yaxis2=dict(title='',titlefont=dict(color="black", size = 15),                    
                                                    tickfont=dict(color="black"), anchor="free", showgrid=False, showticklabels=False,  
                                                    side="left",position=0.14, overlaying="y",
                                                    tickformat =',.2%',# ',.0%',
                                                    range=[-0.35, 3.8])
    ,
    yaxis3=dict(title="", titlefont=dict(color="#204a01", size = 15),
                                    tickfont=dict(color="#204a01"),anchor="free",
                                    side="left",position=0.08,  overlaying="y",
                                    showgrid=False,tickformat ='.2%',# ',.0%',
                                    #zeroline=True,
                                    range = [-0.2,0.4],
                                    dtick=0.03,
                                    #gridcolor='white',
                                    showticklabels=False)
    ,
    legend=dict(x=0.4,y=1.12, traceorder="normal", font=dict(family="sans-serif",size=12, color="black"), bgcolor="white", bordercolor="black", borderwidth=1)
    ,
    autosize=False,  legend_orientation="h",margin=dict(l=50,r=50,b=100,t=100,pad=4)
    ,
    )   
fig.update_layout(width = 1600, height = 800)
## change theme 
fig.update_layout(template = 'plotly_white')

app = dash.Dash(__name__)

server = app.server


app.layout = html.Div([
    # Dropdown for selecting category
    dcc.Dropdown(
        id='category-dropdown',
        options=categories_options,
        value= categories_options[0]['value'],
        # Set default value to the first category
        multi=False,
    ), 

    # Plotly chart
    dcc.Graph(
        id='my-chart',
        figure=fig  # Use the figure you created earlier
    )
])
# Callback to update the chart based on the selected category
@app.callback(
    Output('my-chart', 'figure'),
    [Input('category-dropdown', 'value')]
)

def update_chart(category):
    # Filter the data
    data_model_f = data_model_a.loc[data_model_a['name'] == category].copy()

    forecast_database_f = forecasts_database_a.loc[forecasts_database_a['k'] == category].copy()

    price_f = forecast_database_f.loc[forecast_database_f['yy'] == 'price'].copy()
    rent_f = forecast_database_f.loc[forecast_database_f['yy'] == 'ef_r'].copy()

    expected_irr_f = expected_irr_a.loc[expected_irr_a['k'] == category].copy()
    irr_real_f = irr_real_a.loc[irr_real_a['k'] == category].copy()

    irr_m_f = complete_irr_a.loc[complete_irr_a['name'] == category].copy()

    noi_f = rent_f.copy()
    noi_f['fc'] = (rent_f['fc']*6) / price_f['fc']
    noi_f['fc_lower'] = (rent_f['fc']*6) / price_f['fc_lower']
    noi_f['fc_upper'] = (rent_f['fc']*6) / price_f['fc_upper']

    leverage_f = leverage_a.loc[leverage_a['name'] == category].copy()

    fig = go.Figure()
    fig.update_layout(xaxis_title="Date", 
                    
        xaxis = dict(  domain=[0.05, 0.98],
                                                        title="Date",
                                                        titlefont=dict(color="black"),
                                                        tickfont=dict(color="black"),
                                                        showgrid=False,dtick='M12', 
                                                        ticks="outside", tickcolor="black")
        ,
        yaxis=dict(title="Price - USD" + data_model_f['yax'].unique()[0]
                ,titlefont=dict(color="black",size = 20),
                                        tickfont=dict(color="black"), tickformat = '$,.0f', 
                                        showgrid=False,position=0.04, #overlaying="y",
                                        range=[0,int((data_model_f['price'].max()*1.2)/100)*100],
                                        dtick=int((data_model_f['price'].max()*1.2)/100)*5)
                                        #gridcolor='white',
                                        #gridwidth=0.5
                                        
        ,
        yaxis2=dict(title='',titlefont=dict(color="black", size = 15),                    
                                                        tickfont=dict(color="black"), anchor="free", showgrid=False, showticklabels=False,  
                                                        side="left",position=0.14, overlaying="y",
                                                        tickformat =',.2%',# ',.0%',
                                                        range=[-0.35, 3.8])
        ,
        yaxis3=dict(title="", titlefont=dict(color="#204a01", size = 15),
                                        tickfont=dict(color="#204a01"),anchor="free",
                                        side="left",position=0.08,  overlaying="y",
                                        showgrid=False,tickformat ='.2%',# ',.0%',
                                        #zeroline=True,
                                        range = [-0.2,0.4],
                                        dtick=0.03,
                                        #gridcolor='white',
                                        showticklabels=False)
        ,
        legend=dict(x=0.4,y=1.12, traceorder="normal", font=dict(family="sans-serif",size=12, color="black"), bgcolor="white", bordercolor="black", borderwidth=1)
        ,
        autosize=False,  legend_orientation="h",margin=dict(l=50,r=50,b=100,t=100,pad=4)
        ,
        )   
    fig.update_layout(width = 1600, height = 800, title = category)
    ## change theme 
    fig.update_layout(template = 'plotly_white')
    ## PRECIO DE LA VIVIENDA
    fig.add_trace(go.Scatter(x=data_model_f['period'], y=data_model_f['price'], name='Market Sale Price', line_color='purple', mode='lines+markers', line = dict(color = 'blue', width = 1), marker= dict(size = 2), showlegend= True ))
    fig.add_trace(go.Scatter(x=price_f.index, y=price_f['fc'], mode='lines', line = dict( width = 1, dash = 'dot'), showlegend= False , line_color='blue', name='Forecast Price'))
    fig.add_trace(go.Scatter(x=price_f.index, y=price_f['fc_lower'], fill= 'tonexty', mode= 'markers', marker=dict(color='white', size=1), fillcolor= 'rgba(78, 245, 239,0)',  showlegend= False ))
    fig.add_trace(go.Scatter(x=price_f.index, y=price_f['fc_upper'], fill= 'tonexty', mode= 'markers', marker=dict(color='white', size=1), fillcolor= 'rgba(78, 245, 239,0.2)',  showlegend= False ))
    ## NOI
    fig.add_trace(go.Scatter(x=data_model_f['period'], y=data_model_f['rate'], name='Rate +  Spread', line_color='rgba(255, 0, 0,0.2)' , mode='lines' , fill= 'tozeroy', fillcolor= 'rgba(255, 0, 0,0.1)', showlegend= True, yaxis='y3', line=dict(width=1) , hovertemplate= 'Rate: %{y:.2%}'))
    fig.add_trace(go.Scatter( x = data_model_f['period'], y = data_model_f['yld'] , name='Rate' , line_color= 'rgba(255, 0, 0,0.2)' , mode='lines' , fill= 'tozeroy', fillcolor= 'rgba(255, 0, 0,0.1)', showlegend= False, yaxis='y3', line=dict(width=1), hovertemplate= 'Rate: %{y:.2%}' ))
    fig.add_trace(go.Scatter( x = data_model_f['period'], y = data_model_f['noi'], name='NOI' , line_color='rgba(12, 171, 57,0.2)', mode='lines' , fill= 'tozeroy', fillcolor= 'rgba(12, 171, 57,0.2)', showlegend= True, yaxis='y3' , line=dict(width=1), hovertemplate= 'Rate: %{y:.2%}'))
    #
    fig.add_trace(go.Scatter( x = noi_f.index, y = noi_f['fc'], name='NOI Forecast' , line_color='gray', mode='lines' , showlegend= False, yaxis='y3' , line=dict(width=1, dash="dot"), fill= 'tozeroy', fillcolor= 'rgba(78, 245, 239,0.1)', hovertemplate= 'NOI: %{y:.2%}' ))
    #fig.add_trace(go.Scatter( x = noi_f.index, y = noi_f['fc_lower'], name='NOI Forecast' , line_color='white', mode='lines' , showlegend= False, yaxis='y3' , line=dict(width=1, dash="dot"), hovertemplate= 'NOI: %{y:.2%}' ))#, fill= 'tonexty', fillcolor= 'rgba(78, 245, 239,0)'))
    #fig.add_trace(go.Scatter( x = noi_f.index, y = noi_f['fc_upper'], name='NOI Forecast' , line_color='white', mode='lines' , showlegend= False, yaxis='y3' , line=dict(width=1, dash="dot"), hovertemplate= 'NOI: %{y:.2%}' ))#))#, fill= 'tonexty', fillcolor= 'rgba(78, 245, 239,0.2)'))


    ## IRR
    fig.add_trace(go.Scatter( x = expected_irr_f['date_forecast'], y = expected_irr_f['upper'], mode='lines', line = dict(color = 'white', width = 1), yaxis='y2', showlegend= False , hovertemplate= 'IRR: %{y:.2%}'))
    fig.add_trace(go.Scatter( x = expected_irr_f['date_forecast'], y = expected_irr_f['lower'], name='Forecast IRR (Bands)', mode='lines', line = dict(color = 'white', width = 1), yaxis='y2', fill='tonexty', fillcolor= 'rgba(78, 245, 239, 0.2)', hovertemplate= 'IRR: %{y:.2%}'))
    fig.add_trace(go.Scatter( x = expected_irr_f['date_forecast'], y = expected_irr_f['mean'], name='Forecast IRR (Mean)', mode='lines', line = dict(color = 'black', width = 1, dash = 'dot'), yaxis='y2' , hovertemplate= 'IRR: %{y:.2%}'))
    fig.add_trace(go.Bar( x = irr_real_f['date'], y = irr_real_f['irr'],  name="IRR Current", opacity=0.2, yaxis='y2' , marker_color = 'Royalblue', hovertemplate= 'IRR: %{y:.2%}'))

    ## for each bar in the plot, add an annotation with the y value
    #irr_real_f['date'] = pd.to_datetime(irr_real_f['date'])
    #for x,y in irr_real_f.dropna()[['date', 'irr']].values[0::2]:
    #    fig.add_annotation(x=x, y=y, text= format(y, '.1%'), xanchor='center', yanchor='bottom', showarrow=False, yshift=20, font=dict(color='black', size=10), yref='y2', textangle=-65, bgcolor='rgba(255, 255, 255,1)', bordercolor='rgba(0, 0, 0,0.1)')

    #for x,y in expected_irr_f.dropna().iloc[2:][['date_forecast', 'mean']].values[0::2]:
    #    fig.add_annotation(x=x, y=y, text= format(y, '.1%'), xanchor='center', yanchor='bottom', showarrow=False, yshift=20, font=dict(color='black', size=10), yref='y2', textangle=-65, bgcolor='rgba(10, 242, 234,0.5)', bordercolor='rgba(130, 209, 165,0.5)')

    # OTHERS
    fig.add_annotation(x=0.05, y= -0.13, text="** Assumptions:    1- Expenses at 50% of the net operating income. 2- Spread over the 10 Years Yield of 200 Basis Points. 3- Housing prices given in US dollars", showarrow=False, arrowhead=1, ax=0, ay=-40, bgcolor="white", bordercolor="black", borderwidth=1,  yref='paper',xref = 'paper', font=dict(size=11, color='black')  )
    ################################################################################################################################
    current_price = data_model_f['price'].iloc[-1]
    current_noi = data_model_f['noi'].iloc[-1]
    current_yld = data_model_f['yld'].iloc[-1]
    current_rate = data_model_f['rate'].iloc[-1]

    current_price_s = format(current_price, ',.0f')
    current_noi_s = format(current_noi, '.2%')
    current_yld_s = format(current_yld, '.2%')
    current_rate_s = format(current_rate, '.2%')

    current_price_l = data_model_f['period'].iloc[-1]
    current_noi_l = data_model_f['period'].iloc[-1]
    current_yld_l = data_model_f['period'].iloc[-1]
    current_rate_l = data_model_f['period'].iloc[-1]

    fig.add_annotation(x=current_price_l, y=current_price, text="Current Price : $" +  current_price_s, showarrow=True, arrowhead=1, ax=-70, ay=20, bgcolor="white", bordercolor="black", borderwidth=1,  yref='y1')
    fig.add_annotation(x=current_noi_l, y=current_noi, text="Current NOI : " +  current_noi_s, showarrow=True, arrowhead=1, ax=-70, ay=-30, bgcolor="white", bordercolor="black", borderwidth=1,  yref='y3')
    #fig.add_annotation(x=current_yld_l, y=current_yld, text="Current 10Y : " +  current_yld_s, showarrow=True, arrowhead=1, ax=0, ay=-0, bgcolor="white", bordercolor="black", borderwidth=1,  yref='y3')
    fig.add_annotation(x=current_rate_l, y=current_rate, text="Current 10y + Spread: " +  current_rate_s, showarrow=True, arrowhead=1, ax=-0, ay=70, bgcolor="white", bordercolor="black", borderwidth=1,  yref='y3')
    fig.add_annotation(x=irr_real_f.dropna()['date'].iloc[-1], y= 0, text="Current IRR  ->  Forecast IRR ", showarrow=False, arrowhead=1, ax=0, ay=-40, bgcolor="white", bordercolor="black", borderwidth=1,  yref='paper', font=dict(size=11, color='black')  )


    fig.add_annotation(x=expected_irr_f['date_forecast'].iloc[-1]   , y= expected_irr_f['upper'].iloc[-1], text='5yrs Best IRR: ' + format(expected_irr_f['upper'].iloc[-1], '.1%'),
                    showarrow=True, arrowhead=1, ax=120, ay=-30, bgcolor="white", bordercolor="black", borderwidth=1,  yref='y2', font=dict(size=11, color='black')  )
    
    fig.add_annotation(x=expected_irr_f['date_forecast'].iloc[-1]   , y= expected_irr_f['lower'].iloc[-1], text='5yrs Worst IRR: ' + format(expected_irr_f['lower'].iloc[-1], '.1%'),
                    showarrow=True, arrowhead=1, ax=120, ay=30, bgcolor="white", bordercolor="black", borderwidth=1,  yref='y2', font=dict(size=11, color='black')  )
    
    fig.add_annotation(x=expected_irr_f['date_forecast'].iloc[-1]   , y= expected_irr_f['mean'].iloc[-1], text='5yrs Forecasted IRR: ' + format(expected_irr_f['mean'].iloc[-1], '.1%'),
                    showarrow=True, arrowhead=1, ax=120, ay=0, bgcolor="white", bordercolor="black", borderwidth=1,  yref='y2', font=dict(size=11, color='black')  )

    ################################################################################################################################
    forecast_price = price_f['fc'].iloc[-1]
    forecast_noi = noi_f['fc'].iloc[-1]

    forecast_price_s = format(forecast_price, ',.0f')
    forecast_noi_s = format(forecast_noi, '.2%')

    forecast_price_ch = ((forecast_price) / current_price)**(1/5) - 1
    forecast_noi_ch = (forecast_noi - current_noi)

    forecast_price_l = price_f.index[-1]
    forecast_noi_l = noi_f.index[-1]

    forecast_price_upper = price_f['fc_upper'].iloc[-1]
    forecast_price_lower = price_f['fc_lower'].iloc[-1]

    forecast_price_upper_s = format(forecast_price_upper, ',.0f')
    forecast_price_lower_s = format(forecast_price_lower, ',.0f')

    forecast_price_upper_ch = ((forecast_price_upper) / current_price)**(1/5) - 1
    forecast_price_lower_ch = ((forecast_price_lower) / current_price)**(1/5) - 1


    fig.add_annotation(x=forecast_price_l, y=forecast_price_upper, text="Fcst Upper: $" +  forecast_price_upper_s + ', YoY ' + format(forecast_price_upper_ch, '.2%')
                        , showarrow=True, arrowhead=1, ax=45, ay=-45, bgcolor="white", bordercolor="black", borderwidth=1,  yref='y1', yshift=0, arrowcolor='gray')
    fig.add_annotation(x=forecast_price_l, y=forecast_price_lower, text="Fcst Lower: $" +  forecast_price_lower_s + ', YoY ' + format(forecast_price_lower_ch, '.2%')
                            , showarrow=True, arrowhead=1, ax=45, ay=15, bgcolor="white", bordercolor="black", borderwidth=1,  yref='y1', yshift=0, arrowcolor='gray')

    fig.add_annotation(x=forecast_price_l, y=forecast_price, text="Fcst : $" +  forecast_price_s + ', YoY ' + format(forecast_price_ch, '.2%')
                    , showarrow=True, arrowhead=1, ax=45, ay=-25, bgcolor="white", bordercolor="black", borderwidth=1,  yref='y1', yshift=0, arrowcolor='gray')
    fig.add_annotation(x=forecast_noi_l, y=forecast_noi, text="Fcst NOI: " +  forecast_noi_s #+ ', ' + format(forecast_noi_ch, '.2%')
                    , showarrow=True, arrowhead=1, ax=45, ay=-25, bgcolor="white", bordercolor="black", borderwidth=1,  yref='y3', yshift=0, arrowcolor='gray')

    ################################################################################################################################
    current_rent_less_interest_str = format((current_noi - current_rate), '.2%')
    # Assumpitons chart upper 
    fig.add_annotation(x= current_price_l, y = 0.955 , text= 'Current Assumed Debt Rate  SOFR 10Y + 200 b.p.:  ' + current_rate_s, ax = -150, ay=0, bgcolor="#eb6e74", bordercolor="black", borderwidth=1,  yref='paper')
    fig.add_annotation(x= current_price_l, y = 0.993 , text= 'Current Assumed NOI Margin:  ' + current_noi_s,  ax=-150, ay=0, bgcolor="#86e394", bordercolor="black", borderwidth=1,  yref='paper')
    fig.add_annotation(x= current_price_l, y = 0.915 , text= 'Current Assumed Profit from Holding: ' + current_rent_less_interest_str, ax=-150, ay=0, bgcolor="#d9b0eb", bordercolor="black", borderwidth=1,  yref='paper')
    fig.add_annotation(x= current_price_l, y = 0.875 , text= 'Current Leverage Limit: ' + leverage_f['limit'].iloc[-1]
                    , ax=-150, ay=0, bgcolor="#7299ed", bordercolor="black", borderwidth=1,  yref='paper')
    #fig.write_html(f'C:/Users/JuanEstebanVillalba/Sun Valley Investment/Trading Desk - Quant Group/5. Strategy Publisher/notebooks/latest/re 2.0/Portfolio Forecast/{category}.html')

    ################################################################################################################################
    return fig
################################################################################################################################

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
