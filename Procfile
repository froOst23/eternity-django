web: python eternity/manage.py makemigrations \
&& python eternity/manage.py migrate \
&& python eternity/manage.py runserver 0.0.0.0:$PORT \
&& echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'pass')" | python manage.py shell