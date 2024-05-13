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

def clear_ansi(text):
    for ansi_escape_sequence in COLORS.keys():
        if (ansi_escape_sequence in text):
            text = text.replace(ansi_escape_sequence, '')
    return text

def highlight(text):
    # for ansi_escape_sequence in COLORS.keys():
    #     text = text.replace(ansi_escape_sequence, COLORS[ansi_escape_sequence])
    for ansi_escape_sequence in COLORS.keys():
        if (ansi_escape_sequence in text):
            md_color = get_md_color(ansi_escape_sequence)
            text = text.replace(ansi_escape_sequence, '')# md_color)
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
            st.session_state['prec_t2v'].append(seconds_elapsed)
        else:
            st.session_state['prec_t2v'] = [seconds_elapsed]
        st.session_state["start_time"] = time.time()
    else:
        if ('cov_t2v' in st.session_state):
            st.session_state['cov_t2v'].append(seconds_elapsed)
        else:
            st.session_state['cov_t2v'] = [seconds_elapsed]
        st.session_state["start_time"] = time.time()
    return

def get_substring_indices(text, substring):
    i = 0
    ocurrences = []
    for i in range(len(text)-len(substring)):
        if (substring == text[i:i+len(substring)]):
            ocurrences.append((i,i+len(substring)))
    return ocurrences

def get_cited_sources_for_sentence(cited_sources_ls, citations):
    sources_idxs_to_show = {}
    for citation_num in citations:
        citation = '['+str(citation_num)+']'
        highlighted_citation = "<span class='orange-highlight'>"+citation
        found_citation = False
        for ansi_escape_sequence in COLORS.keys():
            if (found_citation):
                break
            ansi_citation = ansi_escape_sequence+citation

            for j in range(len(cited_sources_ls)):
                source = cited_sources_ls[j]
                if (ansi_citation in source):
                    found_citation = True
                    start_citation_occurrences = get_substring_indices(source, ansi_citation)
                    source_to_use = source[:start_citation_occurrences[0][0]]+highlighted_citation+source[start_citation_occurrences[0][1]:]
                    end_citation_occurrences = get_substring_indices(source_to_use, '\x1b[0m')
                    slice_to_use = None
                    for slice in end_citation_occurrences:
                        if (slice[0] > start_citation_occurrences[0][0]):
                            slice_to_use = slice
                            break
                    source_to_use = source_to_use[:slice_to_use[0]]+"</span>"+source_to_use[slice_to_use[1]:]
                    cited_sources_ls[j] = source_to_use
                    if (j not in sources_idxs_to_show.keys()):
                        sources_idxs_to_show[j] = None
                    break

    sources_to_show = []
    for source_idx in sources_idxs_to_show.keys(): 
        curr_source = clear_ansi(cited_sources_ls[source_idx])
        curr_source_ls = curr_source.split('\n')
        curr_url = curr_source_ls[0][8:]
        if (curr_url[:4] == 'www.'):
            curr_url = curr_url[4:]
        curr_source = ' '.join(curr_source_ls[1:])
        sources_to_show.append('<b>Source: </b>'+curr_url+'\n\n'+curr_source)
    return sources_to_show

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

    p {
    font-size:18px;
    }

    .orange-highlight {
        background-color: hsla(42, 100%, 51%, 0.75);
    }

    .big-font {
    font-size:14px !important;
    font-style:italic;  
    }

    .highlighted-font {
    background-color: green; 
    }

