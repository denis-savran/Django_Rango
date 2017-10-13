from collections import defaultdict

from django.db.models import Case, When
from django_elasticsearch_dsl import DocType, Index
from elasticsearch_dsl.connections import connections

from Django_Rango.settings import ELASTICSEARCH_DSL
from rango.models import Category, Page

connections.create_connection(hosts=[ELASTICSEARCH_DSL['default']['hosts']])

index_name = 'rango'
rango = Index(index_name)

index_settings = {
    "number_of_shards": 5,
    "number_of_replicas": 1,
}


@rango.doc_type
class CategoryDocument(DocType):
    class Meta:
        model = Category

        fields = [
            'name'
        ]


@rango.doc_type
class PageDocument(DocType):
    class Meta:
        model = Page

        fields = [
            'title',
        ]


def get_qs_with_specified_order(model, order):
    qs = model.objects.filter(pk__in=order)
    preserved_order = Case(
        *[When(pk=pk, then=pos) for pos, pk in enumerate(order)]
    )
    return qs.order_by(preserved_order)


def search_all_doc_types(search_text):
    search_result = rango.search().filter('match', _all=search_text)

    hit_dict = defaultdict(lambda: [])
    for hit in search_result:
        hit_dict[hit.meta.doc_type].append(hit.meta.id)

    result = {}
    for doc_type, ids in hit_dict.items():
        if doc_type == 'category_document':
            model = Category
            context_dict_key = 'categories'
        if doc_type == 'page_document':
            model = Page
            context_dict_key = 'pages'
        result[context_dict_key] = get_qs_with_specified_order(model, ids)
    return result
