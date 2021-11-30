import streamlit as st
import pandas as pd
import requests
from pandas.io import json


#Display summary
def summary(df):
    st.write('Summary was called')
    with st.expander("Expand", expanded=True):
        col1,col2,col3 = st.columns(3)
        col1.metric('Columns', len(df.columns))
        col2.metric('Rows', len(df))
        col3.metric('','')

def api_post_call(df):
    r = requests.post(
        'https://classipy-s6bveudxoq-ew.a.run.app/summary_predict',
        df.to_json())
    label_pred = pd.Series(r)
    st.write(r)
    st.write(f"Status Code: {r.status_code}, Response: {r.json()}")
    return label_pred

#Takes a list of column names, type and transformations available and returns
# dictionary with column name as key and a tuple of columns to include and transformation
def display_transformation_options(column_names, pred_labels):
    st.markdown(f'''#### Column Type Prediction''')
    st.write("➖" * 35)
    #transformation_num = ['MinMaxScaler', 'StandardScaler']
    #tranformation_cat = ['OneHotEncoder', 'LabelEncoder']
    column_types = [
        'cat-binary', 'cat-multi', 'date', 'float', 'int', 'text', 'other'
    ]
    with st.expander("Expand"):
        transformation_dict = {}
        columns_width = [1, 3, 2, 2, 2]
        st.markdown(f'''###### *Review Type and Select Transformation*''')
        col1, col2, col3, col4, col5 = st.columns(columns_width)
        col1.write('**Include**')
        col2.write('**Column Name**')
        col3.write('**Prediction **')
        col4.write('**Change Type**')
        col5.write('**Select Transformation**')

        for name,label in zip(column_names,pred_labels):
            col1, col2, col3, col4,col5 = st.columns(columns_width)
            to_include = col1.checkbox('', value = True, key = name)
            col2.markdown(f'###### {name}')
            col3.markdown(f'###### {label}')
            col_type = col4.selectbox(" ",column_types, index=column_types.index(label), key = name)
            st.markdown(
                """<style>[data-baseweb="select"] {margin-top: -40px;}
                        </style>
                    """,
                unsafe_allow_html=True,)
            transformation = col5.selectbox(" ",
                                            suggest_transformation(label),
                                            key=name)
            transformation_dict[name] = (to_include,col_type,transformation)
    return transformation_dict


@st.cache
def suggest_transformation(label):
    if label in ['float','int']:
        transformation_list = ['MinMaxScaler', 'StandardScaler', 'RobustScaler']
    elif label in ['cat-multi','cat-binary']:
        transformation_list = ['LabelEncoder', 'OneHotEncoder', 'OrdinalEncoder']
    elif label in ['date', 'text', 'other']:
        transformation_list = [' ']
    return transformation_list


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
