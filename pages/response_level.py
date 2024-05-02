import streamlit as st
import pandas as pd
import sys
import time

start_time = 0
global end_time
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

st.title("Response Level Task")
st.session_state["username"] = None
text_input_container = st.empty()

def save_start_time():
    # global start_time
    # start_time = time.time()
    st.session_state["start_time"] = time.time()

fluency_rating = text_input_container.number_input(
        "Please enter your Likert rating",
        value=0,
        min_value=0,
        max_value=5,
        key="fluency_likert",
        on_change=save_start_time
    )
if (fluency_rating):
  text_input_container.empty()
  st.write("Fluency rating: ", fluency_rating)
  st.session_state["fluency_rating"] = fluency_rating

def save_end_time():
    global end_time
    end_time = time.time()
    return

def save_time(i, task_str):
    # global start_time
    st.write(task_str)
    st.write('start time: ', st.session_state["start_time"])
    st.write('curr time: ', time.time())
    seconds_elapsed = time.time() - st.session_state["start_time"]
    if (task_str == 'prec'):
        if ('prec_t2v' in st.session_state):
            t2v_so_far = st.session_state['prec_t2v']
            t2v_so_far.append(seconds_elapsed)
            st.session_state['prec_t2v'] = t2v_so_far
        else:
            st.session_state['prec_t2v'] = [seconds_elapsed]
        st.session_state['prec_t2v']
    else:
        if ('cov_t2v' in st.session_state):
            t2v_so_far = st.session_state['cov_t2v']
            t2v_so_far.append(seconds_elapsed)
            st.session_state['cov_t2v'] = t2v_so_far
        else:
            t2v_so_far = [seconds_elapsed]
            st.session_state['cov_t2v'] = t2v_so_far
        st.session_state['cov_t2v']
        st.session_state["start_time"] = time.time()
    return

sentences = ['sentence 1', 'sentence 2']
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
    # save precision results
    # save precision timing results
    # save coverage results
    # save coverage timing results
    # rerun this page with fresh state and new instance <- possible?
    return

def eval_next_sentence(prec_result, i):
    if (i > 0):
        placeholders_prec[i-1].empty()
        placeholders_cov[i-1].empty()
    if (prec_result):
        prec_results[i] = prec_result
        placeholders_prec[i].text("Precision: "+str(prec_results[i]))
        prec_result = None
        task_str = "cov"
        cov_result = placeholders_cov[i].number_input(
                                                    "Is the sentence covered?",
                                                    value=0,
                                                    min_value=0,
                                                    key=str(i)+'coverage',
                                                    on_change=save_time,
                                                    args=(i,'cov',)
                                                    )
        if (cov_result):
            cov_results[i] = cov_result
            placeholders_cov[i].text("Coverage: "+str(cov_results[i]))
            cov_result = None

            i += 1
            if (i < num_sentences):
                prec_result = placeholders_prec[i].number_input(
                                                            "Please enter # precise citations",
                                                            value=0,
                                                            min_value=0,
                                                            key=str(i)+'precision',
                                                            on_change=save_time,
                                                            args=(i,'prec',)
                                                            )
                eval_next_sentence(prec_result, i)
            else:
                finish_up()
                st.session_state['prec_results'] = prec_results
                st.session_state['cov_results'] = cov_results
                st.write(st.session_state['prec_results'])
                st.write(st.session_state['cov_results'])
                st.write(st.session_state['prec_t2v'])
                st.write(st.session_state['cov_t2v'])
                return

i = 0       
if (fluency_rating):
    task_str = 'prec'
    prec_result = placeholders_prec[i].number_input( 
                                                "Please enter # precise citations",
                                                value=0,
                                                min_value=0,
                                                key=str(i)+'precision',
                                                on_change=save_time,
                                                args=(i,'prec',)
                                            )
    
    eval_next_sentence(prec_result, i)
        
    st.session_state['precision_results'] = prec_results
    


  




