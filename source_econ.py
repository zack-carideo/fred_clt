import numpy as np
from pathlib import Path 
from fredapi import Fred

import matplotlib.pyplot as plt 

#https://fredaccount.stlouisfed.org/apikey
api_key = '0af08dd8b3b408fa68d70083c3af4dc1'
monthly = True

fred = Fred(api_key = api_key)


#SICK, YOU CAN PULL IN ALL FED TRACKED INFO , FOR CLT 
series_info = {"series_id":"MHINC37119A052NCEN"
               , "description":"estimate of median household income for mecklenburg county nc"
               , "url":"https://fred.stlouisfed.org/series/MHINC37119A052NCEN"
               }

clt_series_ids = ["MHINC37119A052NCEN","NCMECK9POP","MEDSQUFEE37119","GDPGOVT37119","NEWLISCOU37119","CBR37119NCA647NCEN","BPPRIV037119"
,"HOWNRATEACS037119","ATNHPIUS37119A","PCPI37119"
,"MEDLISPRIPERSQUFEE37119","ACTLISCOU37119","MEDLISPRI37119"
,"B01002001E037119","PENRATMM37119","S1701ACS037119","LDPEPRYYCOUNTY37119","PRIREDCOU37119"
]


#get sereis metadata
series_info = [fred.get_series_info(series_id=_id_).to_dict()
               for _id_ in clt_series_ids]



#get all series containing monthly data 
series_data = {x['title']: {'series':fred.get_series(series_id = x['id'] ) 
               }for x in series_info if x['frequency']=='Monthly'}

#generate basic transformations to view first and second derivatives of slope 
for k in series_data: 

    series_data[k]['mom_dif'] = (series_data[k]['series'] - series_data[k]['series'].shift(1))
    series_data[k]['qoq_dif'] = (series_data[k]['series'] - series_data[k]['series'].shift(3))
    series_data[k]['yoy_dif'] = (series_data[k]['series'] - series_data[k]['series'].shift(12))

    series_data[k]['mom_rat'] = (series_data[k]['series'] / series_data[k]['series'].shift(1))
    series_data[k]['qoq_rat'] = (series_data[k]['series'] / series_data[k]['series'].shift(3))
    series_data[k]['yoy_rat'] = (series_data[k]['series'] / series_data[k]['series'].shift(12))


    series_data[k]['mom_logdif'] = series_data[k]['mom_dif'].apply(lambda x: np.log(x))
    series_data[k]['qoq_logdif'] = series_data[k]['qoq_dif'].apply(lambda x: np.log(x))
    series_data[k]['yoy_logdif'] = series_data[k]['yoy_dif'].apply(lambda x: np.log(x))
    
    series_data[k]['mom_lograt'] = series_data[k]['mom_rat'].apply(lambda x: np.log(x))
    series_data[k]['qoq_lograt'] = series_data[k]['qoq_rat'].apply(lambda x: np.log(x))
    series_data[k]['yoy_logdif'] = series_data[k]['yoy_dif'].apply(lambda x: np.log(x))
    
    
    series_data[k]['series_ma3'] = series_data[k]['series'].rolling(3).mean()
    series_data[k]['series_ma6'] = series_data[k]['series'].rolling(6).mean()
    series_data[k]['series_ma12'] = series_data[k]['series'].rolling(12).mean()
    
    series_data[k]['series_pct_ch'] = series_data[k]['series'].pct_change()
    series_data[k]['series_ma3_pct_ch'] = series_data[k]['series_ma3'].pct_change()
    series_data[k]['series_ma6_pct_ch'] = series_data[k]['series_ma6'].pct_change()
    series_data[k]['series_ma12_pct_ch'] = series_data[k]['series_ma12'].pct_change()

    series_data[k]['ma3_mom_lograt'] = series_data[k]['mom_lograt'].rolling(3).mean()
    series_data[k]['ma6_mom_lograt'] = series_data[k]['mom_lograt'].rolling(6).mean()
    



#plot 
fig, (ax1, ax2) = plt.subplots(2, 1,figsize=(8,3))
fig.subplots_adjust(hspace=0.5)

ax1.plot(series_data[next(iter(series_data))]['series'].index, series_data[next(iter(series_data))]['series'].values)
ax1.plot(series_data[next(iter(series_data))]['series_ma3'].index, series_data[next(iter(series_data))]['series_ma3'].values)

#ax2.plot(series_data[next(iter(series_data))]['series_pct_ch'].index, series_data[next(iter(series_data))]['series_pct_ch'].values)
ax2.plot(series_data[next(iter(series_data))]['mom_lograt'].index, series_data[next(iter(series_data))]['mom_lograt'].values)
ax2.plot(series_data[next(iter(series_data))]['ma6_mom_lograt'].index, series_data[next(iter(series_data))]['ma6_mom_lograt'].values)

#ax2.plot(series_data[next(iter(series_data))]['qoq_logdif'].index, series_data[next(iter(series_data))]['qoq_logdif'].values)
#ax1.plot(series_data[next(iter(series_data))].index, series_data[next(iter(series_data))].values)
ax1.set_xlabel('Time')
ax1.set_title(next(iter(series_data)))
ax2.axhline(y = 0.0, color = 'pink', linestyle = '--')
plt.show()