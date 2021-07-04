from django.shortcuts import render
from plotly.offline import plot
import yfinance as yf
import plotly.graph_objs as go
from pandas_datareader.data import DataReader
from datetime import datetime
import requests
import plotly.express as px
import numpy as np
import pandas as pd
from pytz import timezone


def home(request):
    return render(request, 'home.html')

def company(request):
    return render(request, 'company.html')

def zoom(layout, x_range):
    print('yaxis updated')
    in_view = df.loc[figure.layout.xaxis.range[0]:figure.layout.xaxis.range[1]]
    figure.layout.yaxis.range = [in_view.High.min() - 10, in_view.High.max() + 10]

def get_data(request):
    try:
        s = request.POST['name']
        s = s.strip()

        com = yf.Ticker(s)
        x = com.info
        data = yf.download(tickers=s, period='1d', interval='1m')
        print(com.info)   
        timezon = com.info['exchangeTimezoneName']

        row = data.tail(1).reset_index()
        df = pd.DataFrame(row)
        print(df)
        dt = df.iat[0,0]

        price = "{:.2f}".format(df.iat[0,4])

        open_price = com.info['previousClose']
        diff = "{:.2f}".format(float(price) - float(open_price))
        diff1 = True
        if(float(diff)<0.0):
            diff1 = False

        per = "{:.2f}".format((float(price)*100)/float(open_price)-100)

        format1 = "%Y-%m-%d %H:%M:%S %Z%z"
        now_asia = dt.astimezone(timezone(timezon))
        dt = now_asia.strftime(format1)

        pre_close = com.info['previousClose']
        market_open = com.info['regularMarketOpen']
        market_high = com.info['regularMarketDayHigh']
        market_low = com.info['dayLow']
        
        try:
            longName = x['longName']
        except:
            longName = x['shortName']

        #1
        data = yf.download(tickers=s, period='5d',interval='1m')
        ss = data[['Adj Close']]
        data = ss.reset_index()
        data.columns = [0,1]
        x_data = data[0]
        y_data = data[1]

        layout=go.Layout( 
        xaxis={'title':'day'}, 
        yaxis={'title':'stock price ({})'.format(x['currency'])})
        fig = go.Figure(layout=layout)
        fig.add_trace(
        go.Scatter(x=x_data, y=y_data))
        fig.update_layout(
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                            label="1d",
                            step="day",
                            stepmode="backward"),
                        dict(count=2,
                            label="2d",
                            step="day",
                            stepmode="backward"),
                        dict(count=3,
                            label="3d",
                            step="day",
                            stepmode="backward"),
                        dict(count=4,
                            label="4d",
                            step="day",
                            stepmode="backward"),
                        dict(count=5,
                            label="5d",
                            step="day",
                            stepmode="backward")
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type="date"
            )
        )
        plot_div1 = plot(fig,output_type='div')

        #2
        data = yf.download(tickers=s, period='max',interval='1d')
        ss = data[['Adj Close']]
        print(ss)
        data = ss.reset_index()
        data.columns = [0,1]
        x_data = data[0]
        y_data = data[1]

        layout=go.Layout( 
        xaxis={'title':'Month'}, 
        yaxis={'title':'stock price ({})'.format(x['currency'])})
        fig = go.Figure(layout=layout)
        fig.add_trace(
        go.Scatter(x=x_data, y=y_data))

        fig.update_layout(
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                            label="1m",
                            step="month",
                            stepmode="backward"),
                        dict(count=6,
                            label="6m",
                            step="month",
                            stepmode="backward"),
                        dict(count=1,
                            label="YTD",
                            step="year",
                            stepmode="todate"),
                        dict(count=1,
                            label="1y",
                            step="year",
                            stepmode="backward"),
                        dict(count=2,
                            label="2y",
                            step="year",
                            stepmode="backward"),
                        dict(step="all")
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type="date"
            )
        )
        # fig.update_yaxes(showgrid=False)
        # fig.layout.on_change(zoom, 'xaxis.range')
        plot_div2 = plot(fig,output_type='div')

        sector = 'None'
        if('sector' in x.keys()):   
            sector = x['sector']

        Summary = 'None'
        if('longBusinessSummary' in x.keys()):   
            Summary = x['longBusinessSummary']

        website = 'None'
        if('website' in x.keys()):   
            website = x['website']

        city = 'None'
        if('city' in x.keys()):   
            city = x['city']

        state = 'None'
        if('state' in x.keys()):   
            state = x['state']

        country = 'None'
        if('country' in x.keys()):   
            country = x['country']

        phone = 'None'
        if('phone' in x.keys()):   
            phone = x['phone'] 

        return render(request, 'home.html',
                {   'currency':x['currency'],
                    'longname':longName, 
                    's':s, 
                    'cur_date':dt[0:23],
                    'cur_price': price,
                    'diff':diff,
                    'diff1':diff1, 
                    'per':per,
                    'close': pre_close,
                    'open' : market_open,
                    'day_high' : market_high,
                    'day_low' : market_low,
                    'plot_div1': plot_div1,
                    'plot_div2': plot_div2,
                    'sector' : sector,
                    'Summary' : Summary,
                    'website' : website,
                    'city' : city,
                    'state' : state,
                    'country' : country,
                    'phone' : phone,
                })
    except:
        return render(request,'home.html',{'error' : "Please enter valid symbol...."})
