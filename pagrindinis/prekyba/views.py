from django.shortcuts import render
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.forms import User
from django.contrib import messages

from django.core.paginator import Paginator

from django.shortcuts import render, get_object_or_404

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import ListView,DetailView

from .models import Preke,Krepselis,Sandelys,Pardavejas,Atsiliepimai,Uzsakymas
from .forms import  (
    UzsakymasForm,UserForm,ProfilioForm,
    AtsiliepimuForm,SandelysForm,PrekesIkelimasForm,
    PardavejoForm
)
from django.db.models import Q

from django.http import HttpResponseRedirect



def code(request):
    return render(request,'code.html')

def index(request):
    prekes=Preke.objects.all()

    paginator = Paginator(Preke.objects.all(), 7)
    page_number = request.GET.get('page')
    paged_preke = paginator.get_page(page_number)

    return render(request, 'index.html',context={'prekes':prekes, 'pag':paged_preke})


def prekes(request):
    paginator = Paginator(Preke.objects.all(), 15)
    page_number = request.GET.get('page')
    paged_preke = paginator.get_page(page_number)

    context={
        'prekes':paged_preke,

    }

    return render(request, 'prekes.html', context=context)


def preke(request, preke_id):
    preke= get_object_or_404(Preke, pk=preke_id)
    atsiliepimas=Atsiliepimai.objects.filter(prekes_id=preke_id).order_by('-sukurta')

    atsiliepimo_form=AtsiliepimuForm()
    uzsakymas_form = UzsakymasForm()

    smth = 1 * preke.kaina

    if request.user.is_authenticated:
        data = {
            'perkamas_kiekis':1,
            'sandelio_id': Sandelys.objects.get(prekes_id=preke_id),
            'krepselio_id': Krepselis.objects.get(vartotojo_id=request.user),
        }
        atsiliep={
            'atsiliepimas':"Super Preke :)",
            'vartotojas': request.user,
            'prekes_id': get_object_or_404(Preke,id=preke_id),
        }

        uzsakymas_form = UzsakymasForm(data)
        atsiliepimo_form = AtsiliepimuForm(atsiliep)

        if request.method == "POST":
            if 'uzsakymas' in request.POST:
                uzsakymas_form = UzsakymasForm(request.POST)
                if uzsakymas_form.is_valid():
                    uzsakymas_form.save()
                    messages.success(request, 'Uzsakymas idetas i krepseli')
                    uzsakymas_form

            elif 'pranesimas' in request.POST:
                atsiliepimo_form = AtsiliepimuForm(request.POST)
                if atsiliepimo_form.is_valid():
                    atsiliepimo_form.save()
                    atsiliepimo_form

    context = {
        'form': uzsakymas_form,
        'preke':preke,
        'kaina':smth,
        'atsi':atsiliepimas,
        'atsi_form':atsiliepimo_form,
    }
    return render(request, 'preke.html', context=context)


class KrepselisDetailView(LoginRequiredMixin,DetailView):
    model = Krepselis
    template_name = 'krepselis.html'
    pk_url_kwarg = 'id'


def KrepsDelete(request,id):
    a = Krepselis.objects.filter(vartotojo_id=request.user)
    uzsak = Uzsakymas.objects.filter(krepselio_id=request.user.krepselis.id)

    if request.method == 'POST':
        uzsak.delete()
        messages.success(request,'Uzsakymai Istrinti')
        return HttpResponseRedirect(f"/svetaine/krepselis/{id}")

    context={
        'a':a,
        'b':uzsak,
    }

    return render(request,'krepselio_istrinimas.html',context)


class PardavejasListView(ListView):
    model = Pardavejas
    template_name = 'pardavejai.html'


def Pardavejo_prekes(request, pardavejas_id):
    pardavejas=get_object_or_404(Pardavejas,id=pardavejas_id)

    paginator = Paginator(Preke.objects.filter(pardavejas_id=pardavejas_id), 10)
    page_number = request.GET.get('page')
    paged_preke = paginator.get_page(page_number)

    context = {
        'b':pardavejas,
        'a':paged_preke,
    }
    return render(request, 'pardavejas.html', context=context)


def kontaktai(request):
    return render(request,'kontaktai.html')


def paieska(request):
    query = request.GET.get('query')
    search_results = Preke.objects.filter(Q(pavadinimas__icontains=query) | Q(aprasymas__icontains=query))
    return render(request, 'paieska.html', {'results': search_results, 'query': query})


