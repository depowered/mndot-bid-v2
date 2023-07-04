{{ config(materialized='table') }}

with source as (

    select * from {{ source('dbt_source', 'clean_items') }}

)

select * from source