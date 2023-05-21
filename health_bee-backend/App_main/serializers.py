from rest_framework import serializers

from App_main.models import *


class PatientProfileSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PatientProfile
        fields = '__all__'


class ServiceModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceModel
        fields = '__all__'


class ServiceCartModelSerializer(serializers.ModelSerializer):
    services = ServiceModelSerializer(many=True)

    class Meta:
        model = ServiceCartModel
        fields = '__all__'


class AppointmentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    service = serializers.PrimaryKeyRelatedField(queryset=ServiceCartModel.objects.all())

    class Meta:
        model = Appointment
        fields = '__all__'



class MedicalSampleSerializer(serializers.ModelSerializer):
    patient = serializers.PrimaryKeyRelatedField(queryset=PatientProfile.objects.all(),
                                                 default=serializers.CurrentUserDefault())
    appointment = serializers.PrimaryKeyRelatedField(queryset=Appointment.objects.all(),
                                                     default=serializers.CurrentUserDefault())

    class Meta:
        model = MedicalSample
        fields = '__all__'


class TestResultSerializer(serializers.ModelSerializer):
    medical_sample = serializers.PrimaryKeyRelatedField(queryset=MedicalSample.objects.all(),
                                                        default=serializers.CurrentUserDefault())

    class Meta:
        model = TestResult
        fields = '__all__'