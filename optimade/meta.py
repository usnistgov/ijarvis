from rest_framework.metadata import SimpleMetadata


class MyCustomMetadata(SimpleMetadata):
    def determine_metadata(self, request, view):
        metadata = super(MyCustomMetadata, self).determine_metadata(
            request, view
        )
        metadata[
            "source"
        ] = "jarvis.nist.gov"  # add extra attribute to metadata
        return (
            metadata  # return the metadata with the extra attribute set in it
        )
