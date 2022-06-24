WITH cte_yearly_attrition AS (
select 
epoch_year,
sum(retired) as retired_this_year,
lag(sum(retired)) over (order by epoch_year) as retired_previous_year,
sum(retired) - lag(sum(retired)) over (order by epoch_year) as delta,
round((sum(retired) - lag(sum(retired)) over (order by epoch_year))*100/(lag(sum(retired)) over (order by epoch_year))::numeric,2) as yearly_attrition_rate
from analytics.attrition_stats
group by 1
order by 1 desc
)
SELECT * FROM cte_yearly_attrition
