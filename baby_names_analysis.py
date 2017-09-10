import numpy as np
import matplotlib.pyplot as pp
import pandas as pd
import seaborn


import zipfile #reading zip files
zipfile.ZipFile('names.zip').extractall('.')

import os
os.listdir('names')


open('names/yob2011.txt','r').readlines()[:10]


#creating data frame with columns names
names2011 = pd.read_csv('names/yob2011.txt',names=['name','sex','number'])


names2011.head()

names_all = []

for year in range(1880,2014+1):
    names_all.append(pd.read_csv('names/yob{}.txt'.format(year),names=['name','sex','number']))
    names_all[-1]['year'] = year

allyears = pd.concat(names_all)


allyears.head()

allyears.tail()

#Set index
allyears_indexed = allyears.set_index(['sex','name','year']).sort_index()

allyears_indexed


allyears_indexed.loc['F','Mary']


#Plot the graph by names

def plotname(sex, name):
    data = allyears_indexed.loc[sex, name]

    pp.plot(data.index, data.values)


pp.figure(figsize=(12,2.5))

names = ['Michael','John','David','Martin']

for name in names:
    plotname('M',name)

pp.legend(names)


pp.figure(figsize=(12,2.5))

names = ['Emily','Anna','Claire','Elizabeth']

for name in names:
    plotname('F',name)

pp.legend(names)


#Variance of similar names
pp.figure(figsize=(12,2.5))

names = ['Chiara','Claire','Clare','Clara','Ciara']

for name in names:
    plotname('F',name)

pp.legend(names)


allyears_indexed.loc['F'].loc[names].head()

allyears_indexed.loc['F'].loc[names].unstack(level=0).head()

#Filling NAN with 0

allyears_indexed.loc['F'].loc[names].unstack(level=0).fillna(0).head()

variants = allyears_indexed.loc['F'].loc[names].unstack(level=0).fillna(0)


#ploting the graph
pp.figure(figsize=(12,2.5))

pp.stackplot(variants.index,variants.values.T,label=names)


#Ploting with legends as stackplot doesnot supports legends, manually add legends
pp.figure(figsize=(12,2.5))

palette = seaborn.color_palette()
pp.stackplot(variants.index,variants.values.T,colors=palette)

for i,name in enumerate(names):
    pp.text(1882,5000 + 800*i,name,color=palette[i])


#Yearly top10 names

# Top names in 2008
allyears_indexed.loc['M',:,2008].sort_values('number',ascending=False).head()
pop2008 = allyears_indexed.loc['M',:,2008].sort_values('number',ascending=False).head()
pop2008.reset_index().drop(['sex','year','number'],axis=1).head()


def topten(sex, year):
    simple = allyears_indexed.loc[sex, :, year].sort_values('number', ascending=False).reset_index()
    simple = simple.drop(['sex', 'year', 'number'], axis=1).head(10)

    simple.columns = [year]
    simple.index = simple.index + 1

    return simple

topten('M',2009)




#Top name in years
def toptens(sex, year0, year1):
    years = [topten(sex, year) for year in range(year0, year1 + 1)]

    return years[0].join(years[1:])

toptens('M',2000,2010)

toptens('F',1985,1995)

toptens('F',1985,1995).stack().head()


toptens('F',1985,1995).stack().value_counts()


popular = toptens('F',1985,1995).stack().value_counts().index[:6]


# ploting Names
pp.figure(figsize=(12, 2.5))

for name in popular:
    plotname('F', name)

pp.legend(popular)

#Fading Names

#Identifying spiking in names

allyears.groupby(['sex','name']).sum().head()

#Removing years
allyears.groupby(['sex','name'])['number'].sum().head()

totals = allyears.groupby(['sex','name'])['number'].sum()

def sumsq(x):
    return sum(x**2)

spikyness = allyears.groupby(['sex','name'])['number'].agg(sumsq) / totals**2

spikyness.head()


spiky_common = spikyness[totals > 5000].copy()
spiky_common.sort_index(ascending=False)
spiky_common.head(10)

spiky_common.tail(5)


pp.figure(figsize=(12,2.5))

plotname('F','Louisa')
plotname('M','Shaquille')


fads = spiky_common.head(10).index.values


pp.figure(figsize=(12,2.5))

for sex,name in fads:
    plotname(sex,name)

pp.legend([name for sex,name in fads],loc='upper left')


totals_recent = allyears[allyears['year'] > 2005].groupby(['sex','name'])['number'].sum()


spiky_common = spikyness[(totals > 5000) & (totals_recent < 1000)].copy()
spiky_common.sort_index(ascending=False)
spiky_common.head(10)


fads = spiky_common.head(10).index.values


pp.figure(figsize=(12,2.5))

for sex,name in fads:
    plotname(sex,name)

pp.legend([name for sex,name in fads],loc='upper left')



#for every name, compute the total number of times that the name was used for boys, and the total number of times that it was used for girls.
# Then, identify unisex names where the ratio between the boys total and the girls total is less than four either way.
totals = allyears.groupby(['sex','name'])['number'].sum()


totals_bysex = totals.unstack('sex')
totals_bysex.head()


totals_both = totals_bysex.sum(axis = 1)
totals_both.head()

ratio = totals_bysex['F'] / totals_bysex['M']


ratio.head()

unisex = (ratio > 0.25) & (ratio < 4)


totals_both = totals_both[unisex]
totals_both.sort_values(ascending=False)
totals_both.head(5)


#Plot
pp.figure(figsize=(12, 12))

names = totals_both.head(10).index.values
for i, name in enumerate(names):
    pp.subplot(5, 2, i + 1)

    plotname('M', name)
    plotname('F', name)

    pp.legend([name + ' M', name + ' F'], loc='upper left')