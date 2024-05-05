from django.core.exceptions import ValidationError
import os

def allow_only_images_validator(value):
    extension=os.path.splitext(value.name)[1] # this will give extension name lets suppose cover-image.jgp (0 index will name and 1 index the extension)
    print(extension)
    valid_extensions=['.jpg', '.png', '.jpeg']
    if not extension.lower() in valid_extensions:
        # raise ValidationError('unsupported file extension! only these are accepted '+str(valid_extensions))
        raise ValidationError('unsupported file extension! only ".jpg .png .jpeg" are accepted ')