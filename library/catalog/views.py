from django.shortcuts import render
from django.http import HttpResponse
from .models import Book,Author,BookInstance,Genre,Language
from django.views.generic import CreateView,DetailView,ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.utils import timezone


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
class BookCreate(LoginRequiredMixin,CreateView): # book_form.html
    model = Book
    fields = '__all__'

# kun kirja on lisätty, oletuksena mene sen jälkeen DetailView sivulle:
# luo book_detail.html ja lisää path urls.py
class BookDetail(DetailView):
    model = Book
    # tai success_url = reverse_lazy('x:y')
    
    # date test
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

@login_required
def my_view(request):
    # user needs to be logged in
    return render(request,'catalog/my_view.html')


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'catalog/signup.html'

from django.utils import timezone
class CheckedOutBooksByUserView(LoginRequiredMixin,ListView):
    # List all BookInstances BUT filter based off currently logged in user session
    model = BookInstance
    template_name = 'catalog/profile.html'
    paginate_by = 5 # 5 book instances per page

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).all() # query_set

