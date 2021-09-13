# Create your views here.
import asyncio
from datetime import timedelta, datetime

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView
from .models import Device, DeviceDetail


class Index(ListView):
    template_name = 'mainapp/index.html'
    model = Device

    def get_context_data(self, **kwargs):
        devices = Device.objects.all()
        for device in devices:
            if device.check_online_expires():
                device.online = False
                device.save()
        context = super().get_context_data(**kwargs)
        context['title'] = 'Index'
        return context

    @staticmethod
    def check_online(request):
        devices = [{'pk': el.pk,
                    'host': el.ip_address,
                    'username': el.login,
                    'password': el.password}
                   for el in Device.objects.all()]
        result = asyncio.run(Device.send_command_to_devices(devices))
        for device in result:
            if device:
                modified_device = get_object_or_404(Device, pk=device)
                modified_device.online = True
                modified_device.online_expires = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
                modified_device.save()
        unconnected_devices = Device.objects.all()
        for device in unconnected_devices:
            if device.pk not in result:
                device.online = False
                device.online_expires = datetime.now()
                device.save()
        formObj = {'devices': result}
        return JsonResponse(formObj)
        pass


class DeviceCreateView(CreateView):
    model = Device
    template_name = 'mainapp/device_update.html'
    success_url = reverse_lazy('index')
    fields = 'name', 'ip_address', 'login', 'password', 'hub'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Устройство/создание'
        return context


class GetDeviceInfoView(TemplateView):
    template_name = 'mainapp/device_info.html'

    def get_context_data(self, **kwargs):
        device = Device.objects.filter(pk=self.kwargs['pk']).first()
        context = super().get_context_data(**kwargs)
        context['device'] = device
        context['title'] = f"{device.name}/info"
        device_detail = DeviceDetail(device)
        context['dmvpn'] = device_detail.get_dmvpn_data()
        return context
