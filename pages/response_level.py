import streamlit as st
import pandas as pd
import sys
import time

# OLD_COLORS = {0:'\033[92m', 1:'\033[96m', 2:'\033[95m', 3:'\033[1;31;60m', 4:'\033[102m', 5:'\033[1;35;40m', 6:'\033[0;30;47m', 7:'\033[0;33;47m', 8:'\033[0;34;47m', 9:'\033[0;31;47m', 10:'\033[0m', 11:'\033[1m'}
COLORS = {'\x1b[92m':':green[', '\x1b[96m':':orange[', '\x1b[95m':':red[', '\x1b[1;31;60m':':blue[', '\x1b[102m':':violet[', '\x1b[1;35;40m':':grey[', '\x1b[0;30;47m':':rainbow[', '\x1b[0;33;47m':':orange[', '\x1b[0;34;47m':':blue[', '\x1b[0;31;47m':':red[', '\x1b[0m':']'}
MD_IDX_TO_MD_COLORS = {0:':orange[', 1:':green[', 2:':blue[', 3:':red[', 4:':rainbow[', 5:':violet[', 6:':orange[', 7:':blue[', 8:':green[', 9:':red['}
NUM_TO_ALPHA = {0: 'A', 1:'B', 2:'C', 3:'D', 4:'E', 5:'F', 6:'G', 7:'H', 8:'I', 9:'J'}
def get_md_color(ansi_escape_sequence):
    if ('ANSI_TO_MD_IDX' not in st.session_state):
        st.session_state['ANSI_TO_MD_IDX'] = {}
    if (ansi_escape_sequence == '\x1b[0m'):
        return '] '
    if (len(st.session_state["ANSI_TO_MD_IDX"]) == 0):
        st.session_state["ANSI_TO_MD_IDX"][ansi_escape_sequence] = 0
    if (ansi_escape_sequence not in st.session_state["ANSI_TO_MD_IDX"].keys()):
        st.session_state["ANSI_TO_MD_IDX"][ansi_escape_sequence] = max(st.session_state["ANSI_TO_MD_IDX"].values())+1
    md_idx = st.session_state["ANSI_TO_MD_IDX"][ansi_escape_sequence]
    return MD_IDX_TO_MD_COLORS[md_idx]

def highlight(text):
    # for ansi_escape_sequence in COLORS.keys():
    #     text = text.replace(ansi_escape_sequence, COLORS[ansi_escape_sequence])
    for ansi_escape_sequence in COLORS.keys():
        if (ansi_escape_sequence in text):
            md_color = get_md_color(ansi_escape_sequence)
            text = text.replace(ansi_escape_sequence, md_color)
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
        # st.session_state["started_timer"] = True
    return

