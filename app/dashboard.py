import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="F1 Insights Dashboard", layout="wide")

# Set project and data directories
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "raw"

# Load all required data
@st.cache_data
def load_data():
    results = pd.read_csv(DATA_DIR / "results.csv")
    constructors = pd.read_csv(DATA_DIR / "constructors.csv")
    drivers = pd.read_csv(DATA_DIR / "drivers.csv")
    races = pd.read_csv(DATA_DIR / "races.csv")
    driver_standings = pd.read_csv(DATA_DIR / "driver_standings.csv")
    return results, constructors, drivers, races, driver_standings

results, constructors, drivers, races, driver_standings = load_data()

# ✅ Single Sidebar for Navigation
st.sidebar.title("📂 Dashboard Navigation")
section = st.sidebar.radio(
    "Choose a section to explore:",
    [
        "🏁 Overview",
        "🏆 Constructor Wins",
        "📈 Career Points & Trends",
        "🌍 Nationalities & Teams",
        "📊 Combined Dashboard",
        "ℹ️ About"
    ]
)

# --------------------------
# 🏁 Overview (Optional placeholder)
if section == "🏁 Overview":
    st.header("🏁 Formula 1 Dataset Overview")

    # Extract basic info
    total_races = races['raceId'].nunique()
    total_drivers = drivers['driverId'].nunique()
    total_teams = constructors['constructorId'].nunique()
    total_seasons = races['year'].nunique()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Races", f"{total_races}")
    col2.metric("Total Drivers", f"{total_drivers}")
    col3.metric("Total Teams", f"{total_teams}")
    col4.metric("Total Seasons", f"{total_seasons}")

    st.markdown("---")

    # Show season distribution
    season_counts = races['year'].value_counts().reset_index()
    season_counts.columns = ['Season', 'Race Count']
    season_counts = season_counts.sort_values('Season')

    fig = px.bar(season_counts, x='Season', y='Race Count',
                 title="📅 Number of Races per Season",
                 template='plotly_dark')
    st.plotly_chart(fig, use_container_width=True)

# --------------------------
# 🏆 Constructor Wins
elif section == "🏆 Constructor Wins":
    st.header("🏆 Top Constructors by Wins")

    # Year selection dropdown
    selected_year = st.selectbox(
        "Select a Year", 
        options=sorted(races['year'].unique()), 
        index=len(races['year'].unique()) - 1
    )

    # Filter results for selected year
    race_ids_for_year = races[races['year'] == selected_year]['raceId']
    year_results = results[results['raceId'].isin(race_ids_for_year)].copy()
    year_results['position'] = pd.to_numeric(year_results['position'], errors='coerce')

    # Compute constructor wins
    wins = year_results[year_results['position'] == 1.0]
    wins = pd.merge(wins, constructors[['constructorId', 'constructorRef']], on='constructorId', how='left')
    constructor_wins = wins.groupby('constructorRef').size().reset_index(name='wins')
    constructor_wins.rename(columns={'constructorRef': 'team'}, inplace=True)

    if constructor_wins.empty:
        st.warning("No constructor wins recorded for the selected year.")
    else:
        fig = px.bar(
            constructor_wins.sort_values(by="wins", ascending=False),
            x="team", y="wins",
            title=f"Top Constructors by Wins in {selected_year}",
            template="plotly_dark",
            color="team"
        )
        st.plotly_chart(fig, use_container_width=True)

# --------------------------
# 📈 Career Points & Seasonal Trends
elif section == "📈 Career Points & Trends":
    st.header("📈 Driver Career Points & Seasonal Performance")

    # --- Clean merge to avoid points_x / points_y issues ---
    ds = driver_standings[['raceId', 'driverId', 'points']].rename(columns={'points': 'driver_points'})
    merged = pd.merge(results, ds, on=['raceId', 'driverId'], how='left')
    merged = pd.merge(merged, drivers[['driverId', 'surname']], on='driverId', how='left')
    merged = pd.merge(merged, races[['raceId', 'year']], on='raceId', how='left')

    merged['driver_points'] = pd.to_numeric(merged['driver_points'], errors='coerce')

    # --- Dynamic Driver Selection ---
    total_points = (
        merged.groupby('surname')['driver_points']
        .sum()
        .reset_index()
        .sort_values(by='driver_points', ascending=False)
    )
    all_driver_names = total_points['surname'].tolist()

    selected_drivers = st.multiselect(
        "Select Drivers to Compare (Default: Top 5)",
        options=all_driver_names,
        default=all_driver_names[:5]
    )

    filtered_data = merged[merged['surname'].isin(selected_drivers)]

    # --- Career Points Bar Chart ---
    career_points = (
        filtered_data.groupby('surname')['driver_points']
        .sum()
        .reset_index()
        .sort_values(by='driver_points', ascending=False)
    )

    fig1 = px.bar(
        career_points,
        x='surname', y='driver_points',
        title='Career Points of Selected Drivers',
        template='plotly_dark',
        color='surname'
    )
    st.plotly_chart(fig1, use_container_width=True)

    # --- Season-wise Trend Line Chart ---
    seasonal_points = (
        filtered_data.groupby(['year', 'surname'])['driver_points']
        .sum()
        .reset_index()
    )

    fig2 = px.line(
        seasonal_points,
        x='year', y='driver_points', color='surname',
        title='Season-wise Points of Selected Drivers',
        markers=True,
        template='plotly_dark'
    )
    st.plotly_chart(fig2, use_container_width=True)

