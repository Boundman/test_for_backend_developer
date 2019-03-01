from django import forms


class UploadImageForm(forms.Form):
    device_image = forms.FileField(label='Загрузить с устройства', required=False)
    url_image = forms.CharField(label='Загрузить при помощи url', required=False)

    def __init__(self, *args, **kwargs):
        super(UploadImageForm, self).__init__(*args, **kwargs)
        self.fields['device_image'].widget.attrs.update({'id': 'upload-image-device'})
        self.fields['url_image'].widget.attrs.update({'id': 'upload-image-url'})
