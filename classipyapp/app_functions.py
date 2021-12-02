import streamlit as st
import pandas as pd
import requests
from pandas.io import json
from classipy import DataFrameTransformer
import json


#Display summary
def summary(df):
    st.markdown('''### Summary''')
    st.write("➖" * 35)
    with st.expander("Expand", expanded=True):
        col1,col2,col3 = st.columns(3)
        col1.metric('Columns', len(df.columns))
        col2.metric('Rows', len(df))
        col3.metric('','')


def api_post_call(df):
    r = requests.post(
        'https://classipy-s6bveudxoq-ew.a.run.app/summary_predict',
        df.to_json()).json()
    api_r_dict = json.loads(r)
    #column_names = list(api_r_dict['column_names'].values()) -- using column names directly from df
    label_pred = list(api_r_dict['y_preds_decoded'].values())
    return label_pred

def transform_data(df, file_name):
    #Get and transform dataset
    transformed_df = DataFrameTransformer(dataset_name=file_name).fit_transform(df)
    #Get column names
    column_names = transformed_df['column_name'].to_list()
    return transformed_df, column_names

#Takes a list of column names, type and transformations available and returns
# dictionary with column name as key and a tuple of columns to include and transformation
def display_transformation_options(column_names, pred_labels):
    st.markdown(f'''#### Column Type Prediction''')
    st.write("➖" * 35)
    column_types = [
        'cat-binary', 'cat-multi', 'date', 'float', 'int', 'text', 'other'
    ]
    with st.expander("Expand"):
        transformation_dict = {}
        columns_width = [1, 3, 2, 2, 3]
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
                                            suggest_transformation(col_type),
                                            key=name)
            transformation_dict[name] = (to_include,col_type,transformation)
    return transformation_dict

def suggest_transformation(label):
    if label in ['float','int']:
        transformation_list = ['MinMaxScaler', 'StandardScaler', 'RobustScaler']
    elif label in ['cat-multi','cat-binary']:
        transformation_list = ['LabelEncoder', 'OneHotEncoder', 'OrdinalEncoder']
    elif label in ['date', 'text', 'other']:
        transformation_list = [' ']
    return transformation_list

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
