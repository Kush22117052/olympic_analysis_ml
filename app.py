import streamlit as st
import pandas as pd
from matplotlib.pyplot import autoscale

import preprocessor, helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from helper import fetch_medal_tally, medal_tally, country_year_list
import plotly.figure_factory as ff

# Load datasets
df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df, region_df)

st.sidebar.title("Olympics Analysis")
st.sidebar.image('https://th.bing.com/th/id/R.3b1e44147d6272f41f0be9a7e60e0835?rik=IJlpZ9Fl9j99dg&riu=http%3a%2f%2fclipart-library.com%2fnew_gallery%2f171-1711358_olympic-symbol-png-winter-olympics-logo.png&ehk=UbjSXoHUtC9NuVIKfkNXiorRcGRHQzJZ0OKC6BqbhkU%3d&risl=&pid=ImgRaw&r=0')
user_menu = st.sidebar.radio(
    'Select an Option', ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete-wise Analysis')
)

# Medal Tally Section
if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years, country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)

    st.title(f"{selected_country} Medal Tally in {selected_year} Olympics" if selected_year != 'Overall'
             else f"{selected_country} Overall Tally" if selected_country != 'Overall'
             else "Overall Tally")

    st.table(medal_tally)

# Overall Analysis Section
if user_menu == 'Overall Analysis':
    editions = df['Year'].nunique() - 1
    cities = df['City'].nunique()
    sports = df['Sport'].nunique()
    events = df['Event'].nunique()
    athletes = df['Name'].nunique()
    nations = df['region'].nunique()

    st.title("Top Statistics")

    # First row of statistics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    # Second row of statistics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    # Participating nations over time
    nations_over_time = helper.data_over_time(df,'region')
    fig = px.line(nations_over_time, x="Edition", y="region", title="Number of Participating Countries Over The Years")
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x="Edition", y="Event",title="Events Over The Years")
    st.plotly_chart(fig)

    athletes_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athletes_over_time, x="Edition", y="Name", title="Athletes Over The Years")
    st.plotly_chart(fig)

    st.title("Number of Events per Sport Over The Years")
    fig,ax=plt.subplots(figsize=(15,10))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax=sns.heatmap(
    x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int),annot=True)

    st.pyplot(fig)

    st.title("Most Successfull Athletes")
    sport_list=df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport=st.selectbox('Select a Sport',sport_list)
    x=helper.most_successful(df,selected_sport)
    st.table(x)

if user_menu=='Country-wise Analysis':
    st.sidebar.title('Country-wise Analysis')
    country_list=df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country=st.sidebar.selectbox('Select a country',country_list)



    country_df = helper.year_wise_medal_tally(df, selected_country)
    fig = px.line(country_df, x='Year', y='Medal')
    st.title(selected_country + " Medal Tally Over The Years")
    st.plotly_chart(fig)



    st.title(selected_country + " Excels in following Sports")
    pt=helper.country_event_heatmap(df,selected_country)
    fig, ax = plt.subplots(figsize=(15, 10))
    ax = sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    st.title("Top 10 Athetes of " + selected_country)
    top10_df=helper.most_successful_countrywise(df,selected_country)
    st.table(top10_df)

if user_menu=='Athlete-wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()
    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'], show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title('Distribution Of Age')
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = [
        'Basketball', 'Judo', 'Football', 'Tug Of War', 'Athletics', 'Swimming', 'Badminton', 'Sailing',
        'Gymnastics', 'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling', 'Water Polo', 'Hockey',
        'Rowing', 'Fencing', 'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing', 'Tennis',
        'Golf', 'Softball', 'Archery', 'Volleyball', 'Synchronised Swimming', 'Table Tennis', 'Baseball',
        'Rhythmic Gymnastics', 'Rugby Sevens', 'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey'
    ]

    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        gold_ages = temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna().tolist()  # Convert to list

        if len(gold_ages) > 0:  # Only add if there is data
            x.append(gold_ages)
            name.append(sport)

    # Create the distribution plot
    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)

    # Update layout
    fig.update_layout(
        autosize=False, width=1000, height=600,
        title_text="Age Distribution of Gold Medalists Across Different Sports"
    )

    # If using Streamlit
    st.title('Distribution Of Age of Gold Medalists')
    st.plotly_chart(fig)

    sport_list = sorted(df['Sport'].dropna().unique().tolist())
    sport_list = ['Overall'] + sport_list

    selected_sport = st.selectbox('Select a Sport', sport_list)

    temp_df = helper.weight_v_height(df, selected_sport)
    clean_df = temp_df.dropna(subset=['Weight', 'Height'])

    fig, ax = plt.subplots(figsize=(10, 6))

    ax = sns.scatterplot(x=clean_df['Weight'],
                         y=clean_df['Height'],
                         hue=clean_df['Medal'],
                         style=clean_df['Sex'],
                         s=100, alpha=0.8)

    plt.xlabel("Weight (kg)", fontsize=12)
    plt.ylabel("Height (cm)", fontsize=12)
    plt.title(f"Weight vs. Height of Athletes in {selected_sport}", fontsize=14)

    st.pyplot(fig)

    st.title("Men vs Women Participation Over The Years")
    final=helper.men_vs_women(df)
    fig = px.line(final, x='Year', y=['Male', 'Female'])
    fig.update_layout(autosize=False,width=1000,height=600)
    st.plotly_chart(fig)