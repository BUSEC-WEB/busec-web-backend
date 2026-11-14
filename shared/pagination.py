from rest_framework.pagination import PageNumberPagination


class StandardPagination(PageNumberPagination):
    """Project-wide default. Clients may request a smaller or larger page,
    capped so a single request can't pull the whole table."""

    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100
