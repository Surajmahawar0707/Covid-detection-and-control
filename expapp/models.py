from django.db import models


class usercreatemodel(models.Model):
    picture = models.ImageField(upload_to='pics/', blank=True, null=True)
    contact = models.IntegerField(default=None)
    email = models.EmailField(default=None)
    username = models.CharField(max_length=20, default=None)
    address = models.CharField(max_length=50, default=None)
    district = models.CharField(max_length=50, default=None)
    state = models.CharField(max_length=50, default=None)
    country = models.CharField(max_length=50, default=None)

    def __str__(self):
        return self.username


class data(models.Model):
    username = models.CharField(max_length=20, default=None)
    symp_choices = [("None", "None"), ("Fever", "Fever"), ("Cough", "Cough"), ("Tiredness", "Tiredness"), ("Aches and pain", "Aches and Pain"), ("Sore Throat", "Sore Throat"), ("Diarrhoea", "Diarrhorea"), ("Loss of taste or smell", "Loss of taste or smell")]
    symptoms = models.CharField(max_length=25, choices=symp_choices, default=None)
    contact_tracing = models.IntegerField(default=0)

    def __str__(self):
        return self.username


class output(models.Model):
    username = models.CharField(max_length=50, default=None)
    symptoms = models.CharField(max_length=20, default=None)
    contact_tracing = models.IntegerField(default=0)
    probability = models.FloatField(default=0.0)
    stage = models.IntegerField(default=0)
    inf_users_in_dis = models.IntegerField(default=0)
    inf_users_in_state = models.IntegerField(default=0)
    inf_users_in_coun = models.IntegerField(default=0)
    
    def __str__(self):
        return self.username