# --------------------------
# 🌍 Nationalities & Teams
elif section == "🌍 Nationalities & Teams":
    st.header("🌍 Nationalities & Teams")

    # Driver nationalities distribution
    nationality_counts = drivers['nationality'].value_counts()

    # Keep top 10 nationalities, group the rest as 'Other'
    top_nationalities = nationality_counts.head(10)
    other_count = nationality_counts.iloc[10:].sum()
    final_nationality_data = top_nationalities.to_frame().reset_index()
    final_nationality_data.columns = ['nationality', 'count']
    final_nationality_data.loc[len(final_nationality_data.index)] = ['Other', other_count]

    # Pie Chart
    fig_nat = px.pie(
        final_nationality_data,
        names='nationality',
        values='count',
        title='Driver Nationalities Distribution (Top 10 + Other)',
        template='plotly_dark',
        hole=0.4
    )
    st.plotly_chart(fig_nat, use_container_width=True)

    st.markdown("---")

    # Constructors per nationality
    constructor_nationality = constructors['nationality'].value_counts().reset_index()
    constructor_nationality.columns = ['nationality', 'count']

    fig_team_nat = px.bar(
        constructor_nationality,
        x='nationality',
        y='count',
        title='Number of Constructors by Nationality',
        template='plotly_dark',
        color='nationality'
    )
    st.plotly_chart(fig_team_nat, use_container_width=True)


# --------------------------
# 📊 Combined Dashboard
elif section == "📊 Combined Dashboard":
    st.header("📊 Combined Insights: Driver Points, Teams & Trends")

    # Merge necessary data
    merged = results.merge(driver_standings[['raceId', 'driverId', 'points']], on=['raceId', 'driverId'], how='left')
    merged = merged.merge(drivers[['driverId', 'surname', 'nationality']], on='driverId', how='left')
    merged = merged.merge(constructors[['constructorId', 'constructorRef']], on='constructorId', how='left')
    merged = merged.merge(races[['raceId', 'year']], on='raceId', how='left')

    # Use correct points column
    merged['points'] = pd.to_numeric(merged['points_y'], errors='coerce')
    merged.drop(['points_x', 'points_y'], axis=1, inplace=True)

    if 'points' not in merged.columns:
        st.warning("⚠️ 'points' column missing after merge.")
        st.write("🔍 Columns in final merged DataFrame:")
        st.write(merged.columns.tolist())
    else:
        # Top Drivers
        top_drivers = (
            merged.groupby('surname')['points']
            .sum()
            .sort_values(ascending=False)
            .head(5)
            .index
            .tolist()
        )
        filtered = merged[merged['surname'].isin(top_drivers)]

        col1, col2 = st.columns(2)

        # 1️⃣ Line Chart – Seasonal Points
        with col1:
            trend = filtered.groupby(['year', 'surname'])['points'].sum().reset_index()
            fig1 = px.line(
                trend,
                x='year', y='points', color='surname',
                title='🏎️ Season-wise Points for Top 5 Drivers',
                markers=True,
                template='plotly_dark'
            )
            st.plotly_chart(fig1, use_container_width=True)

        # 2️⃣ Pie Chart – Team Share
        with col2:
            team_share = filtered.groupby('constructorRef').size().reset_index(name='count')
            fig2 = px.pie(
                team_share,
                names='constructorRef', values='count',
                title='🧑‍🔧 Team Distribution Among Top Drivers',
                template='plotly_dark'
            )
            st.plotly_chart(fig2, use_container_width=True)

        # 3️⃣ Pie Chart – Nationality Share
        nationality_share = filtered.groupby('nationality').size().reset_index(name='count')
        fig3 = px.pie(
            nationality_share,
            names='nationality', values='count',
            title='🌍 Nationality Distribution Among Top Drivers',
            template='plotly_dark'
        )
        st.plotly_chart(fig3, use_container_width=True)

# --------------------------
# ℹ️ About Section
elif section == "ℹ️ About":
    st.header("ℹ️ About this Dashboard")
    
    st.markdown("""
    Welcome to the **F1 Insights Dashboard**! 🏎️  
    This interactive dashboard explores Formula 1 racing data, showcasing:
    - Driver career points and seasonal performance 📈  
    - Top constructors and team performance 🏆  
    - Nationalities of drivers and constructors 🌍  
    - A combined analytical view of key race dynamics 📊

    ---
    ### 📚 Data Source
    - Data collected from the **Kaggle Formula 1 Dataset**
    - Originally sourced from the [Ergast Developer API](https://ergast.com/mrd/)

    ---
    ### 🧰 Tech Stack
    - **Python** with `pandas`, `plotly`, `seaborn`
    - **Streamlit** for building this web app
    - Visualizations with **Plotly Express**
    
    ---
    ### 👨‍💻 Developer
    - **Aryan Mohanty**  
    - GitHub: [Aryan-1236](https://github.com/Aryan-1236)

    ---
    Thank you for exploring! Feel free to ⭐️ the [GitHub repo](https://github.com/Aryan-1236/F1-Insights-Dashboard) if you found this project useful.
    """)