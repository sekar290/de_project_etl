# Data Engineering

1. Clone This Repo.
2. Run `make docker-build` for x86 user, or `make docker-build-arm` for arm chip user.

---
```
## docker-build			- Build Docker Images (amd64) including its inter-container network.
## docker-build-arm		- Build Docker Images (arm64) including its inter-container network.
## postgres			- Run a Postgres container
## spark			- Run a Spark cluster, rebuild the postgres container, then create the destination tables
## jupyter			- Spinup jupyter notebook for testing and validation purposes.
## airflow			- Spinup airflow scheduler and webserver.
## clean			- Cleanup all running containers related to the challenge.
```

---

Here are some glimpse of the result from visualization :

1. Total transaction by Country

![transaction_by_country](/images/transaction_by_country.png)

Description : from matrix above, the highest quantity that have sold come from United Kingdom wtih total sales 4263829

2. Here is a matrix that show total amount by date

![sub_total_by_date](/images/sub_total_by_date.png)
