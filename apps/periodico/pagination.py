from rest_framework.pagination import PageNumberPagination,CursorPagination,LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

# lento con el pasar de las paginas

# DEFAULT_PAGE = 1
# DEFAULT_PAGE_SIZE = 5000

# class CustomPagination(PageNumberPagination):
#     page = DEFAULT_PAGE
#     page_size = DEFAULT_PAGE_SIZE
#     page_size_query_param = 'page_size'

#     def get_paginated_response(self, data):
#         return Response({
#             'links': {
#                 'next': self.get_next_link(),
#                 'previous': self.get_previous_link()
#             },
#             'total': self.page.paginator.count,
#             'page': int(self.request.GET.get('page', DEFAULT_PAGE)), # can not set default = self.page
#             'page_size': int(self.request.GET.get('page_size', self.page_size)),
#             'results': data
#         })


# solo se mueve hacia atras y adelante, no es muy flexible pero gana en consitencia de datos para que no halla datos repetidos, rapido

class CursorPagination(CursorPagination):
    page_size = None
    page_size_query_param = 'page_size'
    ordering = '-id' # '-creation' is default

    def get_page_size(self, request):
        if self.page_size is None:
            try:
                param = int(request.query_params['size'])
            except:
                raise NotFound('No se econtro la url, revise el parametro size')
            if param > 0:
                return param
            else:
                raise NotFound('No se econtro la url, parametro size positivo')
        else:
            return self.page_size


# se da un limite y/o un desplazamiento, es mas cercano a un numberpagination, rapido

class LimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10
    # offset_query_param = 'id'
    # max_limit = None
    
    # def get_paginated_response(self, data):
    #     return Response({
    #         'links': {
    #             'next': self.get_next_link(),
    #             'previous': self.get_previous_link()
    #         },
    #         'total': self.page.paginator.count,
    #         'page': int(self.request.GET.get('page', DEFAULT_PAGE)), # can not set default = self.page
    #         'page_size': int(self.request.GET.get('page_size', self.page_size)),
    #         'results': data
    #     })