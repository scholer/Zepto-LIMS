# Copyright 2019, Rasmus Sorensen <rasmusscholer@gmail.com>
"""

A dummy camera that only returns a pre-defined image file.

"""

from .basecamera import BaseCamera

try:
    import cv2
    # from cv2 import imread as _imread
except ImportError:
    cv2 = None
    try:
        from skimage.io import imread
    except ImportError:
        try:
            import PIL.Image as PilImage
        except ImportError:
            raise ImportError("ERROR: Could not load any of the standard image libraries (cv2, PIL, skimage).")
        else:
            def imread(filepath):
                PilImage.open(filepath)
else:
    def imread(filepath):
        # OBS: cv2.imread does NOT support Python pathlib.Path as filename argument, only strings.
        return cv2.imread(str(filepath), cv2.IMREAD_GRAYSCALE)


class DummyFileCamera(BaseCamera):

    @property
    def image_filepath(self):
        return self.config['dummyfilecamera_image_filepath']

    def get_image(self):
        return imread(self.image_filepath)
