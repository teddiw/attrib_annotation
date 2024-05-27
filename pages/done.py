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

completion_code = generate_completion_code(20)
st.session_state["db_conn"].table('hit_completion_codes').insert({
                                             "completion_code": completion_code, 
                                             "annotator_id": st.session_state["username"],
                                             "used_code": 0,
                                             }).execute()
print(completion_code)
st.markdown('''# Done! Thank you so much! :raised_hands:''')
