from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView

from App_main.models import *
from App_main.serializers import *
from django.db.models import Sum
from django.shortcuts import get_object_or_404


class UserHomeData(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        profile_exists_or_not = PatientProfile.objects.filter(user=user).exists()

        appointments_running = Appointment.objects.filter(user=user, status="Scheduled").count()
        appointments_completed = Appointment.objects.filter(user=user, status="Completed").count()

        total_tests = Appointment.objects.filter(user=user, status='Completed').aggregate(Sum('service__services'))
        total_tests_count = total_tests['service__services__sum'] or 0

        return Response({"profile": f"{profile_exists_or_not}", "appointment_running": appointments_running, 'appointment_completed': appointments_completed, 'total_complted': appointments_completed, 'total_tests': f"{total_tests_count}"})


class PatientProfileViewSet(viewsets.ModelViewSet):
    queryset = PatientProfile.objects.all()
    serializer_class = PatientProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        patient_profile = serializer.save()
        return Response({"status": "Successfully Created"}, status=201)

    def retrieve(self, request, pk, **kwargs):
        patient_profile = PatientProfile.objects.get(pk=pk)
        serializer = self.serializer_class(patient_profile)
        return Response(serializer.data)

    def update(self, request, pk, **kwargs):
        patient_profile = PatientProfile.objects.get(pk=pk)
        serializer = self.serializer_class(patient_profile, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        patient_profile = serializer.save()
        return Response({"status": "Successfully Updated!"})

    def destroy(self, request, pk, **kwargs):
        patient_profile = PatientProfile.objects.get(pk=pk)
        patient_profile.delete()
        return Response(status=204)

    def patch(self, request, pk, **kwargs):
        patient_profile = PatientProfile.objects.get(pk=pk)
        serializer = self.serializer_class(patient_profile, data=request.data, partial=True,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        patient_profile = serializer.save()
        return Response({"status": "Successfully Updated!"})


class ServiceModelListCreateView(generics.ListCreateAPIView):
    queryset = ServiceModel.objects.all()
    serializer_class = ServiceModelSerializer


class ServiceModelRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServiceModel.objects.all()
    serializer_class = ServiceModelSerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        service_ids = request.data.get('services', [])  # Extract service IDs from request data
        collection_address = request.data.get('collection_address')
        date = request.data.get('date')
        time = request.data.get('time')

        service_cart_data = {"services": service_ids, "user": request.user.id}  # ServiceCartModel data
        service_cart_serializer = ServiceCartModelSerializer(data=service_cart_data)
        service_cart_serializer.is_valid(raise_exception=True)
        service_cart = service_cart_serializer.save()

        serializer.validated_data['service'] = service_cart
        serializer.validated_data['collection_address'] = collection_address
        serializer.validated_data['date'] = date
        serializer.validated_data['time'] = time

        appointment = serializer.save()

        return Response({"status": "Successfully Created"}, status=status.HTTP_201_CREATED)


    def retrieve(self, request, pk, **kwargs):
        appointment = Appointment.objects.get(pk=pk)
        serializer = self.serializer_class(appointment)
        return Response(serializer.data)

    def update(self, request, pk, **kwargs):
        appointment = Appointment.objects.get(pk=pk)
        serializer = self.serializer_class(appointment, data=request.data)
        serializer.is_valid(raise_exception=True)
        appointment = serializer.save()
        return Response(appointment.data)

    def destroy(self, request, pk, **kwargs):
        appointment = Appointment.objects.get(pk=pk)
        appointment.delete()
        return Response(status=204)


class MedicalSampleViewSet(viewsets.ModelViewSet):
    queryset = MedicalSample.objects.all()
    serializer_class = MedicalSampleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        medical_sample = serializer.save()
        return Response({"status": "Successfully Created"}, status=201)

    def retrieve(self, request, pk, **kwargs):
        medical_sample = MedicalSample.objects.get(pk=pk)
        serializer = self.serializer_class(medical_sample)
        return Response(serializer.data)

    def update(self, request, pk, **kwargs):
        medical_sample = MedicalSample.objects.get(pk=pk)
        serializer = self.serializer_class(medical_sample, data=request.data)
        serializer.is_valid(raise_exception=True)
        medical_sample = serializer.save()
        return Response(medical_sample.data)

    def destroy(self, request, pk, **kwargs):
        medical_sample = MedicalSample.objects.get(pk=pk)
        medical_sample.delete()
        return Response(status=204)


class TestResultViewSet(viewsets.ModelViewSet):
    queryset = TestResult.objects.all()
    serializer_class = TestResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        test_result = serializer.save()
        return Response({"status": "Successfully Created"}, status=201)

    def retrieve(self, request, pk, **kwargs):
        test_result = TestResult.objects.get(pk=pk)
        serializer = self.serializer_class(test_result)
        return Response(serializer.data)