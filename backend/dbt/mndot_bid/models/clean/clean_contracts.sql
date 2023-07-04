{{ config(materialized='table') }}

with source as (

    select * from {{ source('dbt_source', 'clean_contracts') }}

)

select * from source