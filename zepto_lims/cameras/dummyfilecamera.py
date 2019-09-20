# Copyright 2019, Rasmus Sorensen <rasmusscholer@gmail.com>
"""

A dummy camera that only returns a pre-defined image file.

"""

from .basecamera import BaseCamera
from zepto_lims.utils.image import imread


class DummyFileCamera(BaseCamera):

    @property
    def image_filepath(self):
        return self.config['dummyfilecamera_image_filepath']

    def get_image(self):
        return imread(self.image_filepath)
