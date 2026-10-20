-- 1 Продажи
-- продажи по дням
WITH t1 AS (
SELECT
    day,
    SUM(sales_value)
FROM transaction_data
GROUP BY
    day
ORDER BY
    day ASC
)
SELECT *
FROM t1


-- продажи по неделям
WITH t1 AS (
SELECT
    week_no,
    SUM(sales_value)
FROM transaction_data
GROUP BY
    week_no
ORDER BY
    week_no ASC
)
SELECT *
FROM t1

-- количество клиентов, количество посещений магазинов и суммарное количество проданных товаров по неделям
WITH t1 AS (
SELECT
    week_no,
    COUNT(DISTINCT household_key) AS "user_count",
    COUNT(DISTINCT basket_id) AS "sales_count",
    SUM(quantity) AS "saled_product_sum"
FROM transaction_data
GROUP BY
    week_no
ORDER BY
    week_no ASC
)
SELECT
    week_no,
    user_count * 1.0 / MAX(user_count) OVER () AS "user_count",
    sales_count * 1.0 / MAX(sales_count) OVER () AS "sales_count",
    saled_product_sum * 1.0 / MAX(saled_product_sum) OVER () AS "saled_product_sum"
FROM t1


-- выручка по неделям для разных категорий товаров
WITH t1 AS (
SELECT
    td.week_no,
    SUM(td.quantity) AS "saled_product_sum",
    SUM(td.sales_value) AS "sales_sum",
    prd.department
FROM transaction_data AS td
LEFT JOIN product AS prd
    ON prd.product_id = td.product_id
GROUP BY
    td.week_no,
    prd.department
HAVING
    SUM(td.quantity) > 0 AND SUM(td.sales_value) > 0
ORDER BY
    td.week_no ASC
)
SELECT *
FROM t1
ORDER BY 
    week_no ASC


-- доли категорий продуктов в вырочке
WITH t1 AS (
SELECT
    td.week_no,
    SUM(td.quantity) AS "saled_product_sum",
    SUM(td.sales_value) AS "sales_sum",
    prd.department
FROM transaction_data AS td
LEFT JOIN product AS prd
    ON prd.product_id = td.product_id
GROUP BY
    td.week_no,
    prd.department
HAVING
    SUM(td.quantity) > 0 AND SUM(td.sales_value) > 0
ORDER BY
    td.week_no ASC
)
SELECT
    week_no,
    department,
    sales_sum / SUM(sales_sum) OVER (PARTITION BY week_no) AS "sales_rate",
    saled_product_sum / SUM(saled_product_sum) OVER (PARTITION BY week_no) AS "quantity_rate"
FROM t1
ORDER BY
    week_no ASC