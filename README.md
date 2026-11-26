# LinkPro Analytics

LinkPro Analytics is my 2025 data science engineering internship project. I built a tool for tracking clicks and page views on link profiles and exploring which links, traffic sources, and posting times received the most engagement.

## What I built

| Component | Implementation |
| --- | --- |
| Tracking and storage | FastAPI endpoints record and retrieve click and page-view events. Click tracking requires the link to belong to the supplied profile. SQLAlchemy maps profiles, links, and events to PostgreSQL. Pydantic validates inputs and structures API responses. |
| Analytics and dashboard | The API calculates profile and link metrics, classifies referrers, groups events by hour or day, and compares periods. The HTML, CSS, and JavaScript dashboard uses Chart.js and Tailwind CSS to show seven-day KPIs, traffic sources, daily trends, link performance, and the weekday with the most recorded clicks. It refreshes every 30 seconds. |
| Offline analysis and recommendations | The Jupyter notebook extracts events from PostgreSQL and uses pandas, NumPy, SciPy, Matplotlib, seaborn, and scikit-learn for exploratory analysis, statistical tests, feature engineering, model comparison, and posting-slot recommendations. |

The dashboard calls the FastAPI REST endpoints, which query PostgreSQL. The notebook reads the same schema independently. The dashboard's posting suggestion comes from historical click counts.

## Dashboard

The demo uses synthetic events for one profile. Follow the [local setup guide](docs/SETUP.md) to run the API and dashboard on Windows, macOS, or Linux and load the demo data.

![Dashboard showing synthetic KPIs, traffic sources, daily performance, and two link rows](docs/dashboard.webp)

## Notebook results

The notebook contains saved aggregate plots for engagement by time and traffic source, feature importance, model comparisons, and example recommendation scores. The analysis uses a chronological 80/20 train/test split. In the saved run, the selected Lasso model had a test R² of -0.0001, and the selected logistic regression model had a test ROC AUC of 0.5096. These scores indicate limited predictive signal in that run. The original dataset and exported models are unavailable in this checkout. [View the notebook and plots](recommendation_system/RecommendationSystem.ipynb)

The API is intended for local evaluation. Browser access defaults to the dashboard origins in the setup guide. The API has no authentication, and tracking routes store IP addresses, user agents, and referrers. Use synthetic or otherwise approved data.
