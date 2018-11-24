def get_config(current_app):
    return {
        "app_token": current_app.config['APP_TOKEN'],
        "app_secret": current_app.config['APP_SECRET'],
        "access_token": current_app.config['ACCESS_TOKEN'],
        "access_token_secret": current_app.config['ACCESS_TOKEN_SECRET'],
        "url": current_app.config['MKM_URL']
    }
