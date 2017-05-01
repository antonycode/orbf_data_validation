import pandas as pd
import pickle

import sys
sys.path.insert(0, '../monitoring_algorithms/')
from facility_monitoring import *

pkl_file = open( '../../data/processed/TEMP_facilities_aedes.pkl', 'rb')
facilities = pickle.load(pkl_file)
pkl_file.close()


fac = facilities[0]

def get_verification_path(facility_data , algorithm_name):
    supervisions = facility_data.supervisions
    facility_name = facility_data.facility_name
    departement = facility_data.departement
#
    if algorithm_name not in list(supervisions.columns) :
        print('Algorithm ' + algorithm_name + ' does not seem to have been run on ' + facility_name)
    if (algorithm_name in list(supervisions.columns)) :
        verified_months =  supervisions.index[supervisions[algorithm_name].isin([True , 'Initial Training'])]
        unverified_months = supervisions.index[supervisions[algorithm_name] == False]
        verified_data =  pd.DataFrame([] , index = [])
        claimed_data =  pd.DataFrame([] , index = [])
        if (len(list(verified_months)) > 0) | (type(verified_months) == 'Period') :
            try :
                verified_data = facility_data.reports.loc[list(verified_months) , ['indicator_claimed_value'  , 'indicator_verified_value' , 'indicator_tarif']]
                verified_data.columns = ['indicator_claimed_value' ,'indicator_validated_value' , 'indicator_tarif']
            except KeyError :
                pass
        if len(list(unverified_months)) > 0 | (type(unverified_months) == 'Period') :
            try :
                claimed_data = facility_data.reports.loc[list(unverified_months) , ['indicator_claimed_value'  , 'indicator_claimed_value' , 'indicator_tarif']]
                claimed_data.columns = ['indicator_claimed_value' , 'indicator_validated_value' , 'indicator_tarif']
            except ( KeyError , TypeError ):
                pass

        validated_data = verified_data.append(claimed_data)
        validated_data['facility_name'] = facility_name
        validated_data['departement'] = departement

        validated_data = pd.merge(validated_data , supervisions , left_index = True , right_index = True)

        if len(validated_data) > 0 :
            try :
                validated_data = validated_data.reset_index().set_index(['departement' , 'facility_name' , 'period'  , 'indicator_label']).reorder_levels(['departement' , 'facility_name' , 'period' , 'indicator_label']).sort_index()
            except KeyError :
                pass

    return validated_data



validation_path = get_verification_path(fac , 'aedes' )


validation_path.head()
## TODO groupby this so it can extract different algorithms pathes

def get_interesting_quantities(validated_path):
    validated_path


######

import matplotlib.pyplot as plt


%matplotlib inline
plt.plot(a.indicator_claimed_value , a.indicator_validated_value , 'o')





def bar_cols(col_data , order_cols = ['green' , 'orange' , 'red']):
    o = []
    for col in order_cols:
        try :
            n = col_data.loc[col]
            o.append(n)
        except KeyError :
            o.append(0)

    plt.bar([0,1,2], o , color = order_cols)
    plt.xticks([0,1,2] , order_cols)

#classes_counts = u.groupby(level = 0).Class.value_counts()
#fig=plt.figure(figsize=(18, 16) , dpi= 80, facecolor='w', edgecolor='k')
#for i in range(1,17):
#    plt.subplot(4,4,i)
#    departement = list(classes_counts.index.levels[0])[i-1]
#    bar_cols(classes_counts.loc[departement])
#    departement =departement.replace('’' , "'")
#    plt.title(departement , fontsize=15)