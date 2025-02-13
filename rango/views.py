from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category, Page

def index(request):
    # Top 5 categories ordered by likes
    category_list = Category.objects.order_by('-likes')[:5]

    # Top 5 pages ordered by views
    pages = Page.objects.order_by('-views')[:5]

    # Context dictionary
    context_dict = {
        'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!',
        'categories': category_list,
        'pages': pages,
    }

    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    context_dict={'Your_name': 'Uuriintuya'}
    return render(request, 'rango/about.html', context=context_dict)


def show_category(request, category_name_slug):
    # Create a context dictionary
    context_dict = {}
    try:
        # Try to get the category with the given slug
        category = Category.objects.get(slug=category_name_slug)

        # Retrieve pages related to this category
        pages = Page.objects.filter(category=category)

        # Add pages and category to context
        context_dict['pages'] = pages
        context_dict['category'] = category


    except Category.DoesNotExist:
        # If the category doesn't exist, set to None
        context_dict['category'] = None
        context_dict['pages'] = None

    # Render the response with the context dictionary
    return render(request, 'rango/category.html', context=context_dict)