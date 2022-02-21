import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image

## navigation bar
st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)

st.markdown("""
<nav class="navbar fixed-top navbar-expand-lg navbar-dark" style="background-color: #3498DB;">
  <div class="collapse navbar-collapse" id="navbarNav">
    <ul class="navbar-nav">
      <li class="nav-item active">
        <a class="nav-link disabled" href="#">Home <span class="sr-only">(current)</span></a>
      </li>
    </ul>
  </div>
</nav>
""", unsafe_allow_html=True)

### Data Preprocessing

data = pd.read_csv('Data/Heart_Disease_Mortality.csv')
    
# columns - lower case and select a subset of columns
data.columns = data.columns.str.lower()

data = data[['locationabbr', 'locationdesc', 'data_value', 'stratification1', 'stratification2', 'y_lat', 'x_lon']]
data.rename(columns={'locationabbr':'state', 'locationdesc': 'county', 'data_value':'rate', 'stratification1': 'gender', 'stratification2': 'ethnicity', 'y_lat': 'lat', 'x_lon': 'lon'}, inplace=True)


# Data cleaning
data = data[(data.county != 'Nation') & (data.county != 'State')]
data.dropna(subset=['rate'], inplace=True)
data = data[(data.gender != 'Overall')]
data = data[(data.ethnicity != 'Overall')]

# round the rate column to 2 decimal places
data.round({'rate': 2})

#for a better app performance
st.cache(persist=True)

img = Image.open('heart.jpg')
st.image(img)



### PART 1 - Introduction

st.write(
'''
## Heart Disease Mortality Rate Dashboard
'''
)


st.write('''
This dashboard is built to bring greater attention to heart disease as a leading cause of death for Americans. You can find more information and data from [CDC.gov](https://www.cdc.gov/heartdisease/index.htm)
    or [Data.gov](https://catalog.data.gov/dataset?q=heart+disease&sort=score+desc%2C+name+asc&as_sfid=AAAAAAVNvErcp8BfMgCKB54-FA1iL1E3MzgFZIOSUE5u1JrVBifmOXxjnzMxtRLPPKaaqHx5m2OuR4vjJMqrszhv6QgTBUXbuHsd3hmOk6HfO2UtVqq20HGIcEUPWbAyNBhDofw%3D&as_fid=c31a34ca59c3b87c00cf8450453065d5a726ac91).
''')

st.write(
'''
The data used for this dashboard from [Heart Disease Mortality Data Among US Adults (35+) by State/Territory and County - 2016-2018](https://catalog.data.gov/dataset/heart-disease-mortality-data-among-us-adults-35-by-state-territory-and-county-2016-2018)
    on Data.gov which contains 3-year average mortality rate from 2016 to 2018.
''')


# PART 2 - Multiple layer filtering
st.write(
'''
## Heart Disease Motality Rate Lookup
Select the State/County/Gender/Ethnicity to look up for the exact 3-year average mortality rate.
'''
)

st.markdown('######')
st.markdown('######')

state = data['state'].unique()
state_choice = st.selectbox('Select state:', state)

county = data['county'].loc[data['state'] == state_choice].unique()
county_choice = st.selectbox('Select county:', county)

gender = data['gender'].loc[data['county'] == county_choice].unique()
gender_choice = st.selectbox('Select gender:', gender)

ethnicity = data['ethnicity'].loc[data['gender']==gender_choice].unique()
ethnicity_choice = st.selectbox('Select ethnicity:', ethnicity)

data_col = data['rate'][(data['state']==state_choice) & (data['county']==county_choice) & (data['gender']==gender_choice) & (data['ethnicity']==ethnicity_choice)].unique()

st.markdown('######')
st.markdown('######')
st.markdown('######')
st.markdown('######')

st.write(
'''
The 3-year average Heart Disease(Cardiovascular Diseases) mortality rate is:
'''
)

