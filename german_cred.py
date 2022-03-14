#!/usr/bin/env python
# coding: utf-8

# In[29]:


import numpy as np
import pandas as pd
from pandas import Series
from pandas import DataFrame
from numpy import nan as NA
from matplotlib import pyplot as plt
from matplotlib import cm


# **Loading file into Pandas DataFrame**

# In[ ]:




german_file = open('GermanCredit.csv')
german = pd.read_csv(german_file)
german


# In[31]:


none_counts = []
for col in german.iteritems():
    none_count = 0
    for val in col[1].values:
        if str(val) == 'none':
            none_count += 1
    none_counts.append((col[0],none_count))
none_counts = sorted(none_counts, key=lambda x: x[1], reverse=True)
none_counts = none_counts[:3] #only top 3 columns with most 'none' values

# deleting the 3 columns with most 'none' values (18 cols now instead of 21)
for name, _ in none_counts:
    del german[name]
german.info()



# In[32]:


def remove_apostrophes(c):
    for row in c.index:
        if str(c[row]).find("'") != -1:
            c[row] = c[row].replace("'","")
    return c
german = german.apply(remove_apostrophes)
# All apostrophes have been removed!
print(german.head(5)) # Just showing a few rows here



# In[33]:


categories = {'no checking':'No Checking', '<0':'Low', '0<=X<200':'Medium', '>=200':'High'}
def change_check_status(c):
    if categories.get(c,0) == 0:
        return
    c = categories[c]
    return c
german['checking_status'] = german['checking_status'].apply(change_check_status)
# Checking Status has been changed!
german['checking_status']



# In[34]:


categories = {'no known savings':'No Savings','<100':'Low','100<=X<500':'Medium',
              '500<=X<1000':'High','>=1000':'High'}
def change_savings_status(c):
    if categories.get(c,0) == 0:
        return
    c = categories[c]
    return c
german['savings_status'] = german['savings_status'].apply(change_savings_status)
# Savings Status has been changed!
german['savings_status']



# In[35]:


def change_class(c):
    if c=='good':
        return '1'
    return '0'
german['class'] = german['class'].apply(change_class)
# Class has been changed!
german['class']


# Change the employment column value 'unemployed' to 'Unemployed', and for the others, change to 'Amateur', 'Professional', 'Experienced' and 'Expert', depending on year range.**

# In[36]:


categories = {'unemployed':'Unemployed','<1':'Amateur','1<=X<4':'Professional',
              '4<=X<7':'Experienced','>=7':'Expert'}
def change_employment(c):
    return categories[c]
german['employment'] = german['employment'].apply(change_employment)
# Employment has been changed!
german['employment']




# In[37]:


# Good credit = 1, Bad credit = 0
pd.crosstab(german['class'],german['foreign_worker'])




# In[38]:


pd.crosstab(german['savings_status'],german['employment'])



# In[39]:


ser = german.groupby(['employment','personal_status'])['credit_amount'].mean()
# '4<=X<7' years of employment = 'Experienced'
ser[('Experienced','male single')]



# In[40]:


ser = german.groupby('job')['duration'].mean()
ser.name = 'Average Credit Duration per Job Type'
ser



# In[41]:


# Filtering DataFrame- shows only rows where purpose=='education'
df = german[german['purpose']=='education']

# For checking_status
a = pd.crosstab(df['purpose'],df['checking_status'])
max_check = a.loc['education'].max()
for row in a.iterrows():
    ser = row[1]
    for i in ser.index: # Looping through names to see which status is most common
        if ser[i] == max_check:
            mc_check = i # most common checking status
print(f'Most common checking status: {mc_check}')

# For savings_status
b = pd.crosstab(df['purpose'],df['savings_status'])
max_savings = b.loc['education'].max()
for row in b.iterrows():
    ser = row[1]
    for i in ser.index: # Looping through names to see which status is most common
        if ser[i] == max_savings:
            mc_savings = i # most common checking status
print(f'Most common savings status: {mc_savings}')



# #### 1. Subplots of two histograms

# In[50]:


