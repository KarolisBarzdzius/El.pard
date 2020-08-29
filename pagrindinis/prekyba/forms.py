from django import forms

from .models import Uzsakymas,Profilis,Atsiliepimai,Preke,Sandelys,Pardavejas

from django.contrib.auth.models import User


class UzsakymasForm(forms.ModelForm):
    class Meta:
        model=Uzsakymas
        fields = [
            'perkamas_kiekis','sandelio_id','krepselio_id'
        ]
        widgets={'sandelio_id':forms.HiddenInput(),
                 'krepselio_id':forms.HiddenInput(),
        }


class ProfilioForm(forms.ModelForm):
    class Meta:
        model = Profilis
        fields = ['adresas','telefono_numeris','nuotrauka']


class PirkimoProfilioForm(forms.ModelForm):
    adresas=forms.CharField(disabled=True)
    telefono_numeris=forms.IntegerField(disabled=True)
    class Meta:
        model=Profilis
        fields = ['adresas','telefono_numeris']


class UserForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email']


class AtsiliepimuForm(forms.ModelForm):
    class Meta:
        model=Atsiliepimai
        fields=['atsiliepimas','vartotojas','prekes_id']
        widgets = {'vartotojas': forms.HiddenInput(),
                   'prekes_id':forms.HiddenInput(),
                   'atsiliepimas':forms.Textarea(attrs={'rows': 6, 'cols': 100})
                   }


class PrekesIkelimasForm(forms.ModelForm):
    class Meta:
        model=Preke
        fields = ['nuotrauka','pavadinimas','kaina','pardavejas_id','aprasymas',]
        widgets = {'pardavejas_id': forms.HiddenInput()}


class SandelysForm(forms.ModelForm):
    class Meta:
        model=Sandelys
        fields = ['pridetas_kiekis','prekes_id']

    def __init__(self, request, *args, **kwargs):
        super(SandelysForm,self).__init__(*args, **kwargs)
        self.fields['prekes_id'].queryset = Preke.objects.filter(pardavejas_id=request.user.pardavejas.id)


class PardavejoForm(forms.ModelForm):
    class Meta:
        model=Pardavejas
        fields = ['pavad','priklauso']
        widgets = {'priklauso': forms.HiddenInput()}