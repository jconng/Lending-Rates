import os
import pandas as pd
import requests
from scipy.interpolate import interp1d


#excel file online
#https://www.fhlbdm.com/webres/File/fixed-rates-2000-present/FHLBDM_Historical_Rates.xlsx
#get all data into dataframe

url = 'https://www.fhlbdm.com/webres/File/fixed-rates-2000-present/FHLBDM_Historical_Rates.xlsx'
r = requests.get(url)
open('temp.xls', 'wb').write(r.content)
df = pd.read_excel('temp.xls')


#create dataframe from last row
df_rates=pd.DataFrame(df.iloc[-1,:])
df_rates=df_rates.reset_index()
df_rates.columns=['period','rate']

#drop 'Historical Rate Indications','Overnight', Week 1, 2, and 3 rows
df_rates.drop([0,1,2,3,4], axis=0, inplace=True)



#String to month number dictionary
period_keys=['1 Month', '2 Month', '3 Month', '4 Month', '5 Month', '6 Month', '7 Month', '8 Month', '9 Month', '10 Month', '11 Month', '1 Year', '1 1/2 Year', '2 Year', '3 Year', '4 Year', '5 Year', '6 Year', '7 Year', '8 Year', '9 Year', '10 Year', '11 Year', '12 Year', '13 Year', '14 Year', '15 Year', '16 Year', '17 Year', '18 Year', '19 Year', '20 Year', '25 Year', '30 Year']
period_values=[1,2,3,4,5,6,7,8,9,10,11,12,18,24,36,48,60,72,84,96,108,120,132,144,156,168,180,192,204,216,228,240,252,264]
time_dict =  dict(zip(period_keys, period_values))


#Remove weeks from df_rates dataframe (just in case)
df_rates=df_rates[(df_rates.period.str.contains('Year') | df_rates.period.str.contains('Month'))]

#replace 'Month 1' string by month number (as example), to all months and years
df_rates=df_rates.replace({"period": time_dict})

#create period and rate dictionary from dataframe
rates_dict = dict(zip(df_rates.period,df_rates.rate))


#Create new dataframe with 360 months
df_cof =pd.DataFrame( columns=['Month' , 'FHLBDM_Rate'])
df_cof.Month = list(range(1,361))
#Replace month rates with rates dictionary
df_cof.FHLBDM_Rate = df_cof.Month.map(rates_dict)

#feed the interpolate function only real numbers
f = interp1d(df_rates.period, df_rates.rate, kind='linear', fill_value="extrapolate")

#Your clean data frame with FHLB rates from Month 1 to 360
df_cof.FHLBDM_Rate = f(df_cof.Month)




