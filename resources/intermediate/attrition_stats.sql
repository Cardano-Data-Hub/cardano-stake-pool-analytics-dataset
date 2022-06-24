CREATE VIEW analytics.attrition_stats AS
WITH cte_attrition_stats AS (
select pr.retiring_epoch as epoch_no,
EXTRACT(YEAR FROM e.start_time)::bigint as epoch_year,
EXTRACT(MONTH FROM e.start_time)::bigint as epoch_month,
date_trunc('month',e.start_time)::date as epoch_year_month,
count(*) as retired
from pool_retire pr
left join pool_offline_data pod
on pr.hash_id = pod.pool_id
join epoch e on e.no = pr.retiring_epoch 
group by 1,2,3,4
order by 1 desc
)
SELECT * FROM cte_attrition_stats
;

