import numpy as np
import plotly.express as px
from pandas import pivot_table


def medal_tally(summer_olympics):

    medal_tally = summer_olympics.drop_duplicates(
        subset=['Team', 'NOC', 'Games', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal'])

    medal_tally = medal_tally.groupby('region')[['Gold', 'Silver', 'Bronze']].\
        sum().sort_values('Gold', ascending=False).reset_index()

    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    medal_tally['Gold'] = medal_tally['Gold'].astype('int')
    medal_tally['Silver'] = medal_tally['Silver'].astype('int')
    medal_tally['Bronze'] = medal_tally['Bronze'].astype('int')
    medal_tally['Total'] = medal_tally['Total'].astype('int')
    return medal_tally


def country_year_list(summer_olympics):
    years = summer_olympics['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    countries = np.unique(summer_olympics['region'].dropna().values).tolist()
    countries.sort()
    countries.insert(0, 'Overall')

    return years, countries


def fetch_medal_tally(summer_olympics, year, country):
    flag = 0
    medal_df = summer_olympics.drop_duplicates(subset = ['Team', 'NOC', 'Games', 'Year', 'Season', 'City', 'Sport', 'Event','Medal'])
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['region'] == country) & (medal_df['Year'] == int(year))]
    if flag == 1:
        x = temp_df.groupby('Year')[['Gold', 'Silver', 'Bronze']].sum().sort_values('Year', ascending = True).reset_index()
    else:
        x = temp_df.groupby('region')[['Gold', 'Silver', 'Bronze']].sum().sort_values('Gold', ascending = False).reset_index()
    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']

    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['Total'] = x['Total'].astype('int')
    return x

def participating_nations(summer_olympics):
    nation = summer_olympics.drop_duplicates(['Year', 'region'])
    nation_per_olympics = nation.groupby('Year')['region'].count().reset_index().rename(
        columns={'region': 'Count', 'Year': 'Edition'})
    return nation_per_olympics

def events_per_olympics(summer_olympics):
    events = summer_olympics.drop_duplicates(['Year', 'Event'])
    events_per_olympics = events.groupby('Year')['Event'].count().reset_index().rename(
        columns={'Event': 'Count of Events', 'Year': 'Edition'})
    return events_per_olympics

def athletes_per_olympics(summer_olympics):
    athletes = summer_olympics.drop_duplicates(['Year', 'Name'])
    athletes_per_olympics = athletes.groupby('Year')['Name'].count().reset_index().rename(
        columns={'Name': 'Count of Athletes', 'Year': 'Edition'})
    return athletes_per_olympics


def medal_per_country_per_olympics(summer_olympics, country):
    temp_df = summer_olympics.dropna(subset='Medal')
    temp_df.drop_duplicates(subset=['NOC', 'Team', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)


    new_df = temp_df[temp_df['region'] == country].reset_index()
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df

def sportwise_medals(summer_olympics, country):
    temp_df = summer_olympics.dropna(subset='Medal')
    temp_df.drop_duplicates(subset=['NOC', 'Team', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country].reset_index()
    pt = pivot_table(data = new_df, index = 'Sport', columns = 'Year', values = 'Medal', aggfunc = 'count').fillna(0)
    return pt

def top_athletes_countrywise(summer_olympics, country):
    won_medal = summer_olympics.dropna(subset=['Medal'])
    x_df = won_medal.drop_duplicates()
    y_df = x_df[x_df['region'] == country]
    return y_df


def height_weight(summer_olympics, sport):
    athlete_df = summer_olympics.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        ath = athlete_df[athlete_df['Sport'] == sport]
        return ath
    else:
        return athlete_df

def men_vs_women(summer_olympics):
    athlete_df = summer_olympics.drop_duplicates(subset=['Name', 'region'])
    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    final = men.merge(women, on='Year')
    final.rename(columns={'Name_x': 'Men', 'Name_y': 'Women'}, inplace=True)
    final.fillna(0, inplace=True)
    return final
