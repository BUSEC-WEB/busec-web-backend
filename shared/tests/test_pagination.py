from django.test import SimpleTestCase
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from shared.pagination import StandardPagination

ITEMS = list(range(250))


def page_length(query: str = "") -> int:
    request = Request(APIRequestFactory().get(f"/items/{query}"))
    page = StandardPagination().paginate_queryset(ITEMS, request)
    assert page is not None
    return len(page)


class StandardPaginationTests(SimpleTestCase):
    def test_default_page_size_is_20(self) -> None:
        self.assertEqual(page_length(), 20)

    def test_client_can_choose_page_size(self) -> None:
        self.assertEqual(page_length("?page_size=5"), 5)

    def test_page_size_is_capped_at_100(self) -> None:
        self.assertEqual(page_length("?page_size=1000"), 100)

    def test_response_includes_count_and_links(self) -> None:
        request = Request(APIRequestFactory().get("/items/"))
        paginator = StandardPagination()
        page = paginator.paginate_queryset(ITEMS, request)

        response = paginator.get_paginated_response(page)

        self.assertEqual(set(response.data), {"count", "next", "previous", "results"})
        self.assertEqual(response.data["count"], 250)
