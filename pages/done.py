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
def generate_completion_code():
    alphanumeric = string.ascii_letters + string.digits
    return ''.join(random.choice(alphanumeric) for _ in range(25))

completion_code = generate_completion_code()
st.session_state["db_conn"].table('hit_completion_codes').insert({
                                             "completion_code": completion_code, 
                                             "annotator_id": st.session_state["username"],
                                             "code_used": False
                                             }).execute()
st.markdown('''# Done! Thank you so much! :raised_hands:''')
st.markdown('''Please enter the completion code below on the MTurk HIT webpage for compensation.''')
st.markdown(completion_code)