import streamlit as st
import random
import string

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
completion_code = st.session_state["db_conn"].table("hit_completion_codes").select("completion_code").eq("hit_specific_id", st.session_state["hit_specific_id"]).execute().data[0]['completion_code']
if (st.session_state["hit_finished"]):
    st.markdown('''# Done! Thank you so much! :raised_hands:''')
    st.markdown('''Please enter the completion code below on the MTurk HIT webpage for compensation.''')
    st.markdown(completion_code)
else:
    st.markdown('''# Incomplete''')