{{ config(
    materialized='external', 
    location='../../data/processed/prod_item_search.parquet'
    ) 
}}
select * from {{ ref('prod_item_search') }}