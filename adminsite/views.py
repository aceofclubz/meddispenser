from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from .forms import *


def login(request):
    context = {}
    if request.method == 'POST':
        m = Admin.objects.get(adminuser=request.POST['adminuser'])
        if m.adminpass == request.POST['adminpass']:
            request.session['admin_id'] = m.adminid
            request.session['user'] = m.adminuser
            return redirect('/')
        else:
            context['fail'] = True
            return render(request, 'signin.html', context)
    else:
        context['field'] = AdminForm()
        return render(request, 'signin.html', context)


def logout(request):
    try:
        del request.session['admin_id']
        del request.session['user']
    except KeyError:
        pass
    return redirect('/')


def index(request):
    try:
        context = {}
        context['user'] = request.session['user']
        context['transactions'] = Transaction.objects.all().order_by('-datetime')
        return render(request, 'index.html', context)
    except KeyError:
        return redirect('/login')


def users(request):
    context = {}
    context['users'] = User.objects.all()
    return render(request, 'user.html', context)

def transact(request):
    context = {}
    context['transactions'] = Transaction.objects.all().order_by('-datetime')
    return render(request, 'transaction.html', context)

def transact_d(request):
    context = {}
    start_date = request.POST['start']
    end_date = request.POST['end']
    context['transactions'] = Transaction.objects.filter(datetime=(start_date, end_date)).order_by('-datetime')
    return render(request, 'transaction.html', context)


def transact_u(request, user_id):
    context = {}
    user = User.objects.get(uid=user_id)
    context['transactions'] = Transaction.objects.filter(userid=user).order_by('-datetime')
    return render(request, 'transaction.html', context)


def transact_med(request, med_id):
    context = {}
    context['transactions'] = Transaction.objects.filter(medid=med_id).order_by('-datetime')
    return render(request, 'transaction.html', context)


def medicine(request):
    context = {}
    context['medicines'] = Medicine.objects.all()
    return render(request, 'medicine.html', context)


def user_c(request, for_admin=0):
    context = {}
    for_admin = for_admin == 1
    if request.method == 'POST':
        if for_admin:
            form = AdminForm(request.POST)
        else:
            form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/users')
        else:
            if for_admin:
                context['form_a'] = form
                context['form_u'] = UserForm()
            else:
                context['form_u'] = form
                context['form_a'] = AdminForm()
            return render(request, 'create.html', context)
    else:
        context['form_u'] = UserForm()
        context['form_a'] = AdminForm()
        return render(request, 'create.html', context)


def user_u(request, user_id, for_admin=0):
    context = {}
    for_admin = for_admin == 1
    try:
        admin = Admin.objects.get(adminuser=user_id)
        in_admin = True
    except ObjectDoesNotExist:
        in_admin = False

    user = User.objects.get(uid=user_id)
    if request.method == 'POST':
        if for_admin:
            form = AdminForm(request.POST, instance=admin)
        else:
            form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            if in_admin:
                context['form_a'] = AdminForm(instance=admin)
            context['form_u'] = UserForm(instance=user)
            return render(request, 'update.html', context)
    else:
        if in_admin:
            context['form_a'] = AdminForm(instance=admin)
        context['form_u'] = UserForm(instance=user)
        return render(request, 'update.html', context)
    # toDO: account for not existing user but admin