st.markdown(f'<h1 style="color:#e73631;font-size:24px;">{round((sum(data_col)/len(data_col)), 2)}</h1>', unsafe_allow_html=True)

st.write(
'''
per 100,000 population.
'''
)
st.markdown('######')


# PART 3 - Mapping and Filtering Data

st.write(
'''
## Heart Disease Mortality Rate to Location Lookup
Use the silder to choose the Mortality Rate per 100,000 population and look up for its corresponding locations.
'''
)
st.markdown('######')
st.markdown('######')

mortality_input = st.slider('Mortality Rate Slider', int(data['rate'].min()), int(data['rate'].max()), 100)

mortality_filter = data['rate'] < mortality_input
st.map(data.loc[mortality_filter, ['lat', 'lon']])

st.markdown('######')


# PART 4 - Graphing - Distribution

st.write(
'''
## State/Gender/Ethnicitiy Data Distribution
'''
)
# 4.1 graphing - state distribution

#st.write(
#'''
##### 4.1 State Distibution
#'''
#)
fig, ax = plt.subplots()

states = data['state'].value_counts().index
counts = data['state'].value_counts().values
ax.barh(states, counts)
ax.set_xlabel('Num of Occurrences', fontsize=10)
ax.set_ylabel('State', fontsize=10)
plt.xticks(np.arange(0, 1400, 200), fontsize=10)
plt.yticks(fontsize=6)
ax.set_title('State Distribution')

show_graph = st.checkbox('Show State Distritbution', value=True)


if show_graph:
     st.pyplot(fig)


# 4.2 graphing - gender distribution

#st.write(
#'''
##### 4.2 Gender Distibution
#'''
#)

fig, ax = plt.subplots()

states = data['gender'].value_counts().index
counts = data['gender'].value_counts().values
ax.bar(states, counts, width=0.8)
ax.set_xlabel('Gender', fontsize=16)
ax.set_ylabel('Num of Occurrences', fontsize=16)
plt.xticks(fontsize=10)
ax.set_title('Gender Distribution')

show_graph2 = st.checkbox('Show Gender Distritbution', value=True)


if show_graph2:
     st.pyplot(fig)


# 4.3 graphing - ethnicity distribution

#st.write(
#'''
##### 4.3 Ethnicity Distibution
#'''
#)

fig, ax = plt.subplots()

states = data['ethnicity'].value_counts().index
counts = data['ethnicity'].value_counts().values
ax.bar(states, counts, width=0.8)
ax.set_xlabel('Ethnicity', fontsize=16)
ax.set_ylabel('Num of Occurrences', fontsize=16)
plt.xticks(fontsize=6, rotation = 45)
ax.set_title('Ethnicity Distribution')

show_graph3 = st.checkbox('Show Ethnicity Distritbution', value=True)


if show_graph3:
     st.pyplot(fig)

st.markdown('######')
st.markdown('######')
st.markdown('######')
st.markdown('######')

# Part 5 - top 20 mortality rate
st.write(
'''
## Top 20 Mortality Rate
''')

#show_table = st.checkbox('Show Top 20 Mortality Data', value=True)
#df_20 = data.sort_values('rate', ascending=False).head(20)



def highlight_col(x):
    red = 'color: #e73631'
    x = pd.DataFrame('', index=x.index, columns=x.columns)
    x.iloc[:, 2] = red
    return x
    
def show_20(table):
    return table.sort_values('rate', ascending= False).reset_index(drop=True).head(20).style.apply(highlight_col, axis=None).set_properties(**{'text-align': 'left', 'font-size': '15px'})

to_show = (show_20(data))
st.table(to_show)

#if show_table:
#    st.dataframe

st.markdown('######')
st.markdown('######')
st.markdown('######')
st.markdown('######')

# PART 6 - Display Heart Disease Table

st.write(
'''
## Heart Disease Mortality Data Table
This is the dataset used for this dashboard.
''')

show_table = st.checkbox('Show Table', value=True)

if show_table:
    st.dataframe(data)
