select * 
from {{ ref('item_matrix') }}
where 
    in_spec_2016 = false and
    in_spec_2018 = false and
    in_spec_2020 = false