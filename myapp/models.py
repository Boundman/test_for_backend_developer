from django.db import models


class ImageModel(models.Model):
    width = models.IntegerField(null=True)
    height = models.IntegerField(null=True)
    size = models.IntegerField(null=True)
    picture = models.FileField(null=True, blank=True, upload_to='static/')

    def __unicode__(self):
        dictionary = dict()
        dictionary['width'] = self.width
        dictionary['height'] = self.height
        dictionary['size'] = self.size
        dictionary['picture_name'] = self.picture.name
        return dictionary
