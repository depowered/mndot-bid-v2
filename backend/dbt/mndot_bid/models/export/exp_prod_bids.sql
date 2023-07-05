{{ config(
    materialized='external', 
    location='../../data/processed/prod_bids.parquet'
    ) 
}}
select * from {{ ref('prod_bids') }}