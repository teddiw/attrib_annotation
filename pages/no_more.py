import streamlit as st

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
st.markdown('''# All tasks completed for your Worker ID! :hibiscus:\n### No more tasks for your Worker ID at this time.\n### More HITs will be released Friday 3 PM PST and Saturday 10 AM PST.''')