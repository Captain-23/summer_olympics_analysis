from flask import Flask, render_template, request
import pandas as pd
import helper, preprocessor
import plotly.express as px

app = Flask(__name__)

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')
df = preprocessor.preprocess(df, region_df)

## Flask Route
@app.route("/")
def home():
    return render_template("index.html")

# MEDAL TALLY
@app.route("/medal-tally")
def medal_tally():
    years, countries = helper.country_year_list(df)

    selected_year= request.args.get("year", "Overall")
    selected_country = request.args.get("country", "Overall")

    medal_df = helper.fetch_medal_tally(df, selected_year, selected_country)

    total_gold = int(medal_df['Gold'].sum())
    total_silver = int(medal_df['Silver'].sum())
    total_bronze = int(medal_df['Bronze'].sum())
    total_medals = int(medal_df['Total'].sum())
    return render_template(
        "medal_tally.html",
        years=years,
        countries=countries,
        selected_year=selected_year,
        selected_country=selected_country,
        medal_df=medal_df.to_html(classes="dataframe", index=False, border=0),
        total_gold=total_gold,
        total_silver=total_silver,
        total_bronze=total_bronze,
        total_medals=total_medals
    )

# OVERALL ANALYSIS

@app.route("/overall")
def overall():
    editions = df['Year'].nunique()
    cities = df['City'].nunique()
    sports = df['Sport'].nunique()
    events = df['Event'].nunique()
    athletes = df['Name'].nunique()
    nations = df['region'].nunique()

    nations_over_time = helper.data_over_time(df, 'region')
    events_over_time = helper.data_over_time(df, 'Event')
    athletes_over_time = helper.data_over_time(df, 'Name')

    fig_nations = px.line(nations_over_time, x='Year', y='count')
    fig_events = px.line(events_over_time, x='Year', y='count')
    fig_athletes = px.line(athletes_over_time, x="Year", y='count')

    return render_template(
        "overall.html",
        editions = editions,
        cities = cities,
        sports = sports,
        events = events,
        athletes = athletes,
        nations = nations,
        nations_over_time = nations_over_time,
        events_over_time = events_over_time,
        athletes_over_time = athletes_over_time,
        fig_nations = fig_nations.to_html(full_html=False),
        fig_events = fig_events.to_html(full_html=False),
        fig_athletes = fig_athletes.to_html(full_html=False)
    )

# COUNTRY WISE ANALYSIS

@app.route("/country")
def country():
    countries = helper.country_year_list(df)[1]
    
    selected_country = request.args.get("country", "India")

    yearwise_df = helper.yearwise_medal_tally(df, selected_country)
    heatmap_df = helper.country_event_heatmap(df, selected_country)
    top10_df = helper.most_successful_countrywise(df, selected_country).to_html(classes='dataframe', index=False, border=0)

    fig_line = px.line(yearwise_df, x="Year", y="Medal") if not yearwise_df.empty else None
    fig_heatmap = px.imshow(heatmap_df) if not heatmap_df.empty else None

    return render_template(
        "country.html",
        countries = countries,
        selected_country = selected_country,
        top10_df = top10_df,
        fig_line = fig_line.to_html(full_html=False) if fig_line else None,
        fig_heatmap = fig_heatmap.to_html(full_html = False) if fig_heatmap else None

    )

# ATHLETE WISE ANALYSIS

@app.route("/athlete")
def athlete():
    sports = sorted(df['Sport'].unique().tolist())
    sports.insert(0, "Overall")

    selected_sport = request.args.get("sport", "Overall")
    
    top_athletes_df = helper.most_successful(df, selected_sport)
    hw_df = helper.weight_vs_height(df, selected_sport)
    gender_df = helper.men_vs_women(df)

    fig_hw = px.scatter(hw_df, x='Weight', y='Height', color='Sex') if not hw_df.empty else None
    fig_gender = px.line(gender_df, x='Year', y=['Male', 'Female'])

    return render_template(
        "athlete.html",
        sports = sports,
        selected_sport = selected_sport,
        top_athletes_df = top_athletes_df.to_html(classes='dataframe', index=False, border=0),
        fig_hw=fig_hw.to_html(full_html = False) if fig_hw else None,
        fig_gender = fig_gender.to_html(full_html = False)
    
    )
if __name__ == "__main__":
    app.run(debug=False)