def pardavejas_kurimas(request):
    pard = {
        'pavad': f"{request.user.username}",
        'priklauso': request.user,
    }
    pard_form = PardavejoForm(pard)

    if request.user.is_authenticated:


        if request.method == "POST":
            if 'pardav' in request.POST:
                pard_form = PardavejoForm(request.POST)
                if pard_form.is_valid():
                    pard_form.save()
                    messages.success(request, 'Sukurtas Pardavejas')
                    return redirect('profilis')

            if 'istrinimas' in request.POST:
                pavadinimas = get_object_or_404(Pardavejas, id=request.user.pardavejas.id)
                pavadinimas.delete()
                messages.success(request, 'Pardavejas istrintas')
                return redirect('profilis')

    context = {
        'pardavejas': pard_form,
    }

    return render(request, 'pardavejo_sukurimas.html', context)


def ikelimas(request):
        if request.user.pardavejas.id :
            prek = {
                'pardavejas_id': request.user.pardavejas.id,
                'kaina':1,
            }
            sand = {
                'pridetas_kiekis': 1,
            }

            prek_form = PrekesIkelimasForm(prek)
            sand_form = SandelysForm(request,sand)

            if 'prek' in request.POST:
                prek_form = PrekesIkelimasForm(request.POST,request.FILES)
                if prek_form.is_valid():
                    prek_form.save()
                    messages.info(request, 'Preke Ikelta')
                    return redirect('ikelimas')

            if 'sand' in request.POST:
                sand_form = SandelysForm(request,request.POST)
                if sand_form.is_valid():
                    sand_form.save()
                    messages.info(request, 'Pridetas Kiekis')
                    return redirect('ikelimas')

        context={
            'preke':prek_form,
            'sandelys':sand_form,
        }
        return render(request,'prekes_ikelimas.html',context)


def pirkimas(request,id):
    kaina=get_object_or_404(Krepselis, id=request.user.krepselis.id)
    pirkejas=request.user
    uzsak = Uzsakymas.objects.filter(krepselio_id=request.user.krepselis.id)


    if request.method == "POST":
        if 'pirkimas' in request.POST:
            uzsak.delete()
            messages.success(request,
             'Sekmingai Nusipirkote Prekes... '
             'Kazkokiu stebuklingu butu bus nuskaiciuoti pinigai ;D..'
             'Prekes gali buti nepristatytos ')
            return HttpResponseRedirect(f"/svetaine/krepselis/{id}")

    context={
        'p':pirkejas,
        'k':kaina,
    }

    return render(request,'pirkimas.html',context)


@login_required
def profilis(request):
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profilio_form = ProfilioForm(request.POST, request.FILES, instance=request.user.profilis)
        if user_form.is_valid() and profilio_form.is_valid():
            user_form.save()
            profilio_form.save()
            messages.success(request, f"Profilis atnaujintas")
            return redirect('profilis')
    else:
        user_form = UserForm(instance=request.user)
        profilio_form = ProfilioForm(instance=request.user.profilis)

    context = {
        'u_form': user_form,
        'p_form': profilio_form,
    }
    return render(request, 'profilis.html', context)


@csrf_protect
def register(request):
    if request.method == "POST":

        if 'registruotis' in request.POST:
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            password2 = request.POST['password2']

            if password == password2:

                if User.objects.filter(username=username).exists():
                    messages.error(request, f'Vartotojo vardas {username} užimtas!')
                    return redirect('register')
                else:

                    if User.objects.filter(email=email).exists():
                        messages.error(request, f'Vartotojas su el. paštu {email} jau užregistruotas!')
                        return redirect('register')
                    else:

                        User.objects.create_user(username=username, email=email, password=password)
            else:
                messages.error(request, 'Slaptažodžiai nesutampa!')
                return redirect('register')
            return redirect('login')

    return render(request, 'register.html')






# def KrepsUpdate(request,id):
#     a = Krepselis.objects.get(vartotojo_id=request.user)
#     uzsak = Uzsakymas.objects.filter(krepselio_id=request.user.krepselis.id)
#
#     # uz_form=UzsakymasForm(instance=uzsak)
#     uz_form=UzsakymasForm
#
#     # data = {
#     #     'sandelio_id': Sandelys.objects.get(prekes_id=id),
#     #     'krepselio_id': Krepselis.objects.get(vartotojo_id=request.user).id,
#     # }
#     #
#     # if request.method == "POST":
#     #     if 'patvirtinti' in request.POST:
#     #         uz_form = UzsakymasForm(request.POST)
#     #         if uz_form.is_valid():
#     #             uz_form.save()
#
#
#     context={
#         'b':a,
#         'a':uz_form,
#         'uzsakymas':uzsak,
#     }
#
#     return render(request,'kreps_upd.html',context)

# class KrepsUpdate(LoginRequiredMixin,UpdateView):
#     model=Krepselis
#     fields = ['prekamas_kiekis']
#     template_name = 'kreps_upd.html'
#     pk_url_kwarg = 'id'
#
#     def get_queryset(self):
#         return Krepselis.objects.get(vartotojo_id=self.request.user).reikia
#
#
#     # def form_valid(self, form):
#     #     form.instance.krepselio_id = self.request.user.krepselis.id
#     #     return super().form_valid(form)

