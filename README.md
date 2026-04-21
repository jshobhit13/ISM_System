\# ISM System — Industrial Sensor Monitor



A dashboard I built to monitor industrial sensors in real time. It tracks temperature, pressure, and flow rate, flags anomalies, and shows live charts. Backend is Flask + MySQL, frontend is plain JS with Chart.js.



\---



\## Screenshots



\### Database Setup

!\[DB Setup](screenshots/db\_setup.png)



\### Live Dashboard

!\[Dashboard](screenshots/dashboard\_charts.png)



\### Live Readings

!\[Live Readings](screenshots/live\_readings.png)



\### Alert Triggered

!\[Alert](screenshots/alert\_row.png)



\---



\## What it does



\- Polls sensor data every 4 seconds and updates the dashboard live

\- Flags readings that go outside safe thresholds (alerts show in red)

\- Rolling charts for each sensor type (last 30 readings)

\- A simulator script to generate fake sensor data for testing



\---



\## Stack



\- Python / Flask

\- MySQL

\- Chart.js

\- IBM Plex Mono (because monospace fits a monitoring terminal)



\---



\## Getting it running



You'll need Python 3.9+, MySQL 8+, and that's about it.



```bash

git clone https://github.com/jshobhit13/ISM\_System.git

cd ISM\_System

python -m venv venv

source venv/bin/activate  # Windows: venv\\Scripts\\activate

pip install -r requirements.txt

```



Set up the database:



```bash

mysql -u root -p < setup.sql

```



Create a `.env` file from the example and fill in your DB credentials:



```bash

cp .env.example .env

```



Start the server:



```bash

python app.py

```



Open a second terminal and run the simulator to start pushing fake sensor data:



```bash

python simulator.py

```



Then open `http://127.0.0.1:5000`.



\---



\## API



| Method | Endpoint | What it does |

|--------|----------|--------------|

| POST | `/api/data` | Push a sensor reading |

| GET | `/api/readings` | Fetch latest readings (supports `?limit=` and `?type=`) |

| GET | `/api/alerts` | Fetch readings that triggered alerts |

| GET | `/api/summary` | Avg, min, max, alert count per sensor (last hour) |



\---



\## Thresholds



Defined in `config.py`. A reading outside these ranges gets flagged as an alert:



| Sensor | Min | Max |

|--------|-----|-----|

| Temperature | 10 °C | 80 °C |

| Pressure | 1.0 bar | 10.0 bar |

| Flow Rate | 5 L/min | 50 L/min |

