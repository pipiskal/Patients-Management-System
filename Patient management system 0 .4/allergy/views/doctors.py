from django.shortcuts import render, redirect
from django.http import HttpResponse
from allergy.models import Patient, FoodTests, SptTests, Spt_tests_done_by_patients, Food_tests_done_by_patients
from allergy.forms import PatientForm, UpdatePatientForm, DoctorSignUpForm, UpdateFoodTestsDone
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth import login , logout ,authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from datetime import date
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from allergy.my_decorators import is_doctor, doctor_required
from django.contrib.auth.decorators import user_passes_test


@login_required
def add_patient(request):
    if request.method == "POST":
        myPatientForm = PatientForm(request.POST)
        print(type(myPatientForm))
        if myPatientForm.is_valid():
            try:
                # i am getting the instance of my model Patient so i can add the current user to it
                # commit = false return the object of the model without saving it into the database
                fs = myPatientForm.save(commit = False)
                print(type(fs))
                fs.user = request.user
                # now i am saving the model into the database
                fs.save()

                # myPatientForm.save()
                # the redirect link is dynamic cause of the name of the url in urls.py of our app
                return redirect('list_of_patients') 
            except:
                print("it failed to add the patient")
        else:
            print(myPatientForm.errors)
    else:
        form = PatientForm()
        print("the add_patient view is called")
        text = "Καταχώρηση Ασθενή"
        context = {"form" : form, "text" : text}
        return render(request, "create_patient_form.html", context)

def update_patient(request, patient_id): 
    if request.method == "GET":
        patient = Patient.objects.get(patient_id = patient_id)
        food_tests_done_by_patient = Food_tests_done_by_patients.objects.filter(patient = patient)
        spt_tests_done_by_patient = Spt_tests_done_by_patients.objects.filter(patient = patient)
        tests_done_by_patient = list(food_tests_done_by_patient) + list(spt_tests_done_by_patient)
        print(type(tests_done_by_patient))
        form = UpdatePatientForm(instance = patient)
        testform = UpdateFoodTestsDone(instance = patient)
        text = " Update Patient"
        context = {
                    "form" : form,
                    "text" : text,
                    "testform" : testform,
                    "tests_done_by_patient" : tests_done_by_patient, 
                    }
        

        return render(request, "update_patient_form.html", context)
        
    elif request.method == "POST":
        patient = Patient.objects.get(patient_id = patient_id)
        form = UpdatePatientForm(request.POST, instance = patient)
        if form.is_valid():
            form.save()
            return redirect(f"/details/{patient_id}") 
        
def delete_patient(request, patient_id):  
    patient = Patient.objects.get(patient_id = patient_id)  
    patient.delete()  
    return redirect('list_of_patients') 

def patient_details(request, patient_id):

    patient = Patient.objects.get(patient_id = patient_id)
    
    # i will need to query the database to get all the tests done till now for
            # the specific patient and to serve it into the template

    # converting the query set into a list to be able to work wiht that
    all_the_food_tests_done = list(Food_tests_done_by_patients.objects.filter(patient = patient))
    all_the_spt_tests_done = list(Spt_tests_done_by_patients.objects.filter(patient = patient))
    
    
    # i want to bring all the tests done from this patient
    # and then filter all the allergy_grades from all the tests
    # and save into a list all the tests that are done with an allergy grade > 0
    # then serve this list into the template

    have_allergy_spt_tests = []
    have_allergy_food_tests = []
    for test in all_the_food_tests_done:
        if test.allergy_grade > 0:
            have_allergy_food_tests.append(test)
        else:
            pass
            
    for test in all_the_spt_tests_done:
        if test.allergy_grade > 0:
            have_allergy_spt_tests.append(test)
        else:
           pass

    
    have_allergy_tests = have_allergy_food_tests + have_allergy_spt_tests
    all_tests_done = all_the_food_tests_done + all_the_spt_tests_done
            
    template = "patient_details.html"
    context = {
        "patient" : patient,
        "have_allergy_tests" : have_allergy_tests,
        "all_tests_done" : all_tests_done,  
        }
    return render(request, template, context)

