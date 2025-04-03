import re
import pandas as pd
from streamlit import dataframe  # Though not needed in this function

def Preprocess(data):
    # Splitting of Data on basis of message and date
    # Example of Data for pattern Of RE - 19/09/22, 16:20 - Abhishek Swaroop Sir: <Media omitted>

    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    mssgs = re.split(pattern, data)[1:]  # Messages extracted by splitting on timestamps
    dates = re.findall(pattern, data)  # Extract all date occurrences

    print("Extracted Dates:", dates[:5])  # Debugging step to check extracted dates

    # Converting string into dataframe
    df = pd.DataFrame({'user_date': dates, 'user_mssg': mssgs})

    # Fix: Correct date format in parsing**
    df['user_date'] = df['user_date'].str.strip(' -')  # Remove trailing ' -' if present
    df['user_date'] = pd.to_datetime(df['user_date'], format='%d/%m/%y, %H:%M', errors="coerce")

    print("Parsed Dates:", df['user_date'].head())  # Debugging step to check date parsing

    # Coerce meaning: In case of an invalid date-time format, it will show NaT and will not throw an error
    df.rename(columns={'user_date': 'date'}, inplace=True)

    # Separating user names and user messages
    users = []
    mssgs_cleaned = []  # Using a different variable name to avoid confusion

    for mssg in df['user_mssg']:
        entry = re.split(r'([\w\W]+?):\s', mssg, maxsplit=1)  # Ensure it splits correctly
        if len(entry) > 2:  # User exists (i.e., proper message format)
            users.append(entry[1])  # Extract user name
            mssgs_cleaned.append(entry[2])  # Extract actual message
        else:
            users.append("Group Notification")  # Example: "Sanjay Dureja added ~C M Sharma"
            mssgs_cleaned.append(entry[0])  # The entire text is a notification

    # Assign extracted values to the DataFrame
    df['user'] = users
    df['message'] = mssgs_cleaned

    # Fix: Check for any missing values
    print("Users Extracted:", df['user'].unique())  # Debugging step

    # Extract Date and Time components
    df['only_date'] = df['date'].dt.date
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month_name()
    df["month_num"] = df["date"].dt.month
    df["day"] = df["date"].dt.day
    df["hour"] = df["date"].dt.hour
    df["minute"] = df["date"].dt.minute
    df['day_name'] = df['date'].dt.day_name()
    df['only_date'] = df['date'].dt.date

    period = []
    for hour in df[['day_name','hour']]['hour']:
        if hour == 23:
            period.append(str(hour)+"-"+str('00'))
        elif hour == 0:
            period.append(str('00')+"-"+str(hour+1))
        else:
            period.append(str(hour)+"-"+str(hour+1))

    df['period'] = period

    return df  # Ensure the correct DataFrame is returned
