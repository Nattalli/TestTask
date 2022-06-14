from rest_framework import pagination
from rest_framework.response import Response


class NewPagination(pagination.PageNumberPagination):
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'total_count': self.page.paginator.count,
            'page_count': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'results': data
        })
