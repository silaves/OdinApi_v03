import urllib
from uuid import uuid4
from django.http import HttpResponseRedirect
# from django.core.urlresolvers import reverse
from .models import Perfil
from django.contrib.auth.models import Group
from apps.autenticacion.models import Usuario

USER_FIELDS = ['username', 'email']

# obtener el usuario de los datos recibidos para crearlos posteriormente
def get_username(strategy, details, social, backend, user=None, *args, **kwargs):
    if 'username' not in backend.setting('USER_FIELDS', USER_FIELDS):
        return
    storage = strategy.storage
    if not user:
        print('no hay usuario')
        email_as_username = strategy.setting('USERNAME_IS_FULL_EMAIL', False)
        uuid_length = strategy.setting('UUID_LENGTH', 16)
        max_length = storage.user.username_max_length()
        do_slugify = strategy.setting('SLUGIFY_USERNAMES', False)
        do_clean = strategy.setting('CLEAN_USERNAMES', True)

        if do_clean:
            override_clean = strategy.setting('CLEAN_USERNAME_FUNCTION')
            if override_clean:
                clean_func = module_member(override_clean)
            else:
                clean_func = storage.user.clean_username
        else:
            clean_func = lambda val: val

        if do_slugify:
            override_slug = strategy.setting('SLUGIFY_FUNCTION')
            if override_slug:
                slug_func = module_member(override_slug)
            else:
                slug_func = slugify
        else:
            slug_func = lambda val: val

        # if email_as_username and details.get('email'):
        #     username = details['email']
        # elif details.get('username'):
        #     username = details['username']
        # else:
        #     username = uuid4().hex
        username = uuid4().hex
        short_username = (username[:max_length - uuid_length]
                          if max_length is not None
                          else username)
        final_username = slug_func(clean_func(username[:max_length]))

        # Generate a unique username for current user using username
        # as base but adding a unique hash at the end. Original
        # username is cut to avoid any field max_length.
        # The final_username may be empty and will skip the loop.
        while not final_username or \
              storage.user.user_exists(username=final_username):
            username = short_username + uuid4().hex[:uuid_length]
            final_username = slug_func(clean_func(username[:max_length]))
    else:
        final_username = storage.user.get_username(user)
    
    # asocia el usuario a cliente
    if social is not None:
        final_username = str(details['first_name'])+str(social.uid)
        if not Usuario.objects.filter(username=final_username).exists():
            # print(username)
            user.username = final_username
            print('------ username     ',final_username,'     username-------')
            user.nombres = details['first_name']
            user.apellidos = details['last_name']
            user.save()
            perfil = Perfil()
            perfil.usuario = user
            perfil.save()
            grupo = Group.objects.get(name='cliente')
            user.groups.add(grupo)
            user.save()
    return {'username': final_username}

def create_user(strategy, details, backend, user=None, *args, **kwargs):
    """ Replaces the social.pipeline.user.create_user function for valid email check
    """

    if user:
        return {'is_new': False}
    
    # if not allowed_email(details.get('email')):
    #     return
    fields = dict(
            (name, kwargs.get(name, details.get(name))
             )
                  for name in backend.setting('USER_FIELDS', USER_FIELDS))
    if not fields:
        return
    return {
        'is_new': True,
        'user': strategy.create_user(**fields)
    }


def save_profile(backend, user, response, *args, **kwargs):
    if user :
        print(user.username,'      def save_profile()')
    else:
        print('no hay usuarui   def save_profle()')