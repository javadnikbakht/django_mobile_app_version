from rest_framework.pagination import PageNumberPagination


class PageNumberSizedPagination(PageNumberPagination):
    page_size_query_param = 'per_page'
