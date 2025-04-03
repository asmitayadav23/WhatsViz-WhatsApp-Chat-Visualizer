import streamlit as st

def faq():
    faq_data = {
        "Q1: Are you handing over my chat to anyone else?":
            "No. Your data stays private and runs locally.",

        "Q2: How does this app analyze my WhatsApp chats?":
            """ The app processes exported chat files,
             extracts insights, and presents visual analytics.""",

        "Q3: Can I analyze media files too?":
            """ Currently, the app focuses on text analysis.
             Media details (like the number of shared images) can be extracted.""",

        "Q4: How can I contribute to the project?":
            """Check out the 
            [GitHub repository](https://github.com/asmitayadav23) for details.""",

        "Q5: I need custom WhatsApp chat analyses or statistics.":
            """Feel free to contact us. Drop a mail at `Query@gmail.com` or message us on X or facebook."""
    }

    for question, answer in faq_data.items():
        with st.expander(question):
            st.write(answer)
