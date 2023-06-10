from django.contrib import admin
from App_main.models import *

# Register your models here.
admin.site.register(PatientProfile)
admin.site.register(Appointment)
admin.site.register(MedicalSample)
admin.site.register(TestResult)
admin.site.register(ServiceModel)
admin.site.register(ServiceCartModel)
