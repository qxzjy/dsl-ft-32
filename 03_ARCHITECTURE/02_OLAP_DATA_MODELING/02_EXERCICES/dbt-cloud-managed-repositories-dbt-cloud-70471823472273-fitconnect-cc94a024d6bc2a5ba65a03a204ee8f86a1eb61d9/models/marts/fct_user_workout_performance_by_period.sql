-- Reference staging models
with users as (
    select * from {{ ref('stg_users') }}
),

profiles as (
    select * from {{ ref('stg_profiles') }}
),

workouts as (
    select * from {{ ref('stg_workouts') }}
),

workout_exercises as (
    select *
    from {{ ref('stg_workout_exercises') }}
),

-- Join with dim_date to assign time periods
combined AS (
  SELECT
    w.user_id,
    w.workoutid,
    d.month_start,
    w.duration,
    w.caloriesburned,
    w.rating,
    e.repcount,
    e.weight,
    e.duration as exercise_duration
  FROM workouts w
  LEFT JOIN workout_exercises e ON w.workoutid = e.workoutid
  LEFT JOIN {{ ref('dim_date') }} d ON DATE_TRUNC('day', w.workoutdate) = d.date_day
),

-- Aggregate by user and month
agg AS (
  SELECT
    user_id,
    month_start,
    COUNT(*) AS total_workouts,
    AVG(duration) AS avg_workout_duration,
    AVG(caloriesburned) AS avg_calories_burned,
    AVG(rating) AS avg_rating,
    AVG(repcount) AS avg_reps,
    AVG(weight) AS avg_weight,
    AVG(exercise_duration) AS avg_exercise_duration
  FROM combined
  GROUP BY user_id, month_start
)

-- Final output
select
    u.user_id,
    p.firstname,
    p.lastname,
    u.username,
    u.email,
    us.month_start,
    us.total_workouts,
    us.avg_workout_duration,
    us.avg_calories_burned,
    us.avg_rating,
    us.avg_reps,
    us.avg_weight,
    us.avg_exercise_duration
from agg us
join users u on us.user_id = u.user_id
left join profiles p on us.user_id = p.user_id
