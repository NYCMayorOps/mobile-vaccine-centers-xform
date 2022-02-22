import pandas as pd
import os
from pathlib2 import Path
import glob
from datetime import date, datetime, time




#import latest data to be converted. This is df1
#need string, not directory, for glob to work.
path = os.getcwd() + "\\input\\" + "*.xlsx"
print(path)
list_of_files = glob.glob(path) # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getmtime)
#read latest xlsx file in directory.
print(f"latest file: {latest_file}")
df1 = pd.read_excel(latest_file, skiprows=3)
print("df1:")
df1.info()

#import answer df2.
second_path = os.getcwd() + "\\samples\\" + "2021-01-06 CastLight update example.xlsx"
list_of_files = glob.glob(second_path)
answer_template_path = max(list_of_files, key=os.path.getmtime)
print(answer_template_path)
#df2 = pd.read_excel(answer_template_path)
#df2 = df2.truncate()
df2 = pd.DataFrame(columns=[
'flag', 
'unique_id', 
'id', 
'site_name', 
'state', 
'county', 
'address', 
'city', 
'zip_code', 
'phone_number', 
'testing_status', 
'appointment_required',
'physician_order_required',
'screening_required',
'restrictions_apply',
'restriction_details',
'type_of_center',
'rapid_testing',
'non_rapid_testing',
'guidelines',
'provider_url',
'antibody_testing',
'monday',
'tuesday',
'wednesday',
'thursday',
'friday',
'saturday',
'sunday',
'latitude',
'longitude',
'cost_of_test',
'open_date',
'close_date',
'minimum_age',
])


#xfer fields
h_and_h_location = [f"NYC Health + Hospitals/{x}" for x in df1['Location']]
#df2['site_name'] = pd.Series(h_and_h_location)
df2['site_name'] = h_and_h_location
#df2= df2.assign('site_name'= lambda x: )
def convert_borough_to_county(boro):
    boro = str.strip(boro).lower()
    if boro == "manhattan":
        return "New York"
    elif boro == "brooklyn":
        return "Kings"
    elif boro == "queens":
        return "Queens"
    elif boro == "bronx":
        return "Bronx"
    elif boro == "staten island":
        return "Richmond"
    elif boro == "flushing":
        return "Queens"
    else:
        raise Exception(f"{boro} is not a borough!")
county_series = [convert_borough_to_county(x) for x in df1['Borough']]
df2['county'] = pd.Series(county_series)
#aise Exception("stop here")
df2['address'] = df1['Address']

#get city from zipcode
zipcodes_df = pd.read_csv(os.getcwd() + "\\lookup\\us_zipcodes_by_city.csv")
zipcodes_df = zipcodes_df[['zip_code', 'default_city']]
df3 = pd.merge(df1, zipcodes_df, left_on='Zip', right_on='zip_code', how='inner')
df2['city'] = df3['default_city']
df2['zip_code'] = df1['Zip']

#rapid test. Search for text "rapid" in df1['Test Type']
def is_rapid(text):
    text = str.lower(text)
    if text.__contains__('rapid'):
        return True
    else:
        return False

rapid_test = [ "Y" if is_rapid(x) else '' for x in df1['Test Type']]
non_rapid_test = ["Y" if not is_rapid(x) else '' for x in df1['Test Type']]
df2['rapid_testing'] = rapid_test
df2['non_rapid_testing'] = non_rapid_test
df2['guidelines'] = df1['Test Type']


#days of the week
#get the date on the sheet
this_date = pd.read_excel(latest_file, nrows=1, header=None)[4]
this_date = this_date[0]
#find the monday of the week.
#parsed_date = datetime.strptime(this_date, "%m/%d/%Y")
parsed_date = this_date
year, week_num, day_of_week = parsed_date.isocalendar()

