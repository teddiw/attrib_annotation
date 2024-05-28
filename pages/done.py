import streamlit as st
import random
import string
import boto3
import pandas as pd 
## Page configs
st.set_page_config(initial_sidebar_state="collapsed")

st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)

# create mturk client
MTURK_SANDBOX = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
MTURK = 'https://mturk-requester.us-east-1.amazonaws.com'
mturk = boto3.client('mturk',
                    aws_access_key_id = st.secrets["aws_access_key_id"],
                    aws_secret_access_key = st.secrets["aws_secret_access_key"],
                    region_name='us-east-1',
                    endpoint_url = MTURK
                    )
# get new number of completed HITs for this group
num_worker_annotations = len(st.session_state["db_conn"].table(st.session_state['annotations_db']).select("query_id").eq("annotator_id", st.session_state["username"]).execute().data)//5
# update the worker's qualification
NUM_TRIALS_QUAL_ID = '3LW1BECZ1OKIR84E7XGS2E027J5RS4' # SB '3O42DSCJPU0X16ST9JDZLV1W82OX6J' 
worker_id = st.session_state["username"].split('_')[0]
response = mturk.associate_qualification_with_worker(
            QualificationTypeId=NUM_TRIALS_QUAL_ID,
            WorkerId=worker_id,
            IntegerValue=num_worker_annotations
        )
completion_code = st.session_state["db_conn"].table("hit_completion_codes").select("completion_code").eq("hit_specific_id", st.session_state["hit_specific_id"]).execute().data[0]['completion_code']

if (st.session_state["hit_finished"]):
    # this is redundant because it errors if you directly access the done page
    st.markdown('''# Done! Thank you so much! :raised_hands:''')
    st.markdown('''Please enter the one-time-use completion code below on the MTurk HIT webpage for compensation.''')
    st.markdown(completion_code)
else:
    st.markdown('''# Incomplete''')