start_time = 0
## Page configs
st.set_page_config(initial_sidebar_state="collapsed",layout="wide")

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
.big-font {
    font-size:14px !important;
    font-style:italic;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.highlighted-font {
    background-color: green; 
}
</style>
""", unsafe_allow_html=True)

if ("hit_df" in st.session_state):
    st.header("Task "+str(st.session_state["task_n"]+1)+"/"+str(st.session_state["total_tasks"]))
    subheader_container = st.empty()
    col1, col2 = st.columns(2)
    with col1:
        query_container = st.empty()
        query_container.markdown('''**User Query:**\n'''+st.session_state["hit_df"].iloc[st.session_state["task_n"]]['Question'])
        full_response_container = st.empty()
    op = st.session_state["hit_df"].iloc[st.session_state["task_n"]]['op']
    if (op == 'Snippet'):
        unmarked_response = eval(st.session_state["hit_df"].iloc[st.session_state["task_n"]]['Output'])
        unmarked_response = "\n\n".join(unmarked_response)
    else:
        unmarked_response = format_remove_quotation_marks(st.session_state["hit_df"].iloc[st.session_state["task_n"]]['Output'])
    
    # with col2.container(height=700):
    #     fluency_rubric_container = st.empty()
    #     utility_rubric_container = st.empty()
    #     fluency_rubric_df = pd.DataFrame({'Fluency Rating':[1,2,3,4,5], 
    #                                       'Fluency Rubric':['Frequent typos or grammatical errors and often missing natural transitions between sentences',
    #                                                         'Some typos or grammatical errors and sometimes missing natural transitions between sentences',
    #                                                         'No typos, minor grammatical errors, and mostly has natural transitions between sentences',
    #                                                         'No typos, no grammatical errors, and mostly has natural transitions between sentences',
    #                                                         'No typos, no grammatical errors, and always has natural transitions between sentences']},
    #                                                         index=None)
    #     utility_rubric_df = pd.DataFrame({'Utility Rating':[1,2,3,4,5], 
    #                                       'Utility Rubric':['The response does not answer the query or contains a lot of unnecessary content.',
    #                                                         'The response appears to partially answer the query but contains some unnecessary content.',
    #                                                         'The response appears to partially answer the query without unnecessary content.',
    #                                                         'The response appears to fully answer the query with some unnecessary content.',
    #                                                         'The response appears to fully answer the query without unnecessary content.',]},
    #                                                         index=None)
    #     fluency_rubric_container.write(fluency_rubric_df)
    #     utility_rubric_container.write(utility_rubric_df)

    with col1:
        full_response_container.markdown('''**System Response:**\n\n'''+unmarked_response)
        # st.divider()
        # sentence_container = st.empty()
        fluency_container = st.empty()
    fluency_options = ['1: Strongly disagree', '2: Disagree', '3: Neither agree nor disagree', '4: Agree', '5: Strongly agree']
    fluency_rating = fluency_container.radio(
                                        label="*1. To what extent do you agree with the following:*\n\n **The response is fluent and coherent.**",
                                        options=fluency_options,
                                        index=None,
                                        key="fluency_"+str(st.session_state["task_n"]+1),
                                        )
    if (fluency_rating):
        with col1:
            utility_container = st.empty()
        utility_options = ['1: Strongly disagree', '2: Disagree', '3: Neither agree nor disagree', '4: Agree', '5: Strongly agree']
        utility_rating = utility_container.radio(
                            label="*2. To what extent do you agree with the following:*\n\n **If you assume the information is factual, the response is a useful answer to the query.**",
                            options=utility_options,
                            index=None,
                            key="utility_"+str(st.session_state["task_n"]+1),
                            )
        if (utility_rating):
            with col1:
                continue_container = st.empty()
            if ('b1_press' not in st.session_state):
                st.session_state["b1_press"] = False
            b1_press = continue_container.button('Continue task', on_click=save_start_time)
            if (st.session_state["b1_press"] or b1_press):
                st.session_state["utility_rating"] = int(utility_rating[0])
                st.session_state["fluency_rating"] = int(fluency_rating[0])
                st.session_state["b1_press"] = True
                fluency_container.empty()
                utility_container.empty()
                continue_container.empty()
                op = st.session_state["hit_df"].iloc[st.session_state["task_n"]]['op']
                response_id = st.session_state["hit_df"].iloc[st.session_state["task_n"]]['ID']
                if (op == 'Snippet'):
                    # write results to db
                    st.session_state.db_conn.table(st.session_state['annotations_db']).insert({
                    "annotator_id": st.session_state["username"], 
                    "human_fluency_rating": int(st.session_state["fluency_rating"]),
                    "human_utility_rating": int(st.session_state["utility_rating"]),
                    "op": op,
                    "query_id":int(response_id),
                    }).execute()    
                    st.session_state['touched_response_ids'] += [int(response_id)]
                    st.session_state.db_conn.table('annotators').update({'annotated_query_ids': st.session_state['touched_response_ids']}).eq('annotator_id', st.session_state["username"]).execute()
                    
                    # reset fluency/utility button press
                    st.session_state["b1_press"] = False

                    # increment to the next task
                    if (st.session_state["task_n"]<st.session_state["total_tasks"]-1):
                        st.session_state["task_n"] += 1
                        st.session_state['prec_t2v'] = []
                        st.session_state['cov_t2v'] = []
                        st.session_state['ANSI_TO_MD_IDX'] = {}
                        st.switch_page('pages/response_level.py')
                    else:
                        st.switch_page('pages/done.py')
                    
                
                sentences = eval(st.session_state["hit_df"].iloc[st.session_state["task_n"]]['Sent (cited)'])
                num_sentences = len(sentences)
                prec_results = []
                cov_results = [-1]*num_sentences
                requires_attrib_results = []
                placeholders_requires_attrib = []
                placeholders_prec = {}
                placeholders_prec_text = []
                placeholders_cov = []
                placeholders_prec_button = []
                placeholders_cov_button = []
                citations_dict = eval(st.session_state["hit_df"].iloc[st.session_state["task_n"]]['Citation Dict'])
                for i in range(num_sentences):
                    with col1:
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
                        placeholder = st.empty()
                        placeholders_requires_attrib.append(placeholder)
                        placeholders_cov.append(placeholder)
                        placeholder = st.empty()
                        placeholders_cov_button.append(placeholder)
                # with col1:
                    # st.divider()

                def finish_up():
                    # write results to db that user annotated entire response
                    st.session_state.db_conn.table(st.session_state['annotations_db']).insert({
                    "annotator_id": st.session_state["username"], 
                    "human_fluency_rating": int(st.session_state["fluency_rating"]),
                    "human_utility_rating": int(st.session_state["utility_rating"]),
                    "precise_citations": st.session_state['prec_results'],
                    "is_covered": st.session_state['cov_results'],
                    "t2v_precision": st.session_state['prec_t2v'],
                    "t2v_coverage": st.session_state['cov_t2v'],
                    "op": op,
                    "query_id":int(response_id),
                    "requires_attrib":st.session_state['requires_attrib_results']
                    }).execute()  
                    st.session_state['touched_response_ids'] += [int(response_id)]
                    st.session_state.db_conn.table('annotators').update({'annotated_query_ids': st.session_state['touched_response_ids']}).eq('annotator_id', st.session_state["username"]).execute()
                    
                    # reset button presses
                    st.session_state["b1_press"] = False
                    
                    # increment to the next task
                    if (st.session_state["task_n"]<st.session_state["total_tasks"]-1):
                        st.session_state["task_n"] += 1
                        st.session_state['prec_t2v'] = []
                        st.session_state['cov_t2v'] = []
                        st.session_state['ANSI_TO_MD_IDX'] = {}
                        st.switch_page('pages/response_level.py')
                    else:
                        st.switch_page('pages/done.py')
                    
                    return

                def eval_next_sentence(pressed, precision_checklist, requires_attrib, citations_dict, i, save_time):
                    if (i > 0):
                        # for j in range(len(placeholders_prec[i-1])):
                        #     placeholders_prec[i-1][j].empty()
                        # placeholders_prec_text[i-1].empty()
                        placeholders_requires_attrib[i-1].empty()
                        placeholders_cov[i-1].empty()
                    if ('continue_press_sentence'+str(i)+'_task'+str(st.session_state["task_n"]) not in st.session_state):
                        st.session_state['continue_press_sentence'+str(i)+'_task'+str(st.session_state["task_n"])] = False
                    if (pressed or st.session_state['continue_press_sentence'+str(i)+'_task'+str(st.session_state["task_n"])]):# (prec_result!=-1):
                        if (pressed):
                            save_time(i,'prec')
                        pressed = False
                        st.session_state['continue_press_sentence'+str(i)+'_task'+str(st.session_state["task_n"])] = True
                        placeholders_prec_button[i].empty()
                        prec_results.append({"sentence_id": i, "annotations": precision_checklist})
                        requires_attrib_results.append(requires_attrib)
                        # if (len(placeholders_prec[i])>0):
                        #     placeholders_prec[i][0].markdown('''Recorded :white_check_mark:''')
                        placeholders_prec_text[i].empty()
                        for j in range(0, len(placeholders_prec[i])):
                            placeholders_prec[i][j].empty()

                        # check if no citations
                        num_citations_in_sentence = len(citations_dict[str(i)]['citation_numbers'])
                        if (num_citations_in_sentence == 0):
                            cov_result = "No"
                            # save_time(i,'cov')
                        else:
                            cov_result = placeholders_cov[i].radio(
                                        label='''*3. Do the sources of the citation(s) in the italicized sentence together support **all** information in the sentence?*''',
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
                            # placeholders_cov[i].markdown('''Recorded :white_check_mark:''')
                            cov_result = None

                            i += 1
                            if (i < num_sentences):
                                sentence = sentences[i]
                                subheader_container.subheader("Sentence "+str(i+1)+"/"+str(len(sentences)))
                                highlighted_sentence = highlight(sentence)
                                cited_response = st.session_state["hit_df"].iloc[st.session_state["task_n"]]['Output (cited)']
                                full_response_container.markdown('''**Cited System Response:**\n\n'''+highlight(cited_response).replace(highlighted_sentence.strip(), '''***'''+highlighted_sentence.strip()+'''***'''))
                                # sentence_container.markdown('''**Sentence to evaluate:**\n'''+highlighted_sentence)
                                citations = citations_dict[str(i)]['citation_numbers']
                                num_citations_in_sentence = len(citations)
                                
                                if (num_citations_in_sentence==0):
                                    st.session_state['continue_press_sentence'+str(i)+'_task'+str(st.session_state["task_n"])] = True
                                    precision_checklist = []
                                else:
                                    requires_attrib = placeholders_requires_attrib[i].checkbox("2. The sentence contains information that requires citation.", value=True, key='ra_sentence'+str(i))
                                    placeholders_prec_text[i].markdown('<p class="big-font">1. Please select each citation whose source (on the right) supports information in the italicized sentence above.</p>', unsafe_allow_html=True)
                                    precision_checklist = []
                                    for j in range(num_citations_in_sentence):
                                        precision_checklist.append(placeholders_prec[i][j].checkbox(str(citations[j]), key='cb_sentence'+str(i)+'_citation'+str(j)))
                                    pressed = placeholders_prec_button[i].button('Continue task', key='continue_press_button_sentence'+str(i))
                                eval_next_sentence(pressed, precision_checklist, requires_attrib, citations_dict, i, save_time)
                            else:
                                st.session_state['prec_results'] = prec_results
                                st.session_state['cov_results'] = cov_results
                                st.session_state['requires_attrib_results'] = requires_attrib_results
                                finish_up()
                                return
                i = 0
                sentence = sentences[i]
                cited_response = st.session_state["hit_df"].iloc[st.session_state["task_n"]]['Output (cited)']
                cited_sources = st.session_state["hit_df"].iloc[st.session_state["task_n"]]['Used Sources (cited)']
                subheader_container.subheader("Sentence "+str(i+1)+"/"+str(len(sentences)))
                highlighted_sentence = highlight(sentence)
                full_response_container.markdown('''**Cited System Response:**\n\n'''+highlight(cited_response).replace(highlighted_sentence.strip(), '''***'''+highlighted_sentence.strip()+'''***'''))
                # sentence_container.markdown('''**Sentence to evaluate:**\n'''+highlighted_sentence)
                cited_sources_ls = eval(cited_sources)
                for j in range(len(cited_sources_ls)):
                    curr_source = cited_sources_ls[j]
                    curr_source_ls = curr_source.split('\n')
                    curr_url = curr_source_ls[0]
                    curr_source = ' '.join(curr_source_ls[1:])
                    curr_source = '**Source '+NUM_TO_ALPHA[j]+': '+curr_url+'**\n\n'+curr_source
                    cited_sources_ls[j] = curr_source
                highlighted_cited_sources = [highlight(cited_sources_ls[j]) for j in range(len(cited_sources_ls))]
                with col2.container(height=700):
                    sources_container = st.empty()
                    sources_container.markdown("\n_____________________________________________________________\n".join(highlighted_cited_sources))
                citations_dict = eval(st.session_state["hit_df"].iloc[st.session_state["task_n"]]['Citation Dict'])
                citations = citations_dict[str(i)]['citation_numbers']
                num_citations_in_sentence = len(citations)
                if (num_citations_in_sentence==0):
                    st.session_state['continue_press_sentence'+str(i)+'_task'+str(st.session_state["task_n"])] = True
                    precision_checklist = []
                    requires_attrib = False
                else:
                    requires_attrib = placeholders_requires_attrib[i].checkbox('2. The sentence contains information that requires citation.', value=True, key='ra_sentence'+str(i))
                    placeholders_prec_text[i].markdown('<p class="big-font">1. Please select each citation whose source (on the right) supports information in the italicized sentence above.</p>', unsafe_allow_html=True)
                    precision_checklist = []
                    for j in range(num_citations_in_sentence):
                        precision_checklist.append(placeholders_prec[i][j].checkbox(str(citations[j]), key='cb_sentence'+str(i)+'_citation'+str(j)))
                    if ('continue_press_sentence'+str(i)+'_task'+str(st.session_state["task_n"]) not in st.session_state):
                        st.session_state['continue_press_sentence'+str(i)+'_task'+str(st.session_state["task_n"])] = False
                pressed = placeholders_prec_button[i].button('Continue task', key='continue_press_button_sentence'+str(i))

                eval_next_sentence(pressed, precision_checklist, requires_attrib, citations_dict, i, save_time)
                    







