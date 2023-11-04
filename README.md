# Data Engineering

1. Clone This Repo.
2. Run `make docker-build` for x86 user, or `make docker-build-arm` for arm chip user.

---
```
## docker-build			- Build Docker Images (amd64) including its inter-container network.
## docker-build-arm		- Build Docker Images (arm64) including its inter-container network.
## postgres			- Run a Postgres container
## jupyter			- Spinup jupyter notebook for testing and validation purposes.
## airflow			- Spinup airflow scheduler and webserver.
## plotly               - Run a Dash Plotly Container
## clean			- Cleanup all running containers related to the challenge.
```

---

## Source Data
The data used in this project is weather data and air quality data obtained from https://open-meteo.com/. Open-Meteo is an open-source weather API and offers free access for non-commercial use.

## Architecture Overview

![Pipeline](/images/pipeline.png)

1. Get data weather and air-quality from open-meteo daily using airflow as the orchestration
2. Store the data in postgresql
3. Visualize data using dash-plotly

