import numpy as np
import matplotlib.pyplot as pp
import seaborn  # makes plot prety

import urllib.request  # downloading the file from noaa
urllib.request.urlretrieve('ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.txt','stations.txt')

open('stations.txt','r').readlines()[:10]

#Reading data of only has GSN
#specifically, we will use data from the GCOS Surface Network, a global reference network of observation stations.
stations={}

for line in open('stations.txt','r'):
    if 'GSN' in line:
        fields=line.split()
        stations[fields[0]]=''.join(fields[4:])

#fucntion to find station by name

def findstation(s):
    found = {code: name for code,name in stations.items() if s in name}
    print(found)


findstation('LIHUE')
#{'USW00022536': 'HI LIHUE WSO AP 1020.1 GSN 91165'}

findstation('SAN DIEGO')
#{'USW00023188': 'CA SAN DIEGO LINDBERGH FLD GSN 72290'}

findstation('MINNEAPOLIS')
#{'USW00014922': 'MN MINNEAPOLIS/ST PAUL AP GSN HCN 72658'}

findstation('IRKUTSK')
#{'RSM00030710': 'IRKUTSK GSN 30710'}

#Open the data of Lihue The daily weather files for the stations that we have selected can be found in a no-i repository.
open('USW00022536.dly','r').readlines()[:10]

open('readme.txt','r').readlines()[98:121]


dly_delimiter = [11,4,2,4] + [5,1,1,1] * 31
dly_usecols = [1,2,3] + [4*i for i in range(1,32)]
dly_dtype = [np.int32,np.int32,(np.str_,4)] + [np.int32] * 31
dly_names = ['year','month','obs'] + [str(day) for day in range(1,31+1)]

def parsefile(filename):
    return np.genfromtxt(filename,
                         delimiter = dly_delimiter,
                         usecols = dly_usecols,
                         dtype = dly_dtype,
                         names = dly_names)


lihue = parsefile('USW00022536.dly')


# the temperatures for all the days of the month sit on the same row, which is inconvienient because different months have different numbers of days.
#  Instead, each day should have a separate row. Also, I would like to associate each data point with a proper NumPy datetime object.

def unroll(record):
    startdate = np.datetime64('{}-{:02}'.format(record['year'], record['month']))
    dates = np.arange(startdate, startdate + np.timedelta64(1, 'M'), np.timedelta64(1, 'D'))
    rows = [(date, record[str(i + 1)] / 10) for i, date in enumerate(dates)]
    return np.array(rows, dtype=[('date', 'M8[D]'), ('value', 'd')])

unroll(lihue[0])

#We also want to select a single observable, such as minimum temperature. For this we write a function getobs for get observable.

def getobs(filename,obs):
    return np.concatenate([unroll(row) for row in parsefile(filename) if row[2] == obs])

getobs('USW00022536.dly','TMIN')


#Part- Handling missing data
 #1 marking it as not a number using NumPy Boolean masks.
# 2 replacing it with Interpolated values using the numpy.interp function

lihue_tmax = getobs('USW00022536.dly','TMAX')
lihue_tmin = getobs('USW00022536.dly','TMIN')


pp.plot(lihue_tmax['date'],lihue_tmax['value'])


#Converting 999.9 values to nan
def getobs(filename, obs):
    data = np.concatenate([unroll(row) for row in parsefile(filename) if row[2] == obs])

    data['value'][data['value'] == -999.9] = np.nan

    return data

lihue_tmax = getobs('USW00022536.dly','TMAX')
lihue_tmin = getobs('USW00022536.dly','TMIN')


def fillnans(data):
    dates_float = data['date'].astype(np.float64) # modify dates to float
    nan = np.isnan(data['value'])
    data['value'][nan] = np.interp(dates_float[nan], dates_float[~nan], data['value'][~nan]) #use interpolate function to fill nan

fillnans(lihue_tmax)
fillnans(lihue_tmin)

np.mean(lihue_tmin['value']), np.mean(lihue_tmax['value'])


#Part 4 : Smoothing
#Smothing Data using Running Mean

# will smooth out short-term oscillations. There are many ways to do it but generally, it involves averaging other nearby values.
# For simplicity, just take a running mean, that is a mean over a limited window centered at the data point.


#The nampy function correlate multiplies the sliding section of a one-dimensional array with another shorter array,
#  computes the sum of the multiplied values and stores that in a new array.
# This is just what we need for the running mean if we set the shorter array to one divided by its size.
def plot_smoothed(t, win=10):
    smoothed = np.correlate(t['value'], np.ones(win) / win, 'same')

    pp.plot(t['date'], smoothed)



