-- base views need to be created before this can be run

select distinct
    v_epoch_stats.*,
    pool_update.margin,
    round(pool_update.pledge / 1000000, 2) as pledge_ada,
    round(pool_update.fixed_cost / 1000000, 2) as fixed_cost_ada,
    v_epoch_stats.total_staking_address - v_epoch_stats.previous_staking_address as delta_delegations,
    round(
        (
            (
                v_epoch_stats.total_staking_address - v_epoch_stats.previous_staking_address
            )::numeric * 100 / NULLIF(v_epoch_stats.previous_staking_address, 0)
        ),
        2
    ) as percent_change_staking_addr,
    v_epoch_stats.ada_staked - v_epoch_stats.previous_ada_staked as delta_ada_stake,
    round(
        (
            (
                v_epoch_stats.ada_staked - v_epoch_stats.previous_ada_staked
            ) * 100 / nullif(v_epoch_stats.previous_ada_staked, 0)
        ),
        2
    ) as percent_change_ada_staked,
    round(analytics.v_rewards_aggregates.amount / 1000000, 2) as rewards
from analytics.mat_v_epoch_stats as v_epoch_stats
left join pool_update on
    pool_update.hash_id = v_epoch_stats.pool_id
    and pool_update.active_epoch_no = v_epoch_stats.epoch_no
left join analytics.v_rewards_aggregates
    on
        analytics.v_rewards_aggregates.earned_epoch = v_epoch_stats.epoch_no
        and analytics.v_rewards_aggregates.pool_id = v_epoch_stats.pool_id
--where analytics.v_epoch_stats.pool_id = 31
order by v_epoch_stats.epoch_no
