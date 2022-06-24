-- schema analytics need to be created before these can be run

create or replace view analytics.v_recent_pool_updates as
select * from
    (
        select
            pool_offline_data.pool_id,
            pool_offline_data.ticker_name,
            pool_offline_data.json,
            row_number() over(
                partition by
                    pool_offline_data.pool_id
                order by pool_offline_data.id desc
            ) as latest
        from pool_offline_data
    )
where latest = 1;

create or replace view analytics.v_epoch_stats as
(
    select
        pool_id,
        epoch_no,
        count(addr_id) as total_staking_address,
        lag(
            count(addr_id)
        ) over(
            partition by pool_id order by epoch_no
        ) as previous_staking_address,
        round(sum(amount / 1000000), 2) as ada_staked,
        lag(
            round(sum(amount / 1000000), 2)
        ) over(partition by pool_id order by epoch_no) as previous_ada_staked
    from epoch_stake
    --where pool_id in (31, 146, 111)
    group by 1, 2
    order by pool_id, epoch_no
);

create or replace view analytics.v_rewards_aggregates as
(
    select
        pool_id,
        earned_epoch,
        sum(amount/1000000) as amount
    from reward
    group by 1, 2
);

create or replace view analytics.v_recent_pool_metadata as
select * from
    (
        select
            pool_metadata_ref.pool_id,
            pool_metadata_ref.url,
            row_number() over(
                partition by
                    pool_metadata_ref.pool_id
                order by pool_metadata_ref.id desc
            ) as latest
        from pool_metadata_ref
    )
where latest = 1;


create materialized view IF NOT EXISTS analytics.mat_v_epoch_stats as
select
        pool_id,
       epoch_no,
        count(addr_id) as total_staking_address,
        lag(
            count(addr_id)
        ) over(
            partition by pool_id order by epoch_no
        ) as previous_staking_address,
        round(sum(amount / 1000000), 2) as ada_staked,
        lag(
            round(sum(amount / 1000000), 2)
        ) over(partition by pool_id order by epoch_no) as previous_ada_staked
    from epoch_stake
    --where pool_id in (31, 146, 111)
    group by 1, 2
    order by pool_id, epoch_no
;
