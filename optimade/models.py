from django.db import models
from django.conf import settings
try:
   #from jsonfield import JSONField
   from django.contrib.postgres.fields import JSONField
except Exception:
   from jsonfield import JSONField
   pass

# USER = settings.AUTH_USER_MODEL


class species(models.Model):

    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Optimade(models.Model):
    attributes = JSONField(default=dict)
    nelements = models.IntegerField()
    nsites = models.IntegerField()
    jid = models.CharField(max_length=255)
    source = models.CharField(max_length=255)
    id = models.CharField(max_length=255, primary_key=True)
    type = models.CharField(max_length=255, default="structures")
    chemical_formula_reduced = models.CharField(max_length=255)
    chemical_formula_anonymous = models.CharField(max_length=255)
    elements = models.CharField(max_length=255)
    # search = models.CharField(max_length=255)
    crys = models.CharField(max_length=255)
    ehull = models.FloatField(null=True)
    spg_number = models.IntegerField()
    formation_energy_peratom = models.FloatField()
    optb88vdw_total_energy = models.FloatField()
    optb88vdw_bandgap = models.FloatField()
    mbj_bandgap = models.FloatField()
    hse_gap = models.FloatField()
    magmom_oszicar = models.FloatField()
    spillage = models.FloatField()
    slme = models.FloatField()
    encut = models.FloatField()
    kpoint_length_unit = models.IntegerField()
    icsd = models.CharField(max_length=255)
    exfoliation_energy = models.IntegerField()
    bulk_modulus_kv = models.FloatField()
    shear_modulus_gv = models.FloatField()

    def __str__(self):
        return f"{self.attributes}"