</style>
""", unsafe_allow_html=True,
) 

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
                cov_results = []
                placeholders_prec = {}
                placeholders_prec_text = []
                placeholders_cov = []
                placeholders_prec_button = []
                placeholders_cov_button = []
                placeholders_sources = []
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
                        placeholders_cov.append(placeholder)
                        placeholder = st.empty()
                        placeholders_cov_button.append(placeholder)

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

                def eval_next_sentence(cov_pressed, cov_result, citations_dict, i, save_time, col2_container, sources_placeholder):
                     # clear any previous coverage question container
                    if (i > 0):
                        placeholders_prec_text[i].empty()
                        for j in range(0, len(placeholders_prec[i])):
                            placeholders_prec[i][j].empty()
                    
                    # Set state variable for coverage submission button press
                    if ('cov_continue_press_sentence'+str(i)+'_task'+str(st.session_state["task_n"]) not in st.session_state):
                        st.session_state['cov_continue_press_sentence'+str(i)+'_task'+str(st.session_state["task_n"])] = False

                    # if the coverage submission button is pressed, then proceed
                    if ((cov_pressed and cov_result) or st.session_state['cov_continue_press_sentence'+str(i)+'_task'+str(st.session_state["task_n"])]):
                        
                        if (cov_pressed):
                            # if pressed for the first time (not on a internal page re-run), record the time
                            save_time(i,'cov') # TODO change what's needed in this fn to swap
                        
                        # Set coverage submission button variables and remove the button
                        cov_pressed = False
                        st.session_state['cov_continue_press_sentence'+str(i)+'_task'+str(st.session_state["task_n"])] = True
                        placeholders_cov_button[i].empty()

                        # Record the coverage results and remove the coverage text and checklist
                        if cov_result == "Yes":
                            cov_results.append({"sentence_id": i, "coverage": 1})
                        else:
                            cov_results.append({"sentence_id": i, "coverage": 0})
                        
                        cov_result = None
                        placeholders_cov[i].empty()
                        placeholders_cov_button[i].empty()

                        # Now, prepare to ask about precision.
                        # Display precision prompt and checklist
                        placeholders_prec_text[i].markdown('<p class="big-font">2. Please select each citation below whose source supports information in the highlighted sentence above.</p>', unsafe_allow_html=True)
                        precision_checklist = []
                        citations = citations_dict[str(i)]['citation_numbers']
                        for j in range(len(citations)):
                            precision_checklist.append(placeholders_prec[i][j].checkbox('['+str(citations[j])+']', key='cb_sentence'+str(i)+'_citation'+str(j)))
                        # Set state variable for precision submission button press
                        if ('continue_press_sentence'+str(i)+'_task'+str(st.session_state["task_n"]) not in st.session_state):
                            st.session_state['continue_press_sentence'+str(i)+'_task'+str(st.session_state["task_n"])] = False
                    
                        # Display precision submission button
                        pressed = placeholders_prec_button[i].button('Continue task', key='continue_press_button_sentence'+str(i))
                    
                        # Once we get the precision result...
                        if (pressed or st.session_state['continue_press_sentence'+str(i)+'_task'+str(st.session_state["task_n"])]):
                            # save T2V
                            if (pressed):
                                save_time(i,'prec')
                            
                            # remove prec button
                            placeholders_prec_button[i].empty()
                            st.session_state['continue_press_sentence'+str(i)+'_task'+str(st.session_state["task_n"])] = True
                            
                            # Stash the precision result
                            prec_results.append({"sentence_id": i, "annotations": precision_checklist})
                            placeholders_prec_text[i].empty()
                            for j in range(0, len(placeholders_prec[i])):
                                placeholders_prec[i][j].empty()
                            
                            i += 1
                            # On to the next sentence, if there is one
                            if (i < num_sentences):
                                # Get next sentence
                                sentence = sentences[i]
                                # Update subheading
                                subheader_container.subheader("Sentence "+str(i+1)+"/"+str(len(sentences)))

                                # Get and display highlighted response
                                cited_response = st.session_state["hit_df"].iloc[st.session_state["task_n"]]['Output (cited)']
                                sentence = clear_ansi(sentence)
                                full_response_container.markdown("<p>Cited System Response:\n\n"+clear_ansi(cited_response).replace(sentence.strip(), "<span class='orange-highlight'>"+sentence.strip()+"</span>")+"</p>", unsafe_allow_html=True)
                                
                                # Get and display highlighted sources for this sentence
                                cited_sources_ls = eval(st.session_state["hit_df"].iloc[st.session_state["task_n"]]['Used Sources (cited)'])
                                citations = citations_dict[str(i)]['citation_numbers']
                                highlighted_cited_sources = get_cited_sources_for_sentence(cited_sources_ls, citations)
                                with col2_container:
                                    sources_placeholder.write("\n_____________________________________________________________\n".join(highlighted_cited_sources), unsafe_allow_html=True)

                                if (len(citations)==0):
                                    # If there are no citations in the first sentence, set up variables for the next sentence
                                    st.session_state['cov_continue_press_sentence'+str(i)+'_task'+str(st.session_state["task_n"])] = True
                                    st.session_state['continue_press_sentence'+str(i)+'_task'+str(st.session_state["task_n"])] = True

                                else:
                                    if (num_citations_in_sentence == 0):
                                        # TODO may expand this case to allow for "yes" if no citation is needed? or just keep as None.
                                        cov_result = "No"
                                    else:
                                        # build the string citation list
                                        citations_str = ''
                                        for k in range(len(citations)):
                                            citation_num = citations[k]
                                            if (len(citations)==1):
                                                citations_str += '['+str(citation_num)+']'
                                                break
                                            if (k == len(citations)-1):
                                                citations_str += 'and ['+str(citation_num)+']'
                                            elif (len(citations)==2):
                                                citations_str += '['+str(citation_num)+'] '
                                            else:
                                                citations_str += '['+str(citation_num)+'], '
                                        if (num_citations_in_sentence == 1):
                                            coverage_text = '*1. Does the source of '+citations_str+' support **all** information in the sentence?*'
                                        else:
                                            coverage_text = '*1. Do the sources of '+citations_str+' together support **all** information in the sentence?*'
                                        # Show the coverage question and multiple choice
                                        cov_result = placeholders_cov[i].radio(
                                                    label=coverage_text,
                                                    options=["Yes", "No"],
                                                    index=None,
                                                    key=str(i)+'coverage',
                                                    args=(i,'cov',))
                                        cov_pressed = placeholders_cov_button[i].button('Continue task', key='cov_continue_press_button_sentence'+str(i))

                                # Next call to eval
                                eval_next_sentence(cov_pressed, cov_result, citations_dict, i, save_time, col2_container, sources_placeholder)
                            else:
                                # If no next sentence, save everything to the database
                                st.session_state['prec_results'] = prec_results
                                st.session_state['cov_results'] = cov_results
                                finish_up()
                                return
                i = 0
                # Get cited sentences and display subheader
                sentence = sentences[i]
                sentence = clear_ansi(sentence)
                subheader_container.subheader("Sentence "+str(i+1)+"/"+str(len(sentences)))

                # Get cited response and sources
                cited_response = st.session_state["hit_df"].iloc[st.session_state["task_n"]]['Output (cited)']
                cited_sources = st.session_state["hit_df"].iloc[st.session_state["task_n"]]['Used Sources (cited)']
                
                # Display cited response with highlighted sentence
                full_response_container.markdown("<p>Cited System Response:\n\n"+clear_ansi(cited_response).replace(sentence.strip(), "<span class='orange-highlight'>"+sentence.strip()+"</span>")+"</p>", unsafe_allow_html=True)
                
                # Get highlighted sources for this sentence
                cited_sources_ls = eval(cited_sources)
                citations_dict = eval(st.session_state["hit_df"].iloc[st.session_state["task_n"]]['Citation Dict'])
                citations = citations_dict[str(i)]['citation_numbers']
                highlighted_cited_sources = get_cited_sources_for_sentence(cited_sources_ls, citations)
                
                # Display highlighted sources for this sentence
                col2_container = col2.container(height=600)
                with col2_container:
                    sources_placeholder = st.empty()
                    sources_placeholder.write("\n_____________________________________________________________\n".join(highlighted_cited_sources), unsafe_allow_html=True)
                
                if (len(citations)==0):
                    # If there are no citations in the first sentence, set up variables for the next sentence
                    st.session_state['cov_continue_press_sentence'+str(i)+'_task'+str(st.session_state["task_n"])] = True
                    if ('prec_t2v' not in st.session_state):
                        st.session_state['prec_t2v'] = []
                    if ('cov_t2v' not in st.session_state):
                        st.session_state['cov_t2v'] = []
                else:
                
                    # First, get citations
                    citations = citations_dict[str(i)]['citation_numbers']
                    num_citations_in_sentence = len(citations)

                    if (num_citations_in_sentence == 0):
                        # TODO may expand this case to allow for "yes" if no citation is needed? or just keep as None.
                        cov_result = "No"
                    else:
                        # build the string citation list
                        citations_str = ''
                        for k in range(len(citations)):
                            citation_num = citations[k]
                            if (len(citations)==1):
                                citations_str += '['+str(citation_num)+']'
                                break
                            if (k == len(citations)-1):
                                citations_str += 'and ['+str(citation_num)+']'
                            elif (len(citations)==2):
                                citations_str += '['+str(citation_num)+'] '
                            else:
                                citations_str += '['+str(citation_num)+'], '
                        if (num_citations_in_sentence == 1):
                            coverage_text = '*1. Does the source of '+citations_str+' support **all** information in the sentence?*'
                        else:
                            coverage_text = '*1. Do the sources of '+citations_str+' together support **all** information in the sentence?*'
                        # Show the coverage question and multiple choice
                        cov_result = placeholders_cov[i].radio(
                                    label=coverage_text,
                                    options=["Yes", "No"],
                                    index=None,
                                    key=str(i)+'coverage',
                                    args=(i,'cov',))
                        cov_pressed = placeholders_cov_button[i].button('Continue task', key='cov_continue_press_button_sentence'+str(i))
                        
                    
                # Proceed to coverage & then the next sentence
                eval_next_sentence(cov_pressed, cov_result, citations_dict, i, save_time, col2_container, sources_placeholder)
                    