@login_required
@doctor_required
def show_listofpatients(request):
        
    if request.method == "GET": 
        if request.GET.get("searched_for_first_name"):
            searched_value = request.GET.get("searched_for_first_name")
            print(searched_value)
            patient_list = Patient.objects.filter(first_name__icontains = searched_value, user__exact = request.user)
            context = {"patient_list" : patient_list}
            return render(request, "patient_list.html", context)

        elif request.GET.get("searched_for_last_name"):
            searched_value = request.GET.get("searched_for_last_name")
            print(searched_value)
            patient_list = Patient.objects.filter(last_name__icontains = searched_value, user__exact = request.user)
            context = {"patient_list" : patient_list}
            return render(request, "patient_list.html", context)

        elif request.GET.get("searched_for_phone_number"):
            searched_value = request.GET.get("searched_for_phone_number")
            print(searched_value)
            patient_list = Patient.objects.filter(phone_number__icontains = searched_value, user__exact = request.user)
            context = {"patient_list" : patient_list}
            return render(request, "patient_list.html", context)

        else:
            patient_list = Patient.objects.filter(user = request.user)
            context = {"patient_list" : patient_list}
            return render(request, "patient_list.html", context)
        

def register(request):
    # if the user asks to register i will display an empy registration form
    if request.method == "GET":
        register_form = DoctorSignUpForm()
        # print(register_form)
        template_name = "register.html"
        context = {"form" : register_form}
        return render(request, template_name, context)
    # if the user submits data to create an account we need to work on a post request
    if request.method == "POST":
        # create a form with the info that user provided
        register_form = DoctorSignUpForm(request.POST)
        print(register_form)
        # if the data provided is ok
        if register_form.is_valid():
            # we need to create a new user by using this data
            # if we were user The UserCreation form a form.save() would be enough
            # but now since we are using our own created form we need to manually create the user

            username = register_form.cleaned_data.get("username")
            password = register_form.cleaned_data.get("password1")
            email = register_form.cleaned_data.get("email")
            
            print(f"Username : {username}, Password : {password}, Email : {email}")

            # the get_user_model() refers to the User model and with objects.create_user it creates a new user
            # and saves it into the database
            # The most direct way to create users is to use the included create_user() helper function:

            testuser = register_form.save()
            print(testuser)
            
        return redirect('login')

def login_page(request):

    if request.method == "POST":
        print(request.POST)
        username1 = request.POST.get("username")
        password1 = request.POST.get("password")
        print(username1)
        print(password1)
        # the authenticate method needs the request and checks if the username and password provided belongs to someone
        # if yes redirects to the list of patients with the user
        user = authenticate(request, username = username1, password = password1)
        print (user)
        if user is not None:
            login(request, user)
            return redirect("list_of_patients")
        else:
            messages.info(request, "username or password is incorrect")
    
    context = {}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    return redirect('login')


