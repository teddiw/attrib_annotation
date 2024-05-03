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

    button.step-up {display: none;}
    button.step-down {display: none;}
    div[data-baseweb] {border-radius: 4px;}

</style>
""",
    unsafe_allow_html=True,
) 

st.markdown("""
<style>
    
</style>""",
unsafe_allow_html=True)

if ("hit_df" in st.session_state):
    st.header("Task "+str(st.session_state["task_n"]+1)+"/"+str(st.session_state["total_tasks"]))
    query_container = st.empty()
    query_container.markdown('''**User Query:**\n'''+st.session_state["hit_df"].iloc[st.session_state["task_n"]]['Question'])
    full_response_container = st.empty()
    unmarked_response = format_remove_quotation_marks(st.session_state["hit_df"].iloc[st.session_state["task_n"]]['Output'])
    full_response_container.markdown('''**System Response:**\n'''+unmarked_response)
    sentence_container = st.empty()
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
        # st.write("Fluency rating: ", fluency_rating)
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
            if ('b1_press' not in st.session_state):
                st.session_state["b1_press"] = False
            # breakpoint()
            b1_press = continue_container.button('Continue task')
            if (st.session_state["b1_press"] or b1_press):
                st.session_state["b1_press"] = True
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
                    st.session_state['touched_response_ids'] += [int(response_id)]
                    st.session_state.db_conn.table('annotators').update({'annotated_response_ids': st.session_state['touched_response_ids']}).eq('annotator_id', st.session_state["username"]).execute()
                    
                    # increment to the next task
                    if (st.session_state["task_n"]<st.session_state["total_tasks"]-1):
                        st.session_state["task_n"] += 1
                        st.session_state['prec_t2v'] = []
                        st.session_state['cov_t2v'] = []
                        st.switch_page('pages/response_level.py')
                    else:
                        st.switch_page('pages/done.py')
                    # TODO else: landing page with some yayay

                sentences = eval(st.session_state["hit_df"].iloc[st.session_state["task_n"]]['Sent (cited)'])
                num_sentences = len(sentences)
                prec_results = [-1]*num_sentences
                cov_results = [-1]*num_sentences
                placeholders_prec = []
                placeholders_cov = []
                for i in range(num_sentences):
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
                    "n_precise_citations": st.session_state['prec_results'],
                    "is_covered": st.session_state['cov_results'],
                    "t2v_precision": st.session_state['prec_t2v'],
                    "t2v_coverage": st.session_state['cov_t2v'],
                    "op": op,
                    "response_id":int(response_id),
                    }).execute()  
                    st.session_state['touched_response_ids'] += [int(response_id)]
                    st.session_state.db_conn.table('annotators').update({'annotated_response_ids': st.session_state['touched_response_ids']}).eq('annotator_id', st.session_state["username"]).execute()
                    # increment to the next task
                    if (st.session_state["task_n"]<st.session_state["total_tasks"]-1):
                        st.session_state["task_n"] += 1
                        st.session_state['prec_t2v'] = []
                        st.session_state['cov_t2v'] = []
                        st.switch_page('pages/response_level.py')
                    else:
                        st.switch_page('pages/done.py')
                    # TODO else: landing page with some yayay
                    return

                def eval_next_sentence(prec_result, i):
                    if (i > 0):
                        placeholders_prec[i-1].empty()
                        placeholders_cov[i-1].empty()
                    if (prec_result!=-1):
                        prec_results[i] = prec_result
                        placeholders_prec[i].markdown('''Recorded :white_check_mark:''')
                        # placeholders_prec[i].text("Precision: "+str(prec_results[i]))
                        prec_result = -1
                        cov_result = placeholders_cov[i].radio(
                                        label='''Do the citation(s) in the sentence together support all claims in the sentence?''',
                                        options=["Yes", "No"],
                                        index=None,
                                        key=str(i)+'coverage',
                                        on_change=save_time,
                                        args=(i,'cov',))
                        

                        if (cov_result):
                            if cov_result == "Yes":
                                cov_results[i] = 1
                            else:
                                cov_results[i] = 1
                            # placeholders_cov[i].text("Coverage: "+str(cov_results[i]))
                            placeholders_cov[i].markdown('''Recorded :white_check_mark:''')
                            cov_result = None

                            i += 1
                            if (i < num_sentences):
                                sentence = sentences[i]
                                cited_response = st.session_state["hit_df"].iloc[st.session_state["task_n"]]['Output (cited)']
                                cited_sources = st.session_state["hit_df"].iloc[st.session_state["task_n"]]['Used Sources (cited)']
                                full_response_container.markdown('''**Cited System Response:**\n'''+cited_response)
                                sentence_container.markdown('''**Sentence to evaluate:**\n'''+sentence)
                                citations = st.session_state["hit_df"].iloc[st.session_state["task_n"]]['Citation Dict']
                                num_citations_in_sentence = len(eval(citations)[str(i)]['citation_numbers'])
                                prec_result = placeholders_prec[i].number_input(
                                                                            "How many of the citations in the sentence actually support a claim in the sentence, according to the sources below?",
                                                                            value=-1,
                                                                            min_value=-1,
                                                                            max_value=num_citations_in_sentence,
                                                                            key=str(i)+'precision',
                                                                            on_change=save_time,
                                                                            args=(i,'prec',),
                                                                            step=1
                                                                            )
                                sources_container.markdown('''**Sources:**\n'''+cited_sources)
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
                i = 0
                sentence = sentences[i]
                cited_response = st.session_state["hit_df"].iloc[st.session_state["task_n"]]['Output (cited)']
                cited_sources = st.session_state["hit_df"].iloc[st.session_state["task_n"]]['Used Sources (cited)']
                full_response_container.markdown('''**Cited System Response:**\n'''+cited_response)
                sentence_container.markdown('''**Sentence to evaluate:**\n'''+sentence)

                citations = st.session_state["hit_df"].iloc[st.session_state["task_n"]]['Citation Dict']
                num_citations_in_sentence = len(eval(citations)[str(i)]['citation_numbers'])

                prec_result = -1
                prec_result = placeholders_prec[i].number_input( 
                                                            "How many of the citations in the sentence actually support a claim in the sentence, according to the sources below??",
                                                            value=-1,
                                                            min_value=-1, # might be able to add an instance-dependent max?
                                                            max_value=num_citations_in_sentence,
                                                            key=str(i)+'precision',
                                                            on_change=save_time,
                                                            args=(i,'prec',)
                                                        )
                sources_container = st.empty()
                sources_container.markdown('''**Sources:**\n'''+cited_sources)
                if (prec_result!=-1):
                    eval_next_sentence(prec_result, i)
                    







