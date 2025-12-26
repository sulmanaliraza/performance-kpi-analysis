-- KPI SUMMARY BY SERVICE LINE
-- Purpose: Track performance and contractual/SLA-style compliance

-- 1) Overall KPI summary
SELECT
  service_line,
  COUNT(*) AS days_count,
  SUM(incidents) AS total_incidents,
  ROUND(AVG(response_time_min), 2) AS avg_response_min,
  ROUND(AVG(resolution_time_min), 2) AS avg_resolution_min,
  ROUND(AVG(customer_satisfaction), 2) AS avg_cs
FROM performance_data
GROUP BY service_line
ORDER BY service_line;

-- 2) SLA compliance rate (response + resolution)
SELECT
  service_line,
  ROUND(
    100.0 * SUM(CASE WHEN response_time_min <= sla_target_response_min THEN 1 ELSE 0 END) / COUNT(*),
    2
  ) AS response_sla_compliance_pct,
  ROUND(
    100.0 * SUM(CASE WHEN resolution_time_min <= sla_target_resolution_min THEN 1 ELSE 0 END) / COUNT(*),
    2
  ) AS resolution_sla_compliance_pct
FROM performance_data
GROUP BY service_line;

-- 3) Trend: daily performance
SELECT
  date,
  service_line,
  incidents,
  response_time_min,
  resolution_time_min,
  customer_satisfaction
FROM performance_data
ORDER BY date, service_line;

-- 4) Identify outlier days (simple rule-based)
-- Flag if response time exceeds SLA by more than 20%
SELECT
  date,
  service_line,
  response_time_min,
  sla_target_response_min,
  ROUND(100.0 * response_time_min / sla_target_response_min, 2) AS response_vs_sla_pct
FROM performance_data
WHERE response_time_min > (sla_target_response_min * 1.2)
ORDER BY response_vs_sla_pct DESC;

