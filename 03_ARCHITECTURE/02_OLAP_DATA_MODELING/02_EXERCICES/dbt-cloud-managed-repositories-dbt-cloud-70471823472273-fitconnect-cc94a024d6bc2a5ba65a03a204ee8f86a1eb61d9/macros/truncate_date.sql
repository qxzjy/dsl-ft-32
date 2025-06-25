{% macro truncate_date(field, grain) %}
  case
    when '{{ grain }}' = 'day' then date_trunc('day', {{ field }})
    when '{{ grain }}' = 'week' then date_trunc('week', {{ field }})
    when '{{ grain }}' = 'month' then date_trunc('month', {{ field }})
    else date_trunc('month', {{ field }}) -- default
  end
{% endmacro %}
