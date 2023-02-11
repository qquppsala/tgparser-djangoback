from django.db import models

# Create your models here.

class Yandex_Market(models.Model):
    message_id = models.AutoField(primary_key=True, verbose_name="id_Новости")
    message = models.CharField(max_length=5000, verbose_name="Новость")
    date = models.DateField(verbose_name="Дата")
    views = models.CharField(max_length=1024, verbose_name="Просмотры")
    forwards = models.CharField(max_length=1024, verbose_name="Репостов")
    path_to_photo = models.CharField(max_length=1024, verbose_name="Путь к фото")
    

    class Meta:
        managed = False
        db_table = 'Yandex_Market'


class Ozon(models.Model):
    message_id = models.AutoField(primary_key=True, verbose_name="id_Новости")
    message = models.CharField(max_length=5000, verbose_name="Новость")
    date = models.DateField(verbose_name="Дата")
    views = models.CharField(max_length=1024, verbose_name="Просмотры")
    forwards = models.CharField(max_length=1024, verbose_name="Репостов")
    path_to_photo = models.CharField(max_length=1024, verbose_name="Путь к фото")
    
    class Meta:
        managed = False
        db_table = 'OZON'

