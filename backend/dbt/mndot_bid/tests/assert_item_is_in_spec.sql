select * 
from {{ ref('int_spec_year_matrix') }}
where 
    in_spec_2016 = false and
    in_spec_2018 = false and
    in_spec_2020 = false