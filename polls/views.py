from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from .models import Yandex_Market, Ozon


def index(request):
    return render(request, 'polls/index.html')

def Yandex_Market(request):
    table = Yandex_Market.objects.all()
    return render(request, 'polls/yandex.html',
                  {
                      'message_id': table.message_id,
                      'message': table.message,
                      'date': table.date,
                      'views': table.views,
                      'forwards': table.forwards,
                      'path': table.path_to_photo,
                  }
                )

def Ozon(request):
    table = Ozon.objects.all()
    return render(request, 'polls/ozon.html',
                  {
                      'message_id': table.message_id,
                      'message': table.message,
                      'date': table.date,
                      'views': table.views,
                      'forwards': table.forwards,
                      'path': table.path_to_photo,
                  }
                )


# Create your views here
class YandexView(ListView):
    model = Yandex_Market
    template_name = 'yandex.html'
    context_object_name = 'yandex'


class OzonView(ListView):
    model = Ozon
    template_name = 'ozon.html'
    context_object_name = 'ozon'   
