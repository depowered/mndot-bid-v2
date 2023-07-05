{{ config(materialized='table') }}

with source as (

    select * from {{ source('dbt_source', 'clean_bidders') }}

),

staged as (

    select
        contract_id,
        bidder_id,
        bidder_name,
        bid_total_cents

    from source

)

select * from staged