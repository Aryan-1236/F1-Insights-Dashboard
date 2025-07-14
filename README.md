F1 Insights Dashboard: Exploring Race Dynamics and Driver Performance

This project showcases an end-to-end data science workflow using Formula 1 data — from raw dataset handling to insightful visualizations, and eventually an interactive dashboard. Ideal for motorsport fans and data enthusiasts!

────────────────────────────

Project Goal

To collect, clean, analyze, and visualize Formula 1 data — uncovering insights about drivers, constructors, and race dynamics. Bonus: Predictive modeling for future races.

────────────────────────────

Key Features

• Exploratory Data Analysis (EDA): Understand patterns in driver performance and constructor success
• Interactive Visualizations: Bar charts, line graphs, heatmaps, and treemaps with Plotly
• Dashboard (coming soon): Streamlit-powered interface to explore F1 data interactively
• Optional ML Component: Predict race outcomes based on past results and team strength

────────────────────────────

Tech Stack

| Category        | Tools Used                                |
| --------------- | ----------------------------------------- |
| Language        | Python                                    |
| Data Collection | Initially via Ergast API, fallback to CSV |
| Analysis        | pandas, numpy                             |
| Visualization   | matplotlib, seaborn, plotly               |
| Dashboard       | Streamlit (to be built)                   |
| ML (Optional)   | scikit-learn                              |
| Hosting         | GitHub, Streamlit Cloud                   |

────────────────────────────

Project Structure

f1-insights-dashboard/
├── data/
│ ├── raw/ → Original Kaggle datasets
│ └── processed/ → Cleaned data (optional)
├── notebooks/
│ └── formula1_insights_dashboard.ipynb
├── app/
│ └── dashboard.py → Streamlit dashboard (upcoming)
├── utils/
│ └── api_fetcher.py → API code (not used, fallback to CSV)
├── models/
│ └── win_predictor.py → ML prediction model (optional)
├── README.md
├── requirements.txt
└── .gitignore

────────────────────────────

Completed: Exploratory Data Analysis

The EDA notebook (notebooks/formula1_insights_dashboard.ipynb) includes:
• Top 10 drivers by career points
• Seasonal performance comparison
• Team and constructor dominance
• Win trends over time
• Driver nationality and team representation
• Combined visual dashboard (multi-panel)

Status: EDA complete and committed to GitHub.

────────────────────────────

Next Steps

[ ] Build Streamlit dashboard (app/dashboard.py)
[ ] Add custom metrics: Aggression Score, Consistency Index
[ ] (Optional) Develop ML model for race predictions
[ ] Deploy dashboard on Streamlit Cloud

────────────────────────────

Dataset

Source: Kaggle Formula 1 Dataset
Link: [https://www.kaggle.com/datasets/](https://www.kaggle.com/datasets/)
Note: Originally intended to use Ergast API, but due to access issues, switched to static Kaggle data.

────────────────────────────

Author

Name: Aryan Mohanty
Email: [aryanmohanty96@gmail.com](mailto:aryanmohanty96@gmail.com)
GitHub: [https://github.com/Aryan-1236/](https://github.com/Aryan-1236/)

────────────────────────────

If you like this project...

Consider giving it a star on GitHub to show support!
