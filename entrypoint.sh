#!/bin/sh
set -e

echo "Criando e aplicando migrações no SQLite..."
python manage.py makemigrations core
python manage.py migrate

echo "Verificando superusuário padrão..."
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@exemplo.com', 'admin123')
    print('Superusuário criado -> Usuário: admin | Senha: admin123')
else:
    print('Superusuário já existe.')
"

echo "Iniciando servidor do Django..."
exec python manage.py runserver 0.0.0.0:8000