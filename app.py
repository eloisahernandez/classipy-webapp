import streamlit as st
import pandas as pd
from classipyapp.app_functions import api_post_call, display_transformation_options, download_button, summary
from classipy import DataFrameTransformer


st.set_page_config(
    page_title="Classipy",
    page_icon="🎲",
    layout="centered",  # wide,centered
    initial_sidebar_state="auto")  # collapsed

st.markdown('''### Classipy: Coming Soon 🔜''')

uploaded_file = st.file_uploader("Upload your csv file",
                                 type=["csv"],
                                 accept_multiple_files=False)


if uploaded_file is not None:
    uploaded_df = pd.read_csv(uploaded_file)
else:
    uploaded_df = None

if uploaded_df is None:
    st.warning('Please upload a file')
else:
    #Get and transform dataset
    dataset_name_tmp = 'no_dataset_name'
    table_name = uploaded_file.name.split('.csv')[0]
    transformed_df = DataFrameTransformer(dataset_name_tmp,table_name).fit_transform(uploaded_df)
    #Send request to API to get predictions
    #y_pred = api_post_call(transformed_df)
    #Get column names
    column_names = transformed_df['column_name'].to_list()

#-----------------------------#
#Testing Variables
try:
    ##Testing input df and api response
    column_names = transformed_df['column_name'].to_list()
    #temp variables to test label input/columns
    labels = pd.Series(['other', 'other', 'cat-multi', 'cat-multi', 'float', 'date']).to_list()
    #st.write(labels)
    ## Temp variables to test column displays
except:
    pass
#-----------------------------#

#Request user to select output
option_1 = 'Get Summary & Predictions (select transformations)'
option_2 = 'Get Summary - Clean & Transform (output with recommended transformations)'
selection = st.radio('Select an action:', (option_1,option_2))

submit_button = st.button('Submit')

if submit_button and (selection == option_1):
    st.write('You want the summary and predictions')
    st.markdown('''### Summary''')
    summary(uploaded_df)
elif submit_button and (selection == option_2):
    ## Add function to retrieve transformation
    st.write('We will process the data with our own predictions')
    st.markdown('''### Summary''')
#else:
#    st.warning('Please select an action and click Submit')

try:
    transf_dict = display_transformation_options(column_names, labels)
    st.write(transf_dict)
except:
    pass



try:
    download_button(transformed_df)
except:
    pass
