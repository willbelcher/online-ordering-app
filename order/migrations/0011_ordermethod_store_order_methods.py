# Generated by Django 4.2.2 on 2023-06-16 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0010_store_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method', models.PositiveSmallIntegerField(choices=[(0, 'Pickup'), (1, 'Delivery')], default=0)),
            ],
        ),
        migrations.AddField(
            model_name='store',
            name='order_methods',
            field=models.ManyToManyField(to='order.ordermethod'),
        ),
    ]
