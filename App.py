# import streamlit as st
# import numpy as np
# import matplotlib.pyplot as plt
# import Helper
# import Preprocessor as pr
# import Helper as hp
# from PIL import Image, ImageFilter
# import FAQ
# from Helper import inactive_users
# import emoji
# import seaborn as sns
#
# # ✅ Set page config (MUST be the first Streamlit command)
#
# st.set_page_config(
#     page_title="WhatsApp Chat Analyzer",
#     page_icon=":zap:",
#     layout="wide",
#     initial_sidebar_state='auto'
# )
#
# # ✅ Open and process image
#
# img = Image.open('images/image.jpg')
#
# # Apply Unsharp Mask filter
#
# filtered_img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
#
# # Save and reload processed image
#
# filtered_img.save('filtered_image.png')
#
# # ✅ CSS for glowing effect on Streamlit's `st.image()` instead of HTML `<img>`
#
# st.markdown(
#     """
#     <style>
#         .glow-container {
#             display: flex;
#             justify-content: center;
#             align-items: center;
#             position: relative;
#             padding: 20px;
#         }
#
#         .stImage img {  /* Targeting Streamlit images */
#             border-radius: 15px;
#             box-shadow: 0px 0px 15px 5px rgb(79, 121, 66); /* Purple Glow */
#         }
#     </style>
#     """,
#     unsafe_allow_html=True
# )
#
# # ✅ Layout for title and logo with a working image and glow
#
# col1, col2 = st.columns([3, 1])  # Adjusted width ratio
# with col1:
#     st.markdown("<h1 style='text-align: left; color: white;'>WhatsViz: WhatsApp Chat Visualizer</h1>",
#                 unsafe_allow_html=True)
# with col2:
#     st.image(filtered_img, width=175)  # ✅ The correct way to display the image
#
# # ✅ Tagline
#
# st.markdown("""
#
#     <h4 style='text-align: left; color: #E9E8E8;'>Transforming Chats into Insights</h4>
#     <p style='text-align: left; color: #E9E8E8;'>Unlock insights from your chats with complete privacy!
#      Everything runs right in your browser—no servers, no data sharing, just pure analysis. 🚀</p>""",
#             unsafe_allow_html=True)
#
# # ✅ "How it Works" Hyperlink
#
# hyperlink = "https://drive.google.com/file/d/1yYTSYunvFWq_qM3Y5LS-SsTeyuJQ7l8m/view?usp=drive_link"
# st.markdown(f"<p style='text-align: center;'><a href='{hyperlink}' target='_blank' style='color: #4CAF50; font-weight: bold;'>How it Works?</a></p>", unsafe_allow_html=True)
#
# # ✅ FAQ Button
#
# if st.button("📌 FAQ"):
#     st.session_state.show_faq = True  # Toggle FAQ visibility
#
# if st.session_state.get("show_faq", False):  # If FAQ is toggled, show FAQ section
#     st.markdown("<h2 style='text-align: center;'>Frequently Asked Questions (FAQ)</h2>", unsafe_allow_html=True)
#
#     # Import and render FAQ section
#
#     import FAQ
#
#     FAQ.faq()
#
#     # ✅ Collapse All Button (Hides FAQ)
#
#     if st.button("Collapse All FAQs"):
#         st.session_state.show_faq = False  # Hide FAQ section
#
#
# # ✅ File Uploader
#
# st.markdown("### Upload your WhatsApp Chat")
# uploaded_file = st.file_uploader("Choose your file", type=['txt'])
#
# if uploaded_file is not None:
#     bytes_data = uploaded_file.getvalue()
#     data = bytes_data.decode("utf-8")
#
#     # ✅ Preprocess data
#
#     df = pr.Preprocess(data)
#     #st.dataframe(df)  # Display dataframe
#
#     # ✅ Extracting unique users
#
#     user_list = df['user'].unique().tolist()
#     user_list.remove('Group Notification')
#     user_list.sort()
#     user_list.insert(0, "Overall")
#
#     selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)
#
#     if st.button("Show Analysis"):
#
#         # Stats area
#
#         num_mssgs, words, num_media_messages, num_links = hp.fetch_stats(selected_user, df)
#         st.title("Top Statistics")
#         col1, col2, col3, col4 = st.columns(4)
#
#         # ✅ Display results
#
#         with col1:
#             st.write("## Total Messages")
#             st.write(f"### {num_mssgs}")
#
#         with col2:
#             st.write("## Total Words")
#             st.write(f"### {words}")
#
#         with col3:
#             st.write("## Media Shared")
#             st.write(f"### {num_media_messages}")
#
#         with col4:
#             st.write("## Links Shared")
#             st.write(f"### {num_links}")
#
#         # Monthly Timeline Analysis
#
#         st.title('Monthly Timeline')
#         timeline = Helper.monthly_timeline(selected_user, df)
#         fig, ax = plt.subplots()
#         ax.plot(timeline['time'], timeline['message'], color = 'Black')
#         plt.xticks(rotation = 'vertical')
#         st.pyplot(fig)
#
#         # Daily timeline analysis
#
#         st.title('Daily Timeline')
#         daily_timeline = Helper.daily_timeline(selected_user, df)
#         fig, ax = plt.subplots()
#         ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
#         plt.xticks(rotation='vertical')
#         st.pyplot(fig)
#
#         # Activity Map
#
#         st.title("Activity Map")
#         col1, col2 = st.columns(2)
#
#         with col1:
#             st.header('Most Busy Day')
#             busy_day = Helper.week_activity_map(selected_user,df)
#             fig,ax = plt.subplots()
#             ax.bar(busy_day.index, busy_day.values, color= '#191970')
#             plt.xticks(rotation='vertical')
#             st.pyplot(fig)
#
#         with col2:
#             st.header('Most Busy Month')
#             busy_month = Helper.month_activity_map(selected_user, df)
#             fig, ax = plt.subplots()
#             ax.bar(busy_month.index, busy_month.values, color='black')
#             plt.xticks(rotation = 'vertical')
#             st.pyplot(fig)
#
#         st.header("Online Activity Map")
#         user_heatmap = Helper.activity_heatmap(selected_user, df)
#         fig,ax = plt.subplots()
#         ax = sns.heatmap(user_heatmap)
#         st.pyplot(fig)
#
#         # Finding the most active user in the group.
#         # Group Level Analysis
#
#         if selected_user == 'Overall':
#             st.title("Most Active User")
#             x, new_df = Helper.most_busy_users(df)
#
#             fig, ax = plt.subplots()
#             col1, col2 = st.columns(2)
#
#             with col1:
#                 ax.bar(x.index, x.values, color='#191970')
#                 plt.xticks(rotation='vertical')
#                 st.pyplot(fig)
#
#             with col2:
#                 st.markdown("### Top 5 Active Users")
#                 new_df = new_df.rename(columns={"user": "User", "percent": "Contribution (%)"})
#                 st.table(new_df)
#
#             # Display Inactive Users as a Table
#
#             new_df2 = Helper.inactive_users(df)
#             st.markdown("### Top 5 Inactive Users")
#             new_df2 = new_df2.rename(columns={"user": "User", "percent": "Contribution (%)"})
#             st.table(new_df2)
#
#         # WordCLoud creation
#
#         st.title("Chat Wordcloud")
#         df_wc = Helper.create_wordcloud(selected_user, df)
#         fig, ax = plt.subplots()
#         ax.imshow(df_wc)
#         st.pyplot(fig)
#
#
#         # Most common words
#
#         st.title("Most Common Words")
#         most_common_df = Helper.most_common_words(selected_user, df)
#
#         colors = plt.cm.Greys(np.linspace(0.4, 0.8, len(most_common_df[0])))
#         fig,ax = plt.subplots()
#         ax.barh(most_common_df[0],most_common_df[1], color = colors)
#         plt.xticks(rotation = 'vertical')
#         st.pyplot(fig)
#
#         #st.dataframe(most_common_df)
#
#         # Emoji Analysis
#
#         emoji_df = Helper.emoji_helper(selected_user, df)
#         st.title("Emoji Analysis")
#
#         col1, col2 = st.columns(2)
#
#         with col1:
#             st.dataframe(emoji_df)
#         with col2:
#             fig, ax = plt.subplots()
#             ax.set_title("Top 5 Emoji Distribution", fontsize=14, fontweight="bold")
#
#             # Apply .head(5) to both count and labels
#             top_5_counts = emoji_df['Count'].head(5)
#             top_5_labels = [emoji.demojize(e) for e in emoji_df['Emoji'].head(5)]
#
#             ax.pie(top_5_counts, labels=top_5_labels, autopct="%0.2f")
#
#             st.pyplot(fig)
#
#             # st.title("Weekly Activity Map")
#             # user_heatmap = Helper.activity_heatmap(selected_user, df)
#             #
#             # fig, ax = plt.subplots(figsize=(10, 6))
#             # sns.heatmap(user_heatmap, ax=ax, cmap="coolwarm")
#             #
#             # st.pyplot(fig)
# # ✅ Feedback Form using Streamlit native inputs
#
# st.markdown("""
# <h2 style='text-align: center; color: #4CAF50;'>Feedback Form</h2>
# <form action="https://formsubmit.co/yadavasmita2003@gmail.com" method="POST" style="max-width: 600px; margin: auto;">
#      <input type="hidden" name="_captcha" value="false">
#      <input type="text" name="name" placeholder="Your name" required style="width: 100%; padding: 10px; margin-bottom: 10px; border-radius: 8px; border: 1px solid #ccc;">
#      <input type="email" name="email" placeholder="Your email" required style="width: 100%; padding: 10px; margin-bottom: 10px; border-radius: 8px; border: 1px solid #ccc;">
#      <textarea name="message" placeholder="Your message here" required style="width: 100%; height:150px; padding: 12px; margin-bottom: 10px; border-radius: 8px; border: 1px solid #ccc;"></textarea>
#      <button type="submit" style="width: 100%; padding: 12px; background-color: #4CAF50; color: white; border-radius: 8px; border: none; cursor: pointer;">Send</button>
# </form>
# """, unsafe_allow_html=True)


