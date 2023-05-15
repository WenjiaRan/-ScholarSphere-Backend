# Generated by Django 4.2 on 2023-05-15 16:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RealInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, verbose_name='名字')),
                ('phone', models.CharField(max_length=12, verbose_name='电话')),
                ('id_num', models.CharField(max_length=19, verbose_name='身份证号')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='real_info',
            field=models.ForeignKey(db_column='real_info', null=True, on_delete=django.db.models.deletion.CASCADE, to='user.realinformation'),
        ),
    ]
