from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver

from django.utils.translation import gettext as _

class Pardavejas(models.Model):
    priklauso=models.OneToOneField(User,on_delete=models.SET_NULL,null=True)
    pavad=models.CharField(_('Pardavejas'),max_length=30,null=True)

    @property
    def prekiu_skaicius(self):
        a=Preke.objects.filter(pardavejas_id=self.id)
        b=0
        for x in a:
            b+=1
        return b

    def __str__(self):
        return f"Pardavejas: {self.pavad} // Parduodamos prekes: {self.prekiu_skaicius} // {self.priklauso}"

class Preke(models.Model):
    pavadinimas=models.CharField(_('Pavadinimas'),max_length=30)
    aprasymas=models.TextField(_('Aprasymas'),max_length=600,null=True,blank=True)
    nuotrauka=models.ImageField(_('Nuotrauka'),default="default.png",upload_to='prekes_nuotraukos')
    pardavejas_id=models.ForeignKey(Pardavejas,on_delete=models.CASCADE,null=True)
    kaina=models.FloatField(_('Vieneto kaina'),default=0)

    @property
    def atsil_sk(self):
        at=Atsiliepimai.objects.filter(prekes_id=self.id)
        sk=0
        for s in at:
            sk+=1
        return sk

    @property
    def gauti(self):
        a=Sandelys.objects.filter(prekes_id=self.id)
        b=0
        for x in a:
            b=x.liko
        return b

    def __str__(self):
        return f"{self.pavadinimas} vnt.kaina: {self.kaina} // Pardavejas: {self.pardavejas_id.pavad} //liko: {self.gauti}"


class Sandelys(models.Model):
    prekes_id=models.OneToOneField(Preke,on_delete=models.CASCADE,null=True, verbose_name=_('Preke'))
    pridetas_kiekis=models.IntegerField(_('Prideti'),null=True)

    @property
    def liko(self):
        nupirkta=Uzsakymas.objects.filter(sandelio_id=self.id)
        yra = self.pridetas_kiekis
        for x in nupirkta:
            yra-= x.perkamas_kiekis
        return yra


    def __str__(self):
        return f"{self.prekes_id} // prideta: {self.pridetas_kiekis} // liko: {self.liko}//"


class Uzsakymas(models.Model):
    sandelio_id=models.ForeignKey(Sandelys,on_delete=models.SET_NULL,null=True)
    perkamas_kiekis=models.IntegerField(_('Perkamas kiekis'),null=True)
    krepselio_id=models.ForeignKey('Krepselis',on_delete=models.SET_NULL,null=True,)

    @property
    def vartotojas(self):
        vart=Krepselis.objects.filter(uzsakymas=self.id)
        for x in vart:
            vartot=x.vartotojo_id
        return vartot

    @property
    def uzsakymo_kaina(self):
        uzsakymo= Sandelys.objects.filter(uzsakymas=self.id)
        suma=0
        for x in uzsakymo:
            suma = self.perkamas_kiekis * x.prekes_id.kaina
        return suma

    def __str__(self):
        return f"{self.sandelio_id} perkama: {self.perkamas_kiekis} kaina: {self.uzsakymo_kaina} // uzsakovas: {self.vartotojas} "


class Krepselis(models.Model):
    vartotojo_id=models.OneToOneField(User,on_delete=models.SET_NULL,null=True)


    @receiver(post_save,sender=User)
    def prideti(sender,instance,created,**kwargs):
        if created:
            Krepselis.objects.create(vartotojo_id=instance)

    @property
    def reikia(self):
        return Uzsakymas.objects.filter(krepselio_id=self.id)


    @property
    def bendra_suma(self):
        uzsakymai = Uzsakymas.objects.filter(krepselio_id=self.id)
        total = 0
        for line in uzsakymai:
            total += line.uzsakymo_kaina
        return total

    def __str__(self):
        return f"{self.vartotojo_id} krepselis / bendra suma: {self.bendra_suma}"


class Profilis(models.Model):
    vartotojas= models.OneToOneField(User,on_delete=models.SET_NULL,null=True)
    nuotrauka=models.ImageField(default="default.png",upload_to="profilio_nuotraukos")
    adresas = models.CharField(_('Adresas'),max_length=150,null=True, blank=True)
    telefono_numeris = models.IntegerField(_('Telefono numeris'), null=True, blank=True)

    @receiver(post_save, sender=User)
    def prideti(sender, instance, created, **kwargs):
        if created:
            Profilis.objects.create(vartotojas=instance)

    def __str__(self):
        return f"{self.vartotojas.username} profilis"


class Atsiliepimai(models.Model):
    prekes_id=models.ForeignKey(Preke,on_delete=models.SET_NULL,null=True,blank=True)
    vartotojas=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    sukurta=models.DateTimeField(auto_now=True)
    atsiliepimas=models.TextField('',max_length=1234)


    @property
    def nuotrauka(self):
        ntr=self.vartotojas.profilis.nuotrauka
        return ntr

    def __str__(self):
        return f"Kas parase: {self.vartotojas}/Kada: {self.sukurta}/Atsiliepimas: {self.atsiliepimas} // preke: {self.prekes_id}"