import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import Helper as hp
import Preprocessor as pr

# Set Page Configuration
st.set_page_config(
    page_title="WhatsViz - WhatsApp Chat Analyzer",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for Enhanced Styling
st.markdown(
    """
    <style>
        body {
            background-color: #1a1a2e;
            color: #e0e0e0;
            font-family: 'Arial', sans-serif;
        }
        .stButton>button {
            background-color: #6a0dad;
            color: white;
            border-radius: 12px;
            padding: 12px;
            font-size: 18px;
            font-weight: bold;
            transition: 0.3s;
            box-shadow: 0px 4px 10px rgba(106, 13, 173, 0.5);
        }
        .stButton>button:hover {
            background-color: #4b0082;
        }
        .topnav {
            background: linear-gradient(45deg, #6a0dad, #4b0082);
            color: white;
            padding: 15px;
            text-align: center;
            border-radius: 15px;
            box-shadow: 0px 0px 20px rgba(106, 13, 173, 0.7);
            animation: fadeIn 1s ease-in-out;
            position: relative;
        }
        .topnav a {
            color: #ffffff;
            padding: 16px 24px;
            text-decoration: none;
            font-size: 20px;
            font-weight: bold;
            transition: 0.3s;
            position: relative;
        }
        .topnav a:hover, .topnav a.active {
            color: #ffeb3b;
        }
        .topnav a.active::after {
            content: '';
            position: absolute;
            bottom: -6px;
            left: 50%;
            transform: translateX(-50%);
            width: 50%;
            height: 4px;
            background-color: #ffeb3b;
            border-radius: 2px;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Extracting Page Parameter
query_params = st.query_params
page = query_params.get("page", "home")

# Top Navigation with Active Indicator
st.markdown(
    f"""
    <div class="topnav">
        <a href="?page=home" class="{'active' if page == 'home' else ''}">🏠 Home</a>
        <a href="?page=analysis" class="{'active' if page == 'analysis' else ''}">📊 Chat Analysis</a>
        <a href="?page=predictions" class="{'active' if page == 'predictions' else ''}">🔮 Predictions</a>
        <a href="?page=about" class="{'active' if page == 'about' else ''}">📜 About</a>
    </div>
    """,
    unsafe_allow_html=True
)

# Home Page
if page == "home":
    st.markdown("""
        <div style="text-align: center; padding: 50px;">
            <h1 style="font-size: 3rem; color: #6a0dad;">📊 WhatsViz - WhatsApp Chat Analyzer</h1>
            <h3 style="color: #ff9800;">Transforming Your Chats into Data Insights 🔍</h3>
            <p style="font-size: 1.2rem; line-height: 1.6;">Upload your chat file and get detailed analytics on user activity, trends, and even predictions!</p>
            <strong style="color: #e91e63; font-size: 1.2rem;">✨ Privacy First: Your data stays with you. No servers, no sharing!</strong>
        </div>
    """, unsafe_allow_html=True)

# Chat Analysis Page
elif page == "analysis":
    st.title("📈 Chat Analysis")
    uploaded_file = st.file_uploader("Upload WhatsApp Chat (.txt)", type=['txt'])

    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        data = bytes_data.decode("utf-8")
        df = pr.Preprocess(data)

        user_list = df['user'].unique().tolist()
        user_list = [user for user in user_list if user != 'Group Notification']
        user_list.sort()
        user_list.insert(0, "Overall")
        selected_user = st.selectbox("Analyze chats for", user_list)

        if st.button("Show Analysis"):
            num_mssgs, words, num_media, num_links = hp.fetch_stats(selected_user, df)
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Messages", num_mssgs)
            col2.metric("Total Words", words)
            col3.metric("Media Shared", num_media)
            col4.metric("Links Shared", num_links)

            st.subheader("📅 Monthly Timeline")
            timeline = hp.monthly_timeline(selected_user, df)
            fig, ax = plt.subplots()
            ax.plot(timeline['time'], timeline['message'], color='#6a0dad')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

            st.subheader("🔥 Word Cloud")
            df_wc = hp.create_wordcloud(selected_user, df)
            st.image(df_wc.to_array())

            st.title("Activity Map")


            st.subheader("😀 Emoji Analysis")
            emoji_df = hp.emoji_analysis(df)
            st.dataframe(emoji_df)

# Predictions Page
elif page == "predictions":
    st.title("🔮 Future Chat Trends")
    st.write("Coming Soon: AI-powered insights on future chat activity!")

# About Page
elif page == "about":
    st.title("📜 About WhatsViz")
    st.write(
        "Developed to transform WhatsApp chat data into meaningful insights. A fun and secure way to explore your conversations!")

# Footer
st.markdown("---")
st.markdown("© 2025 WhatsViz | All Rights Reserved")

