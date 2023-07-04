{{ config(materialized='table') }}

with source as (

    select * from {{ source('dbt_source', 'clean_items') }}

)

select 
    {{ dbt_utils.generate_surrogate_key(
        [
            's.spec_code', 
            's.unit_code', 
            's.item_code', 
            's.long_description', 
            's.unit_name'
        ]) 
    }} as id,
    s.* 
from source s