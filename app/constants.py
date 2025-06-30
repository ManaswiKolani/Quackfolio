import posixpath 
from flask import url_for

# Duck image filenames
DUCK_IMAGES = {
    'good': 'good_duck.PNG',
    'bad': 'bad_duck.PNG',
    'hover_good': 'good_duck2.PNG',
    'hover_bad': 'bad_duck2.PNG',
    'default': 'good_duck.png'
}


# Background images
BACKGROUND_IMAGES = {
    'start': 'open_page.PNG',
    'search': 'search_page.PNG',
    'pond': 'portfolio_bg.PNG'
}
def get_duck_image_url(mood='default'):
    filename = DUCK_IMAGES.get(mood, DUCK_IMAGES['default'])
    return url_for('static', filename=posixpath.join('images', filename))

def get_background_url(screen='start'):
    filename = BACKGROUND_IMAGES.get(screen, BACKGROUND_IMAGES['start'])
    return url_for('static', filename=posixpath.join('images', filename))
