{{ config(materialized='table') }}

with source as (

    select * from {{ source('dbt_source', 'clean_bids') }}

),

staged as (

    select 
        contract_id,
        bidder_name,
        {{ dbt_utils.generate_surrogate_key([
            'spec_code', 
            'unit_code', 
            'item_code', 
            'item_long_description', 
            'unit_name'
        ]) }} as item_id,
        spec_code,
        unit_code,
        item_code,
        item_long_description,
        quantity,
        unit_name,
        unit_price_cents

    from source

)

select * from staged