-- 3 Товары

-- Популярные категории покупок
WITH t1 AS (
    SELECT
      pr1.commodity_desc,
      SUM(td1.quantity) AS "quant_sum",
      ROUND(CAST(CAST(SUM(td1.sales_value) AS DOUBLE PRECISION) AS DECIMAL), 0) AS "sales_sum"
    FROM transaction_data AS td1
    LEFT JOIN product AS pr1
      ON td1.product_id = pr1.product_id
    WHERE
      td1.quantity > 0
    GROUP BY
      commodity_desc
    ORDER BY
      SUM(sales_value) DESC
    LIMIT 10
  )
SELECT *
FROM t1


-- продажи со скидками и без из топ 10 категорий товаров
WITH t1 AS (
    SELECT
      td1.basket_id,
      pr1.commodity_desc,
      td1.sales_value,
      td1.quantity,
      CASE
        WHEN (
          td1.coupon_match_disc + coupon_disc + retail_disc
        ) <> 0
        THEN 'disc'
        ELSE 'no_disc'
      END AS "discount"
    FROM transaction_data AS td1
    LEFT JOIN product AS pr1
      ON td1.product_id = pr1.product_id
    WHERE
      td1.quantity > 0
  ), top_cat AS (
    SELECT
      commodity_desc,
      SUM(quantity) AS "quant_sum",
      SUM(sales_value) AS "sales_sum"
    FROM t1
    GROUP BY
      commodity_desc
    ORDER BY
      SUM(sales_value) DESC
    LIMIT 10
  )
SELECT
    commodity_desc,
    discount,
    SUM(quantity) AS "quant_sum",
    SUM(sales_value) AS "sales_sum"
FROM t1
WHERE commodity_desc IN (SELECT commodity_desc FROM top_cat)
GROUP BY commodity_desc, discount


-- Частые сочетания категорий в корзине
WITH t1 AS (
    SELECT DISTINCT
      td1.basket_id,
      pr1.commodity_desc AS "name"
    FROM transaction_data AS td1
    LEFT JOIN product AS pr1 ON td1.product_id = pr1.product_id
    WHERE
      quantity > 0
  ), t2 AS (
    SELECT
      t1.name AS name_1,
      t2.name AS name_2,
      COUNT(*) AS pair_count
    FROM t1 AS t1
    INNER JOIN t1 AS t2
      ON t1.basket_id = t2.basket_id AND t1.name < t2.name
    GROUP BY
      t1.name,
      t2.name
  )
SELECT
    name_1,
    name_2,
    pair_count,
    CONCAT(name_1, '+', name_2) AS "pair_name"
FROM t2
ORDER BY pair_count DESC, name_1, name_2
LIMIT 10


-- Распределение категорий покупок по размеру чека
WITH t1 AS (
    SELECT DISTINCT
      td1.basket_id,
      pr1.commodity_desc
    FROM transaction_data AS td1
    LEFT JOIN product AS pr1 ON td1.product_id = pr1.product_id
    WHERE
      quantity > 0
  ), t2 AS (
    SELECT
      commodity_desc,
      COUNT(*) AS cnt
    FROM t1
    GROUP BY
      commodity_desc
    ORDER BY
      cnt DESC
    LIMIT 10
  ), t3 AS (
    SELECT
      basket_id,
      COUNT(DISTINCT pr1.commodity_desc) AS "cnt"
    FROM transaction_data AS td1
    LEFT JOIN product AS pr1
      ON td1.product_id = pr1.product_id
    GROUP BY
      basket_id
  ), t4 AS (
    SELECT
      basket_id,
      CASE
        WHEN cnt < 3
        THEN '1. малый чек'
        WHEN cnt <= 10
        THEN '2. средний чек'
        WHEN cnt > 10
        THEN '3. большой чек'
      END AS "cat_chek"
    FROM t3
  ), final AS (
    SELECT
      t4.cat_chek,
      t1.commodity_desc,
      COUNT(*) / AVG(t2.cnt) AS "cnt_persnt"
    FROM t1
    INNER JOIN t4 ON t4.basket_id = t1.basket_id
    LEFT JOIN t2 ON t2.commodity_desc = t1.commodity_desc
    WHERE
      t1.commodity_desc IN (
        SELECT
          commodity_desc
        FROM t2
      )
    GROUP BY
      t4.cat_chek,
      t1.commodity_desc
  )
