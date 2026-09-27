# Netflix Data Analysis

A Streamlit dashboard for exploring Netflix viewing and revenue data. It includes nine bar, pie, and line charts, filters, and percentage labels on bar charts.

## Run locally

Install dependencies and launch the dashboard:

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

The app loads `netflix.csv` or `netflix.csv.txt` from the project folder. You can also upload a CSV from the sidebar. Expected fields include `Watch_Date`, `Monthly_Revenue`, `Region`, `Rating`, `Device`, `Subscription_Plan`, `Watch_Count`, `Title`, `Category`, `Watch_Time_Minutes`, and `Payment_Method`.

Dashboard images are stored in `Images/`.
