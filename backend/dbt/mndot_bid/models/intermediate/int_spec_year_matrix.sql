with items as (

    select * from {{ ref('stg_items') }}

),

spec_2016 as (

    select 
        id, 
        true as in_spec_2016 

    from items

    where spec_year = 2016

),

spec_2018 as (

    select 
        id, 
        true as in_spec_2018  

    from items

    where spec_year = 2018

),

spec_2020 as (

    select 
        id, 
        true as in_spec_2020 

    from items

    where spec_year = 2020

),

joined as (

    select 
        items.* exclude(spec_year),
        ifnull(spec_2016.in_spec_2016, false) as in_spec_2016,
        ifnull(spec_2018.in_spec_2018, false) as in_spec_2018,
        ifnull(spec_2020.in_spec_2020, false) as in_spec_2020,

    from items

    left join spec_2016 using ( id )
    left join spec_2018 using ( id )
    left join spec_2020 using ( id )

),

keep_unique as (

    select distinct on(id) *

    from joined

)

select * from keep_unique