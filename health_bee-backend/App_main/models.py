from django.core.validators import RegexValidator
from django.db import models

from App_auth.models import CustomUser


class PatientProfile(models.Model):
    GENDER_OPTION = (
        ('M', 'M'),
        ('F', 'F'),
        ('O', 'O'),
    )
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_query_name="patient")
    full_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=GENDER_OPTION)
    dob = models.DateField()
    email = models.EmailField(blank=True)
    phone_regex = RegexValidator(
        regex=r'^\+?880\d{10}$',
        message="Phone number must be entered in the format: '+880xxxxxxxxxx'."
    )
    phone_number = models.CharField(validators=[phone_regex], blank=True, max_length=15)

    def __str__(self):
        return self.full_name


class ServiceModel(models.Model):
    test_name = models.CharField(max_length=100)
    price = models.FloatField(default=0)

    def __str__(self):
        return self.test_name
    
class ServiceCartModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_query_name="service_cart_user")
    services = models.ManyToManyField(ServiceModel, related_name="added_services")
    created_at = models.DateTimeField(auto_now_add=True)
    bought_status = models.BooleanField(default=False)

class Appointment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    collection_address = models.CharField(max_length=255)
    service = models.ForeignKey(ServiceCartModel, on_delete=models.DO_NOTHING, related_query_name="service_details")
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=(
        ('Requested', 'Requested'), ('Confirmed', 'Confirmed'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled'), ('Missed', 'Missed')))

    def __str__(self):
        return f"{self.user.patientprofile} - {self.status} - {self.date} {self.time}"


class MedicalSample(models.Model):
    SAMPLE_TYPES = (
        ('blood', 'Blood'),
        ('urine', 'Urine'),
        ('saliva', 'Saliva'),
        ('stool', 'Stool'),
        ('tissue', 'Tissue'),
        ('swabs', 'Swabs'),
        ('csf', 'Cerebrospinal fluid (CSF)'),
        ('tumor_markers', 'Tumor markers')
    )
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_query_name="patient_profile")
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_query_name="appointment_details")
    sample_type = models.CharField(max_length=50, choices=SAMPLE_TYPES)
    collection_date = models.DateField()
    collection_time = models.TimeField()
    is_sent_to_lab = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.patient.full_name} - {self.sample_type}"


class TestResult(models.Model):
    medical_sample = models.OneToOneField(MedicalSample, on_delete=models.CASCADE)
    resultDocument = models.FileField(upload_to="test_result_documents/")
    result = models.TextField()
    date_processed = models.DateField(auto_now_add=True)
    seen = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.medical_sample.patient.full_name} - {self.medical_sample.sample_type}"