{{ config(materialized='table') }}

with raw_bidders as (

    select * from {{ source('dbt_source', 'raw_bidders') }}

)

select * from raw_bidders