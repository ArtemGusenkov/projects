-- 2 Покупатели 

-- Количество уникальных пользователей
SELECT 
    COUNT(DISTINCT household_key)
FROM transaction_data


-- Количество новых покупателей по дням
WITH t1 AS (
    SELECT
      household_key,
      MIN(day) AS "s_day"
    FROM transaction_data
    GROUP BY household_key
  )
SELECT
    t1.s_day AS "usel_start",
    COUNT(t1.s_day) AS "cnt_lfs"
FROM t1
GROUP BY t1.s_day


-- Количество визитов клиентов за все время
SELECT
    household_key,
    COUNT(DISTINCT basket_id)
FROM transaction_data
GROUP BY household_key


-- количество покупок в неделю
WITH t1 AS (
    SELECT
      week_no,
      household_key,
      basket_id
    FROM transaction_data
    GROUP BY week_no, household_key, basket_id
  )
SELECT
    week_no,
    COUNT(household_key)
FROM t1
GROUP BY week_no


-- частота визитов клиентов
WITH t1 AS (
    SELECT
      household_key,
      week_no,
      COUNT(DISTINCT basket_id) AS "visits_per_week"
    FROM transaction_data
    GROUP BY
      week_no,
      household_key
  )
SELECT
    week_no,
    AVG(visits_per_week) AS "freq_of visits"
FROM t1
GROUP BY week_no


-- распредление покупателей по сумме покупок
WITH t1 AS (
    SELECT
      household_key,
      SUM(sales_value) AS "sum_sales"
    FROM transaction_data
    GROUP BY
      household_key
  )
SELECT *
FROM t1


-- распределение всех пользователей по давности посещений
WITH t1 AS (
    SELECT DISTINCT
      household_key,
      day
    FROM transaction_data
    WHERE
      quantity > 0 AND sales_value >= 0
  ), t2 AS (
    SELECT
      household_key,
      day,
      day - LAG(day) OVER (PARTITION BY household_key ORDER BY day) AS "days_btwn_sales"
    FROM t1
  )
SELECT
    household_key,
    COUNT(*) AS "sales_days_count",
    ROUND(CAST(AVG(days_btwn_sales) AS DECIMAL), 2) AS "avg_days_btwn_sales"
FROM t2
GROUP BY household_key


-- распределение 90% пользователей по давности посещений
WITH t1 AS (
    SELECT DISTINCT
      household_key,
      day
    FROM transaction_data
    WHERE
      quantity > 0 AND sales_value >= 0
  ), t2 AS (
    SELECT
      household_key,
      day,
      day - LAG(day) OVER (PARTITION BY household_key ORDER BY day) AS "days_btwn_sales"
    FROM t1
  )
SELECT
    household_key,
    COUNT(*) AS "sales_days_count",
    ROUND(CAST(AVG(days_btwn_sales) AS DECIMAL), 2) AS "avg_days_btwn_sales"
FROM t2
GROUP BY household_key
HAVING AVG(days_btwn_sales) < 30


-- Вклад клиентских групп в общую выручку
WITH t1 AS (
    SELECT
      household_key,
      SUM(sales_value) AS "sales_per_user"
    FROM public.transaction_data
    GROUP BY
      household_key
  ), t2 AS (
    SELECT
      household_key,
      sales_per_user,
      NTILE(3) OVER (ORDER BY sales_per_user, household_key) AS "cat_grp"
    FROM t1
  ), t3 AS (
    SELECT
      household_key,
      sales_per_user,
      CASE cat_grp
        WHEN 1
        THEN 'Низкие траты (<1300$)'
        WHEN 2
        THEN 'Средние траты (1300-3300$)'
        WHEN 3
        THEN 'Высокие траты (>3300$)'
      END AS "cat_group"
    FROM t2
    ORDER BY
      sales_per_user,
      household_key
  )
SELECT
    cat_group,
    MIN(sales_per_user),
    MAX(sales_per_user),
    SUM(sales_per_user) AS "group_sales_sum",
    SUM(sales_per_user) / (SELECT SUM(sales_per_user) FROM t3) AS "group_sales_shr"
FROM t3
GROUP BY cat_group


-- Вклад клиентских групп по давности посещения в общую выручку
WITH t1 AS (
    SELECT DISTINCT
      household_key,
      day
    FROM transaction_data
    WHERE
      quantity > 0 AND sales_value >= 0
  ), t2 AS (
    SELECT
      household_key,
      day,
      day - LAG(day) OVER (PARTITION BY household_key ORDER BY day) AS "days_btwn_sales"
    FROM t1
  ), t3 AS (
    SELECT
      household_key,
      COUNT(*) AS "sales_days_count",
      ROUND(CAST(AVG(days_btwn_sales) AS DECIMAL), 2) AS "avg_days_btwn_sales"
    FROM t2
    GROUP BY
      household_key
  ), t4 AS (
    SELECT
      household_key,
      CASE
        WHEN avg_days_btwn_sales < 4
        THEN '1. менее 4 дней'
        WHEN avg_days_btwn_sales < 7
        THEN '2. 4-6 дней'
        WHEN avg_days_btwn_sales < 30
        THEN '3. 7-30 дней'
        ELSE '4. больше 30 дней'
      END AS "cat_days"
    FROM t3
  ), users_sums AS (
    SELECT
      household_key,
      SUM(sales_value) AS "sums"
    FROM transaction_data
    GROUP BY
      household_key
  ), sum_vals AS (
    SELECT
      COUNT(DISTINCT household_key) AS "all_users_count",
      SUM(sales_value) AS "all_sales_value"
    FROM transaction_data
  )
SELECT
    cat_days,
    SUM(us.sums) AS "sum_sales_per_group",
    SUM(us.sums) / AVG(sv.all_sales_value) AS "perc_sum_sales_per_group",
    COUNT(us.sums) AS "count_sales_per_group",
    COUNT(us.sums) / AVG(sv.all_users_count) AS "perc_count_sales_per_group"
FROM t4
LEFT JOIN users_sums AS us ON us.household_key = t4.household_key
CROSS JOIN sum_vals AS sv
GROUP BY cat_days


-- распределение возрастных групп по категориям трат
WITH t1 AS (
    SELECT
      td.household_key,
      SUM(td.sales_value) AS "sales_per_user"
    FROM transaction_data AS td
    GROUP BY
      td.household_key
  ), t2 AS (
    SELECT
      household_key,
      CASE
        WHEN sales_per_user < 1300
        THEN '1.Низкие траты (<1300$)'
        WHEN sales_per_user >= 1300 AND sales_per_user < 3350
        THEN '2.Средние траты (1300-3300$)'
        ELSE '3.Высокие траты (>3300$)'
      END AS "cat_sales"
    FROM t1
  )
SELECT
    SUM(td.sales_value) AS "sum_cat",
    hd.classification_1,
    t2.cat_sales
FROM transaction_data AS td
LEFT JOIN t2 ON t2.household_key = td.household_key
LEFT JOIN hh_demographic AS hd ON t2.household_key = hd.household_key
GROUP BY t2.cat_sales, hd.classification_1
