{{ config(materialized='table') }}

with raw_items as (

    select * from {{ source('dbt_source', 'raw_items') }}

)

select * from raw_items