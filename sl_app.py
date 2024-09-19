import streamlit as st
import pandas as pd
# import sys
import ssl
from streamlit_gsheets import GSheetsConnection
# from st_supabase_connection import SupabaseConnection
from supabase import create_client, Client
import random
# import collections

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
        "Please enter your username",
        key="get_username",
        max_chars=20,
    )
st.session_state["hit_specific_id"] = st.query_params['hit_specific_id']
st.session_state["hit_finished"] = False

if (st.session_state["username"]):
    st.session_state["total_tasks"] = 5
    if (int(st.session_state["hit_specific_id"]) != 1):
        # # NQ
        # conn = st.connection("gsheets_mturk_nq", type=GSheetsConnection) 
        # st.session_state['annotations_db'] = 'mturk_nq_annotations'
        # instances_to_annotate = 'mturk_nq_ita' 
        # st.session_state['annotator_db_str'] = 'mturk_qualified_nq_annotators'
        # st.session_state['NUM_TRIALS_QUAL_ID'] = '33LB4W8Z0K0VC3F20PYG4DMMLUTU40'
        # st.session_state["total_tasks"] = 3
        # # ELI3
        # conn = st.connection("gsheets_mturk_eli3", type=GSheetsConnection) 
        # st.session_state['annotations_db'] = 'mturk_eli3_annotations'
        # instances_to_annotate = 'mturk_eli3_ita' 
        # st.session_state['annotator_db_str'] = 'mturk_qualified_eli3_annotators'
        # st.session_state['NUM_TRIALS_QUAL_ID'] = '3KKCXPMQWIB6698RR1ZSF6BKSU9IZS'
        # MH
        # conn = st.connection("gsheets_mturk_mh", type=GSheetsConnection) 
        # st.session_state['annotations_db'] = 'mturk_mh_annotations'
        # instances_to_annotate = 'mturk_mh_ita' 
        # st.session_state['annotator_db_str'] = 'mturk_qualified_mh_annotators'
        # st.session_state['NUM_TRIALS_QUAL_ID'] = '3QBA3SDJNY6XMNNNS49D7ALN5NXAPV'
        # MASH
        # conn = st.connection("gsheets_mturk_emr", type=GSheetsConnection) 
        # st.session_state['annotations_db'] = 'mturk_emr_annotations'
        # instances_to_annotate = 'mturk_emr_ita' 
        # st.session_state['annotator_db_str'] = 'mturk_qualified_emr_annotators'
        # st.session_state['NUM_TRIALS_QUAL_ID'] = '3ROUCZRAY0LLODKEL1FO8OBTRKJREZ'
        # REQUAL
        # conn = st.connection("gsheets_mturk_requal", type=GSheetsConnection) 
        # st.session_state['annotations_db'] = 'mturk_requal_annotations'
        # # instances_to_annotate = '' # not needed because the instances are fixed
        # st.session_state['annotator_db_str'] = 'mturk_qualified_requal_annotators'
        # st.session_state['NUM_TRIALS_QUAL_ID'] = '3M0XATTAEN2FOUVZGJMZD95M85W95B' 
        # NQ BASELINE
        # conn = st.connection("gsheets_mturk_nq_baseline", type=GSheetsConnection) 
        # st.session_state['annotations_db'] = 'mturk_baseline_nq_annotations'
        # instances_to_annotate = 'mturk_baseline_nq_ita' 
        # st.session_state['annotator_db_str'] = 'mturk_qualified_baseline_nq_annotators'
        # st.session_state['NUM_TRIALS_QUAL_ID'] = '3TJ7PBKXJ9XGBEOPZ4O8EWR0TDWOGM'
        # st.session_state["total_tasks"] = 3
        # # ELI3 BASELINE
        # conn = st.connection("gsheets_mturk_eli3_baseline", type=GSheetsConnection) 
        # st.session_state['annotations_db'] = 'mturk_baseline_eli3_annotations'
        # instances_to_annotate = 'mturk_baseline_eli3_ita' 
        # st.session_state['annotator_db_str'] = 'mturk_qualified_baseline_eli3_annotators'
        # st.session_state['NUM_TRIALS_QUAL_ID'] = '3KYNP8H8ZS0AO2O8FRSPT69O7LQTHC'
        # st.session_state["total_tasks"] = 3
        # # MH BASELINE
        # conn = st.connection("gsheets_mturk_mh_baseline", type=GSheetsConnection) 
        # st.session_state['annotations_db'] = 'mturk_baseline_mh_annotations'
        # instances_to_annotate = 'mturk_baseline_mh_ita' 
        # st.session_state['annotator_db_str'] = 'mturk_qualified_baseline_mh_annotators'
        # st.session_state['NUM_TRIALS_QUAL_ID'] = '3BERVBF4P9WYI5LQ8ANTAW3U8EIYPB'
        # st.session_state["total_tasks"] = 3
        # # MASH BASELINE
        # conn = st.connection("gsheets_mturk_mash_baseline", type=GSheetsConnection) 
        # st.session_state['annotations_db'] = 'mturk_baseline_mash_annotations'
        # instances_to_annotate = 'mturk_baseline_mash_ita' 
        # st.session_state['annotator_db_str'] = 'mturk_qualified_baseline_mash_annotators'
        # st.session_state['NUM_TRIALS_QUAL_ID'] = '3Q14PV9RQ8GV7WDA45OSF5YPWOYM15'
        # st.session_state["total_tasks"] = 3

        # # ALL NQ
        # conn = st.connection("gsheets_mturk_ALL_NQ", type=GSheetsConnection) 
        # st.session_state['annotations_db'] = 'mturk_all_nq_uf_annotations' # mturk_all_mh_uf_annotations, mturk_all_eli3_uf_annotations, mturk_all_mash_uf_annotations
        # instances_to_annotate = 'mturk_all_nq_uf_ita' # mturk_all_mh_uf_ita, mturk_all_eli3_uf_ita, mturk_all_mash_uf_ita
        # st.session_state['annotator_db_str'] = 'mturk_qualified_all_nq_annotators' # mturk_qualified_all_mh_annotators, mturk_qualified_all_eli3_annotators, mturk_qualified_all_mash_annotators
        # st.session_state['NUM_TRIALS_QUAL_ID'] = '3D3MXTCY124IYA1JRGUEC9TD2AZC1I'
        # st.session_state["total_tasks"] = 7
        # # ALL MH
        # conn = st.connection("gsheets_mturk_ALL_MH", type=GSheetsConnection) 
        # st.session_state['annotations_db'] = 'mturk_all_mh_uf_annotations' # mturk_all_mh_uf_annotations, mturk_all_eli3_uf_annotations, mturk_all_mash_uf_annotations
        # instances_to_annotate = 'mturk_all_mh_uf_ita' # mturk_all_mh_uf_ita, mturk_all_eli3_uf_ita, mturk_all_mash_uf_ita
        # st.session_state['annotator_db_str'] = 'mturk_qualified_all_mh_annotators' # mturk_qualified_all_mh_annotators, mturk_qualified_all_eli3_annotators, mturk_qualified_all_mash_annotators
        # st.session_state['NUM_TRIALS_QUAL_ID'] = '33AQ1MMGKMJRC87O87UFO30GUQH1WG'
        # st.session_state["total_tasks"] = 7
        # # ALL ELI3G
        # conn = st.connection("gsheets_mturk_ALL_ELI3", type=GSheetsConnection) 
        # st.session_state['annotations_db'] = 'mturk_all_eli3_uf_annotations' # mturk_all_mh_uf_annotations, mturk_all_eli3_uf_annotations, mturk_all_mash_uf_annotations
        # instances_to_annotate = 'mturk_all_eli3_uf_ita' # mturk_all_mh_uf_ita, mturk_all_eli3_uf_ita, mturk_all_mash_uf_ita
        # st.session_state['annotator_db_str'] = 'mturk_qualified_all_eli3_annotators' # mturk_qualified_all_mh_annotators, mturk_qualified_all_eli3_annotators, mturk_qualified_all_mash_annotators
        # st.session_state['NUM_TRIALS_QUAL_ID'] = '3SHVTVENCC25086JERQKVETHIULJSN'
        # st.session_state["total_tasks"] = 7
        # ALL MASH
        conn = st.connection("gsheets_mturk_ALL_MASH", type=GSheetsConnection) 
        st.session_state['annotations_db'] = 'mturk_all_mash_uf_annotations' # mturk_all_mh_uf_annotations, mturk_all_eli3_uf_annotations, mturk_all_mash_uf_annotations
        instances_to_annotate = 'mturk_all_mash_uf_ita' # mturk_all_mh_uf_ita, mturk_all_eli3_uf_ita, mturk_all_mash_uf_ita
        st.session_state['annotator_db_str'] = 'mturk_qualified_all_mash_annotators' # mturk_qualified_all_mh_annotators, mturk_qualified_all_eli3_annotators, mturk_qualified_all_mash_annotators
        st.session_state['NUM_TRIALS_QUAL_ID'] = '39J7LX74DTQNMBL3VB8YCWFDSAV3WA'
        st.session_state["total_tasks"] = 7
    else:
        st.session_state['annotator_db_str'] = 'annotators'
        # Connect to google sheets
        if ("_Trial" == st.session_state["username"][-6:]):
            conn = st.connection("gsheets_mturk_trial", type=GSheetsConnection) 
            st.session_state['annotations_db'] = 'mturk_trial_annotations' # 'annotations_trial'
            instances_to_annotate = 'mturk_trial_ita'# 'instances_to_annotate_mturk_trial' # not used
            st.session_state['annotator_db_str'] = 'mturk_trial_annotators'
        elif ("Practice" in st.session_state["username"]):
            conn = st.connection("gsheets_mturk_trial", type=GSheetsConnection) 
            # conn = st.connection("gsheets", type=GSheetsConnection)
            # conn = st.connection("gsheets_practice", type=GSheetsConnection)
            # conn = st.connection("gsheets_teddi_eli5", type=GSheetsConnection)
            st.session_state['annotations_db'] = 'annotations_practice'
            instances_to_annotate = 'instances_to_annotate_practice'
        elif ("Teddi Eli5" == st.session_state["username"]):
            conn = st.connection("gsheets_teddi_eli5", type=GSheetsConnection)
            st.session_state['annotations_db'] = 'annotations_teddi_eli5'
            instances_to_annotate = 'instances_to_annotate_teddi_eli5'
        elif ("Teddi Eli5 Debug" == st.session_state["username"]):
            conn = st.connection("gsheets_teddi_eli5", type=GSheetsConnection)
            st.session_state['annotations_db'] = 'annotations_practice'
            instances_to_annotate = 'instances_to_annotate_practice'
        elif ("Teddi MH" == st.session_state["username"]):
            # conn = st.connection("gsheets_teddi_mh", type=GSheetsConnection)
            conn = st.connection("gsheets_mturk_nq", type=GSheetsConnection) 
            st.session_state['annotations_db'] = 'annotations_practice'
            instances_to_annotate = 'instances_to_annotate_practice'

            # # reeval for mturk:
            # conn = st.connection("gsheets_mturk_mh", type=GSheetsConnection)
            # st.session_state['annotations_db'] = 'annotations_teddi_reeval_mh'
            # instances_to_annotate = 'reeval_ita'

        elif ("Teddi MH Debug" == st.session_state["username"]):
            # conn = st.connection("gsheets_mturk_mh", type=GSheetsConnection)
            # conn = st.connection("gsheets_teddi_nq", type=GSheetsConnection)
            # conn = st.connection("gsheets_mturk_nq", type=GSheetsConnection) 
            conn = st.connection("gsheets_mturk_emr", type=GSheetsConnection)
            st.session_state['annotations_db'] = 'annotations_practice'
            instances_to_annotate = 'instances_to_annotate_practice'
        elif ("Teddi NQ" == st.session_state["username"]):
            conn = st.connection("gsheets_teddi_nq", type=GSheetsConnection)
            st.session_state['annotations_db'] = 'annotations_teddi_nq'
            instances_to_annotate = 'instances_to_annotate_teddi_nq'
        elif ("Teddi Mash" == st.session_state["username"]):
            # conn = st.connection("gsheets_teddi_mash", type=GSheetsConnection) 
            conn = st.connection("gsheets_teddi_retrieved_mash", type=GSheetsConnection)
            st.session_state['annotations_db'] = 'annotations_teddi_mash_retrieved'
            instances_to_annotate = 'instances_to_annotate_teddi_mash'
        elif ("Teddi Baselines" == st.session_state["username"]):
            # conn = st.connection("gsheets_teddi_baselines_nq", type=GSheetsConnection)
            # conn = st.connection("gsheets_teddi_baselines_eli3", type=GSheetsConnection)
            conn = st.connection("gsheets_teddi_baselines_mash", type=GSheetsConnection)
            st.session_state['annotations_db'] = 'annotations_teddi_baselines_mash'
            instances_to_annotate = 'instances_to_annotate_teddi_baselines'
        elif ("Teddi Requal" == st.session_state["username"]):
            conn = st.connection("gsheets_mturk_requal", type=GSheetsConnection) 
            st.session_state['annotations_db'] = 'mturk_requal_annotations'
            # instances_to_annotate = '' # not needed because the instances are fixed
            st.session_state['annotator_db_str'] = 'mturk_qualified_requal_annotators'
        elif ("All" == st.session_state["username"]):
            conn = st.connection("gsheets_mturk_ALL_MH", type=GSheetsConnection) 
            st.session_state['annotations_db'] = 'annotations' # mturk_all_mh_uf_annotations, mturk_all_eli3_uf_annotations, mturk_all_mash_uf_annotations
            st.session_state['annotator_db_str'] = 'annotators' # mturk_qualified_all_mh_annotators, mturk_qualified_all_eli3_annotators, mturk_qualified_all_mash_annotators
            st.session_state["total_tasks"] = 7
            instances_to_annotate = 'mturk_trial_ita'
        else:
            conn = st.connection("gsheets", type=GSheetsConnection)
            instances_to_annotate = 'instances_to_annotate'
            st.session_state['annotations_db'] = 'annotations'
    
    # get data
    df = conn.read()

    # get annotator's history
    annotator_rows = db_conn.table(st.session_state['annotator_db_str']).select("*").execute()
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

    
    # if (True): # TODO remove for real mturk experiments
    #     # this serves instances for the requalification round
    #     st.session_state["hit_ops"] = ['Gemini','Gemini','Post Hoc','Gemini','Post Hoc']
    #     st.session_state["hit_response_ids"] = [27,22,22,40,36]
    #     hit_df_rows = []
    #     for i in range(len(st.session_state["hit_response_ids"])):
    #         curr_response_id = st.session_state["hit_response_ids"][i]
    #         curr_hit_op = st.session_state["hit_ops"][i]
    #         curr_row = df[(df['ID']==curr_response_id)&(df['op']==curr_hit_op)]
    #         hit_df_rows.append(curr_row)
    #     hit_df = pd.concat(hit_df_rows, ignore_index=True)
    # else: # TODO remove for real mturk experiments
    # get instances that still need annotation
    remaining_response_ids = pd.DataFrame(db_conn.table(instances_to_annotate).select("*").execute().data)
    if (len(remaining_response_ids) == 0):
        st.switch_page('pages/no_more.py')
    remaining_response_ids = remaining_response_ids.sort_values(by='query_id', ascending=True)
    viable_response_ids = remaining_response_ids[~remaining_response_ids['query_id'].isin(touched_response_ids)]
    
    # hit_response_ids_df = viable_response_ids.iloc[:min(len(viable_response_ids), st.session_state["total_tasks"])]
    if ("_Trial" == st.session_state["username"][-6:]):
        hit_df = df.iloc[:5] # already randomized in the spreadsheet
        st.session_state["hit_response_ids"] = hit_df['ID'].tolist()
        st.session_state["hit_ops"] = hit_df['op'].tolist()
    elif ("Practice" in st.session_state["username"]):
        hit_df = df.iloc[:5] # already randomized in the spreadsheet
        st.session_state["hit_response_ids"] = hit_df['ID'].tolist()
        st.session_state["hit_ops"] = hit_df['op'].tolist()
    elif ("Teddi Eli5 Debug" == st.session_state["username"]):
        st.session_state["hit_response_ids"] = [23, 133, 23, 133, 133]
        st.session_state["hit_ops"] = ['Snippet', 'Quoted', 'Quoted', 'Paraphrased', 'Entailed']
        hit_df_rows = []
        for i in range(len(st.session_state["hit_response_ids"])):
            curr_response_id = st.session_state["hit_response_ids"][i]
            curr_hit_op = st.session_state["hit_ops"][i]
            curr_row = df[(df['ID']==curr_response_id)&(df['op']==curr_hit_op)]
            hit_df_rows.append(curr_row)
        hit_df = pd.concat(hit_df_rows, ignore_index=True)
    elif ("Teddi MH Debug" == st.session_state["username"]):
        # (50, Quoted)
        st.session_state["hit_response_ids"] = [180, 215, 92, 92]
        st.session_state["hit_ops"] = ['Paraphrased', 'Paraphrased', 'Paraphrased', 'Quoted']
        hit_df_rows = []
        for i in range(len(st.session_state["hit_response_ids"])):
            curr_response_id = st.session_state["hit_response_ids"][i]
            curr_hit_op = st.session_state["hit_ops"][i]
            curr_row = df[(df['ID']==curr_response_id)&(df['op']==curr_hit_op)]
            hit_df_rows.append(curr_row)
        hit_df = pd.concat(hit_df_rows, ignore_index=True)
    elif ("Teddi Baselines" == st.session_state["username"]):
        # (50, Quoted)
        st.session_state["hit_response_ids"] = [22, 22]
        st.session_state["hit_ops"] = ['Post Hoc', 'Post Hoc']
        hit_df_rows = []
        for i in range(len(st.session_state["hit_response_ids"])):
            curr_response_id = st.session_state["hit_response_ids"][i]
            curr_hit_op = st.session_state["hit_ops"][i]
            curr_row = df[(df['ID']==curr_response_id)&(df['op']==curr_hit_op)]
            hit_df_rows.append(curr_row)
        hit_df = pd.concat(hit_df_rows, ignore_index=True)
    elif ("All" == st.session_state["username"]):
        # (50, Quoted)
        st.session_state["hit_response_ids"] = [137, 139, 140, 141, 142, 143, 144] 
        st.session_state["hit_ops"] = ['Snippet', 'Quoted', 'Entailed', 'Abstractive', 'Paraphrased', 'Gemini', 'Post Hoc']
        hit_df_rows = []
        for i in range(len(st.session_state["hit_response_ids"])):
            curr_response_id = st.session_state["hit_response_ids"][i]
            curr_hit_op = st.session_state["hit_ops"][i]
            curr_row = df[(df['ID']==curr_response_id)&(df['op']==curr_hit_op)]
            hit_df_rows.append(curr_row)
        hit_df = pd.concat(hit_df_rows, ignore_index=True)
    else:
        i = 0
        n_hit = 0
        hit_op_ls = []
        hit_id_ls = []
        tt = viable_response_ids['query_id'].tolist()
        # continue until there are no more responses to annotate or all OPs are collected 
        while ((i < len(viable_response_ids)) & (n_hit < st.session_state["total_tasks"])):
            instance = viable_response_ids.iloc[i]
            remaining_ops = instance['ops']
            # shuffle to avoid undesired ordering patterns
            remaining_ops_shuffled_copy = random.sample(remaining_ops.copy(), len(remaining_ops))
            for op in remaining_ops_shuffled_copy:
                # if this op is not yet in the hit, add it
                if (op not in hit_op_ls):
                # if (True):
                    hit_op_ls.append(op)
                    query_id = int(instance['query_id'])
                    hit_id_ls.append(query_id)
                    n_hit += 1
                    # remove op from instances_to_annotate
                    if (len(remaining_ops) == 1):
                        # remove row from instances_to_annotate
                        db_conn.table(instances_to_annotate).delete().eq('query_id', query_id).execute()
                    else:
                        remaining_ops.remove(op) 
                        db_conn.table(instances_to_annotate).update({'ops': remaining_ops}).eq('query_id', query_id).execute()
                    break
            i+=1
        st.session_state["hit_ops"] = hit_op_ls
        st.session_state["hit_response_ids"] = hit_id_ls

        # form the dataframe of instance info for this hit
        rows_to_annotate = []
        for query_id, op in zip(st.session_state["hit_response_ids"], st.session_state["hit_ops"]):
            rows_to_annotate.append(df[(df['ID']==query_id)&(df['op']==op)])
        if (len(rows_to_annotate)==0):
            st.switch_page('pages/no_more.py')
            
        hit_df = pd.concat(rows_to_annotate, ignore_index=True) # yay :D
        if ((len(hit_df)==0) or (st.session_state["total_tasks"]==0)):
            st.switch_page('pages/no_more.py')

    promised_query_ids.append(st.session_state["hit_response_ids"]+[-1]*(st.session_state["total_tasks"]-len(st.session_state["hit_response_ids"])))
    promised_ops.append(st.session_state["hit_ops"]+["Null"]*(st.session_state["total_tasks"]-len(st.session_state["hit_response_ids"])))
    db_conn.table(st.session_state['annotator_db_str']).update({'promised_query_ids': promised_query_ids,  'promised_ops':promised_ops}).eq('annotator_id', st.session_state["username"]).execute()
    st.session_state["total_tasks"] = min(st.session_state["total_tasks"], len(hit_df))
    st.session_state["hit_df"] = hit_df
    st.session_state["task_n"] = 0
    st.switch_page('pages/response_level.py')
  




