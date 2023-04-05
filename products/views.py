from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import HttpResponseRedirect, render
from django.views.generic import ListView
from django.views.generic.base import TemplateView


from common.views import TitleMixin
from products.models import Basket, Product, ProductCategory


class IndexView(TitleMixin, TemplateView):
    template_name = 'products\index.html'
    title = 'Store'


# def index(request):
#    context = {'title': 'Store'}
#    return render(request, 'products\index.html', context)


class ProductsListView(TitleMixin, ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 3
    title = 'Каталог'

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['categories'] = ProductCategory.objects.all()
        return context


# def products(request, category_id=None, page=1):
#     products = Product.objects.filter(
#         category=category_id) if category_id else Product.objects.all()
#     per_page = 1
#     paginator = Paginator(products, per_page)
#     products_paginator = paginator.page(page)

#     context = {
#         'title': 'Store - Каталог',
#         'categories': ProductCategory.objects.all(),
#         'products': products_paginator,
#     }
#     return render(request, 'products\products.html', context)


@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
