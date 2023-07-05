{{ config(
    materialized='external', 
    location='../../data/processed/prod_item_weighted_avg_by_year.parquet'
    ) 
}}
select * from {{ ref('prod_item_weighted_avg_by_year') }}