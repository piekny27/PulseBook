from testy.routes import *

@app.template_filter('getImage')
def get_image(name):
    """Convert cloudinary image name to url."""
    avatar = current_user.profiles.avatars
    options = None
    if avatar.options:
        options = json.loads(avatar.options)
        if 'width' in options:
            return CloudinaryImage(name).build_url(
                    height=options['height'],
                    width=options['width'],
                    x=options['x'],
                    y=options['y'],
                    crop="crop"
                    )
    else:
        if avatar.name != Avatar.DEFAULT:
            return CloudinaryImage(Avatar.DEFAULT).build_url()
        return CloudinaryImage(name).build_url()

