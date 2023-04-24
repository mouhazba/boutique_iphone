from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, get_user_model

from app.models import Iphone, Client, Moratoire, Versement
from app.forms import IphoneForm, ClientForm, MoratoireForm, VersementForm


User = get_user_model()


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
    return render(request, 'app/accounts/index.html', {'msg': msg})


def logout_user(request):
    logout(request)
    return redirect('index')


def register(request):
    msg = None

    if request.method == 'POST':
        name = request.POST["username"]
        pwd1 = request.POST["pwd1"]
        pwd2 = request.POST["pwd2"]

        if pwd1 == pwd2:
            user = User.objects.create_user(username=name, password=pwd1)
            login(request, user)
        else:
            msg = 'Mot de passe ne correspondent pas'
            return render(request, 'app/accounts/register.html', {'msg': msg})

    return render(request, 'app/accounts/register.html')


#@user_passes_test(lambda u: u.username == "mahadiou" or u.username == 'abass')
def home(request):
    iphones = Iphone.objects.all()
    stock = iphones.filter(stock__lte=0)

    clients = Client.objects.all()
    mora = Moratoire.objects.all()
    return render(request, 'app/home.html', {'iphones': iphones, 'stock': stock, 'clients': clients, 'mora': mora})


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
    return render(request, 'app/iphones/iphone_add.html', {'form': form, 'msg': msg})


def iphone_update(request, id_iphone):
    iphone = get_object_or_404(Iphone, id=id_iphone)
    form = IphoneForm(request.POST or None, instance=iphone)
    if form.is_valid():
        form.save()
        return redirect('home')
    return render(request, 'app/iphones/iphone_update.html', {'form': form})


# client Simple ******************************************************************
def client_add(request):
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
                if f.quantity > 1:
                    f.montant = f.quantity * f.montant
                f.iphone.save()
                f.save()
                return redirect('client_list')
            else:
                info_stock = 'Stock insuffisant'
                form = ClientForm()
                return render(request, 'app/clients/client_add.html', {'info_stock': info_stock, 'form': form})
        else:
            info_stock = 'Erreur'
            form = ClientForm()
            return render(request, 'app/clients/client_add.html', {'info_stock': info_stock, 'form': form})
    else:
        form = ClientForm()
    return render(request, 'app/clients/client_add.html', {'form': form, 'msg': msg})


def client_list(request):
    clients = Client.objects.all()
    return render(request, 'app/clients/client_list.html', {'clients': clients})


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
            return render(request, 'app/clients/client_edit.html', {'form': form, 'info_stock': info_stock})

    return render(request, 'app/clients/client_edit.html', {'form': form})


def client_detail(request, id_client):
    client = get_object_or_404(Client, id=id_client)
    return render(request, 'app/clients/client_detail.html', {'client': client})


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
                return render(request, 'app/moratoires/moratoire_add.html', {'info_stock': info_stock, 'form': form})
        else:
            msg = "erreur"
    else:
        form = MoratoireForm()
    return render(request, 'app/moratoires/moratoire_add.html', {'form': form, 'msg': msg})


def client_list_moratoire(request):
    clients_moratoire = Moratoire.objects.all()
    return render(request, 'app/moratoires/moratoire_list.html', {'clients': clients_moratoire})


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
            return render(request, 'app/moratoires/moratoire_edit.html', {'form': form, 'info_stock': info_stock})

    return render(request, 'app/moratoires/moratoire_edit.html', {'form': form})


def client_moratoire_detail(request, id_client):
    client = get_object_or_404(Moratoire, id=id_client)
    return render(request, 'app/moratoires/moratoire_detail.html', {'client': client})


def client_moratoire_delete(request, id_client):
    client = get_object_or_404(Moratoire, id=id_client)
    if request.method == 'POST':
        client.delete()
        return redirect('moratoire_list')

    return render(request, 'app/moratoires/moratoire_delete.html', {'client': client})


# client Versement ******************************************************************
def versement_add(request):
    msg = None
    info_stock = None
    if request.method == "POST":
        client_id = request.POST['client_moratoire']
        form = VersementForm(request.POST or None)
        moratoire_id = get_object_or_404(Moratoire, id=client_id)
        v_list = Versement.objects.all().filter(restant_v__gte=0)
        tel = moratoire_id.tel

        def get_Restant():
            for v in v_list:
                if v.client_moratoire.tel == tel:
                    restantX = v.restant_v
                    return restantX
            return 0

        restant = get_Restant()

        if form.is_valid():
            fv = form.save(commit=False)
            if fv.client_moratoire.restant != 0:
                if fv.versement != 0:
                    if restant == 0:
                        fv.restant_v = fv.client_moratoire.restant - fv.versement
                        fv.save()
                        return redirect('versement_list')

                    else:
                        fv.restant_v = restant - fv.versement
                        fv.save()
                        return redirect('versement_list')

                else:
                    info_stock = 'No change'
                    form = VersementForm()
                    return render(request, 'app/versements/versement_add.html', {'info_stock': info_stock, 'form': form})
            else:
                info_stock = 'plus de restant'
                form = VersementForm()
                return render(request, 'app/versements/versement_add.html', {'info_stock': info_stock, 'form': form})
        else:
            msg = "erreur"
    else:
        form = VersementForm()

    return render(request, 'app/versements/versement_add.html', {'form': form, 'msg': msg})


def versement_list(request):
    clients_moratoire = Versement.objects.all()
    return render(request, 'app/versements/versement_list.html', {'clients': clients_moratoire})


def versement_delete(request, id_client):
    client = get_object_or_404(Versement, id=id_client)
    if request.method == 'POST':
        client.delete()
        return redirect('versement_list')

    return render(request, 'app/versements/versement_delete.html', {'client': client})


def versement_detail(request, id_client):
    client = get_object_or_404(Versement, id=id_client)
    return render(request, 'app/versements/versement_detail.html', {'client': client})
