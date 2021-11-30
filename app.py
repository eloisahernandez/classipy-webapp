import streamlit as st
import pandas as pd
from classipyapp.app_functions import convert_df, display_transformation_options, download_button, summary
from classipy import DataFrameTransformer
import requests

st.set_page_config(
    page_title="Classipy",
    page_icon="🎲",
    layout="centered",  # wide,centered
    initial_sidebar_state="auto")  # collapsed


st.markdown('''
### Classipy: Coming Soon 🔜
''')

uploaded_file = st.file_uploader("Upload your csv file",
                                 type=["csv", "json"],
                                 accept_multiple_files=False)


if uploaded_file is not None:
    uploaded_df = pd.read_csv(uploaded_file)
try:
    dataset_name_tmp = 'no_dataset_name'
    table_name = uploaded_file.name.split('.csv')[0]
    transformed_df = DataFrameTransformer(dataset_name_tmp,table_name).fit_transform(uploaded_df)
    r = requests.post('https://classipy-s6bveudxoq-ew.a.run.app/summary_predict',
    json = transformed_df.to_json())
    #st.write(f"Status Code: {r.status_code}, Response: {r.json()}")
except:
    pass

#Request user to select output
option_1 = 'Get Summary & Predictions (select transformations)'
option_2 = 'Get Summary - Clean & Transform (output with recommended transformations)'
selection = st.radio('Select an action:', (option_1,option_2))

submit_button = st.button('Submit')

if submit_button and (selection == option_1):
    ## Add functions to retrieve summary
    st.write('You want the summary and predictions')
    st.markdown('''### Summary''')
    try:
        summary(uploaded_df)
    except:
        pass
elif submit_button and (selection == option_2):
    ## Add function to retrieve transformation
    st.write('We will process the data with our own predictions')
    st.markdown('''### Summary''')
else:
    st.info('Please select an action and click Submit')

## Temp variables to test column displays
column_names_c = ['Column1','Column2', 'Column5']
column_names_n = ['Column3','Column4', 'Column6']
categorical_transformation =  ['OneHotEncoder','LabelEncoder']
numerical_transformation = ['StandardScaling','MinMaxValue']

st.text(display_transformation_options(column_names_c, 'Categorical',
                             categorical_transformation))
st.text(display_transformation_options(column_names_n, 'Numerical',
                               numerical_transformation))

try:
    download_button(transformed_df)
except:
    pass
