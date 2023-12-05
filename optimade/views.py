from django.db.models import Q
from django_filters import rest_framework as filters
import django_filters
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
import os
from .models import Optimade
from jarvis.db.jsonutils import loadjson
import ast
from jarvis.core.composition import Composition

# from .models import Mat,JARVIS_DFT,Atomss
from jarvis.core.specie import Specie
from .serializers import Optimade_Serializer
from django.http import JsonResponse
from django.http import HttpResponse
import math, json
from django.db.models import F

# from .serializers import MatSerializer,JARVIS_DFT_Serializer,Atomss_Serializer

#Note: for each new filter, add in models.py, views.py, serializers.py, OptimadeFilter etc

# http://127.0.0.1:8000/optimade_new/optim/?nsites_range=1-5&chemical_formula_reduced=CoO2
class OptimadeFilter(filters.FilterSet):
    # nsites_range = django_filters.CharFilter(method="nsites_range_filter")
    nsites = django_filters.CharFilter(method="nsites_filter")
    #nelements = django_filters.CharFilter(method="nelements_filter")
    nelements = django_filters.CharFilter(method="nelements_filter")
    chemical_formula_anonymous = django_filters.CharFilter(
        method="chemical_formula_anonymous_filter"
    )
    chemical_formula_reduced = django_filters.CharFilter(
        method="chemical_formula_reduced_filter"
    )
    id = django_filters.CharFilter(method="id_filter")
    elements = django_filters.CharFilter(method="elements_filter")
    #source = django_filters.CharFilter(method="source_filter")
    def nelements_filter(self, queryset, name, value):
        print("value nelements", value)
        if ">" in value and "=" not in value:
            # print("condition 1")
            array = value.split(">")[1].replace(" ", "")
            minv = Q(nelements__gt=int(array))
            return queryset.filter(minv)
        elif "<" in value and "=" not in value:
            array = value.split("<")[1].replace(" ", "")
            # print("condition 2", array)
            maxv = Q(nelements__lt=int(array))
            return queryset.filter(maxv)
        if ">" in value and "=" in value:
            # print("condition 3")
            array = value.split(">=")[1].replace(" ", "")
            #array = value.split("<")[1].split("=")[1].replace(" ", "")
            minv = Q(nelements__gte=int(array))
            return queryset.filter(minv)
        elif "<" in value and "=" in value:
            # print("condition 4")
            #array = value.split("<")[1].split("=")[1].replace(" ", "")
            array = value.split("<=")[1].replace(" ", "")
            maxv = Q(nelements__lte=int(array))
            print("<= is",array, maxv)
            return queryset.filter(maxv)

        elif "=" in value and "!" not in value:
            # print("condition 5")
            array = (value.split("=")[1]).replace(" ", "")
            print("EQUAL 2", array)
            eq = Q(nelements=int(array))
            return queryset.filter(eq)

        elif "!" in value:
            # print("condition 6", value)
            # print("Found !")
            array = (value.split("!")[1]).replace(" ", "")
            eq = Q(nelements=int(array))
            return queryset.filter(~eq)
        else:
            # print("condition 7")
            return queryset

    def elements_filter(self, queryset, name, value):
        # print("value elements", value, type(value))
        value = json.loads(value.replace("'", '"').replace(" ",""))
        #value = json.loads(value.replace("'", '"'))
        print("value elements", value, type(value))
        isearch = "-" + "-".join(sorted(list(set(value["elements"]))))
        if value["condition"] == "only" or value["condition"] == "all":
            # print(
            #    "condition", "only", value["elements"], type(value["elements"])
            # )  # ,queryset,type(queryset))
            # print("queryset", queryset, type(queryset))
            # eq = Q(ast.literal_eval(elements)==['Se','Se'])
            # eq = Q(elements=str(sorted(list(set(value['elements'])))))
            eq = Q(elements=isearch)
            # print("eq el", eq)
            return queryset.filter(eq)
        elif value["condition"] == "any":
            # print(
            #    "condition", "any", value["elements"], type(value["elements"])
            # )  # ,queryset,type(queryset))
            # print("queryset", queryset, type(queryset))
            # eq = Q(ast.literal_eval(elements)==['Se','Se'])
            # eq = Q(elements=str(sorted(list(set(value['elements'])))))
            eq = Q(elements__contains=isearch)
            # print("eq el", eq)
            return queryset.filter(eq)
        else:
            return queryset



    #def source_filter(self, queryset, name, value):
    #    print("value hereeee source", value)
    #    if "!" not in value:
    #        array = value.replace(" ", "").strip('"').strip("'")
    #        eq = Q(source=array)
    #        print("eq src", eq)
    #        return queryset.filter(eq)
    #    else:
    #        # print("condition 7")
    #        return queryset



    def id_filter(self, queryset, name, value):
        # print("value hereeee", value)
        if "=" in value and "!" not in value:
            array = (value.split("=")[1]).replace(" ", "").strip('"')
            eq = Q(id=int(float(array)))
            # print("eq id", eq)
            return queryset.filter(eq)
        elif ">" in value and "=" not in value:
            # print("condition 1")
            array = value.split(">")[1].replace(" ", "").strip('"')
            minv = Q(id__gt=int(float(array)))
            return queryset.filter(minv)
        elif "<" in value and "=" not in value:
            # print("condition 1")
            array = value.split("<")[1].replace(" ", "").strip('"')
            minv = Q(id__gt=int(float(array)))
            return queryset.filter(minv)

        elif "!" in value:
            # print("condition 6")
            # print("Found !")
            array = value.split("!")[1].replace(" ", "").strip('"')
            eq = Q(id=int(array))
            return queryset.filter(~eq)
        else:
            # print("condition 7")
            return queryset

    def chemical_formula_anonymous_filter(self, queryset, name, value):
        value = value.replace('"', "").replace("'", "")
        print("value hereeee", value)
        if "=" in value and "!" not in value:
            array = (value.split("=")[1]).replace(" ", "")
            eq = Q(chemical_formula_anonymous=array)
            return queryset.filter(eq)
        #elif "=" in value and "!" in value:
        #    array = (value.split("=")[1]).replace(" ", "")
        #    eq = Q(chemical_formula_anonymous=array)
        #    return queryset.filter(~eq)
        elif "=>" in value:
            array = (value.split("=>")[1]).replace(" ", "")
            eq = Q(chemical_formula_anonymous=array)
            return queryset.filter(eq)
        elif "<=" in value:
            array = (value.split("<=")[1]).replace(" ", "")
            eq = Q(chemical_formula_anonymous=array)
            return queryset.filter(eq)
        elif ">" in value and "=" not in value:
            # print("condition 1")
            array = value.split(">")[1].replace(" ", "").strip('"')
            minv = Q(chemical_formula_anonymous__gt=array)
            return queryset.filter(minv)
        elif "<" in value and "=" not in value:
            # print("condition 1")
            array = value.split("<")[1].replace(" ", "").strip('"')
            minv = Q(chemical_formula_anonymous__gt=array)
            return queryset.filter(minv)
        elif "!"  in value:
        #elif "!" not in value:
            array = (value.split("!")[1]).replace(" ", "")
            eq = Q(chemical_formula_anonymous=array)
            return queryset.filter(~eq)
        else:
            # print("condition 7")
            return queryset

    def chemical_formula_reduced_filter(self, queryset, name, value):
        # print("value hereeee", value)
        # value=value.strip("'").strip('"') #replace('"','').replace("'","")
        value = value.replace('"', "").replace("'", "")
        if "=" in value and "!" not in value:
            array = (value.split("=")[1]).replace(" ", "")
            # array=(Composition.from_string(array)).reduced_formula
            # print ('array comp',array)
            eq = Q(chemical_formula_reduced=array)
            return queryset.filter(eq)
        elif "=>" in value and "!" not in value:
            array = (value.split("=>")[1]).replace(" ", "")
            # array=Composition.from_string(array).reduced_formula
            eq = Q(chemical_formula_reduced=array)
            return queryset.filter(eq)
        elif "<=" in value and "!" not in value:
            array = (value.split("<=")[1]).replace(" ", "")
            # array=Composition.from_string(array).reduced_formula
            eq = Q(chemical_formula_reduced=array)
            return queryset.filter(eq)
        elif ">" in value and "=" not in value:
            # print("condition 1")
            array = value.split(">")[1].replace(" ", "").strip('"')
            # array=Composition.from_string(array).reduced_formula
            minv = Q(chemical_formula_reduced__gt=array)
            return queryset.filter(minv)
        elif "<" in value and "=" not in value:
            # print("condition 1")
            array = value.split("<")[1].replace(" ", "").strip('"')
            # array=Composition.from_string(array).reduced_formula
            minv = Q(chemical_formula_reduced__gt=array)
            return queryset.filter(minv)
        elif "!" in value:
            array = (value.split("!")[1]).replace(" ", "")
            # array=Composition.from_string(array).reduced_formula
            eq = Q(chemical_formula_reduced=array)
            return queryset.filter(~eq)
        else:
            # print("condition 7")
            return queryset

    def nsites_filter(self, queryset, name, value):
        if ">" in value and "=" not in value:
            # print("condition 1")
            array = value.split(">")[1].replace(" ", "")
            minv = Q(nsites__gt=int(array))
            return queryset.filter(minv)
        elif "<" in value and "=" not in value:
            # print("condition 2")
            array = value.split("<")[1].replace(" ", "")
            # print("array", array)
            maxv = Q(nsites__lt=int(array))
            return queryset.filter(maxv)
        if ">=" in value:
            # print("condition 3")
            array = value.split(">=")[1].replace(" ", "")
            minv = Q(nsites__gte=int(array))
            return queryset.filter(minv)
        elif "<=" in value:
            # print("condition 4")
            array = value.split("<=")[1].replace(" ", "")
            maxv = Q(nsites__lte=int(array))
            return queryset.filter(maxv)

        elif "=" in value and "!" not in value:
            # print("condition 5")
            # print("EQUAL 2")
            array = (value.split("=")[1]).replace(" ", "")
            eq = Q(nsites=int(array))
            return queryset.filter(eq)

        elif "!" in value and "=" not in value:
            # print("condition 6")
            # print("Found !")
            array = (value.split("!")[1]).replace(" ", "")
            # print('array',array)
            eq = Q(nsites=int(array))
            return queryset.filter(~eq)
        elif "!=" in value:
            # print("condition 6")
            # print("Found !")
            array = (value.split("!=")[1]).replace(" ", "")
            # print('array',array)
            eq = Q(nsites=int(array))
            return queryset.filter(~eq)
        else:
            # print("condition 7")
            return queryset


    # nsites = django_filters.CharFilter(method="nsites_filter")

    class Meta:
        model = Optimade
        fields = (
            "id",
            "type",
            "jid",
            "nelements",
            "nsites",
            "source",
            # "nsites_range",
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

    @staticmethod
    def search_in_names(queryset, name, value):
        for term in value.split():
            qs = queryset.filter(
                Q(jid__icontains=term)
                | Q(chemical_formula_reduced__icontains=term)
            )

        return qs


class Optimade_ViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = Optimade_Serializer

    # queryset = Optimade.objects.all()
    def get_queryset(self):
        queryset = Optimade.objects.all()
        if not self.request.GET._mutable:
            self.request.GET._mutable = True
        # request.GET = request.GET.copy()
        print("self.request.GET.copy().", self.request.GET.copy())
        for i, j in self.request.GET.copy().items():
            if "!=" in j:
                # print("condition 1a")
                val = j.split("!=")
                self.request.GET[val[0].replace(" ", "")] = str("!") + str(
                    val[1].replace(" ", "")
                )
            elif ">" in j:
                # print("condition 2a")
                val = j.split(">")
                self.request.GET[val[0].replace(" ", "")] = str(">") + str(
                    val[1].replace(" ", "")
                )
            elif ">=" in j:
                # print("condition 3a")
                val = j.split(">=")
                self.request.GET[val[0].replace(" ", "")] = str(">=") + str(
                    val[1].replace(" ", "")
                )
            elif "<" in j:
                # print("condition 4a")
                val = j.split("<")
                self.request.GET[val[0].replace(" ", "")] = str("<") + str(
                    val[1].replace(" ", "")
                )
            elif "<=" in j:
                # print("condition 5a")
                val = j.split("<=")
                self.request.GET[val[0].replace(" ", "")] = str("<=") + str(
                    val[1].replace(" ", "")
                )
            elif "=" in j and "!" not in j:
                # print("condition 6a")
                # print("EQUAL 1")
                val = j.split("=")
                self.request.GET[val[0].replace(" ", "")] = str("=") + str(
                    val[1].replace(" ", "")
                )
            elif "HAS" in i or "HAS" in j:

                if "HAS" in i:
                    val = i
                    # self.request.GET[val.split('HAS')[0]]=tmp_elements_arr
                else:
                    val = j

                tmp_elements_arr = []
                if "ANY" in val.split("elements HAS")[1]:
                    tmp = val.split("elements HAS")[1].split("ANY")
                    condition = "any"
                elif "ALL" in val.split("elements HAS")[1]:
                    tmp = val.split("elements HAS")[1].split("ALL")
                    condition = "all"
                else:
                    condition = "any"
                    tmp = val.split("elements HAS")[1]
                if condition != "only":
                    for ii in tmp:
                        if ii != "" and ii != " " and ii != "   ":
                            tmp_elements = ii.split(",")
                            for jj in ii.split(","):
                                print("jj", jj)
                                sp = Specie(str(jj.strip(" ").strip('"')))
                                try:
                                    z = sp.Z
                                    if z != "na" and not math.isnan(z):
                                        tmp_elements_arr.append(sp.symbol)
                                except Exception as exp:
                                    print("HAS1", exp)
                                    pass
                            # tmp_elements_arr =  [str(jj.strip(' ').strip('"')) for jj in ii.split(',')]
                            print(
                                " tmp_elements_arr",
                                tmp_elements_arr,
                                condition,
                            )
                else:
                    try:
                        sp = Specie(tmp.strip(" ").strip('"'))
                        z = sp.Z
                        if z != "na" and not math.isnan(z):
                            tmp_elements_arr = [sp.symbol]

                    except Exception as exp:
                        print("HAS2", exp)
                        pass
                    print(" tmp_elements_arr", tmp_elements_arr, condition)
                if "HAS" in i:
                    self.request.GET[val.split("HAS")[0].replace(" ", "")] = {
                        "condition": condition,
                        "elements": tmp_elements_arr,
                    }
                    print("self.request.GET i", self.request.GET)
                    # print('self.request.GET[val.split(HAS)[0]]= i',self.request.GET[val.split('HAS')[0]], val.split('HAS')[0])
                else:
                    self.request.GET[val.split("HAS")[0].replace(" ", "")] = {
                        "condition": condition,
                        "elements": tmp_elements_arr,
                    }
                    print("self.request.GET j", self.request.GET)
                    # print('self.request.GET[val.split(HAS)[0]]= j',self.request.GET[val.split('HAS')[0]],  val.split('HAS')[0])

            else:
                # print("condition 7a")
                self.request.GET[i] = j

        self.request.GET._mutable = False
        # print ('self.request',self.request,type(self.request),self.request.GET,'x',self.request.query_params)
        for i, j in self.request.query_params.items():
            print("xyz", i, "-", j)
        nsites = self.request.query_params.get("nsites")
        if nsites is not None:
            print("nsites", nsites)
            # queryset = queryset.filter(purchaser__username=username)
        return queryset

    filter_backends = (
        filters.DjangoFilterBackend,
        OrderingFilter,
        SearchFilter,
    )
    filterset_class = OptimadeFilter
    # filterset_fields = {'nsites':['gte','lte',"exact","in"]}
    ordering_fields = (
        "id",
        "type",
        "jid",
        "nelements",
        "elements",
        "source",
        # "search",
        "nsites",
        "chemical_formula_reduced",
        "chemical_formula_anonymous",
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
    # search_fields = ("full_name", "nelements", "chemical_formula_reduced")
    class Meta:
        model = Optimade
        fields = (
            "id",
            "type",
            "jid",
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


def jarvisdft_general_info(request):
    # def get_post_structures(request):
    if request.method == "GET":
        # return (info)
        info_path = os.path.join(
            os.path.dirname(__file__), "jarvisdft_general_info.json"
        )
        info = loadjson(info_path)
        return JsonResponse(info, json_dumps_params={"indent": 2})


# @api_view(["GET"])  # , 'POST'])
def jarvisdft_info(request):
    # def get_post_structures(request):
    if request.method == "GET":
        info_path = os.path.join(
            os.path.dirname(__file__), "jarvisdft_info.json"
        )
        info = loadjson(info_path)
        # return (info)
        return JsonResponse(info, json_dumps_params={"indent": 2})


def jarvisdft_versions(request):
    if request.method == "GET":
        return HttpResponse(
            "version\n1", content_type="text/csv;header=present"
        )


def jarvisdft_links(request):
    # def get_post_structures(request):
    if request.method == "GET":
        # return (info)
        info_path = os.path.join(
            os.path.dirname(__file__), "jarvisdft_links.json"
        )
        info = loadjson(info_path)
        return JsonResponse(info, json_dumps_params={"indent": 2})
