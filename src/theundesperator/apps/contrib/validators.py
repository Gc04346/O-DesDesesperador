from django.core.exceptions import ValidationError


def validate_file_max_size(file: object, max_size_kb: int):
    file_size = file.file.size
    limit_kb = max_size_kb
    if file_size > limit_kb * 1024:
        raise ValidationError("Max size of file is %s KB" % limit_kb)


def validate_image_max_500(image):
    return validate_file_max_size(image, 500)
