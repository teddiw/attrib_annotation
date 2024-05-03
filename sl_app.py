import streamlit as st
import pandas as pd
import sys
import ssl
from streamlit_gsheets import GSheetsConnection
from st_supabase_connection import SupabaseConnection
from supabase import create_client, Client
import random

ssl._create_default_https_context = ssl._create_stdlib_context
st.set_page_config(initial_sidebar_state="collapsed",
                   page_title="Username Form", 
                   page_icon=":mag_right:")

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

# Connect to google sheets
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read()

# Connect to supabase
@st.cache_resource
def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

db_conn = init_connection()
st.session_state["db_conn"] = db_conn
## Page configs
st.title("Citation Quality Evaluation")

st.session_state["username"] = st.text_input(
        "Please enter your WorkerID",
        key="get_username",
        max_chars=20,
    )

if (st.session_state["username"]):

    # get annotator's history
    annotator_rows = db_conn.table("annotators").select("*").execute()
    touched_response_ids = None
    for row in annotator_rows.data:
        if (row['annotator_id']==st.session_state["username"]):
            # get annotator's annotation history if they've been here before
            touched_response_ids = row['annotated_response_ids']
    if (touched_response_ids is None):
        # add annotator if they are new
        db_conn.table('annotators').insert({
            "annotator_id": st.session_state["username"], 
             "annotated_response_ids": [],
             }).execute()
        touched_response_ids = []

    # get instances that still need annotation
    remaining_response_ids = pd.DataFrame(db_conn.table("instances_to_annotate").select("*").execute().data)
    remaining_response_ids = remaining_response_ids.sort_values(by='response_id', ascending=True)
    viable_response_ids = remaining_response_ids[~remaining_response_ids['response_id'].isin(touched_response_ids)]
    hit_response_ids_df = viable_response_ids.iloc[:min(len(viable_response_ids), 10)]
    
    # identify the instances for this hit
    st.session_state["hit_response_ids"] = hit_response_ids_df['response_id'].tolist()
    hit_op_ls = []
    for i in range(len(hit_response_ids_df)):
        remaining_ops = hit_response_ids_df.iloc[i]['ops']
        sampled_op = random.sample(remaining_ops, 1)[0]
        hit_op_ls.append(sampled_op)
        response_id = hit_response_ids_df.iloc[i]['response_id']
        # remove op from instances_to_annotate
        if (len(remaining_ops) == 1):
            # remove row from instances_to_annotate
            db_conn.table('instances_to_annotate').delete().eq('response_id', response_id).execute()
        else:
            remaining_ops.remove(sampled_op) 
            db_conn.table('instances_to_annotate').update({'ops': remaining_ops}).eq('response_id', response_id).execute()
    st.session_state["hit_ops"] = hit_op_ls

    # form the dataframe of instance info for this hit
    rows_to_annotate = []
    for response_id, op in zip(st.session_state["hit_response_ids"], st.session_state["hit_ops"]):
        rows_to_annotate.append(df[(df['ID']==response_id)&(df['op']==op)])
    hit_df = pd.concat(rows_to_annotate, ignore_index=True) # yay :D
    st.session_state["hit_df"] = hit_df
    st.session_state["task_n"] = 0
    st.switch_page('pages/response_level.py')
  




