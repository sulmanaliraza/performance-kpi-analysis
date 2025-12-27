import pandas as pd

# Load KPI data
df = pd.read_csv("../data/performance_data.csv", parse_dates=["date"])

# Calculate baseline statistics
baseline = (
    df.groupby("service_line")
      .agg(
          avg_response=("response_time_min", "mean"),
          std_response=("response_time_min", "std")
      )
      .reset_index()
)

# Merge baseline back to main data
df = df.merge(baseline, on="service_line", how="left")

# Anomaly detection rule:
# Flag if response time > mean + 2 * std deviation
df["is_anomaly"] = df["response_time_min"] > (
    df["avg_response"] + 2 * df["std_response"]
)

# Extract anomalies
anomalies = df[df["is_anomaly"]]

print("\n=== REAL-TIME KPI ANOMALY DETECTION ===")
if anomalies.empty:
    print("No anomalies detected.")
else:
    print(
        anomalies[
            ["date", "service_line", "response_time_min",
             "avg_response", "std_response"]
        ].to_string(index=False)
    )
