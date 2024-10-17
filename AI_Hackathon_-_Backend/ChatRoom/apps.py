from django.apps import AppConfig

class ChatRoomConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ChatRoom'

    # Eliminăm metoda ready() care accesează baza de date prea devreme
