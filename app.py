import streamlit as st
import pandas as pd
import time
from classipyapp.app_functions import display_transformation_options

st.set_page_config(
    page_title="Quick reference",  # => Quick reference - Streamlit
    page_icon="🎲",
    layout="centered",  # wide,centered
    initial_sidebar_state="auto")  # collapsed


st.markdown('''
### Classipy: Coming Soon 🔜
''')

uploaded_file = st.file_uploader("Upload your csv file",
                                 type=["csv", "json"],
                                 accept_multiple_files=False)

pd.DataFrame(uploaded_file)

#Request user to select output
st.write('Select an action:')
option_1 = st.checkbox('Get Summary')
option_2 = st.checkbox('Clean & Transform (recommended transformations)')

submit_button = st.button('Submit')

if submit_button and (option_1 and option_2):
    ## Add functions to retrieve summary and transformation
    st.write('You will get summary and transformation')
    st.markdown('''### Summary''')
elif submit_button and option_1:
    ## Add functions to retrieve summary
    st.write('You want the summary')
    st.markdown('''### Summary''')
elif submit_button and option_2:
    ## Add function to retrieve transformation
    st.write('You only want the transformation')
else:
    st.write('Please select an action')



column_names = ['Column1','Column2']
categorical_transformation =  ['OneHotEncoder','LabelEncoder']
numerical_transformation = ['StandardScaling','MinMaxValue']

display_transformation_options(column_names, 'Categorical',
                               categorical_transformation)
display_transformation_options(column_names, 'Numerical',
                               numerical_transformation)
