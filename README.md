#  Платформа для Электронных Дневников
___
## Учебный проект

___
## Используемый Стек

+ python 3.10
+ Django 4.1
+ Celery
+ PostgreSQL
+ Docker
+ Docker-compose
+ Git
___

## Техническое Задание
+ #### Общие возможности Платформы
  + Регистрация Учеников/Учителей на основе пригласительных токенов
  + Возможность добавлять школы
  + Реализовать интеграцию с платежной системой STRIPE , для оплаты услуг платформы
  + Предоставлять доступ персоналу к базе данных своей школы, возможность персоналу генерировать токены
  + Создание расписания
  + Добавление предметов, создание классов
  + Автоматический переход на новый учебный год, обновление классов , четвертей. 

+ #### Возможности учителя
  + Консоль учителя
    + Возможность задавать домашнее задание ученикам
    + Реализовать блок классов отфильтрованных по школе, с возможностью переходить к журналу класса 
  + Возможность по своему предмету смотреть/ставить/изменять/удалять оценки ученикам. Реализовать с помощью api+js. 
    + Получение выше указанного функционала должно быть в удобочитаемом виде, т.е реализованно должно быть через таблицу с расписанием занятий на четверть 
  + Возможность скачать/распечатать оценки

+ #### Ученика
  + Получать оценки по предметам
  + Возможность смотреть оценки за пройденные четверти/полугодия
  + Возможность смотреть заданное задание по датам

___

## Установка

