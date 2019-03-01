from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views.generic import View
from myapp.forms import UploadImageForm
from myapp.models import ImageModel
from urllib.request import urlretrieve
from django.core.files import File
from PIL import Image
import os
import json


class StartPage(View):
    def get(self, request):
        images = ImageModel.objects.all()
        return render(request, 'start page.html', {'images': images})

    def post(self, request):
        if request.method == "POST":
            data = request.POST.get('data')
            if data == 'to upload page':
                return HttpResponse(
                    json.dumps(''),
                    content_type="application/json"
                )


class UploadImage(View):
    def get(self, request):
        form = UploadImageForm(request.POST or None)
        return render(request, 'upload image.html', {'form': form})

    def post(self, request):
        if request.method == "POST":
            if 'upload-image-btn' in request.POST:
                form = UploadImageForm(request.POST, request.FILES)
                if form.is_valid():
                    form_data = form.cleaned_data
                    img_url = form_data['url_image']
                    img_from_device = form_data['device_image']

                    if img_url and img_from_device:  # Загрузили изображение двумя способами
                        return render(request, 'upload image.html', {'errors': 'Вы должны загрузить изображение ОДНИМ из представленных способов', 'form': form})
                    elif img_url:  # Загрузиил через url
                        img = ImageModel()
                        name = img_url.split('/')[-1]
                        content = urlretrieve(img_url)  # Скачали изображение
                        img.picture.save(name, File(open(content[0], 'rb')), save=True)

                        width, height = Image.open(img.picture).size  # Нашли ширину и высоту
                        img.width = width
                        img.height = height
                        img.size = os.stat(str(img.picture)).st_size  # Записали размер
                        img.save()
                        return HttpResponseRedirect('/')
                    elif img_from_device:  # Загрузили с устройства
                        (width, height) = Image.open(img_from_device).size  # Нашли ширину и высоту изобржения
                        image = ImageModel(picture=img_from_device,
                                           width=width,
                                           height=height)
                        image.save()  # Сначала сохранили изобржение, брать его размер так будет удобнее

                        image.size = os.stat(str(image.picture)).st_size  # Теперь определили размер и сохранили
                        image.save()
                        return HttpResponseRedirect('/')
                    elif not img_url and not img_from_device:  # Изображение не загружено ни одним из способов
                        return render(request, 'upload image.html', {'errors': 'Вы должны загрузить изображение', 'form': form})


class ResizeImage(View):
    def get(self, request, image_id, width, height, size):
        img_object = ImageModel.objects.get(id=image_id)
        return render(request, 'resize image.html', {'image': img_object})

    def post(self, request, image_id, width, height, size):
        if request.method == "POST":
            if 'resize-image-btn' in request.POST:

                image = ImageModel.objects.get(id=image_id)
                try:
                    width = int(request.POST.get('width'))
                    height = int(request.POST.get('height'))
                    size = int(request.POST.get('size'))
                except ValueError:  # Если ввели не числовые значения полей
                    return render(request, 'resize image.html', {'image': image, 'errors': 'Для размеров рекомендуется использовать числовые значения'})

                if width == image.width and height == image.height and size == image.size:  # Ничего не меняли
                    return HttpResponseRedirect('/')

                original_image = Image.open(image.picture)
                resized_image = original_image.resize((width, height))

                # Путь до копии
                path_to_resized = os.path.dirname(str(image.picture)) + '\\resized' + str(image.picture).split('/')[-1]
                resized_image.save(path_to_resized)  # Сохранили копию
                size_resized = os.stat(path_to_resized).st_size  # Нашли её размер

                if size_resized <= size:  # Если указанные размеры корректны и размер ресайзнутого изображения меньше указанного
                    resized_image.save(str(image.picture))  # Сохраняем рейзнутое поверх оригинала
                    os.remove(path_to_resized)  # Копию, которая нужна была для проверки удаляем

                    # Сохраняем новые параметры изображения
                    image.width = width
                    image.height = height
                    image.size = size_resized
                    image.save()
                    return HttpResponseRedirect('/')
                else:  # Если размер больше указанного
                    os.remove(path_to_resized)  # Копию, которая нужна была для проверки удаляем
                    # Выводим сообщение об ошибке
                    return render(request, 'resize image.html', {'image': image, 'errors': 'Размер изображения больше допустимого указанного'})
