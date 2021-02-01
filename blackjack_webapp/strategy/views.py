from django.shortcuts import render
from django.http import HttpResponse

from .models import Card_Image
from .one_time_setups import setup_database_images


# make sure that card images are in database
setup_database_images()



def index(request):
    return HttpResponse("Hello, you are at the strategy index.")


def infinite_bj(request):
    return render(request, 'infinite_bj.html', {
        'cards_imgs': Card_Image.objects.all(),
        'test': [i.image for i in Card_Image.objects.all()]
    })
















