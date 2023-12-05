from collections import OrderedDict
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

meta = {
    "api_version": "1.1.0",
    "query": {"representation": "v1/structures"},
    "more_data_available": True,
    # "schema": "https://schemas.optimade.org/openapi/v1.1.0/optimade_index.json",
    "provider": {
        "name": "Joint Automated Repository for Various Integrated Simulations (JARVIS)",
        "description": "JARVIS is a repository designed to automate materials discovery using classical force-field, density functional theory, machine learning calculations and experiments.",
        "prefix": "jarvis",
        "homepage": "https://jarvis.nist.gov",
    },
}


class Pagination(PageNumberPagination):
    page_size = 4

    def get_paginated_response(self, data):
        more_data_available = True
        if self.get_previous_link() is None and self.get_next_link() is None:
            more_data_available = False

        meta = {
            "api_version": "1.1.0",
            "query": {"representation": "v1/structures"},
            "more_data_available": more_data_available,
            # "schema": "https://schemas.optimade.org/openapi/v1.1.0/optimade_index.json",
            "provider": {
                "name": "Joint Automated Repository for Various Integrated Simulations (JARVIS)",
                "description": "JARVIS-DFT is a repositiory of density functional theory claculations for 3D and 2D materials.",
                "prefix": "jarvis",
                "homepage": "https://jarvis.nist.gov/jarvisdft",
            },
        }

        return Response(
            OrderedDict(
                [
                    ("meta", meta),
                    ("count", self.page.paginator.count),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("data", data),
                ]
            )
        )
