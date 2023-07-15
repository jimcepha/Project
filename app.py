import streamlit as st
import pickle
import numpy as np
import math
# TO DO
#create 4 drop downs, loc, bed, bath, sqft
#write the predict function here
# create a submit button
# get the inputes from dropdowns and give in function
#if submit is pressed, do the calculation and show optput

all_columns = pickle.load(open('columns.pkl', 'rb'))
model = pickle.load(open('model.pkl', 'rb'))

st.markdown("<h1 style='text-align: center; color: white;'>Welcome to our Realest Estate !</h1>", unsafe_allow_html=True)
#st.markdown("<h3 style='text-align: center; color: grey;'>We show you the realest and affordable Prices</h3>", unsafe_allow_html=True)

st.markdown('##### Just enter your requirements here : ')


selected_sqft = st.number_input('Required Area/Sqft: ', min_value=300)

locations = all_columns[4:]
selected_loc = st.selectbox('Select Location Name:', locations)

data_inputs = all_columns[0:4]

selected_bath = st.selectbox('No. of Bathrooms: ', ['1', '2', '3', '4', '5'])
selected_bhk = st.selectbox('No. of BHK rooms: ', ['1', '2', '3', '4', '5'])

clicked = st.button("Show Best/Cheaptest Prices")

#Predict Function
def predict_prices(location,total_sqft,bath,bhk):
    try:
        loc_index = all_columns.index(location)
    except:
        loc_index = -1    
    
    z = np.zeros(len(all_columns))
    z[0] = total_sqft
    z[1] = bath
    z[2] = bhk
    if loc_index >= 0:
        z[loc_index] = 1
        
    price = round(model.predict([z])[0], 2)   
    strr = ' lakhs'

    if math.log10(price) >= 2:
        price = price / 100
        price = round(price, 2)
        strr = " crores"

    return str(price) + strr

#if clicked, show results
if clicked:
    result = predict_prices(selected_loc,selected_sqft,selected_bath,selected_bhk)
    st.markdown(f'<span style="color: white;font-size:24px">**The Price is just {result}**</span>', unsafe_allow_html=True)

# code for adding bg image
import base64
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover;
        
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local('realestate.jpg')       
# image url https://www.pexels.com/photo/brown-wooden-house-infront-of-swimming-pool-under-blue-sky-32870/