#In the graph we see that on the edges the graph runs out of smoothing to average
pp.plot(lihue_tmin[10000:12000]['date'],lihue_tmin[10000:12000]['value'])
plot_smoothed(lihue_tmin[10000:12000])
plot_smoothed(lihue_tmin[10000:12000],30)


datastations = ['USW00022536','USW00023188','USW00014922','RSM00030710']
pp.figure(figsize=(10, 6))  # increase the size of the image
for i, code in enumerate(datastations):
    pp.subplot(2, 2, i + 1)
    plot_smoothed(getobs('{}.dly'.format(code), 'TMIN'), 365)
    plot_smoothed(getobs('{}.dly'.format(code), 'TMAX'), 365)
    pp.title(stations[code])
    pp.axis(xmin=np.datetime64('1952'), xmax=np.datetime64('2012'), ymin=-10, ymax=30)

pp.tight_layout()



# Plot temperature data for a year by plotting, also, historical records,
# that is the most extreme temperatures achieved on that day of the year across all available years.

def selectyear(data, year):
    start = np.datetime64('{}'.format(year))
    end = start + np.timedelta64(1, 'Y')

    return data[(data['date'] >= start) & (data['date'] < end)]['value']

lihue_tmin_all = np.vstack([selectyear(lihue_tmin,year)[:365] for year in range(1951,2014+1)]) # 365 days of year

lihue_tmin_all.shape
selectyear(lihue_tmin,1951)

lihue_tmin_recordmin = np.min(lihue_tmin_all,axis=0)
lihue_tmin_recordmax = np.max(lihue_tmin_all,axis=0)

pp.plot(lihue_tmin_recordmax,'.')

lihue_tmax_all = np.vstack([selectyear(lihue_tmax,year)[:365] for year in range(1951,2014+1)])


#ploting
pp.figure(figsize=(12,4))
days = np.arange(1,365+1)
pp.fill_between(days,np.min(lihue_tmin_all,axis=0),np.max(lihue_tmin_all,axis=0),alpha=0.4)
pp.plot(selectyear(lihue_tmin,2009))
pp.fill_between(days,np.min(lihue_tmax_all,axis=0),np.max(lihue_tmax_all,axis=0),alpha=0.4)
pp.plot(selectyear(lihue_tmax,2009))
pp.axis(xmax=365)

#Part 5:Minneapolis; analyze the data to find the year with the lowest mean TMIN in San Diego, a warm place; then in the same plot, show the TMIN
# and TMAX series for those years and for those two cities.
minneapolis_tmax = getobs('USW00014922.dly','TMAX')
minneapolis_tmin = getobs('USW00014922.dly','TMIN')
sandiego_tmax = getobs('USW00023188.dly','TMAX')
sandiego_tmin = getobs('USW00023188.dly','TMIN')

fillnans(minneapolis_tmax)
fillnans(minneapolis_tmin)
fillnans(sandiego_tmax)
fillnans(sandiego_tmin)

years = np.arange(1940,2014+1)

minneapolis_tmax_all = np.vstack([selectyear(minneapolis_tmax,year)[:365] for year in years])

minneapolis_mean = np.mean(minneapolis_tmax_all,axis=1)

pp.plot(years,minneapolis_mean)

minneapolis_warmest = years[np.argmax(minneapolis_mean)]
minneapolis_warmest

sandiego_tmin_all = np.vstack([selectyear(sandiego_tmin,year)[:365] for year in years])
sandiego_mean = np.mean(sandiego_tmin_all,axis=1)
sandiego_coldest = years[np.argmin(sandiego_mean)]
sandiego_coldest


#Plotting the data
pp.figure(figsize=(12,4))
days = np.arange(1,366+1)
pp.fill_between(days,
                selectyear(minneapolis_tmin,minneapolis_warmest),
                selectyear(minneapolis_tmax,minneapolis_warmest),
                color='b',alpha=0.4)
pp.fill_between(days,
                selectyear(sandiego_tmin,sandiego_coldest),
                selectyear(sandiego_tmax,sandiego_coldest),
                color='r',alpha=0.4)
pp.axis(xmax=366)
pp.title('{} in Minneapolis vs. {} in San Diego'.format(minneapolis_warmest,sandiego_coldest))