#assign variables mapping the days to dates
'''
dates_dict_bak =  {
    'monday': datetime.date.fromisocalendar(year, week_num, 1),
    'tuesday':datetime.date.fromisocalendar(year, week_num, 2),
    'wednesday': datetime.date.fromisocalendar(year, week_num, 3),
    'thursday': datetime.date.fromisocalendar(year, week_num, 4),
    'friday': datetime.date.fromisocalendar(year, week_num, 5),
    'saturday': datetime.date.fromisocalendar(year, week_num, 6),
    'sunday': datetime.date.fromisocalendar(year, week_num, 7)
}
'''

dates_dict = {
    'monday': pd.Timestamp.fromisocalendar(year, week_num, 1).strftime('%Y-%m-%d'),
    'tuesday':pd.Timestamp.fromisocalendar(year, week_num, 2).strftime('%Y-%m-%d'),
    'wednesday': pd.Timestamp.fromisocalendar(year, week_num, 3).strftime('%Y-%m-%d'),
    'thursday': pd.Timestamp.fromisocalendar(year, week_num, 4).strftime('%Y-%m-%d'),
    'friday': pd.Timestamp.fromisocalendar(year, week_num, 5).strftime('%Y-%m-%d'),
    'saturday': pd.Timestamp.fromisocalendar(year, week_num, 6).strftime('%Y-%m-%d'),
    'sunday': pd.Timestamp.fromisocalendar(year, week_num, 7).strftime('%Y-%m-%d')      
}
#parse the start and end date from the sheet.
start_dates = df1['Start Date']
end_dates = df1['End Date']
#create date ranges.
def find_range(start_date, end_date):
    delta = end_date - start_date
    date_range = []
    for i in range(delta.days + 1):
        #day = start_date + datetime.timedelta(days=i)
        day = start_date + pd.Timedelta(days=i)
        day = day.isoformat()
        day = day[0:10]
        date_range.append(day)
    return date_range

my_daterange = [ find_range(x, y) for x, y in zip(start_dates, end_dates) ]
#print(my_daterange)
def check_date(dates_dict, day_name, my_daterange):
    if f'{dates_dict[day_name]}' in my_daterange:
        return True
    else:
        #print(f"failed to match: {dates_dict[day_name]} and {my_daterange}")
        return False

def assign_time(index, df1, df2, day_name):
    df2.loc[index, day_name] = df1.loc[index, 'Open Hours']
    return df2
#for each of the days of the week:
    #if the date is between the start and end dates:
def assign_day(df1, df2, day_name, my_daterange):
    for i in range(0, len(df1)):
        if (check_date(dates_dict, day_name, my_daterange[i])):
            assign_time(i, df1, df2, day_name)
        #else assign none
    return df2

#input open hours into the day field.
df2 = assign_day(df1, df2, 'monday', my_daterange)
df2 = assign_day(df1, df2, 'tuesday', my_daterange)
df2 = assign_day(df1, df2, 'wednesday', my_daterange)
df2 = assign_day(df1, df2, 'thursday', my_daterange)
df2 = assign_day(df1, df2, 'friday', my_daterange)
df2 = assign_day(df1, df2, 'saturday', my_daterange)
df2 = assign_day(df1, df2, 'sunday', my_daterange)
print(df2[['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']])

df2['open_date'] = df1['Start Date']
df2['close_date'] = df1['End Date']
df2['minimum_age'] = df1['Age']

#constant fields
df2['flag'] = 'Add'
df2['state'] = 'NY'
df2['phone_number'] = "(844) 692-4692"
df2['testing_status'] = 'Testing'
df2['appointment_required'] = 'N'
df2['physician_order_required'] = 'N'
df2['screening_required'] = "In-Person Screening"
df2["restrictions_apply"] = 'N'
df2["type_of_center"] = "Walk up only"
df2["provider_url"] = "https://www.nychealthandhospitals.org/covid-19-testing-sites/?redirect&notification"
df2["antibody_testing"] = "N"
df2["cost_of_test"] = 0.0





#print("df2")
print(df2.info())
output_path = os.path.join(os.getcwd(), "output", f"mobile_testing_sites_{this_date.strftime('%Y-%m-%d')}.csv")

df2.to_csv(output_path)
