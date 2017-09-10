import pandas as pd

s = pd.Series([0,1,4,9,16,25],name='squares')

s

s.values

s.index

s[0]

s[2]

s[2:4]

#indexing bu values
pop2014 = pd.Series([100,99.3,95.5,93.5,92.4,84.8,84.5,78.9,74.3,72.8],
                    index=['Java','C','C++','Python','C#','PHP','JavaScript','Ruby','R','Matlab'])

pop2014

pop2014.index

pop2014[0]

pop2014[0:2]

pop2014['Python']

pop2014['C++':'C#']


#retriving values by index
pop2014.iloc[0:2]


#retriving values by name
pop2014.loc[:'Ruby']

pop2014[pop2014 > 90]

pop2015 = pd.Series({'Java': 100,'C': 99.9,'C++': 99.4,'Python': 96.5,'C#': 91.3,
                     'R': 84.8,'PHP': 84.5, 'JavaScript': 83.0, 'Ruby': 76.2, 'Matlab': 72.4})

pop2015


#Part 2
pop2014 = pd.Series([100,99.3,95.5,93.5,92.4,84.8,84.5,78.9,74.3,72.8],
                    index=['Java','C','C++','Python','C#','PHP','JavaScript','Ruby','R','Matlab'])

pop2015 = pd.Series({'Java': 100,'C': 99.9,'C++': 99.4,'Python': 96.5,'C#': 91.3,
                     'R': 84.8,'PHP': 84.5,'JavaScript': 83.0,'Ruby': 76.2,'Matlab': 72.4})

#merging data
twoyears = pd.DataFrame({'2014': pop2014,'2015': pop2015})

twoyears

twoyears = twoyears.sort('2015',ascending=False)

twoyears

twoyears.values

twoyears.index

twoyears.columns

twoyears['2014']

twoyears.iloc[0:2]

twoyears.loc['C':'Python']

twoyears['avg'] = 0.5*(twoyears['2014'] + twoyears['2015'])

twoyears

presidents = pd.DataFrame([{'name': 'Barack Obama','inauguration': 2009,'birthyear': 1961},
                          {'name': 'George W. Bush','inauguration': 2001,'birthyear': 1946},
                          {'name': 'Bill Clinton','birthyear': 1946,'inauguration': 1993},
                          {'name': 'George H. W. Bush','inauguration': 1989,'birthyear': 1924}])

presidents


#Set index to change the index
presidents_indexes = presidents.set_index('name')

presidents_indexes

presidents_indexes.loc['Bill Clinton']

presidents_indexes.loc['Bill Clinton']['inauguration']

presidents_indexes['inauguration']['Bill Clinton']

presidents_fathers = pd.DataFrame([{'son': 'Barack Obama','father': 'Barack Obama, Sr.'},
                                   {'son': 'George W. Bush','father': 'George H. W. Bush'},
                                   {'son': 'George H. W. Bush','father': 'Prescott Bush'}])

pd.merge(presidents,presidents_fathers,left_on='name',right_on='son')

pd.merge(presidents,presidents_fathers,left_on='name',right_on='son').drop('son',axis=1)

pd.merge(presidents,presidents_fathers,left_on='name',right_on='son',how='left').drop('son',axis=1)

pd.DataFrame(np.random.choice(['a','b','c','d'],(3,3)),index=[1,2,3],columns=['A','B','C'])

#part 4:
flights = seaborn.load_dataset('flights')

flights.head()

flights_indexed = flights.set_index(['year','month'])
flights_indexed.head()

flights_indexed.loc[1949]

flights_indexed.loc[1949:1950]

flights_indexed.loc[1949,'January']

flights_indexed.loc[1949].loc['January':'June']

flights_unstacked = flights_indexed.unstack()

flights_unstacked

flights_unstacked.sum(axis=1)

flights_unstacked['passengers','total'] = flights_unstacked.sum(axis=1)

flights_unstacked

flights_restacked = flights_unstacked.stack()

flights_restacked

flights_restacked.loc[pd.IndexSlice[:,'total'],'passengers']

flights_restacked[flights_restacked['passengers'] > 120]


#part 4:
open('tips.csv','r').readlines()[:10]

tips = pd.read_csv('tips.csv')

tips.head()

tips.mean()

tips.describe()

tips.groupby('sex').mean()

tips.groupby(['sex','smoker']).mean()

pd.pivot_table(tips,'total_bill','sex','smoker')

pd.pivot_table(tips,'total_bill',['sex','smoker'],['day','time'])