import numpy as np
from PIL import Image

def load_pic_arr(img_name: str):
    """Load picture from moudle directory to np array."""
    with Image.open(img_name) as img:
        return np.array(img)
    

def show_img_from_arr(arr: np.array):
    Image.fromarray(arr).show()