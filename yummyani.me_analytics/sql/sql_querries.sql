-- Общая статистика
SELECT 
	COUNT(DISTINCT anime_id) AS "общее количество аниме",
	SUM(views) AS "сумма всех простмотров",
	SUM(comments_count) AS "количество всех комментариев"
FROM anime_main


-- Общая статистика
SELECT COUNT(DISTINCT genre_id) AS "общее количество жанров"
FROM genres


-- Общая статистикаs
SELECT COUNT(DISTINCT studio_id) AS "общее количество жанров"
FROM studios


-- Топ-20 аниме по рейтингу
SELECT m.anime_id, m.title, m.year, m.type_ru, m.views, r.y_rating_avg
FROM anime_main AS m
	LEFT JOIN ratings AS r ON r.anime_id = m.anime_id
ORDER BY r.y_rating_avg DESC
LIMIT 20


