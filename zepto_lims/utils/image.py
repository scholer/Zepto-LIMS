# Copyright 2019, Rasmus Sorensen <rasmusscholer@gmail.com>
"""


"""


try:
    import cv2
except ImportError:
    cv2 = None
    try:
        from skimage.io import imread, imshow as _imshow, show as _show
        print("WARNING: Using un-tested skimage to read and show images.")
        # skimage.io.imshow uses matplotlib by default.
        def imshow(image, title='window title'):
            _imshow(image)
            _show()
    except ImportError:
        try:
            import PIL.Image as PilImage
        except ImportError:
            raise ImportError("ERROR: Could not load any of the standard image libraries (cv2, PIL, skimage).")
        else:
            def imread(filepath, as_gray=True):
                PilImage.open(filepath)

            def imshow(image, title='window title'):
                PilImage.Image(image).show(title=title)
else:
    def imread(filepath, as_gray=True):
        # OBS: cv2.imread does NOT support Python pathlib.Path as filename argument, only strings.
        return cv2.imread(str(filepath), cv2.IMREAD_GRAYSCALE)

    def imshow(image, title='window title'):
        cv2.imshow(title, image)
