{{ config(materialized='table') }}

with source as (

    select * from {{ source('dbt_source', 'clean_contracts') }}

),

staged as (

    select
        contract_id,
        letting_date,
        job_description,
        sp_number,
        district,
        county

    from source
)

select * from staged