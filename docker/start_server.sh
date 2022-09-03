echo '>>> Устанавливаю requirements.txt'

python -m pip install -r requirements.txt

echo '>>> Запускаю сервер'

python manage.py runserver 0.0.0.0:8000


