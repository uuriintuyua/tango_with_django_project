from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from rango.models import Category, Page
from rango.forms import CategoryForm
from django.shortcuts import redirect
from rango.forms import PageForm

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

def add_category(request):
    form = CategoryForm()
 # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)
 # Have we been provided with a valid form?
        if form.is_valid():
 # Save the new category to the database.
            form.save(commit=True)
 # Now that the category is saved, we could confirm this.
 # For now, just redirect the user back to the index view.
            return redirect('/rango/')
    else:
        print(form.errors)
# Will handle the bad form, new form, or no form supplied cases.
# Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
 # You cannot add a page to a Category that does not exist...
    if category is None:
        return redirect('/rango/')
    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                 page = form.save(commit=False)
                 page.category = category
                 page.views = 0
                 page.save()
                 return redirect(reverse('rango:show_category',
                                         kwargs={'category_name_slug':
                                                     category_name_slug}))
            else:
                print(form.errors)
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)