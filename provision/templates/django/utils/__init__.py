# -*- coding: utf-8 -*-
import os

from cStringIO import StringIO

from PIL import Image

from django.core.files.uploadedfile import SimpleUploadedFile


def flat(*nums):
    """
    Build a tuple of ints from float or integer arguments.
    Useful because PIL crop and resize require integer points.
    """
    return tuple(int(round(n)) for n in nums)


class Size(object):

    def __init__(self, pair):
        self.width = float(pair[0])
        self.height = float(pair[1])

    @property
    def aspect_ratio(self):
        return self.width / self.height

    @property
    def size(self):
        return flat(self.width, self.height)


def cropped_thumbnail(img, size):
    """
    Builds a thumbnail by cropping out a maximal region from the center
    of the original with the same aspect ratio as the target size, and
    then resizing. The result is a thumbnail which is always EXACTLY
    the requested size and with no aspect ratio distortion (although two
    edges, either top/bottom or left/right depending whether the image
    is too tall or too wide, may be trimmed off.)
    """

    original = Size(img.size)
    target = Size(size)

    if target.aspect_ratio > original.aspect_ratio:
        # image is too tall: take some off the top and bottom
        scale_factor = target.width / original.width
        crop_size = Size((original.width, target.height / scale_factor))
        top_cut_line = (original.height - crop_size.height) / 2
        img = img.crop(flat(
            0, top_cut_line, crop_size.width, top_cut_line + crop_size.height
        ))

    elif target.aspect_ratio < original.aspect_ratio:
        # image is too wide: take some off the sides
        scale_factor = target.height / original.height
        crop_size = Size((target.width / scale_factor, original.height))
        side_cut_line = (original.width - crop_size.width) / 2
        img = img.crop(flat(
            side_cut_line, 0, side_cut_line + crop_size.width, crop_size.height
        ))

    return img.resize(target.size, Image.ANTIALIAS)


def make_thumbnail(obj, field, thumbnail_field, size):

    # Zip attributes in order to have a list of tupples with the necesary
    # attributes to make the thumbnails [0]= thumnail_field [1]=size
    zipped_attributes = zip(thumbnail_field, size)

    original_image_field = getattr(obj, field)

    for attribute in zipped_attributes:

        thumbnail_image_field = getattr(obj, attribute[0])

        # Thumbnail size in a tuple (width, height).
        cropping_size = tuple(int(v) for v in attribute[1].split('x'))

        # Open original photo.
        picture = Image.open(original_image_field.path)

        # Crop/resize image.
        picture = cropped_thumbnail(picture, cropping_size)

        # Save the thumbnail,
        image_buffer = StringIO()
        try:
            picture.save(image_buffer, 'jpeg')
        except IOError:
            picture = picture.convert('RGB')
            picture.save(image_buffer, 'jpeg')

        image_buffer.seek(0)

        # Saves the image to a SingleUploadedFile which can be
        # saved into an ImageField.

        original_image_name = os.path.split(original_image_field.name)[-1]

        simple_uploaded_file = SimpleUploadedFile(
            original_image_name,
            image_buffer.read(),
            content_type='image/jpeg'
        )

        thumbnail_image_name = '{0}_{1}.{2}'.format(
            os.path.splitext(original_image_name)[0], attribute[1], 'jpg'
        )

        # Save SimpleUploadedFile into thumbnail field.
        thumbnail_image_field.save(
            thumbnail_image_name,
            simple_uploaded_file,
            save=False
        )
