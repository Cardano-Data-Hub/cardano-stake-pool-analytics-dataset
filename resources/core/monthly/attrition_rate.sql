WITH cte_monthly_attrition AS (
select 
epoch_year_month,
sum(retired) as retired_this_month,
lag(sum(retired)) over (order by epoch_year_month) as retired_previous_month,
sum(retired) - lag(sum(retired)) over (order by epoch_year_month) as delta,
round((sum(retired) - lag(sum(retired)) over (order by epoch_year_month))*100/(lag(sum(retired)) over (order by epoch_year_month))::numeric,2) as monthly_attrition_rate
from analytics.attrition_stats
group by 1
order by 1 desc
)
SELECT * FROM cte_monthly_attrition
