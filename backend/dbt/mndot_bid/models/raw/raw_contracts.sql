{{ config(materialized='table') }}

with raw_contracts as (

    select * from {{ source('dbt_source', 'raw_contracts') }}

)

select * from raw_contracts