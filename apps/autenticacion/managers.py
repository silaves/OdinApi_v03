from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class CustomUserManager(BaseUserManager):

    # def create_user(self, username, password, nombres, **extra_fields):
    #     if not username:
    #         raise ValueError(_('El nombre de usuarios no es correcto'))
    #     if not nombres:
    #         raise ValueError(_('Los nombres no son correctos'))
    #     #email = self.normalize_email(email)
    #     printf("creando usuario")
    #     user = self.model(username=username, nombres=nombres, **extra_fields)
    #     user.set_password(password)
    #     user.save()
    #     return user
    def create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError(_('El nombre de usuario no es correcto'))
        user = self.model(username=username,email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError(_('El nombre de usuario no es correcto'))
        if password is None:
            password = ' '
        user = self.model(username=username,email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password):
        """
        Create and save a SuperUser with the given email and password.
        """
        # extra_fields.setdefault('is_staff', True)
        # extra_fields.setdefault('is_superuser', True)
        # extra_fields.setdefault('is_active', True)

        # if extra_fields.get('is_staff') is not True:
        #     raise ValueError(_('Superuser must have is_staff=True.'))
        # if extra_fields.get('is_superuser') is not True:
        #     raise ValueError(_('Superuser must have is_superuser=True.'))
        if password is None:
            raise TypeError('Superusers must have a password.')
        user = self.create_user(username=username, email=email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()
        return user