import streamlit as st
import pickle
import pandas as pd
import numpy as np

st.set_page_config(page_title="Viz Demo")
#property_type	location	bedRoom	bathroom	balcony	floorNum
# agePossession	Store Room	Servant Room	furnishing_type	luxury_score
# luxury_category	floor_category	built_up_area
with open('df (1).pkl', 'rb') as file:
    df = pickle.load(file)

with open('pipeline (1).pkl','rb') as file:
    pipeline = pickle.load(file)
#st.dataframe(df)

st.header('Enter your inputs')

# property_type
property_type = st.selectbox('Property Type',['flat','house'])

# location
location = st.selectbox('Location',sorted(df['location'].unique().tolist()))

bedRooms = float(st.selectbox('Number of BedRoom',sorted(df['bedRoom'].unique().tolist())))

bathRooms = float(st.selectbox('Number of BathRoom',sorted(df['bathroom'].unique().tolist())))

balcony =(st.selectbox('Balconies',[0,1]))

Property_Age = st.selectbox('Property Age',sorted(df['agePossession'].unique().tolist()))

store_room = (st.selectbox('Store Room',[0,1]))

servant_room = (st.selectbox('Servant Room',[0,1]))

furnishing_type = st.selectbox('Furnishing Type',sorted(df['furnishing_type'].unique().tolist()))

luxury_category = st.selectbox('Luxury Category',sorted(df['luxury_category'].unique().tolist()))

floor_category = st.selectbox('Floor Category',sorted(df['floor_category'].unique().tolist()))

built_up_area = float(st.number_input('Built Up Area'))

if st.button('Predict'):

    # form a dataframe
    data = [[property_type, location, bedRooms, bathRooms, balcony, Property_Age,store_room, servant_room,  furnishing_type, luxury_category, floor_category, built_up_area,]]
    columns = ['property_type', 'location', 'bedRoom', 'bathroom', 'balcony',
               'agePossession', 'Store Room','Servant Room',
               'furnishing_type', 'luxury_category', 'floor_category','built_up_area']
    # Convert to DataFrame
    one_df = pd.DataFrame(data, columns=columns)

    #st.dataframe(one_df)

    # predict
    base_price = np.expm1(pipeline.predict(one_df))[0]
    low = base_price - 0.22
    high = base_price + 0.22

    # display
    st.text("The price of the flat is between {} Cr and {} Cr".format(round(low, 2), round(high, 2)))
