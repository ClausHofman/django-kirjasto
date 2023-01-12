from django.shortcuts import render
from django.http import HttpResponse
from .models import Book,Author,BookInstance,Genre,Language
from django.views.generic import CreateView,DetailView


# Create your views here.

def index(request):
    
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    num_instances_avail = BookInstance.objects.filter(status__exact='a').count()

    context = {
        'num_books':num_books,
        'num_instances':num_instances,
        'num_instances_avail':num_instances_avail

    }

    return render(request,'catalog/index.html',context=context)

# luo kirja CreateView:lla (malli Book), luo book_form.html, yhdistä näkymät urls.py (catalog/urls.py)
class BookCreate(CreateView): # book_form.html
    model = Book
    fields = '__all__'

# kun kirja on lisätty, oletuksena mene sen jälkeen DetailView sivulle:
# luo book_detail.html ja lisää path urls.py
class BookDetail(DetailView):
    model = Book
    # tai success_url = reverse_lazy('x:y')