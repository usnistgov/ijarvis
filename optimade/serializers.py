from rest_framework import serializers

# pip install djangorestframework-queryfields
from .models import Optimade
from drf_queryfields import QueryFieldsMixin

# from .models import Mat,JARVIS_DFT,Atomss

# class SpecieSerializer(serializers.ModelSerializer):
#    authors = serializers.PrimaryKeyRelatedField(queryset=Specie.objects.all(), many=True)

#    class Meta:
#        model = Specie
#        fields = ( 'name')


class Optimade_Serializer(QueryFieldsMixin, serializers.ModelSerializer):
    attributes = serializers.JSONField()
    nelements = serializers.IntegerField()
    nsites = serializers.IntegerField()
    jid = serializers.CharField()
    id = serializers.CharField()
    type = serializers.CharField()
    chemical_formula_reduced = serializers.CharField()
    chemical_formula_anonymous = serializers.CharField()
    # elements = SpecieSerializers
    elements = serializers.CharField()
    source = serializers.CharField()
    # search = serializers.CharField()
    crys = serializers.CharField()
    ehull = serializers.FloatField()
    spg_number = serializers.IntegerField()
    formation_energy_peratom = serializers.FloatField()
    optb88vdw_total_energy = serializers.FloatField()
    optb88vdw_bandgap = serializers.FloatField()
    mbj_bandgap = serializers.FloatField()
    hse_gap = serializers.FloatField()
    magmom_oszicar = serializers.FloatField()
    spillage = serializers.FloatField()
    slme = serializers.FloatField()
    encut = serializers.FloatField()
    slme = serializers.FloatField()
    kpoint_length_unit = serializers.IntegerField()
    icsd = serializers.CharField()
    exfoliation_energy = serializers.FloatField()
    bulk_modulus_kv = serializers.FloatField()
    shear_modulus_gv = serializers.FloatField()
    # full_name = serializers.CharField(read_only=True, source="full_name")
    # return {self.jid,self.chemical_formula_reduced,self.nelements, self.elements, self.lattice_vectors, self.cartesian_site_positions}
    class Meta:
        model = Optimade
        fields = (
            "id",
            "type",
            "jid",
            "attributes",
            "nelements",
            "source",
            "nsites",
            "chemical_formula_reduced",
            "chemical_formula_anonymous",
            "elements",
            # "search",
            "crys",
            "ehull",
            "spg_number",
            "formation_energy_peratom",
            "optb88vdw_total_energy",
            "optb88vdw_bandgap",
            "mbj_bandgap",
            "hse_gap",
            "magmom_oszicar",
            "spillage",
            "slme",
            "encut",
            "kpoint_length_unit",
            "icsd",
            "exfoliation_energy",
            "bulk_modulus_kv",
            "shear_modulus_gv",
        )
