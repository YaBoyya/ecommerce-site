from django.db.models import Q


class SearchMixin:
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        q = request.GET.get('q')
        if q:
            queryset = queryset.filter(name__icontains=q)

        page = self.paginate_queryset(queryset)

        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class ProductSearchMixin:
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        q = request.GET.get('q')
        if q:
            queryset = queryset.filter(Q(name__icontains=q)
                                       | Q(category_id__name__icontains=q))

        page = self.paginate_queryset(queryset)

        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