fig, axes = plt.subplots(2,1,figsize=(26,16))
axes1, axes2 = axes.flatten()

width= 0.15

subplot1 = german.groupby(['personal_status','savings_status'])['checking_status'].count().reset_index()
subplot2 = german.groupby(['personal_status','checking_status'])['savings_status'].count().reset_index()

#1st 
xaxis1 = np.arange(len(subplot1['savings_status'].unique()))
axes1.bar(xaxis1 - 2*width, subplot1[subplot1['personal_status']=='female div/dep/mar']['checking_status'] , width=width , label = 'female div/dep/mar')
axes1.bar(xaxis1 - width, subplot1[subplot1['personal_status']=='male div/sep']['checking_status'] , width=width , label = "male div/sep")
axes1.bar(xaxis1 , subplot1[subplot1['personal_status']=='male mar/wid']['checking_status'] , width = width , label = "male mar/wid" )
axes1.bar(xaxis1 + width , subplot1[subplot1['personal_status']=='male single']['checking_status'] , width = width , label = "male single")

axes1.set_title('Personal Status with Saving Status', fontsize=16)
axes1.set_xticks(ticks=xaxis1)
axes1.set_xticklabels(labels=list(subplot1['savings_status'].unique()))
axes1.set_xlabel('Personal Status', fontsize=13)
axes1.legend(loc='center left', bbox_to_anchor=(1,0.5))

#2nd
xaxis2 = np.arange(len(sub2['checking_status'].unique()))
axes2.bar(xaxis2 - 2*width, subplot2[subplot2['personal_status']=='female div/dep/mar']['savings_status'] , width=width , label = 'female div/dep/mar')
axes2.bar(xaxis2 - width, subplot2[subplot2['personal_status']=='male div/sep']['savings_status'] , width=width , label = "male div/sep")
axes2.bar(xaxis2 , subplot2[subplot2['personal_status']=='male mar/wid']['savings_status'] , width = width , label = "male mar/wid" )
axes2.bar(xaxis2 + width , subplot2[subplot2['personal_status']=='male single']['savings_status'] , width = width , label = "male single")

axes2.set_title('Checking Status based on personal status',fontsize=16)
axes2.set_xticks(ticks = xaxis2)
axes2.set_xticklabels(labels = list(subplot2['checking_status'].unique()))
axes2.set_xlabel('Checking Status',fontsize=13)
axes2.legend(loc='center left', bbox_to_anchor=(1, 0.50))


# In[47]:





# #### Average customer age vs. Property Magnitude of people having credit > 4000

# In[54]:


g2 = german[german['credit_amount']>4000].groupby(['property_magnitude'])['age'].mean().reset_index()

figure = plt.figure(figsize=(15,5))
plt.bar(g2['property_magnitude'], g2['age'])
plt.title('Average Customer age of property for people with credit greater than 4000')
plt.xlabel('Property magnitude', fontsize=13)
plt.ylabel('Average Age', fontsize=13)


# #### 3. Pie chart subplots

# In[58]:


figure, axes = plt.subplots(1,3, figsize = (21,7))
axes1, axes2, axes3 = axes.flatten()

subplot1 = german[(german['savings_status']=='High')&(german['age']>40)].groupby(['personal_status'])['checking_status'].count().reset_index()
subplot2 = german[(german['savings_status']=='High')&(german['age']>40)].groupby(['credit_history'])['checking_status'].count().reset_index()
subplot3 = german[(german['savings_status']=='High')&(german['age']>40)].groupby(['job'])['checking_status'].count().reset_index()

axes1.pie(subplot1['checking_status'],labels=list(subplot1['personal_status'].unique()))
axes1.set_title('personal_status',fontsize=16)

axes2.pie(subplot2['checking_status'],labels=list(subplot2['credit_history'].unique()))
axes2.set_title('credit_history',fontsize=16)

axes3.pie(subplot3['checking_status'],labels=list(subplot3['job'].unique()))
axes3.set_title('job',fontsize=16)


# In[ ]:





# In[ ]:





# In[ ]:




