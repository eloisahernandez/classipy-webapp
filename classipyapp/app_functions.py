import streamlit as st
import pandas as pd


#Display summary
def summary(df):
    col1,col2,col3 = st.columns(3)
    col1.metric('Columns', len(df.columns))
    col2.metric('Rows', len(df))
    col3.metric('','')

#Takes a list of column names, type and transformations available and returns
# dictionary with column name as key and a tuple of columns to include and transformation
def display_transformation_options(column_names, column_type,
                                   transformation_types):
    st.markdown(f'''#### {column_type}''')
    st.write("➖" * 35)
    with st.expander("Expand"):
        transformation_dict = {}
        st.markdown(f'''##### Select Transformation''')
        for name in column_names:
            col1, col2, col3, col4 = st.columns(4)
            to_include = col1.checkbox('Include', key = name)
            col2.markdown(f'###### {name}')
            col3.markdown(f'###### cat-multi')
            st.markdown(
                """<style>[data-baseweb="select"] {margin-top: -40px;}
                        </style>
                    """,
                unsafe_allow_html=True,
            )
            transformation = col4.selectbox(" ", transformation_types, key = name)
            transformation_dict[name] = (to_include,transformation)
    return transformation_dict



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
    return transformed_df.to_csv().encode('utf-8')


#2. Create Download button
def download_button(transformed_csv):
    st.download_button(
        label="Download data as CSV",
        data=convert_df(transformed_csv),
        file_name='transformed_df.csv',
        mime='text/csv',
    )
