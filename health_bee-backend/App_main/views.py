from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
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
        appointments_requests = Appointment.objects.filter(user=user, status="Requested").count()
        appointments_running = Appointment.objects.filter(user=user, status="Confirmed").count()
        appointments_completed = Appointment.objects.filter(user=user, status="Completed").count()
        appointments_missed = Appointment.objects.filter(user=user, status="Missed").count()
        passed_appointments = appointments_completed + appointments_missed
        results = TestResult.objects.filter(medical_sample__appointment__user=user).count()

        

        return Response({"profile": f"{profile_exists_or_not}", 
                         "appointment_running": appointments_running, 
                         'appointment_completed': passed_appointments, 
                         "appointments_requests": appointments_requests,
                         'results': results})
        



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
    

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def services(request, pk):
    try:
        service_cart = ServiceCartModel.objects.get(pk=pk)
        services = service_cart.services.all()
        service_data = [{"test_name": service.test_name, "price": service.price} for service in services]
        return Response({"services": service_data})
    except ServiceCartModel.DoesNotExist:
        return Response({"error": "Service cart not found."}, status=404)

    
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def appointmentCreateAPIView(request):
    collection_address = request.data['collection_address']
    services = request.data['services']
    date = request.data['date']
    time = request.data['time']
    status = request.data['status']
    print(collection_address, status, date, time, services)
    my_list = eval(services)
    cart = ServiceCartModel.objects.get_or_create(user=request.user, bought_status=False)
    for i in my_list:
        cart[0].services.add(i)
        
    cart[0].bought_status = True

    cart[0].save()
    query = Appointment(
        user = request.user,
        collection_address = collection_address,
        service = cart[0],
        date = date,
        time = time,
        status = status,
    )

    query.save()

    return Response({"status": "Successfully Created"}, status=201)


class ServiceCartModelDetailView(generics.RetrieveAPIView):
    queryset = ServiceCartModel.objects.all()
    serializer_class = ServiceCartModelSerializer
    lookup_field = 'pk'
    
    




class AppointmentViewSet(viewsets.ModelViewSet): # This class is not being used for appointment creation
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        service_ids = request.data.get('services', [])
        collection_address = request.data.get('collection_address')
        date = request.data.get('date')
        time = request.data.get('time')

        service_cart = ServiceCartModel.objects.create(user=request.user)

        for service_id in service_ids:
            service = ServiceModel.objects.get(pk=service_id)
            service_cart.services.add(service)

        service_cart.bought_status = True
        service_cart.save()
        print(service_cart, "eva")
        
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
    
    def get(self, request, format=None):
        user = request.user
        appointments = Appointment.objects.filter(user=user).order_by('date').order_by('time')

        return Response({"appointments": appointments, })


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
        test_result.seen = True
        test_result.save()
        serializer = self.serializer_class(test_result)
        return Response(serializer.data)