SELECT *
FROM final


-- Доли в прибыли самых популярных категорий товаров
WITH t1 AS (
    SELECT
      pr1.commodity_desc,
      td1.sales_value,
      td1.quantity
    FROM transaction_data AS td1
    LEFT JOIN product AS pr1 ON td1.product_id = pr1.product_id
    WHERE
      td1.quantity > 0
  ), t2 AS (
    SELECT
      SUM(sales_value) AS "sum_sales",
      SUM(quantity) AS "sum_quantity"
    FROM t1
  ), top_cat AS (
    SELECT
      commodity_desc,
      SUM(quantity) AS "quant_sum",
      ROUND(CAST(SUM(sales_value) AS DECIMAL), 0) AS "sales_sum"
    FROM t1
    GROUP BY
      commodity_desc
    ORDER BY
      SUM(sales_value) DESC
    LIMIT 10
  )
SELECT
    commodity_desc,
    quant_sum / (
      SELECT
        sum_quantity
      FROM t2
    ) AS "quantity_rate",
    sales_sum / (
      SELECT
        sum_sales
      FROM t2
    ) AS "sales_rate"
FROM top_cat
ORDER BY sales_rate DESC


-- Категории одиночных покупок
WITH t1 AS (
    SELECT DISTINCT
      td1.basket_id,
      pr1.commodity_desc
    FROM transaction_data AS td1
    LEFT JOIN product AS pr1 ON td1.product_id = pr1.product_id
    WHERE
      td1.quantity > 0
  ), t2 AS (
    SELECT
      basket_id
    FROM t1
    GROUP BY
      basket_id
    HAVING
      COUNT(basket_id) = 1
  ), t3 AS (
    SELECT
      t1.commodity_desc,
      COUNT(t1.commodity_desc) AS cnt
    FROM t2
    LEFT JOIN t1 ON t1.basket_id = t2.basket_id
    GROUP BY
      t1.commodity_desc
    ORDER BY
      cnt DESC
  )
SELECT
    commodity_desc,
    cnt,
    cnt / SUM(cnt) OVER () AS "percnt"
FROM t3
LIMIT 10


-- Доли проданных товаров и выручки по размеру корзины
WITH t1 AS (
    SELECT
      td1.basket_id,
      pr1.commodity_desc,
      td1.sales_value,
      td1.quantity
    FROM transaction_data AS td1
    LEFT JOIN product AS pr1
      ON td1.product_id = pr1.product_id
    WHERE
      quantity > 0 AND quantity < 100
  ), t2 AS (
    SELECT
      SUM(sales_value) AS "sum_sales",
      SUM(quantity) AS "sum_quantity"
    FROM t1
  ), t3 AS (
    SELECT
      basket_id,
      SUM(quantity) AS "cnt"
    FROM transaction_data AS td1
    GROUP BY
      basket_id
  ), t4 AS (
    SELECT
      basket_id,
      CASE
        WHEN cnt < 3
        THEN '1. малый чек(<3тов.)'
        WHEN cnt <= 10
        THEN '2. средний чек(3-10тов.)'
        WHEN cnt > 10
        THEN '3. большой чек(>10тов.)'
      END AS "cat_chek"
    FROM t3
  ), final AS (
    SELECT
      t4.cat_chek,
      SUM(sales_value) / (
        SELECT
          sum_sales
        FROM t2
      ) AS "sales_persnt",
      SUM(quantity) / (
        SELECT
          sum_quantity
        FROM t2
      ) AS "quantiny_persnt"
    FROM t1
    INNER JOIN t4
      ON t4.basket_id = t1.basket_id
    GROUP BY
      t4.cat_chek
  )
SELECT *
FROM final