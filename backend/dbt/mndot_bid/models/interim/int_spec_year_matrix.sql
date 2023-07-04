with items as (
    select 
        spec_code, 
        unit_code, 
        item_code,
        short_description,
        long_description, 
        unit_name,
        plan_unit_description
    from 
        {{ ref('clean_items') }}
),

spec_2016 as (
    select 
        spec_code, 
        unit_code, 
        item_code, 
        long_description, 
        unit_name,
        true as in_spec_2016 
    from 
        {{ ref('clean_items') }}
    where 
        spec_year = 2016
),

spec_2018 as (
    select 
        spec_code, 
        unit_code, 
        item_code, 
        long_description, 
        unit_name,
        true as in_spec_2018  
    from 
        {{ ref('clean_items') }}
    where 
        spec_year = 2018
),

spec_2020 as (
    select 
        spec_code, 
        unit_code, 
        item_code, 
        long_description, 
        unit_name,
        true as in_spec_2020 
    from 
        {{ ref('clean_items') }}
    where 
        spec_year = 2020
),

joined as (
    select 
        items.*,
        ifnull(spec_2016.in_spec_2016, false) as in_spec_2016,
        ifnull(spec_2018.in_spec_2018, false) as in_spec_2018,
        ifnull(spec_2020.in_spec_2020, false) as in_spec_2020,
    from
        items
    left join 
        spec_2016 
    using (
        spec_code, 
        unit_code, 
        item_code, 
        long_description, 
        unit_name,
    )
    left join
        spec_2018
    using (
        spec_code, 
        unit_code, 
        item_code, 
        long_description, 
        unit_name,
    )
    left join
        spec_2020
    using (
        spec_code, 
        unit_code, 
        item_code, 
        long_description, 
        unit_name,
    )
),

item_matrix as (
    select distinct * from joined
)

select * from item_matrix