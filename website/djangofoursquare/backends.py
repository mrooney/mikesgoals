from django.contrib.auth.models import User, check_password
# email_re moved in Django 1.2
try:
    from django.core.validators import email_re
except ImportError:
    from django.forms.fields import email_re

FOURSQUARE_USER_PREFIX = '4sq_'

class BasicBackend:
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

class FoursquareBackend(BasicBackend):
    def authenticate(self, foursquare_user_data, access_token):
        
        id = foursquare_user_data['id']
        first_name = foursquare_user_data.get('firstname', '')
        last_name = foursquare_user_data.get('lastname', '')
        photo = foursquare_user_data.get('photo', '')
        gender = foursquare_user_data.get('gender', '')
        phone = foursquare_user_data.get('phone', '')
        email = foursquare_user_data.get('email', '')
        
        username = '%s%d' % (FOURSQUARE_USER_PREFIX, id)
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = User.objects.create_user(username, email, None)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            
        return user