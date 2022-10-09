
echo '>>> Запускаю сервер...'

python manage.py makemigrations
python manage.py migrate

python manage.py runserver 0.0.0.0:8000
echo '>>> Сервер запущен'


