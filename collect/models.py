from django.db import models


# Create your models here.

class TitTesouro(models.Model):
    Nome = models.CharField(max_length=30)
    # Dia = models.DateField()
    # TxCompra = models.FloatField()
    # TxVenda = models.FloatField()
    # PUCompra = models.FloatField()
    # PUVenda = models.FloatField()
    # PUBase = models.FloatField()
    # LastUp = models.DateTimeField(auto_now=True)
