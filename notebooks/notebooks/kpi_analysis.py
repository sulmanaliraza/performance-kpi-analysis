import pandas as pd

# Load data
df = pd.read_csv("../data/performance_data.csv", parse_dates=["date"])

# KPI summary by service line
summary = (
    df.groupby("service_line")
      .agg(
          days_count=("date", "count"),
          total_incidents=("incidents", "sum"),
          avg_response_min=("response_time_min", "mean"),
          avg_resolution_min=("resolution_time_min", "mean"),
          avg_cs=("customer_satisfaction", "mean")
      )
      .round(2)
      .reset_index()
)

# SLA compliance rates
df["response_sla_met"] = df["response_time_min"] <= df["sla_target_response_min"]
df["resolution_sla_met"] = df["resolution_time_min"] <= df["sla_target_resolution_min"]

sla = (
    df.groupby("service_line")
      .agg(
          response_sla_compliance_pct=("response_sla_met", lambda s: round(100 * s.mean(), 2)),
          resolution_sla_compliance_pct=("resolution_sla_met", lambda s: round(100 * s.mean(), 2)),
      )
      .reset_index()
)

# Outlier detection (simple, explainable rule)
df["response_vs_sla_pct"] = (100 * df["response_time_min"] / df["sla_target_response_min"]).round(2)
outliers = df[df["response_vs_sla_pct"] > 120].sort_values("response_vs_sla_pct", ascending=False)

print("\n=== KPI SUMMARY ===")
print(summary.to_string(index=False))

print("\n=== SLA COMPLIANCE ===")
print(sla.to_string(index=False))

print("\n=== OUTLIER DAYS (Response > 120% of SLA) ===")
if outliers.empty:
    print("No outliers found.")
else:
    print(outliers[["date","service_line","response_time_min","sla_target_response_min","response_vs_sla_pct"]].to_string(index=False))
