import streamlit as st
import pandas as pd

#Takes a list of column names, type and transformations available and returns
#column names with options to transform
def display_transformation_options(column_names, column_type,
                                   transformation_types):
    st.markdown(f'''#### {column_type}''')
    st.write("➖" * 35)
    with st.expander("Expand"):
        st.markdown(f'''##### Select Transformation''')

        for name in column_names:
            st.markdown(f'###### {name}')
            st.markdown(
                """<style>[data-baseweb="select"] {margin-top: -40px;}
                        </style>
                    """,
                unsafe_allow_html=True,
            )
            transformation = st.selectbox(" ", transformation_types, key=name)



#Temporarily displays a message while executing a block of code
def processing_feedback(status):
    '''Displays message while code executes'''
    with st.spinner('Wait for it...'):
        status = 'Done'
    st.success('Done!')
    pass


#Allow user to download output as csv:
# 1. Convert df to csv
#@st.cache - add cache before function to prevent computation on every rerun
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
        mime='text/csv',
    )
