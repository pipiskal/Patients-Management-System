from django.urls import path
from .views import doctors, startingpage


urlpatterns = [
    path('', startingpage.main_page, name= 'home'),
    path("update/<int:patient_id>", doctors.update_patient, name = "update_patient"),
    path('delete/<int:patient_id>', doctors.delete_patient, name = "delete_patient"),
    path('add/', doctors.add_patient, name = 'add_patient'),
    path('patientslist/',doctors.show_listofpatients, name = 'list_of_patients'),
    path('register/', doctors.register, name = 'register'),
    path('login', doctors.login_page, name = 'login' ),
    path('logout', doctors.logout_user, name="logout"),
    path('details/<int:patient_id>',doctors.patient_details, name="patient_details" ),
    path('create_new_test/<int:pid>', doctors.create_new_test, name= "create_new_test"),
    path('print_test/<int:patient_id>', doctors.print_test, name = "print test"),
    path('delete_food_test/<int:test_id>',doctors.delete_food_test, name = "delete_food_test"),
    path('delete_spt_test/<int:test_id>',doctors.delete_spt_test, name = "delete_spt_test"),
    path('update_food_test/<int:test_id>', doctors.update_food_test, name= "update_food_test"),
    path('update_spt_test/<int:test_id>', doctors.update_spt_test, name= "update_spt_test"),
    
    
]