import numpy as np
import pandas as pd
from pandas_datareader import data as web
from sklearn.preprocessing import MinMaxScaler
from tensorflow.python.keras.layers import Dense,Dropout,LSTM
from tensorflow.python.keras.models import Sequential,load_model
import tensorflow as tf
import random
from datetime import datetime,timedelta
import yfinance as yfin
import sys
import requests
import time

yfin.pdr_override() 

while True:
    # The model is trained to take yesterdays' price data, but between 12pm and 7am, yahoo finance hasn't posted the next days' prices, so we use what seems like todays' prices
    current_time=datetime.now().strftime('%H')
    if int(current_time[0])==0 and int(current_time[1])<=6: # Time between 12pm and 7am
        start_type_1=None # Till USA time today-Greece time yesterday
        start_type_2=0 # We use it with 2 different methods
    else:
        start_type_1=-1 # Till yesterday
        start_type_2=-1

    while True:
        predict_type_answer=input("\nPress (1) to predict the 'Top Cryptos of the Day' or (2) to predict a specific coin: ")
        if predict_type_answer=='1' or predict_type_answer=='2':
            break

    url='https://api.coingecko.com/api/v3/coins/markets'
    if predict_type_answer=='1': # Will look through the top cryptos find which one will have the biggest increase
        # Send a GET request to the CoinGecko API to retrieve the top 100 cryptocurrencies by market cap
        params={'vs_currency':'usd','order':'market_cap_desc','per_page':100}

        while True:
            try:
                crypto_data=requests.get(url,params=params).json()
                break
            except requests.exceptions.ConnectionError:
                print('\nNo internet connection!')
                time.sleep(5)
                
        # Extract the names of the cryptocurrencies from the API response
        crypto_names=[coin['symbol'] for coin in crypto_data]
        percentage_change=[] # For later
    else:
        crypto_names=[input('\nWhich coin do you want to predict: ')]
            
    for i in range(len(crypto_names)):
        print('\nCrypto',str(i+1)+'/'+str(len(crypto_names)))

        # Finds if this crypto is in the database
        already_analysed_crypto=pd.read_csv('C:/Users/Kostas/Desktop/Codes/Crypto Price Prediction/Data_Analysed.csv')
        with open('C:/Users/Kostas/Desktop/Codes/Crypto Price Prediction/Data_Analysed.csv','r') as file:
            new_coin_flag=True
            pos=len(already_analysed_crypto)
            for j in range(len(already_analysed_crypto)):
                if crypto_names[i]==already_analysed_crypto.loc[j,'Ticker_Name']: 
                    new_coin_flag=False
                    pos=j
        
        prediction_days=150
        if new_coin_flag: # If its a new coin it adds it to the database
                next_date=datetime.strptime('2000-01-01','%Y-%m-%d') # Random date to avoid bug later
                start_date=None # From which date to start getting data (None=from the start)
        else: # If its not a new coin it's just get the date
            next_date=datetime.strptime(already_analysed_crypto.loc[pos,'Next_Date'],'%Y-%m-%d') # The last date this coin was fitted (It doesn't have to do the fitting again, till this date)
            start_date=next_date-timedelta(days=prediction_days) # It needs prediction_days days of past data to make a prediction for one new day

        continue_flag=False
        while True:
            try:
                print('\nGathering data...\n')
                fiat_currency='USD' # Small cryptos don't have a euro comparison, will convert it later
                temp_usd_to_eur=web.get_data_yahoo('USDEUR=X') # The rate fee for usd to eur
                usd_to_eur=temp_usd_to_eur['Adj Close'][-1] # The rate for today

                train_data=web.get_data_yahoo(f'{crypto_names[i]}-{fiat_currency}',start=start_date)
                if len(train_data)<prediction_days+1-start_type_2: # The program needs 151 days of data to work, it blocks coins that it doesn't have enough data on
                    continue_flag=True
                    break

                # Keeps only the close-highest price of yesterday and converts it to a 0-1 format, because it's easier to work with
                # Every 1 variable is for the adjusted close prediction and every 2 variable is for the highest price prediction
                scaler_1=MinMaxScaler(feature_range=(0,1)) 
                close_scaled_data=scaler_1.fit_transform(train_data['Adj Close'][:start_type_1].values.reshape(-1,1)) 
                
                scaler_2=MinMaxScaler(feature_range=(0,1))
                high_scaled_data=scaler_2.fit_transform(train_data['High'][:start_type_1].values.reshape(-1,1))

                break # If it reaches here, it means that there is enough data on the coin inputed and there is a stable connection
            except IndexError:
                # If it reaches here, it means that there is not a stable connection
                print('\nNo internet connection')
                time.sleep(5)

        # The model is trained by taking the last prediction_days days worth of data (every x_train index), starting from the start and continuing 
        # And predicting the next day (every y_train index)
        # Reminder, this is just the training of the model and it's not predicting future prices, just yet
        
        current_day=datetime.today().strftime('%d/%m/%Y') # Normal format for printing
        if next_date.strftime('%Y-%m-%d')!=datetime.now().strftime('%Y-%m-%d'): # If last time the model was fitted was today, it doesn't need to do it again
            if continue_flag: 
                if predict_type_answer=='1':
                    percentage_change.append(0) # No change since it's not going to look through this coin (have to do this for prediction type 1)
                continue
            x_train_2,y_train_2=[],[]
            for j in range(prediction_days,len(close_scaled_data)):
                x_train_2.append(high_scaled_data[j-prediction_days:j,0])
                y_train_2.append(high_scaled_data[j,0])

            # The data needs to have this specific format, to be trained
            x_train_2,y_train_2=np.array(x_train_2),np.array(y_train_2)
            x_train_2=np.reshape(x_train_2,(x_train_2.shape[0],x_train_2.shape[1],1))

            # Uses a set seed so not to get different results eah time
            random.seed(42)
            np.random.seed(42)
            tf.random.set_seed(42)

            # Creates the neural network
            # It will be trained to predict high prices, but we will also predict close prices with it because if I create 2 models they will work way differently 
            # Which will cause the 2 prediction to not collerate very well with each other, eg the close price will be higher than the high price
            # Its not best practice but I only really care about the high price and the close price is just there to give a general idea
            print('\nTraining the model...\n')

            if not new_coin_flag: # If its not a new coin, on the database, it loads the model that has been trained already, on the past data
                model=load_model('C:/Users/Kostas/Desktop/Codes/Crypto Price Prediction/Coins/'+crypto_names[i])

            model=Sequential()

            model.add(LSTM(units=30,return_sequences=True,input_shape=(x_train_2.shape[1],1)))
            model.add(LSTM(units=30,return_sequences=True))
            model.add(LSTM(units=30))
            model.add(Dense(units=1))

            model.compile(optimizer='adam',loss='mean_squared_error')
            model.fit(x_train_2,y_train_2,epochs=70,batch_size=20)
            model.save('C:/Users/Kostas/Desktop/Codes/Crypto Price Prediction/Coins/'+crypto_names[i])

            # Testing the model

            # Getting the data of the last prediction_days days
            x_test_1=[close_scaled_data[-prediction_days:]]
            x_test_1=np.array(x_test_1)

            x_test_2=[high_scaled_data[-prediction_days:]]
            x_test_2=np.array(x_test_2)

            # Making the predictions
            prediction_1=model.predict(x_test_1)
            prediction_1=scaler_1.inverse_transform(prediction_1)*usd_to_eur

            prediction_2=model.predict(x_test_2)
            prediction_2=scaler_2.inverse_transform(prediction_2)*usd_to_eur

            percentage_change_temp=((prediction_2[0][0]-(train_data['High'][start_type_2-1]*usd_to_eur))/prediction_2[0][0])*100
            if predict_type_answer=='1': # Appends the increase or decrease of the price from yesterday's actual price to todays' prediction
                percentage_change.append(percentage_change_temp)
            else:
                print('\n| Prediction for',current_day,'| [Highest price]:',prediction_2[0][0],'| [Close price]:',prediction_1[0][0],'| [Change]:',str(round(percentage_change_temp,2))+'% |')
            
            date=datetime.now().strftime('%Y-%m-%d') # Format needed for the api
            if new_coin_flag: # If its a new coin it appends all the data
                with open('C:/Users/Kostas/Desktop/Codes/Crypto Price Prediction/Data_Analysed.csv','a') as file:
                    file.write(crypto_names[i]+','+date+','+str(prediction_2[0][0])+','+str(prediction_1[0][0])+'\n')
            else: # Else it only updates the date and the last predictions
                already_analysed_crypto.loc[pos,'Next_Date']=date 
                already_analysed_crypto.loc[pos,'High_Prediction']=prediction_2[0][0]
                already_analysed_crypto.loc[pos,'Close_Prediction']=prediction_1[0][0]
                already_analysed_crypto.to_csv('C:/Users/Kostas/Desktop/Codes/Crypto Price Prediction/Data_Analysed.csv',index=False)
        else:
            prediction_2=already_analysed_crypto.loc[pos,'High_Prediction']
            prediction_1=already_analysed_crypto.loc[pos,'Close_Prediction']

            percentage_change_temp=((prediction_2-(train_data['High'][start_type_2-1]*usd_to_eur))/prediction_2)*100
            if predict_type_answer=='1':
                percentage_change.append(((prediction_2-(train_data['High'][start_type_2-1]*usd_to_eur))/prediction_2)*100)
            else:
                print('\n| Prediction for',current_day,'| [Highest price]:',prediction_2,'| [Close price]:',prediction_1,'| [Change]:',str(round(percentage_change_temp,2))+'% |')

    if predict_type_answer=='1': # To print the top 5 best cryptos for the day
        temp_percentage_change=percentage_change[:]
        print('\nTop 5 Cryptos of the Day:\n')
        for j in range(5): # For each crypto on the top 5
            # It finds the max on the temp array and then the index of it on the actual array, because we remove each max item every time to find the next one, so the index of temp array changes 
            max_num=max(temp_percentage_change) 
            for k in range(len(percentage_change)):
                if percentage_change[k]==max_num:
                    pos=k

            print(crypto_names[pos]+':',str(round(percentage_change[pos],2))+'%')
            temp_percentage_change.pop(temp_percentage_change.index(max(temp_percentage_change)))

    while True:
        answer=input('\nPress (Q) to quit or (R) to make another prediction: ').upper()
        if answer=='Q' or answer=='R':
            if answer=='Q':
                sys.exit()
            break
