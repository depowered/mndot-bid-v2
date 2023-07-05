with bids as (

    select contract_id, bidder_name, item_id, quantity, unit_price_cents
    from {{ ref('stg_bids') }}

),

dates as (

    select contract_id, letting_date
    from {{ ref('stg_contracts') }}

),

lowest_bids as (

    select contract_id, bidder_name, lowest_bid
    from {{ ref('int_lowest_bid') }}

),

joined as (

    select 
        dates.letting_date, 
        lowest_bids.lowest_bid,
        bids.*
    from bids
    left join dates using( contract_id )
    left join lowest_bids using( contract_id, bidder_name )

),

renamed as (

    select
        contract_id,
        letting_date,
        bidder_name,
        item_id,
        quantity,
        unit_price_cents,

        case 
            when bidder_name = 'Engineers' then 'engineers'
            when lowest_bid = true then 'winning'
            else 'losing'
        end as category

        from joined

)

select * from renamed