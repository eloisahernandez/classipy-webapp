import streamlit as st
import pandas as pd
from streamlit.state.session_state import SessionState
from classipyapp.app_functions import api_post_call, display_transformation_options, download_button, summary, transform_data
from classipyapp.parsing import Parsing

st.set_page_config(
    page_title="Classipy",
    page_icon="🎲",
    layout="centered",  # wide,centered
    initial_sidebar_state="auto")  # collapsed

st.markdown('''## Classipy''')

uploaded_file = st.file_uploader("Upload your csv file",
                                 type=["csv"],
                                 accept_multiple_files=False)


if uploaded_file is not None:
    uploaded_df = pd.read_csv(uploaded_file)
    file_name = uploaded_file.name.split('.csv')[0]
else:
    uploaded_df = None

#Request user to select output
option_1 = 'Get Summary & Predictions (select transformations)'
option_2 = 'Get Summary - Clean & Transform (output with recommended transformations)'
selection = st.radio('Select an action:', (option_1,option_2))


submit_button = st.button('Submit')

#Harcoded labels to test.
#labels = pd.Series(
#    ['other', 'other', 'cat-multi', 'cat-multi', 'float', 'date']).to_list()


if (submit_button and (selection == option_1) and uploaded_file is not None) or 'postsubmit' in st.session_state:
    st.session_state['postsubmit'] = True
    summary(uploaded_df)
    transformed_df, column_names = transform_data(uploaded_df, file_name)
    with st.spinner('Wait for it...'):
        if 'labels' not in st.session_state:
            st.session_state['labels'] = api_post_call(transformed_df)
        labels = st.session_state['labels']
        transf_dict = display_transformation_options(column_names,labels)
elif (submit_button and uploaded_file is None):
    st.warning('Please upload a file')
elif submit_button and (selection == option_2):
    ## Add function to retrieve transformation
    st.write('We will process the data with our own predictions')
    st.markdown('''### Summary''')
else:
    st.warning('Please select an action and click Submit')


# Implement parser and transformer after user confirms selections

transform_button = st.button('Transform')

if transform_button:
    parse_type = Parsing(transf_dict)
    transformed_df, status = parse_type.parse_and_transform(uploaded_df)
    st.success('You can now download your transformed data')
    download_button(transformed_df)
