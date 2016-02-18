import datetime
from django.shortcuts import render


def home(request):
    context_dict = {
        'profile': {
            'name': 'Yevhen',
            'surname': 'Malov',
            'date_of_birth': datetime.date.today(),
            'bio': 'My bio',
            'contact': 'yvhn.yvhn@gmail.com'
        }
    }
    return render(request, 'hello/index.html', context_dict)
