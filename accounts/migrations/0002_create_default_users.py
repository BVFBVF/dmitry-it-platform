from django.db import migrations
from django.contrib.auth.hashers import make_password


def create_default_users(apps, schema_editor):
    User = apps.get_model('accounts', 'User')
    users = [
        {
            'username': 'admin',
            'email': 'admin@example.com',
            'role': 'admin',
            'is_staff': True,
            'is_superuser': True,
        },
        {
            'username': 'mentor',
            'email': 'mentor@example.com',
            'role': 'mentor',
        },
        {
            'username': 'viewer',
            'email': 'viewer@example.com',
            'role': 'viewer',
        },
    ]
    for data in users:
        if not User.objects.filter(username=data['username']).exists():
            # Добавляем хешированный пароль
            data['password'] = make_password('password123')
            User.objects.create(**data)


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_users, migrations.RunPython.noop),
    ]