def create_new_test(request, pid):
    
    # getting all the foodtests
    foodtests = FoodTests.objects.all()
    # getting all the spttests
    spttests = SptTests.objects.all()
    #getting the patient that the test is going to be created for
    #i use pid from the url to pass patients private key
    patient = Patient.objects.get(patient_id = pid)

    
    if request.method == "POST":
        # if the "get_tests" submit button is clicked only this post function will run
        if "get_tests" in request.POST:
            # at the beggining no tests will be selected
            selected_food_tests = []

            # since there is nothing inside that list, the if statement will always be true
            if len(selected_food_tests) == 0 :
                # i will take the test id that was selected for each checkbox and save them in a list 
                # this information is included in the Post request
                # maybe i should clean the data its always better to work with cleaned data
                
                #getting the ids as a list of strings
                selected_food_tests_id = request.POST.getlist('food_tests_id')
                selected_spt_tests_id = request.POST.getlist('spt_tests_id')

                # i am also getting the names of the selected tests so i can diplay it on the table
                selected_food_test_names = []
                selected_spt_test_names = []
                food_tests_done_ids = []
                spt_tests_done_ids = []
                
                # Since i have the id of the tests that was selected by the user, i can querry the database
                # and add it in the database as a new relation, as the food_test and spt_test done by patient 
                for selected_food_test_id in selected_food_tests_id:
                    foodtest = FoodTests.objects.get(id = int(selected_food_test_id))
                    # filling the list with the names of the food_tests
                    selected_food_test_names.append(foodtest.food_test_name)
                                       
                    # creating and saving the new food_test_done by patient
                    new_food_test_done = Food_tests_done_by_patients( patient = patient, foodtest = foodtest, date_created = date.today(), allergy_grade = 0  )
                    new_food_test_done.save()
                    food_tests_done_ids.append(new_food_test_done.food_tests_done_id)

            
                for selected_spt_test_id in selected_spt_tests_id:
                    spttest = SptTests.objects.get(id = int(selected_spt_test_id))
                    # filling the list with the names of the spt_tests
                    selected_spt_test_names.append(spttest.spt_test_name) 
                                      
                    # creating and saving the new food_test_done by patient
                    new_spt_test_done = Spt_tests_done_by_patients( patient = patient, spttest = spttest, date_created = date.today(), allergy_grade = 0  )
                    new_spt_test_done.save()
                    spt_tests_done_ids.append(new_spt_test_done.spt_tests_done_id)
                
                

                # selected_food_test_names and selected_spt_names are ok they contain the names as a list of strings  
                selected_test_names = selected_food_test_names + selected_spt_test_names

                

                context = {
                    "patient" : patient, 
                    "foodtests" : foodtests,
                    "spttests" : spttests,
                    "selected_test_names" : selected_test_names,
                    "food_tests_done_ids" : food_tests_done_ids,
                    "spt_tests_done_ids" : spt_tests_done_ids
                    }
        
        template = "create_new_test.html" 

        # this post will run if the submit inside the table is clicked so we can save 
        # the values that the doctor wanted to change

        if "get_percentages" in request.POST:

            # percentage is a list of the values (allergy grades) that the user provides
            percentages = request.POST.getlist("percentage")
          

            food_tests_done_ids = request.POST.getlist("food_tests_done_ids")
            spt_tests_done_ids = request.POST.getlist("spt_tests_done_ids")

            # i  am only doing this just to update the allergy_grade value
            # from the html file we seperated the ids of the food and spt tests
            # because if we get 1 list full of ids we could not know when the food tests stop
            # and the spt tests start. So we seperated into 2 lists and we can normally run the querries
        
            
            # for each test_id in the food tests that the user selected
            # we will find the correct test_done using the id and then upgrade the allergy_grade value

            # since i know the length of both the food and spt tests the user selected
            # i am using the length of the food tests selected to seperate the percentages lists
            # so i will be able to save the correct tests with the allergy grade the user provided


            food_percentages = percentages[0 : len(food_tests_done_ids)]
            spt_percentages = percentages[len(food_tests_done_ids) :]
            i,j = 0, 0
            for food_tests_done_id in food_tests_done_ids:
                foodtestdone = Food_tests_done_by_patients.objects.get(food_tests_done_id = int(food_tests_done_id))
                foodtestdone.allergy_grade = float(food_percentages[i])
                foodtestdone.save()
                i+=1
                

            # same here but for spt tests
            
            for spt_tests_done_id in spt_tests_done_ids:
                spttestdone = Spt_tests_done_by_patients.objects.get(spt_tests_done_id = int(spt_tests_done_id))
                spttestdone.allergy_grade = float(spt_percentages[j])
                spttestdone.save()
                j+=1
                
    

            # i will need to query the database to get all the tests done till now for
            # the specific patient and to serve it into the template

            all_the_food_tests_done = list(Food_tests_done_by_patients.objects.filter(patient = patient))
            all_the_spt_tests_done = list(Spt_tests_done_by_patients.objects.filter(patient = patient))
            all_tests_done = all_the_food_tests_done + all_the_spt_tests_done

        
            # i want to bring all the tests done from this patient
            # and then filter all the allergy_grades from all the tests
            # and save into a list all the tests that are done with an allergy grade > 0
            # then serve this list into the template
            # it will be used from patient details page to show the tests that are done 
            # and also the tests that the patiens has allergy 

            have_allergy_spt_tests = []
            have_allergy_food_tests = []
            for foodtest in all_the_food_tests_done:
                if foodtest.allergy_grade > 0:
                    have_allergy_food_tests.append(foodtest)
                else:
                    pass

            for spttest in all_the_spt_tests_done:
                if spttest.allergy_grade > 0:
                    have_allergy_spt_tests.append(spttest)
                else:
                    pass

            
            have_allergy_tests = have_allergy_food_tests + have_allergy_spt_tests
            

            context = {
                "all_tests_done" : all_tests_done,
                "patient" : patient,
                "food_tests" : foodtests,
                "all_the_food_tests_done" : all_the_food_tests_done,
                "have_allergy_tests" : have_allergy_tests
                }
            template  = "patient_details.html"


        return render(request, template, context)
    else:
        # if its a get request load the page with the correct items 
        # like the patient details that was clicked and load the list of the tests will all the items
        

        template = "create_new_test.html"
        
        context = {
            "patient" : patient, 
            "foodtests" : foodtests,
            "spttests" : spttests  
            }
        return render(request, template, context)



