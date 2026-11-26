# Local setup

Use Python 3.12, Git, and a running PostgreSQL server with the `psql` client on your PATH. The dashboard loads Chart.js, Tailwind CSS, Font Awesome, and Poppins from public CDNs, so the browser needs internet access for the charts and full styling.

## Clone and install

```sh
git clone https://github.com/akadmiri/linkpro-analytics.git
cd linkpro-analytics
```

Run commands from the repository root unless indicated otherwise.

**macOS and Linux**

```sh
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r backend/requirements.txt
cp .env.example .env
```

**Windows PowerShell**

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r backend/requirements.txt
Copy-Item .env.example .env
```

On Windows, use `.\.venv\Scripts\python.exe` in place of `python` in the commands below.

## Create a local database

Connect to the `postgres` maintenance database as a PostgreSQL administrator, for example with `psql -h localhost -U postgres -d postgres`. On Linux installations using peer authentication, use `sudo -u postgres psql -d postgres`. On macOS, if your installer used your system account as the PostgreSQL administrator, try `psql -d postgres`.

In `psql`, run the following. The `\password` command prompts twice for a local password.

```sql
CREATE ROLE linkpro_user LOGIN;
\password linkpro_user
CREATE DATABASE linkpro_analytics OWNER linkpro_user;
\q
```

Set `DB_PASS` in the root `.env` to the password you entered. Quote values that contain spaces or comment characters. If your database settings differ, also set `DB_HOST`, `DB_PORT`, `DB_NAME`, and `DB_USER`. Shell environment variables take precedence over the file. See [.env.example](../.env.example).

## Start the API and dashboard

From the root, start the API. SQLAlchemy creates missing tables at startup.

```sh
python -m uvicorn --app-dir backend/src main:app --host 127.0.0.1 --port 8000
```

In a second terminal, serve the dashboard from the repository root. On macOS and Linux, activate the virtual environment again or use `python3.12` for this command.

```sh
python -m http.server 8080 --bind 127.0.0.1 --directory frontend
```

- Check [API health](http://127.0.0.1:8000/health) for `"status": "healthy"`.
- Open the [interactive API documentation](http://127.0.0.1:8000/docs) to try the tracking and analytics endpoints.
- Open the [dashboard](http://127.0.0.1:8080/). If you use a different API URL, update the `analytics-api-url` meta tag in [frontend/index.html](../frontend/index.html).

## Load demo data

After the first API startup, run the following in a third terminal. Enter the database role's password when prompted. Substitute your database settings if you changed them.

```sh
psql -h localhost -p 5432 -U linkpro_user -d linkpro_analytics -v ON_ERROR_STOP=1 -f docs/demo-data.sql
```

The script prints the synthetic profile ID, normally `1` on a fresh database. Select that ID in the dashboard. The script timestamps the events when first loaded and can be run again without duplicating them. The dashboard ships with selector options 1–13. If your profile ID is outside that range, update the options in `frontend/index.html`. Refresh to see the KPIs, traffic chart, daily time series, and two link rows. You can also use Swagger UI to record a click or page view for the seeded profile.

The seed is for dashboard evaluation. The notebook needs a larger dataset with clicks and views across multiple time slots and traffic sources for the statistical tests and model fitting.

## Run the recommendation notebook

Install the optional analysis packages into the same virtual environment.

```sh
python -m pip install -r recommendation_system/requirements.txt
```

Open [RecommendationSystem.ipynb](../recommendation_system/RecommendationSystem.ipynb) in a Jupyter-compatible editor and select the virtual environment's Python kernel. If the editor prompts for the kernel package, install it with `python -m pip install ipykernel`. Use the `recommendation_system/` directory as the notebook working directory. The notebook loads database settings from the environment or the root `.env`.

Point the notebook at a PostgreSQL database populated with approved analytics data that follows the application schema, then run all cells in order. The notebook writes local model and report artifacts into its working directory. Load only artifacts you trust, and keep generated files and datasets out of version control. The notebook is run separately from the dashboard.
