from rest_framework.pagination import PageNumberPagination


class OrderPaginator(PageNumberPagination):
    page_size = 10
