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



-- количество проданных товаров по категориям магазинов
WITH t1 AS (
    SELECT
      td.store_id,
      SUM(td.quantity) AS "sum_quantt",
      SUM(td.sales_value) AS "sum_sales",
      CASE
        WHEN (ROW_NUMBER() OVER (ORDER BY SUM(td.sales_value) DESC)) <= 10 THEN 'top 10'
        WHEN (ROW_NUMBER() OVER (ORDER BY SUM(td.sales_value) DESC)) <= 100 THEN 'top 100'
        WHEN (ROW_NUMBER() OVER (ORDER BY SUM(td.sales_value) DESC)) > 100 THEN 'after top 100'
      END AS "store_rank"
    FROM transaction_data AS td
    GROUP BY
      td.store_id
    ORDER BY
      sum_sales DESC
  )
WITH t2 AS (
    SELECT
      td.week_no,
      SUM(td.quantity) AS "sum_quantt",
      SUM(td.sales_value) AS "sum_sales",
      t1.store_rank
    FROM transaction_data AS td
    LEFT JOIN t1
      ON t1.store_id = td.store_id
    GROUP BY
      td.week_no,
      t1.store_rank
    ORDER BY
      sum_sales DESC
  )
SELECT
    week_no,
    store_rank,
    AVG(sum_quantt) OVER (PARTITION BY store_rank ORDER BY week_no ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING) AS "sum_quantt",
    AVG(sum_sales) OVER (PARTITION BY store_rank ORDER BY week_no ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING) AS "sum_sales"
FROM t2

-- продажи по категориям магазинов
WITH t1 AS (
    SELECT
      week_no,
      COUNT(product_id) AS "n_uniq_prod",
      SUM(quantity) AS "sum_quantt",
      SUM(sales_value) AS "sum_sales"
    FROM transaction_data AS td
    GROUP BY week_no, basket_id
  ), t2 AS (
    SELECT
      week_no,
      AVG(n_uniq_prod) AS "avg_n_per_buskt",
      AVG(sum_quantt) AS "avg_quant_per_buskt",
      AVG(sum_sales) AS "avg_sales_per_buskt"
    FROM t1
    GROUP BY week_no
  )
  SELECT
    week_no,
    ROUND(CAST(AVG(avg_n_per_buskt) OVER (ORDER BY week_no ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING) AS DECIMAL), 3) AS "avg_n_per_buskt",
    ROUND(CAST(AVG(avg_quant_per_buskt) OVER (ORDER BY week_no ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING) AS DECIMAL), 3) AS "avg_quant_per_buskt",
    ROUND(CAST(AVG(avg_sales_per_buskt) OVER (ORDER BY week_no ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING) AS DECIMAL), 3) AS "avg_sales_per_buskt"
  FROM t2


-- количество продуктов в корзине
WITH t1 AS (
    SELECT
      week_no,
      COUNT(product_id) AS "n_uniq_prod",
      SUM(quantity) AS "sum_quantt",
      SUM(sales_value) AS "sum_sales"
    FROM transaction_data AS td
    GROUP BY week_no, basket_id
  ), t2 AS (
    SELECT
      week_no,
      AVG(n_uniq_prod) AS "avg_n_per_buskt",
      AVG(sum_quantt) AS "avg_quant_per_buskt",
      AVG(sum_sales) AS "avg_sales_per_buskt"
    FROM t1
    GROUP BY week_no
  )
SELECT
    week_no,
    ROUND(CAST(AVG(avg_n_per_buskt) OVER (ORDER BY week_no ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING) AS DECIMAL), 3) AS "avg_n_per_buskt",
    ROUND(CAST(AVG(avg_quant_per_buskt) OVER (ORDER BY week_no ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING) AS DECIMAL), 3) AS "avg_quant_per_buskt",
    ROUND(CAST(AVG(avg_sales_per_buskt) OVER (ORDER BY week_no ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING) AS DECIMAL), 3) AS "avg_sales_per_buskt"
FROM t2

-- Динамика среднего чека по неделям
WITH t1 AS (
    SELECT
      week_no,
      basket_id,
      SUM(quantity) AS "quantity",
      SUM(sales_value) AS "sales_value"
    FROM transaction_data
    GROUP BY
      week_no,
      basket_id
  )
SELECT
    week_no,
    AVG(quantity) AS "avg_count",
    AVG(sales_value) AS "avg_sales",
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY sales_value) AS "median_sales",
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY quantity) AS "median_count"
FROM t1
GROUP BY week_no