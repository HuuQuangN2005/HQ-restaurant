from rest_framework.pagination import PageNumberPagination

class AccountInfoPaginator(PageNumberPagination):
    page_size = 3
    
