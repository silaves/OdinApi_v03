from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from drf_yasg.utils import swagger_serializer_method

from .models import Usuario, Perfil, Ciudad, Horario

# registrar nuevo usuario
class RegistrarseSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""

    # Ensure passwords are at least 8 characters long, no longer than 128
    # characters, and can not be read by the client.
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    # The client should not be able to send a token along with a registration
    # request. Making `token` read-only handles that for us.
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = Usuario
        # List all of the fields that could possibly be included in a request
        # or response, including fields specified explicitly above.
        fields = ['email', 'username', 'password', 'token']

    def create(self, validated_data):
        # Use the `create_user` method we wrote earlier to create a new user.
        return Usuario.objects.create_user(**validated_data)



# logeo mediante tokens (campos requeridos:{user,password})
class LoginSerializer(serializers.Serializer):
    # email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        # The `validate` method is where we make sure that the current
        # instance of `LoginSerializer` has "valid". In the case of logging a
        # user in, this means validating that they've provided an email
        # and password and that this combination matches one of the users in
        # our database.

        # email = data.get('email', None)
        username = data.get('username', None)
        password = data.get('password', None)
        print(data,'   loginSErializer()')
        # Raise an exception if an
        # email is not provided.
        if username is None:
            raise serializers.ValidationError(
                'Se requiere una dirección de correo electrónico para iniciar sesión.'
            )

        # Raise an exception if a
        # password is not provided.
        if password is None:
            raise serializers.ValidationError(
                'Se requiere una contraseña para iniciar sesión.'
            )

        # The `authenticate` method is provided by Django and handles checking
        # for a user that matches this email/password combination. Notice how
        # we pass `email` as the `username` value since in our User
        # model we set `USERNAME_FIELD` as `email`.
        user = authenticate(username=username, password=password)

        # If no user was found matching this email/password combination then
        # `authenticate` will return `None`. Raise an exception in this case.
        if user is None:
            raise serializers.ValidationError(
                'No se encontró un usuario con este correo electrónico y contraseña.'
            )

        # Django provides a flag on our `User` model called `is_active`. The
        # purpose of this flag is to tell us whether the user has been banned
        # or deactivated. This will almost never be the case, but
        # it is worth checking. Raise an exception in this case.
        if not user.is_active:
            raise serializers.ValidationError(
                'Este usuario ha sido desactivado.'
            )

        # The `validate` method should return a dictionary of validated data.
        # This is the data that is passed to the `create` and `update` methods
        # that we will see later on.
        return {
            'email': user.email,
            'username': user.username,
            'token': user.token
        }



class UsuarioSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of User objects."""

    # Passwords must be at least 8 characters, but no more than 128 
    # characters. These values are the default provided by Django. We could
    # change them, but that would create extra work while introducing no real
    # benefit, so lets just stick with the defaults.
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = Usuario
        fields = ('email', 'username', 'password', 'token',)

        # The `read_only_fields` option is an alternative for explicitly
        # specifying the field with `read_only=True` like we did for password
        # above. The reason we want to use `read_only_fields` here is that
        # we don't need to specify anything else about the field. The
        # password field needed the `min_length` and 
        # `max_length` properties, but that isn't the case for the token
        # field.
        read_only_fields = ('token',)


    def update(self, instance, validated_data):
        """Performs an update on a User."""

        # Passwords should not be handled with `setattr`, unlike other fields.
        # Django provides a function that handles hashing and
        # salting passwords. That means
        # we need to remove the password field from the
        # `validated_data` dictionary before iterating over it.
        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            # For the keys remaining in `validated_data`, we will set them on
            # the current `User` instance one at a time.
            setattr(instance, key, value)

        if password is not None:
            # `.set_password()`  handles all
            # of the security stuff that we shouldn't be concerned with.
            instance.set_password(password)

        # After everything has been updated we must explicitly save
        # the model. It's worth pointing out that `.set_password()` does not
        # save the model.
        instance.save()

        return instance


class ChangePasswordSerializer(serializers.Serializer):
        
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
        
    class Meta:
        model = Usuario

    def validate_new_password(self, value):
        validate_password(value)
        return value



class PerfilNormalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfil
        fields = ('telefono',)


class UsuarioNormalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('nombres','apellidos','foto','token_firebase','ciudad')

class UsuarioEditResponse(serializers.ModelSerializer):
    telefono = serializers.IntegerField(required=False)

    class Meta:
        model = Usuario
        fields = ('nombres','apellidos','foto','token_firebase','telefono','ciudad')
        

class VerCiudad_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Ciudad
        fields = ['id','nombre','estado']

class VerHorario_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Horario
        fields = ['entrada','salida','estado']


class PerfilSerializer(serializers.ModelSerializer):
    telefono = serializers.SerializerMethodField('getTelefono')
    calificacion = serializers.SerializerMethodField('getCalificacion')
    disponibilidad = serializers.SerializerMethodField('getDisponibilidad')
    ciudad = VerCiudad_Serializer()
    horario = serializers.SerializerMethodField()

    class Meta:
        model = Usuario
        fields = ('id','username','email','nombres','apellidos','token_firebase','foto','ciudad','perfil','telefono','calificacion','disponibilidad','grupos','horario')
    
    def getTelefono(self, usuario):
        try:
            telefono = Perfil.objects.get(usuario__id=usuario.id).telefono
        except:
            telefono = ""
        return telefono
    
    def getCalificacion(self, usuario):
        try:
            calificacion = Perfil.objects.get(usuario__id=usuario.id).calificacion
        except:
            calificacion = 0
        return calificacion
    
    def getDisponibilidad(self, usuario):
        try:
            disponibilidad = Perfil.objects.get(usuario__id=usuario.id).disponibilidad
        except:
            disponibilidad = 0
        return disponibilidad
    
    def get_horario(self, obj):
        horarios = Horario.objects.filter(usuario__id=obj.id)
        return VerHorario_Serializer(horarios, many=True).data
    


      

# perfil edtiar

class EditarPerfilSerializer(serializers.ModelSerializer):
    telefono = serializers.SerializerMethodField('getTelefono')

    class Meta:
        model = Usuario
        fields = ('email','nombres','apellidos','foto','telefono')
    
    def getTelefono(self, usuario):
        try:
            telefono = Perfil.objects.get(pk=usuario.id).telefono
        except:
            telefono = ""
        return telefono

    # def update(self, instance, validata_data):
    #     print('update mi update')
    #     return 1

class SocialSerializer(serializers.Serializer):
    """Serializer which accepts an OAuth2 access token and provider."""
    provider = serializers.CharField(max_length=255, required=True)
    access_token = serializers.CharField(max_length=4096, required=True, trim_whitespace=True)

# crear empresario
class CrearEmpresario_Serializer(serializers.ModelSerializer):
    telefono = serializers.IntegerField(max_value=99999999, required=False)

    class Meta:
        model = Usuario
        fields = ('username','password','email','nombres','apellidos','foto','telefono','ciudad')

    def create(self, validated_data):
        try:
            data = validated_data.pop('telefono')
        except:
            pass
        # Use the `create_user` method we wrote earlier to create a new user.
        return Usuario.objects.create_user(**validated_data)



# class ShowVersionAndroidApp(serializers.Serializer):