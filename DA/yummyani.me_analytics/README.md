# Аналитика сайта для просмотра аниме

## Описание проекта

### Задача:
Сбор и анализ данных об аниме с целью создания рекомендательной модели

### Данные:
Данные собраны с [сайта онлайн-кинотеатра аниме](https://ru.yummyani.me) и сложены в PostgreS

Обзор платформы

<!-- ![1](imgs/PowerBI_1.png)

Временные зависимости 
![1](imgs/PowerBI_2.png)

Распределения по жанрам, первоисточнику, времени года выхода аниме и возрастным ограничениям
![1](imgs/PowerBI_5.png)

Структура аниме по числу эпизодов
![1](imgs/PowerBI_6.png) -->


<p align="center">
  <img src="imgs/PowerBI_1.png" width="49%">
  <img src="imgs/PowerBI_2.png" width="49%">
</p>

<p align="center">
  <img src="imgs/PowerBI_5.png" width="49%">
  <img src="imgs/PowerBI_6.png" width="49%">
</p>

<!-- Обзор платформы
![1](imgs/PowerBI_1.png) -->

<!-- Обзор платформы
![1](imgs/PowerBI_1.png) -->

[тут](data_analys.ipynb) юпитер с EDA, feature engineering и обучением модели (knn)

В качестве доп. фичей используются эмбеддинги комментариев и описания аниме, их небольшой разбор можно глянуть в колабе 

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1XPWsaJ-D7x35QCUZmroId-yCG6q_oeZy?usp=drive_link)


Моделька рекомендаций обернута в [FastAPI-сервис](app/app.py), добавлен endpoint для предсказаний, сервис завернут в [Docker-контейнер](app/Dockerfile).  

Модель загружается при старте приложения, запросы отправляются через HTTP запрос с содержанием в JSON-формате
