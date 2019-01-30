from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .models import *
from .forms import *


def login(request):
    context = {}
    if request.method == 'POST':
        m = Admin.objects.get(adminuser=request.POST['adminuser'])
        if m.adminpass == request.POST['adminpass']:
            request.session['admin_id'] = m.adminid
            return redirect('/')
        else:
            context['fail'] = True
            return render(request, 'signin.html', context)
    else:
        context['form'] = AdminForm()
        return render(request, 'signin.html', context)


def logout(request):
    try:
        del request.session['admin_id']
    except KeyError:
        pass
    return HttpResponse("You're logged out.")


def index(request):
    try:
        context = {'id': request.session['admin_id']}

        return render(request, 'index.html', context)
    except KeyError:
        return redirect('/login')


def users(request):
    pass


def transact(request):
    start_date = request.POST['start']
    end_date = request.POST['end']
    Transaction.objects.filter(datetime=(start_date, end_date))
    pass


def transact_u(request, user_id):
    Transaction.objects.filter(userid=user_id)
    pass


def transact_med(request, med_id):
    Transaction.objects.filter(medid=med_id)
    pass
def medicine(request):


    pass


def specificMedicine(request, med_id):
    pass
