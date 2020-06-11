from django.urls import path
from . import views

urlpatterns = [
    # CATEGORIA
    path('ecommerce/categoria/<str:estado>/', views.get_categorias_productos, name='Lista de Categorias Productos Lista'),
    path('ecommerce/categoria/<str:estado>/nivel/', views.get_categorias_productos_niveles, name='Lista de Categorias Productos por Niveles'),
    path('ecommerce/categoria/<int:id_categoria>/<str:estado>/hijo/', views.get_categorias_productos_hijo, name='Lista de Categorias Productos de una Categoria Padre - Lista'),
    path('ecommerce/categoria/<int:id_categoria>/<str:estado>/hijo_nivel/', views.get_categorias_productos_hijo_niveles, name='Lista de Categorias Productos de una Categoria Padre - Por Niveles'),

    # SUCURSAL
    path('ecommerce/sucursal/<str:estado>/lista/ciudad/<int:id_ciudad>/', views.getAll_Sucursales_eco, name='Lista de todas las Sucursales - Ecommerce'),

    # ARTICULO

    path('ecommerce/articulo/crear/', views.crear_articulo, name='Crear Articulo'),
    path('ecommerce/articulo/<int:id_producto>/editar/', views.editar_articulo, name='Editar Articulo'),
    path('ecommerce/articulo/<int:id_producto>/', views.ver_articulo, name='Ver articulo'),
    path('ecommerce/articulo/<str:estado>/todos/', views.get_articulos, name='Listar todos los articulos'),
    path('ecommerce/articulo/<str:estado>/todos/cursor/', views.get_articulos_cursor_pagination, name='Listar todos los articulos - Cursor'),
    path('ecommerce/articulo/<str:estado>/todos/number/', views.get_articulos_number_pagination, name='Listar todos los articulos - Number'),

    # por categoria
    # path('ecommerce/articulo/<str:estado>/categoria/<int:id_categoria>/', views.get_articulos_categoria, name='Listar de Articulos por Categoria'),

    # FAVORITO

    path('ecommerce/articulo/<int:id_producto>/to_favorito/',views.add_favorito,name="Agregar articulo a favoritos"),
    path('ecommerce/articulo/<int:id_producto>/remove_favorito/',views.remove_favorito,name="Quitar articulo de favoritos"),
    path('ecommerce/articulo/favorito/',views.get_favoritos,name="Listar Favoritos"),
]