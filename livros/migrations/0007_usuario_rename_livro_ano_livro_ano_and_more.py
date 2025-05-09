# Generated by Django 5.2 on 2025-04-20 06:38

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('livros', '0006_rename_user_perfil_usuario'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('senha', models.CharField(max_length=50)),
                ('is_logged', models.BooleanField()),
                ('imagem', models.ImageField(default='default.png', upload_to='')),
            ],
        ),
        migrations.RenameField(
            model_name='livro',
            old_name='livro_ano',
            new_name='ano',
        ),
        migrations.RenameField(
            model_name='livro',
            old_name='livro_id',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='livro',
            old_name='livro_titulo',
            new_name='titulo',
        ),
        migrations.DeleteModel(
            name='Perfil',
        ),
    ]
