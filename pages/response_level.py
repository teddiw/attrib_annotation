import streamlit as st
import pandas as pd
import sys
import time

def format_remove_quotation_marks(output):
    list_output = list(output)
    i=0
    while i < len(list_output):
        if (list_output[i] == "\""):
            del list_output[i]
            i -= 1
        i += 1
    fixed_output = "".join(list_output)
    return fixed_output

def save_start_time():
    st.session_state["start_time"] = time.time()

def save_time(i, task_str):
    # global start_time
    # st.write(task_str)
    # st.write('start time: ', st.session_state["start_time"])
    # st.write('curr time: ', time.time())
    seconds_elapsed = time.time() - st.session_state["start_time"]
    if (task_str == 'prec'):
        if ('prec_t2v' in st.session_state):
            t2v_so_far = st.session_state['prec_t2v']
            t2v_so_far.append(seconds_elapsed)
            st.session_state['prec_t2v'] = t2v_so_far
        else:
            st.session_state['prec_t2v'] = [seconds_elapsed]
    else:
        if ('cov_t2v' in st.session_state):
            t2v_so_far = st.session_state['cov_t2v']
            t2v_so_far.append(seconds_elapsed)
            st.session_state['cov_t2v'] = t2v_so_far
        else:
            t2v_so_far = [seconds_elapsed]
            st.session_state['cov_t2v'] = t2v_so_far
        st.session_state["start_time"] = time.time()
    return

start_time = 0
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
st.header("Task "+str(st.session_state["task_n"]+1)+"/10")
query_container = st.empty()
query_container.markdown('''**User Query:**\n'''+st.session_state["hit_df"].iloc[st.session_state["task_n"]]['Question'])
query_container = st.empty()
unmarked_response = format_remove_quotation_marks(st.session_state["hit_df"].iloc[st.session_state["task_n"]]['Output'])
query_container.markdown('''**System Response:**\n'''+unmarked_response)
# query_container.text(st.session_state["hit_df"].iloc[st.session_state["task_n"]]['Question'])
# st.markdown('''Happy Streamlit-ing! :balloon:''')
st.divider()

fluency_container = st.empty()
fluency_rating = fluency_container.number_input(
        "Please enter your Likert rating",
        value=None,
        min_value=0,
        max_value=5,
        key="fluency_likert"+str(st.session_state["task_n"]+1),
        on_change=save_start_time,
    )
if (fluency_rating):
    fluency_container.markdown('''Recorded :white_check_mark:''')
    #   st.write("Fluency rating: ", fluency_rating)
    st.session_state["fluency_rating"] = fluency_rating

    utility_container = st.empty()
    utility_rating = utility_container.number_input(
            "Please enter your Likert rating",
            value=None,
            min_value=0,
            max_value=5,
            key="utility_likert"+str(st.session_state["task_n"]+1),
            on_change=save_start_time,
        )
    if (utility_rating):
        utility_container.markdown('''Recorded :white_check_mark:''')
        st.session_state["utility_rating"] = utility_rating
        continue_container = st.empty()
        if (continue_container.button('Continue task')):
            fluency_container.empty()
            utility_container.empty()
            continue_container.empty()
            op = st.session_state["hit_df"].iloc[st.session_state["task_n"]]['op']
            response_id = st.session_state["hit_df"].iloc[st.session_state["task_n"]]['ID']
            if (op == 'Snippet'):
                # write results to db
                st.session_state.db_conn.table('annotations').insert({
                "annotator_id": st.session_state["username"], 
                "human_fluency_rating": int(st.session_state["fluency_rating"]),
                "human_utility_rating": int(st.session_state["utility_rating"]),
                "op": op,
                "response_id":int(response_id),
                }).execute()    
                
                # increment to the next task
                if (st.session_state["task_n"]<9):
                    st.session_state["task_n"] += 1
                    st.switch_page('pages/response_level.py')
                # TODO else: landing page with some yayay

            sentences = st.session_state["hit_df"].iloc[st.session_state["task_n"]]['Sent (cited)']
            num_sentences = len(sentences)
            prec_results = [-1]*num_sentences
            cov_results = [-1]*num_sentences
            placeholders_prec = []
            placeholders_cov = []
            for i in range(len(sentences)):
                placeholder = st.empty()
                placeholders_prec.append(placeholder)
                placeholder = st.empty()
                placeholders_cov.append(placeholder)

            def finish_up():
                # write results to db that user annotated entire response
                st.session_state.db_conn.table('annotations').insert({
                "annotator_id": st.session_state["username"], 
                "human_fluency_rating": int(st.session_state["fluency_rating"]),
                "human_utility_rating": int(st.session_state["utility_rating"]),
                "n_precise_citations": st.session_state['precision_results'],
                "is_covered": st.session_state['coverage_results'],
                "t2v_precision": st.session_state['prec_t2v'],
                "t2v_coverage": st.session_state['cov_t2v'],
                "op": op,
                "response_id":int(response_id),
                }).execute()    
                
                # increment to the next task
                if (st.session_state["task_n"]<9):
                    st.session_state["task_n"] += 1
                    st.switch_page('pages/response_level.py')
                # TODO else: landing page with some yayay
                return

            def eval_next_sentence(prec_result, i):
                if (i > 0):
                    placeholders_prec[i-1].empty()
                    placeholders_cov[i-1].empty()
                if (prec_result):
                    prec_results[i] = prec_result
                    placeholders_prec[i].markdown('''Recorded :white_check_mark:''')
                    # placeholders_prec[i].text("Precision: "+str(prec_results[i]))
                    prec_result = None
                    cov_result = None
                    cov_result = placeholders_cov[i].number_input(
                                                                "Is the sentence covered?",
                                                                value=None,
                                                                min_value=0,
                                                                key=str(i)+'coverage',
                                                                on_change=save_time,
                                                                args=(i,'cov',)
                                                                )
                    if (cov_result):
                        cov_results[i] = cov_result
                        # placeholders_cov[i].text("Coverage: "+str(cov_results[i]))
                        placeholders_cov[i].markdown('''Recorded :white_check_mark:''')
                        cov_result = None

                        i += 1
                        if (i < num_sentences):
                            prec_result = placeholders_prec[i].number_input(
                                                                        "Please enter # precise citations",
                                                                        value=None,
                                                                        min_value=0,
                                                                        key=str(i)+'precision',
                                                                        on_change=save_time,
                                                                        args=(i,'prec',)
                                                                        )
                            eval_next_sentence(prec_result, i)
                        else:
                            st.session_state['prec_results'] = prec_results
                            st.session_state['cov_results'] = cov_results
                            finish_up()
                            # st.write(st.session_state['prec_results'])
                            # st.write(st.session_state['cov_results'])
                            # st.write(st.session_state['prec_t2v'])
                            # st.write(st.session_state['cov_t2v'])
                            return

            prec_result = placeholders_prec[i].number_input( 
                                                        "Please enter # precise citations",
                                                        value=None,
                                                        min_value=0,
                                                        key=str(i)+'precision',
                                                        on_change=save_time,
                                                        args=(0,'prec',)
                                                    )
            
            eval_next_sentence(prec_result, i)
                
            st.session_state['precision_results'] = prec_results
            st.session_state['coverage_results'] = cov_results
                







