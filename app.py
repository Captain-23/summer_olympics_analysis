import streamlit as st
import pandas as pd
import preprocessor, helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

st.set_page_config(page_title="Olympics Data Analysis", layout="wide")
st.markdown("<h1 style='text-align:center; color:#0077b6;'>🏆 Olympics Data Analysis Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<hr style='border:1px solid #0077b6;'>", unsafe_allow_html=True)

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')
df = preprocessor.preprocess(df, region_df)

# SIDEBAR

st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/5/5c/Olympic_rings_without_rims.svg", use_column_width=True)
st.sidebar.title("🏅 Menu")
user_menu = st.sidebar.radio(
    "Select an Option",
    ('Medal Tally', 'Overall Analysis', 'Country Wise Analysis', 'Athlete Wise Analysis')
)
st.sidebar.markdown("---")

# MEDAL TALLY

if user_menu == 'Medal Tally':
    st.sidebar.header("🎖️ Medal Tally Filters")
    years, country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)
    medal_tally_df = helper.fetch_medal_tally(df, selected_year, selected_country)

    st.markdown(f"<h2 style='color:#023e8a;'>🏅 Medal Tally</h2>", unsafe_allow_html=True)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.subheader("Overall Tally")
    elif selected_year != 'Overall' and selected_country == 'Overall':
        st.subheader(f"Medal Tally in {selected_year} Olympics")
    elif selected_year == 'Overall' and selected_country != 'Overall':
        st.subheader(f"{selected_country} Overall Performance")
    else:
        st.subheader(f"{selected_country} Performance in {selected_year}")

    st.table(medal_tally_df)

# OVERALL ANALYSIS

if user_menu == 'Overall Analysis':
    st.markdown("<h2 style='color:#023e8a;'>📊 Overall Olympic Statistics</h2>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    editions = df['Year'].nunique() - 1
    cities = df['City'].nunique() - 1
    sports = df['Sport'].nunique()
    events = df['Event'].nunique()
    athletes = df['Name'].nunique()
    nations = df['region'].nunique()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Editions", editions)
    with col2:
        st.metric("Hosts", cities)
    with col3:
        st.metric("Sports", sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Events", events)
    with col2:
        st.metric("Nations", nations)
    with col3:
        st.metric("Athletes", athletes)

    st.markdown("---")
    st.markdown("### 📈 Participation Trends")
    nations_over_time = helper.data_over_time(df, 'region')
    fig = px.line(nations_over_time, x='Year', y='count', title="Participating Nations Over The Years")
    st.plotly_chart(fig, use_container_width=True)

    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x='Year', y='count', title="Events Over The Years")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 🧩 Events by Sport Over Time")
    fig, ax = plt.subplots(figsize=(18, 12))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'), annot=True, cmap="Blues")
    st.pyplot(fig)

    st.markdown("### 🥇 Most Successful Athletes")
    sport_list = sorted(df['Sport'].unique().tolist())
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    x = helper.most_successful(df, selected_sport)
    st.table(x)


# COUNTRY WISE ANALYSIS

if user_menu == 'Country Wise Analysis':
    st.markdown("<h2 style='color:#023e8a;'>🌎 Country Wise Performance</h2>", unsafe_allow_html=True)

    country_list = sorted(df['region'].dropna().unique().tolist())
    selected_country = st.sidebar.selectbox("Select Country", country_list)

    country_df = helper.yearwise_medal_tally(df, selected_country)
    fig = px.line(country_df, x="Year", y='Medal', markers=True, title=f"{selected_country} Medal Tally Over The Years")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"### 🏋️‍♀️ {selected_country} excels in the following sports")
    pt = helper.country_event_heatmap(df, selected_country)
    pt = pt.apply(pd.to_numeric, errors='coerce').fillna(0)
    fig, ax = plt.subplots(figsize=(18, 12))
    sns.heatmap(pt, annot=True, cmap="Greens")
    st.pyplot(fig)

    st.markdown(f"### 🥇 Top 10 Athletes of {selected_country}")
    top10_df = helper.most_successful_countrywise(df, selected_country)
    st.table(top10_df)

#  ATHLETE WISE ANALYSIS

if user_menu == "Athlete Wise Analysis":
    st.markdown("<h2 style='color:#023e8a;'>🏃 Athlete Wise Analysis</h2>", unsafe_allow_html=True)
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    # AGE DISTRIBUTION
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    valid_data = [arr for arr in [x1, x2, x3, x4] if len(arr.unique()) > 2]
    valid_labels = [
        label for arr, label in zip(
            [x1, x2, x3, x4],
            ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist']
        ) if len(arr.unique()) > 2
    ]

    if valid_data:
        fig = ff.create_distplot(valid_data, valid_labels, show_hist=False, show_rug=False)
        fig.update_layout(autosize=False, width=1000, height=600)
        st.subheader("Distribution Of Age")
        st.plotly_chart(fig)
    else:
        st.info("Not enough data to display age distribution.")

    # AGE BY SPORT
    x, name = [], []
    famous_sports = sorted(df['Sport'].unique().tolist())

    for sport in famous_sports:
        sport_df = athlete_df[athlete_df['Sport'] == sport]
        gold_ages = sport_df[sport_df['Medal'] == 'Gold']['Age'].dropna()
        if len(gold_ages.unique()) > 2:
            x.append(gold_ages)
            name.append(sport)

    if x:
        fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
        fig.update_layout(autosize=False, width=1000, height=600)
        st.subheader("Distribution Of Age w.r.t Sports (Gold Medalists)")
        st.plotly_chart(fig)
    else:
        st.info("Not enough valid data for Gold Medalists by sport.")

    # HEIGHT VS WEIGHT
    st.subheader("Height vs Weight Analysis")
    sport_list = sorted(df['Sport'].unique().tolist())
    selected_sport = st.selectbox("Select a Sport", sport_list)

    hw_df = helper.weight_vs_height(df, selected_sport)
    if not hw_df.empty:
        fig, ax = plt.subplots()
        sns.scatterplot(data=hw_df, x="Weight", y="Height", hue="Medal", style="Sex", s=100, ax=ax)
        st.pyplot(fig)
    else:
        st.info("No height and weight data available for this sport.")

    # MEN VS WOMEN
    st.subheader("Men vs Women Participation Over The Years")
    men_vs_women = helper.men_vs_women(df)
    fig = px.line(men_vs_women, x='Year', y=['Male', 'Female'], markers=True)
    st.plotly_chart(fig)

    # COUNTRY PARTICIPATION
    st.subheader("Top Countries by Athlete Participation")
    top_countries = df['region'].value_counts().reset_index().head(10)
    top_countries.columns = ['Country', 'Athletes']
    fig = px.bar(top_countries, x='Country', y='Athletes', text='Athletes', color='Country')
    st.plotly_chart(fig)

    # MOST DECORATED
    st.subheader("Most Decorated Athletes (Overall)")
    top_athletes = df.dropna(subset=['Medal'])['Name'].value_counts().reset_index().head(15)
    top_athletes.columns = ['Athlete', 'Medals Won']
    fig = px.bar(top_athletes, x='Athlete', y='Medals Won', text='Medals Won', color='Medals Won')
    st.plotly_chart(fig)
