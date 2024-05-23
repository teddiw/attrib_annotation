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
        "Please enter your UserID",
        key="get_username",
        max_chars=20,
    )

if (st.session_state["username"]):

    # Connect to google sheets
    if ("Practice" in st.session_state["username"]):
        conn = st.connection("gsheets", type=GSheetsConnection)
        # conn = st.connection("gsheets_practice", type=GSheetsConnection)
        # conn = st.connection("gsheets_teddi_eli5", type=GSheetsConnection)
        st.session_state['annotations_db'] = 'annotations_practice'
        instances_to_annotate = 'instances_to_annotate_practice'
        df = conn.read()
    elif ("Teddi Eli5" == st.session_state["username"]):
        conn = st.connection("gsheets_teddi_eli5", type=GSheetsConnection)
        st.session_state['annotations_db'] = 'annotations_teddi_eli5'
        instances_to_annotate = 'instances_to_annotate_teddi_eli5'
        df = conn.read()
    elif ("Teddi Eli5 Debug" == st.session_state["username"]):
        conn = st.connection("gsheets_teddi_eli5", type=GSheetsConnection)
        st.session_state['annotations_db'] = 'annotations_practice'
        instances_to_annotate = 'instances_to_annotate_practice'
        df = conn.read()
    else:
        conn = st.connection("gsheets", type=GSheetsConnection)
        instances_to_annotate = 'instances_to_annotate'
        st.session_state['annotations_db'] = 'annotations'
        df = conn.read()

    # get annotator's history
    annotator_rows = db_conn.table("annotators").select("*").execute()
    touched_response_ids = None
    promised_query_ids = []
    promised_ops = []
    for row in annotator_rows.data:
        if (row['annotator_id']==st.session_state["username"]):
            # get annotator's annotation history if they've been here before
            touched_response_ids = row['annotated_query_ids']
            promised_query_ids = row['promised_query_ids']
            promised_ops = row['promised_ops']
    if (touched_response_ids is None):
        st.switch_page('pages/unknown_user.py')

    st.session_state['touched_response_ids'] = touched_response_ids

    # get instances that still need annotation
    remaining_response_ids = pd.DataFrame(db_conn.table(instances_to_annotate).select("*").execute().data)
    remaining_response_ids = remaining_response_ids.sort_values(by='query_id', ascending=True)
    viable_response_ids = remaining_response_ids[~remaining_response_ids['query_id'].isin(touched_response_ids)]
    st.session_state["total_tasks"] = 5
    hit_response_ids_df = viable_response_ids.iloc[:min(len(viable_response_ids), st.session_state["total_tasks"])]
    
    if ("Practice" in st.session_state["username"]):
        hit_df = df.iloc[:5]
        st.session_state["hit_response_ids"] = hit_df['ID'].tolist()
        st.session_state["hit_ops"] = hit_df['op'].tolist()
        
        # st.session_state["hit_response_ids"] = [
        #                                         # 76,
        #                                         # 77,
        #                                         # 78,
        #                                         # 79,
        #                                         # 80,
        #                                     ]
        # st.session_state["hit_ops"] = [# "Abstractive",
        # #                                 "Entailed",
        # #                                 "Abstractive",
        # #                                 "Paraphrased",
        # #                                 "Paraphrased",
        #                             ]
        # hit_df_rows = []
        # for i in range(len(st.session_state["hit_response_ids"])):
        #     curr_response_id = st.session_state["hit_response_ids"][i]
        #     curr_hit_op = st.session_state["hit_ops"][i]
        #     curr_row = df[(df['ID']==curr_response_id)&(df['op']==curr_hit_op)]
        #     hit_df_rows.append(curr_row)
        # hit_df = pd.concat(hit_df_rows, ignore_index=True)
        # st.session_state["total_tasks"] = len(st.session_state["hit_response_ids"])

    elif ("Teddi Eli5 Debug" == st.session_state["username"]):
        st.session_state["hit_response_ids"] = [47]
        st.session_state["hit_ops"] = ['Quoted']
        hit_df = df[(df['ID']==47)&(df['op']=='Quoted')]
    else:
        # identify the instances for this hit
        st.session_state["hit_response_ids"] = hit_response_ids_df['query_id'].tolist()
        hit_op_ls = []
        for i in range(len(hit_response_ids_df)):
            remaining_ops = hit_response_ids_df.iloc[i]['ops']
            sampled_op = random.sample(remaining_ops, 1)[0]
            hit_op_ls.append(sampled_op)
            response_id = hit_response_ids_df.iloc[i]['query_id']
            # remove op from instances_to_annotate
            if ("Practice" not in st.session_state["username"]):
                if (len(remaining_ops) == 1):
                    # remove row from instances_to_annotate
                    db_conn.table(instances_to_annotate).delete().eq('query_id', response_id).execute()
                else:
                    remaining_ops.remove(sampled_op) 
                    db_conn.table(instances_to_annotate).update({'ops': remaining_ops}).eq('query_id', response_id).execute()
        st.session_state["hit_ops"] = hit_op_ls

        # form the dataframe of instance info for this hit
        rows_to_annotate = []
        for query_id, op in zip(st.session_state["hit_response_ids"], st.session_state["hit_ops"]):
            rows_to_annotate.append(df[(df['ID']==query_id)&(df['op']==op)])
        if (len(rows_to_annotate)==0):
            st.switch_page('pages/no_more.py')
    
        hit_df = pd.concat(rows_to_annotate, ignore_index=True) # yay :D

    promised_query_ids.append(st.session_state["hit_response_ids"])
    promised_ops.append(st.session_state["hit_ops"])
    db_conn.table('annotators').update({'promised_query_ids': promised_query_ids,  'promised_ops':promised_ops}).eq('annotator_id', st.session_state["username"]).execute()
    
    st.session_state["total_tasks"] = min(st.session_state["total_tasks"], len(hit_df))
    st.session_state["hit_df"] = hit_df
    st.session_state["task_n"] = 0
    st.switch_page('pages/response_level.py')
  




