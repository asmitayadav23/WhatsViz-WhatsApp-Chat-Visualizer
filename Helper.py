import pandas as pd
from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import emoji

# Creating object or URLExtract
extract = URLExtract()

def fetch_stats(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # fetch the number of messages
    num_messages = df.shape[0]

    # fetch the total number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # fetch number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    # fetch number of links shared

    links = []
    for mssg in df['message']:
        links.extend(extract.find_urls(mssg))

    return num_messages, len(words),num_media_messages, len(links)

# Function for active/ busy users

def most_busy_users(df):
    # Get message counts
    temp = df[df['user'] != 'Group Notification']
    user_counts = temp['user'].value_counts().head(5)

    # Create a DataFrame for percentage calculation
    df2 = round((temp['user'].value_counts() / temp.shape[0]) * 100, 2).reset_index().head(5)

    # Rename columns properly
    df2.columns = ['User', 'Contribution Percent']

    return user_counts, df2

# Inactive Users

def inactive_users(df):
    # Create a DataFrame for percentage calculation
    df3 = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().tail(5)

    # Rename columns properly
    df3.columns = ['User', 'Contribution Percent']

    return df3

# Creating Word Cloud

def create_wordcloud(selected_user, df):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'Group Notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)

        return " ".join(y)

    wc = WordCloud(width = 300, height = 300, min_font_size = 10, background_color = 'white')
    temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep = " "))

    return df_wc

# Most common words

def most_common_words(selected_user, df):

    f = open('stop_hinglish.txt','r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'Group Notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(10))

    return most_common_df

# Emoji Analysis

def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])  # Corrected condition

    # Convert emoji counts to a DataFrame
    emoji_df = pd.DataFrame(Counter(emojis).most_common(), columns=["Emoji", "Count"])  # Fixed column names

    return emoji_df

# Monthly Timeline Analysis

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []

    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

# Daily Timeline Analysis

def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

# Activity Map
def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

# Activity Heat Map

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap