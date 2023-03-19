from rest_framework.pagination import PageNumberPagination, _positive_int


class CustomPagination(PageNumberPagination):
    # def get_page_size(self, request):
    page_size_query_param = 'limit'
    page_size = 6
        # if page_size_query_param:
        #     try:
        #         return _positive_int(
        #             page_size_query_param,
        #             strict=True,
        #             cutoff=self.max_page_size
        #         )
        #     except Exception:
        #         return self.page_size
