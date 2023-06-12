import streamlit as st
import plotly.express as px
import seaborn as sns
import scipy

import numpy as np
from matplotlib import pyplot as plt
import plotly.figure_factory as ff
from plotly.figure_factory import create_distplot
import preprocessor, helper

summer_olympics = preprocessor.preprocess()

st.sidebar.title('Olympics Analysis')
st.sidebar.image('https://encrypted-tbn0.gstatic.com/'
                 'images?q=tbn:ANd9GcS-Yjnkauyx5IIisCXFcP4CAMyYG41fm5cTgsWqeer6wY5I2M94k7sotloFTVneoGciMvkudlKsMwY&ec=48600113')

user_menu = st.sidebar.radio(
    'Select an option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete wise Analysis')
)


if user_menu == 'Athlete wise Analysis':
    athlete_df = summer_olympics.drop_duplicates(subset=['Name', 'region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()
    l1 = [x1, x2, x3, x4]
    m = ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist']
    #fig = create_distplot(l1, m,
                          #show_hist=False, show_rug=False)
    #st.plotly_chart(fig)

    sports = summer_olympics['Sport'].unique().tolist()

    sports.sort()
    sports.insert(0, 'Overall')
    selected_sport = st.sidebar.selectbox('Select Sport', sports)
    st.title('Medal Distribution in ' + selected_sport +' wrt Height and Weight')
    ath = helper.height_weight(summer_olympics, selected_sport)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.scatterplot(data=ath, x='Weight', y='Height', hue='Medal', style='Sex', s=200)
    st.pyplot(fig)

    st.title('-------------------------------------------------------------')
    st.title('Men vs Women Participation Over Years')
    final = helper.men_vs_women(summer_olympics)
    fig = px.line(final, x='Year', y=['Men', 'Women'])
    st.plotly_chart(fig)


if user_menu == 'Medal Tally':
    st.sidebar.header("Medals Tally")
    years, countries = helper.country_year_list(summer_olympics)
    select_year = st.sidebar.selectbox('Select Year', years)
    selected_country = st.sidebar.selectbox('Select Country', countries)
    medal_tally = helper.fetch_medal_tally(summer_olympics, select_year, selected_country)
    if selected_country == 'Overall' and select_year == 'Overall':
        st.title('Overall Tally')
    elif selected_country == 'Overall' and select_year != 'Overall':
        st.title('Medal Tally in ' +str(select_year) +' Olympics')
    elif selected_country != 'Overall' and select_year != 'Overall':
        st.title('Medal Tally in ' +str(select_year) +' Olympics for ' +selected_country )
    elif selected_country != 'Overall' and select_year == 'Overall':
        st.title('Overall Medal Tally for ' +selected_country )
    st.table(medal_tally)


if user_menu == 'Overall Analysis':
    editions = summer_olympics['Year'].unique().shape[0] - 1
    cities = summer_olympics['City'].unique().shape[0]
    sports = summer_olympics['Sport'].unique().shape[0]
    events = summer_olympics['Event'].unique().shape[0]
    athletes = summer_olympics['Name'].unique().shape[0]
    country_participated = summer_olympics['region'].unique().shape[0]

    st.title("TOP STATISTICS")
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

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Athletes")
        st.title(athletes)
    with col3:
        st.header("Nations")
        st.title(country_participated)

    st.title("-------------------------------------------------------------")
    st.title('Number of Nations Participating')
    nation_per_olympics = helper.participating_nations(summer_olympics)
    fig = px.line(nation_per_olympics, x="Edition", y="Count")
    st.plotly_chart(fig)

    st.title("-------------------------------------------------------------")
    st.title('Number of Events per Olympics')
    events_per_olympics = helper.events_per_olympics(summer_olympics)
    fig = px.line(events_per_olympics, x="Edition", y="Count of Events")
    st.plotly_chart(fig)

    st.title("-------------------------------------------------------------")
    st.title('Number of Athletes per Olympics')
    athletes_per_olympics = helper.athletes_per_olympics(summer_olympics)
    fig = px.line(athletes_per_olympics, x="Edition", y="Count of Athletes")
    st.plotly_chart(fig)

    st.title("-------------------------------------------------------------")
    st.title('Number of Events per Sport')
    fig,ax = plt.subplots(figsize=(20, 20))
    x = summer_olympics.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                annot=True)
    st.pyplot(fig)

    st.title("-------------------------------------------------------------")
    st.title('Top Athletes in History of Olympics')
    won_medal = summer_olympics.dropna(subset=['Medal'])
    top_athletes = won_medal[['Name', 'region', 'Sport']].value_counts().reset_index().\
        rename(columns={'count': 'Total Medals'}).head(10)
    st.table(top_athletes)


if user_menu == 'Country-wise Analysis':

    st.title('Country-wise Analysis')
    countries = np.unique(summer_olympics['region'].dropna().values).tolist()
    countries.sort()
    selected_country = st.selectbox('Select Country', countries)
    country_df = helper.medal_per_country_per_olympics(summer_olympics, selected_country)
    st.title('Medals over the Years ' + selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.plotly_chart(fig)

    st.title("-------------------------------------------------------------")
    pt = helper.sportwise_medals(summer_olympics, selected_country)
    st.title('Medals per Sport for ' + selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt.astype('int'), annot = True)
    st.pyplot(fig)

    st.title("-------------------------------------------------------------")
    y_df = helper.top_athletes_countrywise(summer_olympics, selected_country)
    st.title('Top Athletes for ' + selected_country)
    z_df = y_df[['region', 'Name', 'Sport']].value_counts().reset_index().rename(columns = {'count':'Total Medals'}).head(10)
    st.table(z_df)






