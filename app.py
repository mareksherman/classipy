import streamlit as st
import pandas as pd

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


#Temporarily displays a message while executing a block of code
def processing_feedback(status):
    '''Displays message while code executes'''
    with st.spinner('Wait for it...'):
        status = 'Done'
    st.success('Done!')
    pass

#Allow user to download output as csv:
# 1. Convert df to csv
@st.cache
def convert_df(transformed_df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    transformed_csv = transformed_df.to_csv().encode('utf-8')
    return transformed_csv

#2. Create Download button
def download_button(transformed_csv):
    st.download_button(
    label="Download data as CSV",
    data=convert_df(transformed_csv),
    file_name='transformed_df.csv',
    mime='text/csv',)
