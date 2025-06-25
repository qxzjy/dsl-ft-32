-- ===============================
-- dbt/models/marts/fct_user_workout_performance.sql
-- ===============================
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

user_workout_summary as (
    select
        w.user_id,
        count(*) as total_workouts,
        avg(w.duration) as avg_workout_duration,
        avg(w.caloriesburned) as avg_calories_burned,
        avg(w.rating) as avg_rating,
        avg(e.repcount) as avg_reps,
        avg(e.weight) as avg_weight,
        avg(e.duration) as avg_exercise_duration
    from workouts w
    left join workout_exercises e on w.workoutid = e.workoutid
    group by w.user_id
)

select
    u.user_id,
    p.firstname,
    p.lastname,
    u.username,
    u.email,
    us.total_workouts,
    us.avg_workout_duration,
    us.avg_calories_burned,
    us.avg_rating,
    us.avg_reps,
    us.avg_weight,
    us.avg_exercise_duration
from user_workout_summary us
join users u on us.user_id = u.user_id
left join profiles p on us.user_id = p.user_id
