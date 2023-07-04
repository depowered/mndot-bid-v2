{{ config(materialized='table') }}

with raw_bids as (

    select * from {{ source('dbt_source', 'raw_bids') }}

)

select * from raw_bids