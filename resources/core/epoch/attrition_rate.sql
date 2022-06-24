with cte_epoch_attrition AS (
select 
epoch_no,
retired as retired_this_epoch,
lag(retired) over (order by epoch_no) as retired_previous_epoch,
retired - lag(retired) over (order by epoch_no) as delta,
round((retired - lag(retired) over (order by epoch_no))*100/(lag(retired) over (order by epoch_no))::numeric,2) as epoch_attrition_rate
from analytics.attrition_stats
order by 1 desc
)

select * from cte_epoch_attrition
