from django.db import models
from django.db.models.deletion import DO_NOTHING
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Patient(models.Model):
    # we should not import directly the User Model from  auth
    # but its better to always refer to that 
    user = models.ForeignKey(User, null=True, on_delete = models.CASCADE)
    patient_id = models.AutoField(primary_key=True)
    first_name = models.CharField("persons first name",max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=12)
    amka =models.CharField(max_length=12)
    address = models.CharField(max_length=30)
    email = models.EmailField(null=True)
    diagnose = models.TextField(null=True)
    atomic_history = models.TextField(null=True)
    medication = models.TextField(null=True)
    objective_examination = models.TextField(null=True)
    treatment = models.TextField(null=True)




    def __str__(self):
        full_name = self.first_name + " " + self.last_name
        return full_name


class FoodTests(models.Model):
    food_test_name = models.CharField(max_length=30)
    patient_tests = models.ManyToManyField(Patient, through="Food_tests_done_by_patients")
    allergy_grade = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.food_test_name


class SptTests(models.Model):
    
    spt_test_name = models.CharField(max_length=30)
    patient_tests = models.ManyToManyField(Patient, through="Spt_tests_done_by_patients")
    allergy_grade = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.spt_test_name


class Food_tests_done_by_patients(models.Model):
    food_tests_done_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    foodtest = models.ForeignKey(FoodTests, on_delete=models.CASCADE)
    date_created = models.DateField()
    allergy_grade = models.FloatField()


    def __str__(self):
        title = f"patient with name {self.patient}, id: {self.patient.patient_id}, food test name: {self.foodtest} and allergy grade {self.allergy_grade}"
        return title

class Spt_tests_done_by_patients(models.Model):
    spt_tests_done_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    spttest = models.ForeignKey(SptTests, on_delete=models.CASCADE)
    allergy_grade = models.FloatField()
    date_created = models.DateField()
    
    def __str__(self):
        title = f"patient with name {self.patient} , id: {self.patient.patient_id}, spt test name: {self.spttest} and allergy grade : {self.allergy_grade}" 
        return title





