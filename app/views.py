from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout


from app.models import Iphone, Client, Moratoire, Versement
from app.forms import IphoneForm, ClientForm, MoratoireForm, VersementForm


# Create your views here.
def login_user(request):
    msg = None
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            msg = 'Donnees invalides'
    return render(request, 'app/index.html', {'msg': msg})


def logout_user(request):
    logout(request)
    return redirect('index')


def register(request):
    return render(request, 'app/register.html')


def home(request):
    iphones = Iphone.objects.all()
    return render(request, 'app/home.html', {'iphones': iphones})


def iphone_add(request):
    msg = None
    if request.method == "POST":
        form = IphoneForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            msg = "erreur"
    else:
        form = IphoneForm()
    return render(request, 'app/iphone_add.html', {'form': form, 'msg': msg})


def iphone_update(request, id_iphone):
    iphone = get_object_or_404(Iphone, id=id_iphone)
    form = IphoneForm(request.POST or None, instance=iphone)
    if form.is_valid():
        form.save()
        return redirect('home')
    return render(request, 'app/iphone_update.html', {'form': form})


# client Simple ******************************************************************
def client_add(request):
    '''stock_models_iphone = Iphone.objects.all().filter(stock__gt=0)

    init_values = {'iphone': stock_models_iphone, 'nome': 'mouhaz'}
    print(init_values)
'''
    msg = None
    info_stock = None
    if request.method == "POST":
        form = ClientForm(request.POST or None)
        if form.is_valid():
            f = form.save(commit=False)
            tmp = f.iphone.stock
            if f.iphone.stock and f.quantity <= f.iphone.stock:
                tmp = f.iphone.stock - f.quantity
                f.iphone.stock = tmp
                f.iphone.save()
                f.save()
                return redirect('client_list')
            else:
                info_stock = 'Stock insuffisant'
                form = ClientForm()
                return render(request, 'app/client_add.html', {'info_stock': info_stock, 'form': form})
        else:
            msg = "erreur"
    else:
        form = ClientForm()
        #form = ClientForm(initial={'nom': "mama", 'iphone': stock_models_iphone, 'prenom': 'faye'})
    return render(request, 'app/client_add.html', {'form': form, 'msg': msg})


def client_list(request):
    clients = Client.objects.all()
    return render(request, 'app/client_list.html', {'clients': clients})


def client_edit(request, id_client):
    info_stock = None
    client = get_object_or_404(Client, id=id_client)
    tmp_qtty_client = client.quantity
    form = ClientForm(request.POST or None, instance=client)
    if form.is_valid():
        f = form.save(commit=False)
        tmp_stock = f.iphone.stock

        if f.iphone.stock and f.quantity <= f.iphone.stock:
            if f.quantity > tmp_qtty_client:
                diff = f.quantity - tmp_qtty_client
                f.iphone.stock -= diff
                f.iphone.save()
                f.save()
                return redirect('client_list')

            elif f.quantity < tmp_qtty_client:
                diff = tmp_qtty_client - f.quantity
                f.iphone.stock += diff
                f.iphone.save()
                f.save()
                return redirect('client_list')
            else:
                f.save()
                f.iphone.save()
                return redirect('client_list')

        else:
            info_stock = "stock insuffisant"
            return render(request, 'app/client_edit.html', {'form': form, 'info_stock': info_stock})

    return render(request, 'app/client_edit.html', {'form': form})


# client Moratoire ******************************************************************
def client_moratoire_add(request):
    msg = None
    info_stock = None
    if request.method == "POST":
        form = MoratoireForm(request.POST or None)

        if form.is_valid():
            f = form.save(commit=False)
            tmp = f.iphone.stock
            if f.iphone.stock and f.quantity <= f.iphone.stock:
                f.restant = f.montant - f.avance
                tmp = f.iphone.stock - f.quantity
                f.iphone.stock = tmp
                f.iphone.save()
                f.save()
                return redirect('moratoire_list')
            else:
                info_stock = 'Stock insuffisant'
                form = MoratoireForm()
                return render(request, 'app/moratoire_add.html', {'info_stock': info_stock, 'form': form})
        else:
            msg = "erreur"
    else:
        form = MoratoireForm()
    return render(request, 'app/moratoire_add.html', {'form': form, 'msg': msg})


def client_list_moratoire(request):
    clients_moratoire = Moratoire.objects.all()
    return render(request, 'app/moratoire_list.html', {'clients': clients_moratoire})


def client_moratoire_edit(request, id_client):
    info_stock = None
    client = get_object_or_404(Moratoire, id=id_client)
    tmp_qtty_client = client.quantity
    form = MoratoireForm(request.POST or None, instance=client)
    if form.is_valid():
        f = form.save(commit=False)
        tmp_stock = f.iphone.stock

        if f.iphone.stock and f.quantity <= f.iphone.stock:
            if f.quantity > tmp_qtty_client:
                diff = f.quantity - tmp_qtty_client
                f.iphone.stock -= diff
                f.restant = f.montant - f.avance
                f.iphone.save()
                f.save()
                return redirect('moratoire_list')

            elif f.quantity < tmp_qtty_client:
                diff = tmp_qtty_client - f.quantity
                f.iphone.stock += diff
                f.restant = f.montant - f.avance
                f.iphone.save()
                f.save()
                return redirect('moratoire_list')
            else:
                f.restant = f.montant - f.avance
                f.save()
                f.iphone.save()
                return redirect('moratoire_list')

        else:
            info_stock = "stock insuffisant"
            return render(request, 'app/moratoire_edit.html', {'form': form, 'info_stock': info_stock})

    return render(request, 'app/moratoire_edit.html', {'form': form})


# client Versement ******************************************************************
def versement_add(request):
    versement_existant = Versement.objects.all()

    #init_values = {'iphone': stock_models_iphone, 'nome': 'mouhaz'}
    print(versement_existant)

    msg = None
    info_stock = None
    if request.method == "POST":
        form = VersementForm(request.POST or None)
        if form.is_valid():
            fv = form.save(commit=False)
            print('client req', fv.client_moratoire )
            if fv.client_moratoire.restant != 0:
                if fv.versement != 0:
                    if fv.restant_v == 0:
                        print("existant")
                        fv.restant_v = fv.restant_v - fv.versement
                        fv.save()
                        return redirect('versement_list')
                    else:
                        print("nouvau")
                        fv.client_moratoire.avance += fv.versement
                        fv.restant_v = fv.client_moratoire.restant - fv.versement
                        fv.client_moratoire.save()
                        fv.save()
                        return redirect('versement_list')

                else:
                    info_stock = 'No change'
                    form = VersementForm()
                    return render(request, 'app/versement_add.html', {'info_stock': info_stock, 'form': form})
            else:
                info_stock = 'plus de restant'
                form = VersementForm()
                return render(request, 'app/versement_add.html', {'info_stock': info_stock, 'form': form})
        else:
            msg = "erreur"
    else:
        form = VersementForm()

    return render(request, 'app/versement_add.html', {'form': form, 'msg': msg})


def versement_list(request):
    clients_moratoire = Versement.objects.all()
    return render(request, 'app/versement_list.html', {'clients': clients_moratoire})


def versement_delete(request, id_client):
    client = get_object_or_404(Versement, id=id_client)
    client.delete()
    return redirect('versement_list')
