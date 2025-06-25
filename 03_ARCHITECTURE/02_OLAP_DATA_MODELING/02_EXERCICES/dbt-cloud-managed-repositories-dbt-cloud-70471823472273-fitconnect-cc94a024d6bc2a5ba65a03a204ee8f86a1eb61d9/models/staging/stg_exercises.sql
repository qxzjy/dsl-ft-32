-- ===============================
-- dbt/models/staging/stg_exercises.sql
-- ===============================

select
    exerciseid,
    name,
    description,
    category,
    musclegroup,
    difficultylevel,
    demovideourl
from {{ source('fitconnect', 'exercises') }}
