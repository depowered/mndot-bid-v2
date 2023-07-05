{{ config(materialized='table') }}

with source as (

    select * from {{ source('dbt_source', 'clean_items') }}

),

staged as (

    select 
        {{ dbt_utils.generate_surrogate_key([
            'spec_code', 
            'unit_code', 
            'item_code', 
            'long_description', 
            'unit_name'
        ]) }} as id,
        spec_code,
        unit_code,
        item_code,
        spec_code || '.' || unit_code || '/' || item_code as item_number,
        short_description,
        long_description,
        unit_name,
        plan_unit_description,
        spec_year

    from source

)

select * from staged