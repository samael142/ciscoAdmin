# from django import forms
#
# from mainapp.models import Device
#
#
# class DeviceCategoryEditForm(forms.ModelForm):
#     class Meta:
#         model = Device
#         fields = '__all__'
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field_name, field in self.fields.items():
#             field.widget.attrs['class'] = 'form-control'
#             field.help_text = ''
