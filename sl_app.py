import streamlit as st
import pandas as pd
import sys
import ssl
from streamlit_gsheets import GSheetsConnection


ssl._create_default_https_context = ssl._create_stdlib_context
st.set_page_config(initial_sidebar_state="collapsed",
                   page_title="Username Form", 
                   page_icon=":mag_right:")

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

# Connect to google sheets
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read()
# Print results.
i = 0
for row in df.itertuples():
    st.write(f"{row.ID} has a :{row.Question}:")
    i+=1
    if (i > 10):
       break


## Page configs
st.title("Citation Correctness Task")

st.session_state["username"] = st.text_input(
        "Please enter your WorkerID",
        key="get_username",
        max_chars=20,
    )
# data = pd.read_json('https://drive.google.com/file/d/1vzVPykQIGH3uL7Tr48hMFe-SroV2lsrw/view?usp=sharing', lines=True)
# data = pd.read_csv('https://drive.google.com/file/d/1ZFQ9x3T6hjh_rJogiR2w4yy_chxQj_S5/view?usp=sharing', on_bad_lines='skip')
# breakpoint()

if (st.session_state["username"]):
  st.write("You entered: ", st.session_state["username"])
  st.switch_page('pages/response_level.py')
  




