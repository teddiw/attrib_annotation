import streamlit as st
import pandas as pd
import sys
import time

# COLORS = {0:'\033[92m', 1:'\033[96m', 2:'\033[95m', 3:'\033[1;31;60m', 4:'\033[102m', 5:'\033[1;35;40m', 6:'\033[0;30;47m', 7:'\033[0;33;47m', 8:'\033[0;34;47m', 9:'\033[0;31;47m', 10:'\033[0m', 11:'\033[1m'}
COLORS = {'\x1b[92m':':green[', '\x1b[96m':':orange[', '\x1b[95m':':red[', '\x1b[1;31;60m':':blue[', '\x1b[102m':':violet[', '\x1b[1;35;40m':':grey[', '\x1b[0;30;47m':':rainbow[', '\x1b[0;33;47m':':orange[', '\x1b[0;34;47m':':blue[', '\x1b[0;31;47m':':red[', '\x1b[0m':']'}

def highlight(text):
    for ansi_escape_sequence in COLORS.keys():
        text = text.replace(ansi_escape_sequence, COLORS[ansi_escape_sequence])
    return text

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
    op = st.session_state["hit_df"].iloc[st.session_state["task_n"]]['op']
    if (op == 'Snippet'):
        unmarked_response = eval(st.session_state["hit_df"].iloc[st.session_state["task_n"]]['Output'])
        unmarked_response = "\n_____________________________________________________________\n".join(unmarked_response)
    else:
        unmarked_response = format_remove_quotation_marks(st.session_state["hit_df"].iloc[st.session_state["task_n"]]['Output'])
    
    # highlighted_cited_sources = [highlight(s) for s in eval(cited_sources)]
    #     sources_container.markdown('''**Sources:**\n\n'''+"\n_____________________________________________________________\n".join(highlighted_cited_sources))
    
    # TODO I think we should be calling eval?
    # if (st.session_state["hit_df"].iloc[st.session_state["task_n"]]['op']=='Snippet'):
    #     full_response_container.markdown('''**System Response:**\n\n'''+"\n_____________________________________________________________\n".join(eval(unmarked_response)))
    # else:
    full_response_container.markdown('''**System Response:**\n'''+unmarked_response)
    sentence_container = st.empty()
    # query_container.text(st.session_state["hit_df"].iloc[st.session_state["task_n"]]['Question'])
    # st.markdown('''Happy Streamlit-ing! :balloon:''')
    st.divider()

    fluency_container = st.empty()
    fluency_options = ['1', '2', '3', '4', '5']
    fluency_rating = fluency_container.radio(
                                        label="Please rate the fluency of the response to the query.",
                                        options=fluency_options,
                                        index=None,
                                        key="fluency_"+str(st.session_state["task_n"]+1),
                                        )
    # fluency_rating = fluency_container.number_input(
    #         "Please enter your Likert rating",
    #         value=None,
    #         min_value=0,
    #         max_value=5,
    #         key="fluency_likert"+str(st.session_state["task_n"]+1),
    #         on_change=c,
    #         step=1
    #     )
    if (fluency_rating):
        # fluency_container.markdown('''Recorded :white_check_mark:''')
        # st.write("Fluency rating: ", fluency_rating)
        utility_container = st.empty()
        # utility_rating = utility_container.number_input(
        #         "Please enter your Likert rating",
        #         value=None,
        #         min_value=0,
        #         max_value=5,
        #         key="utility_likert"+str(st.session_state["task_n"]+1),
        #         on_change=save_start_time,
        #         step=1
        #     )
        utility_options = ['1', '2', '3', '4', '5']
        utility_rating = utility_container.radio(
                            label="Please rate the utility of the response to the query.",
                            options=utility_options,
                            index=None,
                            key="utility_"+str(st.session_state["task_n"]+1),
                            )
        if (utility_rating):
            # utility_container.markdown('''Recorded :white_check_mark:''')
            continue_container = st.empty()
            if ('b1_press' not in st.session_state):
                st.session_state["b1_press"] = False
            b1_press = continue_container.button('Continue task')
            if (st.session_state["b1_press"] or b1_press):
                st.session_state["utility_rating"] = int(utility_rating)
                st.session_state["fluency_rating"] = int(fluency_rating)
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
                    
                    # reset fluency/utility button press
                    st.session_state["b1_press"] = False

                    # increment to the next task
                    if (st.session_state["task_n"]<st.session_state["total_tasks"]-1):
                        st.session_state["task_n"] += 1
                        st.session_state['prec_t2v'] = []
                        st.session_state['cov_t2v'] = []
                        st.switch_page('pages/response_level.py')
                    else:
                        st.switch_page('pages/done.py')
                    
                
                sentences = eval(st.session_state["hit_df"].iloc[st.session_state["task_n"]]['Sent (cited)'])
                num_sentences = len(sentences)
                prec_results = []
                cov_results = [-1]*num_sentences
                placeholders_prec = {}
                placeholders_prec_text = []
                placeholders_cov = []
                placeholders_prec_button = []
                placeholders_cov_button = []
                citations_dict = eval(st.session_state["hit_df"].iloc[st.session_state["task_n"]]['Citation Dict'])
                for i in range(num_sentences):
                    placeholder = st.empty()
                    placeholders_prec_text.append(placeholder)
                    num_citations = len(citations_dict[str(i)]['citation_numbers'])
                    placeholders_prec[i] = []
                    for j in range(num_citations):
                        placeholder = st.empty()
                        placeholders_prec[i].append(placeholder)
                    placeholder = st.empty()
                    placeholders_prec_button.append(placeholder)
                    placeholder = st.empty()
                    placeholders_cov.append(placeholder)
                    placeholder = st.empty()
                    placeholders_cov_button.append(placeholder)

                def finish_up():
                    # write results to db that user annotated entire response
                    st.session_state.db_conn.table('annotations').insert({
                    "annotator_id": st.session_state["username"], 
                    "human_fluency_rating": int(st.session_state["fluency_rating"]),
                    "human_utility_rating": int(st.session_state["utility_rating"]),
                    "precise_citations": st.session_state['prec_results'],
                    "is_covered": st.session_state['cov_results'],
                    "t2v_precision": st.session_state['prec_t2v'],
                    "t2v_coverage": st.session_state['cov_t2v'],
                    "op": op,
                    "response_id":int(response_id),
                    }).execute()  
                    st.session_state['touched_response_ids'] += [int(response_id)]
                    st.session_state.db_conn.table('annotators').update({'annotated_response_ids': st.session_state['touched_response_ids']}).eq('annotator_id', st.session_state["username"]).execute()
                    
                    # reset button presses
                    st.session_state["b1_press"] = False
                    
                    # increment to the next task
                    if (st.session_state["task_n"]<st.session_state["total_tasks"]-1):
                        st.session_state["task_n"] += 1
                        st.session_state['prec_t2v'] = []
                        st.session_state['cov_t2v'] = []
                        st.switch_page('pages/response_level.py')
                    else:
                        st.switch_page('pages/done.py')
                    
                    return

                def eval_next_sentence(pressed, precision_checklist, citations_dict, i):
                    if (i > 0):
                        for j in range(len(placeholders_prec[i-1])):
                            placeholders_prec[i-1][j].empty()
                        placeholders_cov[i-1].empty()
                        placeholders_prec_text[i-1].empty()
                    if ('continue_press_sentence'+str(i)+'_task'+str(st.session_state["task_n"]) not in st.session_state):
                        st.session_state['continue_press_sentence'+str(i)+'_task'+str(st.session_state["task_n"])] = False
                    if (pressed or st.session_state['continue_press_sentence'+str(i)+'_task'+str(st.session_state["task_n"])]):# (prec_result!=-1):
                        if (pressed):
                            save_time(i,'prec',)
                        st.session_state['continue_press_sentence'+str(i)+'_task'+str(st.session_state["task_n"])] = True
                        placeholders_prec_button[i].empty()
                        prec_results.append({"sentence_id": i, "annotations": precision_checklist})
                        placeholders_prec[i][0].markdown('''Recorded :white_check_mark:''')
                        for j in range(1, len(placeholders_prec[i])):
                            placeholders_prec[i][j].empty()
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
                                # cited_response = st.session_state["hit_df"].iloc[st.session_state["task_n"]]['Output (cited)']
                                # cited_sources = st.session_state["hit_df"].iloc[st.session_state["task_n"]]['Used Sources (cited)']
                                # full_response_container.markdown('''**Cited System Response:**\n'''+highlight(cited_response))
                                sentence_container.markdown('''**Sentence to evaluate:**\n'''+highlight(sentence))
                                citations = citations_dict[str(i)]['citation_numbers']
                                num_citations_in_sentence = len(citations)
                                # prec_result = placeholders_prec[i].number_input(
                                #                                             "How many of the citations in the sentence actually support a claim in the sentence, according to the sources below?",
                                #                                             value=-1,
                                #                                             min_value=-1,
                                #                                             max_value=num_citations_in_sentence,
                                #                                             key=str(i)+'precision',
                                #                                             on_change=save_time,
                                #                                             args=(i,'prec',),
                                #                                             step=1
                                #                                             )
                                placeholders_prec_text[i].markdown('''*Please select each citation that supports a claim in the sentence.*''')
                                # sources_container.markdown('''**Sources:**\n'''+highlight(cited_sources))

                                precision_checklist = []
                                for j in range(num_citations_in_sentence):
                                    precision_checklist.append(placeholders_prec[i][j].checkbox(str(citations[j]), key='cb_sentence'+str(i)+'_citation'+str(j)))
                                # if ('continue_press_sentence'+str(i)+'_task'+str(st.session_state["task_n"]) not in st.session_state):
                                #     st.session_state['continue_press_sentence'+str(i)] = False
                                pressed = False
                                pressed = placeholders_prec_button[i].button('Continue task', key='continue_press_button_sentence'+str(i))
                                eval_next_sentence(pressed, precision_checklist, citations_dict, i)
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
                save_start_time()
                sentence = sentences[i]
                cited_response = st.session_state["hit_df"].iloc[st.session_state["task_n"]]['Output (cited)']
                cited_sources = st.session_state["hit_df"].iloc[st.session_state["task_n"]]['Used Sources (cited)']
                full_response_container.markdown('''**Cited System Response:**\n'''+highlight(cited_response))
                sentence_container.markdown('''**Sentence to evaluate:**\n'''+highlight(sentence))
                sources_container = st.empty()
                highlighted_cited_sources = [highlight(s) for s in eval(cited_sources)]
                sources_container.markdown('''**Sources:**\n\n'''+"\n_____________________________________________________________\n".join(highlighted_cited_sources))
                citations_dict = eval(st.session_state["hit_df"].iloc[st.session_state["task_n"]]['Citation Dict'])
                citations = citations_dict[str(i)]['citation_numbers']
                num_citations_in_sentence = len(citations)

                prec_result = -1
                # prec_result = placeholders_prec[i].number_input( 
                #                                             "How many of the citations in the sentence actually support a claim in the sentence, according to the sources below?",
                #                                             value=-1,
                #                                             min_value=-1, # might be able to add an instance-dependent max?
                #                                             max_value=num_citations_in_sentence,
                #                                             key=str(i)+'precision',
                #                                             on_change=save_time,
                #                                             args=(i,'prec',),
                #                                             step=1
                #                                         )
                # prec_result = placeholders_prec[i].radio(
                #                         label='''How many of the citations in the sentence actually support a claim in the sentence, according to the sources below?''',
                #                         options=citations,
                #                         index=None,
                #                         key=str(i)+'precision',
                #                         on_change=save_time,
                #                         args=(i,'prec',))                    
                # "Select the citation(s) that support a claim in the sentence, according to the sources below.")

                placeholders_prec_text[i].markdown('''*Please select each citation that supports a claim in the sentence.*''')
                precision_checklist = []
                for j in range(num_citations_in_sentence):
                    precision_checklist.append(placeholders_prec[i][j].checkbox(str(citations[j]), key='cb_sentence'+str(i)+'_citation'+str(j)))
                if ('continue_press_sentence'+str(i)+'_task'+str(st.session_state["task_n"]) not in st.session_state):
                    st.session_state['continue_press_sentence'+str(i)+'_task'+str(st.session_state["task_n"])] = False
                pressed = placeholders_prec_button[i].button('Continue task', key='continue_press_button_sentence'+str(i))
                # if (st.session_state['continue_press'+str(i)] or pressed):
                #     # store as json file
                eval_next_sentence(pressed, precision_checklist, citations_dict, i)
                    