# i am having the same code 2 times cause i want to update and delete
# food and spt tests
# its the exact same code so that means is a bad practice and prbably the code
# could be written as 1 function


def update_food_test(request, test_id):
    if request.method == "GET":
        test = Food_tests_done_by_patients.objects.get(food_tests_done_id = test_id)
        context = { "test" : test}
        template = "update_test.html"
        return render(request, template, context)
        
    elif request.method == "POST":
        print(request.POST)
        # i will get the data from the form 
        # i will have to validate them
        # to clean them 
        # and then update the test record
        food_test = Food_tests_done_by_patients.objects.get(food_tests_done_id = test_id)
        patient_done_the_food_test = food_test.patient
        pid= patient_done_the_food_test.patient_id

        updated_value_fo_allergy_grade = float(request.POST.get("update_allergy_grade"))
        test = Food_tests_done_by_patients.objects.get(food_tests_done_id = test_id)
        test.allergy_grade = updated_value_fo_allergy_grade
        test.save()
        return redirect('update_patient', patient_id = pid)
    
def update_spt_test(request, test_id):
    if request.method == "GET":
        test = Spt_tests_done_by_patients.objects.get(spt_tests_done_id = test_id)
        context = { "test" : test}
        template = "update_test.html"
        return render(request, template, context)
        
    elif request.method == "POST":
        print(request.POST)
        # i will get the data from the form 
        # i will have to validate them
        # to clean them 
        # and then update the test record
        spt_test = Spt_tests_done_by_patients.objects.get(spt_tests_done_id = test_id)
        patient_done_the_spt_test = spt_test.patient
        pid= patient_done_the_spt_test.patient_id

        updated_value_fo_allergy_grade = float(request.POST.get("update_allergy_grade"))
        test = Spt_tests_done_by_patients.objects.get(spt_tests_done_id = test_id)
        test.allergy_grade = updated_value_fo_allergy_grade
        test.save()
        return redirect('update_patient', patient_id = pid)

def delete_food_test(request, test_id):
    
    foodtest = Food_tests_done_by_patients.objects.get(food_tests_done_id = test_id)  
    patient_done_the_food_test = foodtest.patient
    pid = patient_done_the_food_test.patient_id
    foodtest.delete()  
    return redirect('update_patient', patient_id = pid)


def delete_spt_test(request,test_id):
    spttest = Spt_tests_done_by_patients.objects.get(spt_tests_done_id = test_id)
    patient_done_the_spt_test = spttest.patient
    pid = patient_done_the_spt_test.patient_id
    spttest.delete() 
    return redirect('update_patient', patient_id = pid)  

def print_test(request, patient_id):
    if request.method == "GET":
        patient = Patient.objects.get(patient_id = patient_id)

        all_the_food_tests_done = list(Food_tests_done_by_patients.objects.filter(patient = patient))
        all_the_spt_tests_done = list(Spt_tests_done_by_patients.objects.filter(patient = patient))
        
        # having the same code again
        # maybe i should create a method in models to get all the tests with allergy grade > 0 at once

        have_allergy_spt_tests = []
        have_allergy_food_tests = []
        for test in all_the_food_tests_done:
            if test.allergy_grade > 0:
                have_allergy_food_tests.append(test)
            else:
                pass

        for test in all_the_spt_tests_done:
            if test.allergy_grade > 0:
                have_allergy_spt_tests.append(test)
            else:
                pass
        have_allergy_tests = have_allergy_food_tests + have_allergy_spt_tests
        all_tests_done = all_the_food_tests_done + all_the_spt_tests_done

        template = "print.html"
        context = {
            "patient" : patient,
            "all_tests_done" : all_tests_done,
            "have_allergy_tests" : have_allergy_tests
        }
        return render(request, template , context)