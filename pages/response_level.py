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
    for i in range(len(text)-len(substring)+1):
        if (substring == text[i:i+len(substring)]):
            ocurrences.append((i,i+len(substring)))
    return ocurrences

def get_highlighted_snippet(snippet_ls):
    for i in range(len(snippet_ls)):
        for ansi_escape_sequence in COLORS.keys():
            if (ansi_escape_sequence == '\x1b[0m'):
                snippet_ls[i] = snippet_ls[i].replace(ansi_escape_sequence, "</span>")
            else:
                snippet_ls[i] = snippet_ls[i].replace(ansi_escape_sequence, "<span class='orange-highlight'>")
    return snippet_ls

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
        curr_source = clear_ansi(cited_sources_ls[source_idx]).strip()
        curr_source_ls = curr_source.split('\n')
        if ('https://' in curr_source_ls[0]):
            curr_source_ls = curr_source.split('\n')
            curr_url = curr_source_ls[0][8:]
            if (curr_url[:4] == 'www.'):
                curr_url = curr_url[4:]
            curr_source = ' '.join(curr_source_ls[1:]).strip()
            sources_to_show.append(replace_dollar_signs('<b>Source: </b>'+curr_url+'\n\n'+curr_source))
        else:
            sources_to_show.append(replace_dollar_signs('<b>Source: </b>\n\n'+curr_source))
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

def replace_dollar_signs(text):
    return text.replace('$', '\$').strip()

def continue_from_snippet(response_id, fluency_rating, utility_rating):
    # write results to db
    st.session_state.db_conn.table(st.session_state['annotations_db']).insert({
    "annotator_id": st.session_state["username"], 
    "human_fluency_rating": int(fluency_rating),
    "human_utility_rating": int(utility_rating),
    "op": op,
    "query_id":int(response_id),
    }).execute()    
    st.session_state['touched_response_ids'] += [int(response_id)]
    st.session_state.db_conn.table(st.session_state['annotator_db_str']).update({'annotated_query_ids': st.session_state['touched_response_ids']}).eq('annotator_id', st.session_state["username"]).execute()
    
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
        st.session_state["hit_finished"] = True
        st.switch_page('pages/done.py')

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
        snippets_to_show = get_highlighted_snippet(unmarked_response)
        
        if (len(snippets_to_show) == 0):
            response_id = st.session_state["hit_df"].iloc[st.session_state["task_n"]]['ID']
            continue_from_snippet(response_id, -1, -1)
    
        unmarked_response = "\n\n".join(snippets_to_show)
        
    else:
        unmarked_response = format_remove_quotation_marks(st.session_state["hit_df"].iloc[st.session_state["task_n"]]['Output'])
        cited_response = st.session_state["hit_df"].iloc[st.session_state["task_n"]]['Output (cited)']
        sentences = eval(st.session_state["hit_df"].iloc[st.session_state["task_n"]]['Sent (cited)'])
        if (clear_ansi(sentences[0].strip()) not in clear_ansi(cited_response)):
            if (clear_ansi(sentences[0].strip()) in clear_ansi("\'"+cited_response)):
                unmarked_response = "\'"+format_remove_quotation_marks(st.session_state["hit_df"].iloc[st.session_state["task_n"]]['Output'])
    with col1:
        fluency_container = st.empty()
        unmarked_response = replace_dollar_signs(unmarked_response) 
        full_response_container.write("<p><b>System Response:</b>\n\n"+unmarked_response+"</p>", unsafe_allow_html=True)    

    fluency_options = ['1: Response has misprints or disfluent transitions and sentences', 
                       '2: Response has no misprints and mostly smooth transitions and sentences', 
                       '3: Response has no misprints and all of the sentences flow nicely together']
    fluency_label = "**Fluency Question:** To what extent is the response fluent and coherent?"
    fluency_rating = fluency_container.radio(
                                        label=fluency_label,
                                        options=fluency_options,
                                        index=None,
                                        key="fluency_"+str(st.session_state["task_n"]+1),
                                        )
    if (fluency_rating):
        with col1:
            utility_container = st.empty()
            
        utility_options = ['1: Response includes too many irrelevant details or the query is not addressed', 
                           '2: Response is only a partially satisfying answer to the query', 
                           '3: The response is concise and seems to be a satisfying answer to the query']
        utility_label = "**Utility Question:** To what extent does the response seem to be a useful answer to the query?"
        utility_rating = utility_container.radio(
                            label=utility_label,
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
                continue_from_snippet(response_id, st.session_state["fluency_rating"], st.session_state["utility_rating"])