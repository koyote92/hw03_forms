from django.core.paginator import Paginator


def paginate_page(request, page, count):
    paginator = Paginator(page, count)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)
