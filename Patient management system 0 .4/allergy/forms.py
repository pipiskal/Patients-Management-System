from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db.models.fields import CommaSeparatedIntegerField
from .models import Food_tests_done_by_patients, Patient
# we should not hard impor the user it will cause issues later
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


User = get_user_model()
# the model form creates a form base on the fields of the model that we will provide it
# we can choose what fields will be vissible
class PatientForm(forms.ModelForm):

    required_label = " *"

    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={"class" : "form-inputs"}),
        label_suffix=required_label,
        )
    phone_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class" : "form-inputs"})
        )
    amka = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class" : "form-inputs"})
        )
    address = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class" : "form-inputs"})
        )
    

    class Meta:

        model = Patient

        fields = ['first_name', 'last_name', 'email', 'phone_number','amka', 'address']
        

        labels = {
            "first_name" : "Όνομα ",
            "last_name" : "Επώνυμο",
            "phone_number" : "Αριθμός τηλεφώνου",
            "email" : " Email",
            "amka" : "ΑΜΚΑ",
            "address" : "Διεύθυνση"
        }
        # widgets uses input not fields
        widgets = {
            "first_name" : forms.TextInput(attrs={"class" : "form-inputs"}),
            "last_name" : forms.TextInput(attrs={"class" : "form-inputs"}), 
        }

class UpdatePatientForm(forms.ModelForm):

    class Meta:
        model = Patient
        fields = [
                'first_name', 'last_name', 'phone_number', 'email', 'amka', 'address',
                'diagnose', 'atomic_history', 'medication', 'objective_examination', 'treatment'
                ]
        labels = {
            "first_name" : "Όνομα ",
            "last_name" : "Επώνυμο",
            "phone_number" : "Αριθμός τηλεφώνου",
            "email" : " Email",
            "amka" : "ΑΜΚΑ",
            "address" : "Διεύθυνση",
            "diagnose" : "Διάγνωση",
            "atomic_history" : "Ατομικό Ιστορικό",
            "medication" : "Φαρμακευτική Αγωγή",
            'objective_examination' : "Αντικειμενική Εξέταση",
            "treatment" : "Θεραπεία"
        }

        widgets = {
            "first_name" : forms.TextInput(attrs={"class" : "form-inputs"}),
            "last_name" : forms.TextInput(attrs={"class" : "form-inputs"}),
            "phone_number" : forms.NumberInput(attrs={"class" : "form-inputs"}),
            "email" : forms.EmailInput(attrs={"class" : "form-inputs"}),
            "amka" : forms.NumberInput(attrs={"class" : "form-inputs"}),
            "address" : forms.TextInput(attrs={"class" : "form-inputs"}),
            "diagnose" : forms.Textarea(attrs={"class" : "form-inputs-extra"}),
            "atomic_history" : forms.Textarea(attrs={"class" : "form-inputs-extra"}),
            "medication" : forms.Textarea(attrs={"class" : "form-inputs-extra"}),
            "objective_examination" : forms.Textarea(attrs={"class" : "form-inputs-extra"}),
            "treatment" : forms.Textarea(attrs={"class" : "form-inputs-extra"})

            
        }

class UpdateFoodTestsDone(forms.ModelForm):

    class Meta:
        model = Food_tests_done_by_patients
        fields = [
                "patient", 'date_created','foodtest', "allergy_grade"
            ]


# this class inherits from the UserCreationForm
# so it was all the features from the parent class (need to check more the UserCreationForm)
# THATS THE FORM THAT I USE RIGHT NOW FOR REGISTRATION
class  DoctorSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit = True):
        user = super().save(commit=False)
        user.is_doctor = True
        if commit:
            user.save()
        return user
        

class  PatientSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def save(self):
        user = super().save(commit=False)
        user.is_patient = True
        user.save()
        patient = User.objects.create(user = user)
        return user


# i will craate my own registration form , it will have no validation for password matching
# or hashing the password but i am doing this to undestand how to create my own registration form
class UserRegistrationForm(forms.Form):
    # we add the fields like we did on the models, methods of classes that indicate a html tag
    
    username = forms.CharField() # it can take a lot of parameters like required = False so the field must be filed from the user
    # by default the required field is true no need to add it as i did below
    email = forms.EmailField(required = True, label = "Email Address]") # i can choose how its going to show over the browser
    password1 = forms.CharField(label = "Password",
                                widget = forms.PasswordInput(
                                    attrs= {
                                            "class" : "register-form",
                                            "id" : "user-confirm-password"
                                        }
                                    )
                                )
    password2 = forms.CharField(label = "Confirmation Password",
                                widget = forms.PasswordInput(
                                    attrs= {
                                            "class" : "register-form",
                                            "id" : "user-confirm-password"
                                        }
                                    )
                                )

