from django.urls import path
from . import views

urlpatterns = [
    # path('test/0/', views.MyListAPIView.as_view(), name='-'),
    # path('test/1/', views.lista_productos_paginator, name='Paginador'),
    # path('test/2/', views.lista_productos_paginator2, name='Paginador'),
    # EMPRESA
    path('empresa/crear/', views.crearEmpresa, name='Crear Empresa'),
    path('empresa/<int:id_empresa>/editar/', views.editar_empresa, name='Modificar Empresa'),
    path('empresa/usuario/', views.getEmpresaByUsuario, name='Lista Empresas por Usuario'),
    path('empresa/lista/', views.get_empresas, name='Lista todas las Empresas'),

    path('empresa/ciudad/<str:estado>/lista/', views.lista_ciudades, name='Lista de Ciudades'),
    # SUCURSAL
    path('empresa/sucursal/crear/', views.crearSucursal, name='Crear Sucursal'),
    path('empresa/sucursal/<int:id_sucursal>/editar/', views.editar_sucursal, name='Modificar Sucursal'),
    path('empresa/sucursal/<str:estado>/lista/ciudad/<int:id_ciudad>/', views.getAll_Sucursales, name='Lista todas Sucursales por ciudad'),
    path('empresa/sucursal/<str:estado>/lista/ciudad/<int:id_ciudad>/categoria/<int:id_categoria>/', views.getAll_Sucursales_by_categoria, name='Lista todas Sucursales por ciudad y categoria'),
    path('empresa/sucursal/<str:estado>/lista/ciudad/<int:id_ciudad>/todo/', views.get_sucurales_sistema, name='Lista todas Sucursales del sistema comida e ecommerce'),

    path('empresa/sucursal/<str:estado>/lista/ciudad/<int:id_ciudad>/cercanas/', views.get_sucurales_by_distancia, name='Lista de Sucursales mas Cercanas por Ciudad'),
    path('empresa/sucursal/<str:estado>/lista/ciudad/<int:id_ciudad>/categoria/<int:id_categoria>/cercanas/', views.get_sucurales_by_distancia_categoria, name='Lista de Sucursales mas Cercanas,Ciudad y Categoria'),

    path('empresa/sucursal/<str:estado>/lista/ciudad/<int:id_ciudad>/max/', views.getAll_Sucursales_max_calificacion, name='Lista todas Sucursales del Sistema por Calificacion'),
    path('empresa/<int:id_empresa>/sucursal/<str:estado>/lista/', views.getSucursales, name='Lista de Sucursales por Empresa'),
    path('empresa/sucursal/<int:id_sucursal>/', views.getSucursal, name='Obtener Sucursal'),
    path('empresa/sucursal/<int:id_sucursal>/disponible/', views.cambiar_diponible_sucursal, name='Cambiar Disponibilidad Sucursal'),
    
    path('empresa/sucursal/<int:id_sucursal>/token_firebase/',views.get_token_firebase, name='Obtener Toke Firebase'),

    # PRODUCTO
    path('empresa/sucursal/producto/crear/', views.crear_producto, name='Crear Producto'),
    path('empresa/sucursal/producto/<int:id_producto>/editar/', views.editar_producto, name='Editar Producto'),
    path('empresa/sucursal/producto/<int:id_producto>/', views.get_productos_finales, name='Ver Producto'),
    path('empresa/sucursal/<int:id_sucursal>/producto/<str:estado>/', views.get_productos_estado_by_sucursal, name='Lista Producto por Sucursal (activos o inactivos)'),

    path('empresa/sucursal/producto/<str:tipo_producto>/rank/', views.get_productos_estado_ranking, name='Lista Todos los Productos mejores puntuados (activos o inactivos) RANKING Cursor'),
    path('empresa/sucursal/producto/<str:estado>/ultimos/<int:limite>/', views.get_productos_estado_by_sucursal_ultimos, name='Lista Producto por Sucursal (activos o inactivos) ULTIMOS'),
    path('empresa/sucursal/producto/<str:estado>/categoria/<int:id_categoria>/', views.get_productos_categoria, name='Lista Producto por Categoria (activos o inactivos)'),
    path('empresa/sucursal/producto/<str:estado>/tipo/<str:tipo_producto>/', views.get_productos_estado, name='Lista Todos los Productos (activos o inactivos) Combo o Producto TODO'),
    path('empresa/sucursal/<int:id_sucursal>/producto/<str:estado>/cliente/', views.get_productos_estado_by_sucursal_cliente, name='Lista Producto por Sucursal (activos o inactivos) para cliente'),

    path('empresa/sucursal/<int:id_sucursal>/producto/<str:estado>/producto/', views.get_productos_estado_productos_by_sucursal, name='Lista Producto por Sucursal (activos o inactivos) productos'),
    path('empresa/sucursal/<int:id_sucursal>/producto/<str:estado>/combo/', views.get_productos_estado_combos_by_sucursal, name='Lista Producto por Sucursal (activos o inactivos) combos'),

    # RANKING
    path('empresa/sucursal/producto/<int:id_producto>/calificar/', views.calificar_producto, name='Calificar Producto'),

    
    # COMBO
    path('empresa/sucursal/combo/crear/', views.crear_combo, name='Crear Combo'),
    path('empresa/sucursal/combo/<int:id_combo>/editar/', views.editar_combo, name='Editar Combo'),


    # CATEGORIA
    path('empresa/categoria/lista/', views.getCategoria, name='Lista de Categorias Empresa'),
    
    # PEDIDO
    path('empresa/sucursal/pedido/crear_f/', views.crear_pedido_f, name='Crear Pedido'),
    
    path('empresa/sucursal/pedido/crear_f/empresario/', views.crear_pedido_empresario, name='Crear Pedido para Empresarios'),
    path('empresa/sucursal/pedido/<int:id_pedido>/editar_f/empresario/', views.editar_pedido_empresario, name='Editar Pedido para Empresarios'),

    path('empresa/sucursal/pedido/<int:id_pedido>/editar_f/', views.editar_pedido_f, name='Editar Pedido'),
    path('empresa/sucursal/pedido/<int:id_pedido>/curso/', views.cambiar_pedido_en_curso, name='Cambiar pedido a en curso'),
    path('empresa/sucursal/pedido/<int:id_pedido>/marcha/', views.cambiar_pedido_en_marcha, name='Cambiar pedido a en marcha'),
    path('empresa/sucursal/pedido/<int:id_pedido>/finalizado/', views.cambiar_pedido_en_finalizado, name='Cambiar pedido a finalizado'),
    path('empresa/sucursal/pedido/<int:id_pedido>/cancelar/', views.cambiar_pedido_en_cancelado, name='Cambiar pedido a cancelado'),
    path('empresa/sucursal/pedido/<int:id_pedido>/cliente_finalizado/', views.cambiar_pedido_en_finalizado_cliente, name='Cambiar pedido a finalizado-cliente'),
    
    path('empresa/sucursal/<int:id_sucursal>/pedido/<str:estado>/', views.get_pedidos_by_sucursal, name='Lista de Pedidos por Sucursal (DIA)'),
    path('empresa/sucursal/<int:id_sucursal>/pedido/<str:estado>/cursor/', views.get_pedidos_by_sucursal_paginacion, name='Lista de Pedidos por Sucursal (DIA) PAGINADOR CURSOR'),
    
    path('empresa/sucursal/<int:id_sucursal>/pedido/<str:estado>/semana/', views.get_pedidos_by_sucursal_semana, name='Lista de Pedidos por Sucursal (SEMANA)'),
    path('empresa/sucursal/<int:id_sucursal>/pedido/<str:estado>/semana/cursor/', views.get_pedidos_by_sucursal_semana_paginacion_cursor, name='Lista de Pedidos por Sucursal (SEMANA) PAGINADOR CURSOR'),

    path('empresa/sucursal/<int:id_sucursal>/pedido/<str:estado>/rango/', views.get_pedidos_by_sucursal_rango, name='Lista de Pedidos por Sucursal (RANGO)'),
    path('empresa/sucursal/<int:id_sucursal>/pedido/<str:estado>/rango/cursor/', views.get_pedidos_by_sucursal_rango_paginacion_cursor, name='Lista de Pedidos por Sucursal (RANGO) PAGINADOR CURSOR'),

    path('empresa/<int:id_empresa>/sucursal/pedido/<str:estado>/', views.get_pedidos_by_empresa, name='Lista de Pedidos por Empresa'),
    path('empresa/sucursal/<int:id_sucursal>/pedido/<str:estado>/todo/', views.get_todos_pedidos_by_sucursal, name='Lista de Pedidos por Sucursal'),
    path('empresa/sucursal/<int:id_sucursal>/pedido/<str:estado>/todo/cursor/', views.get_todos_pedidos_by_sucursal_paginacion_cursor, name='Lista de Pedidos por Sucursal PAGINADOR CURSOR'),

    path('empresa/sucursal/pedido/<str:estado>/cliente/lista/', views.get_pedidos_by_estado_cliente, name='Lista de Pedidos Cliente (DIA)'),
    path('empresa/sucursal/pedido/<str:estado>/cliente/lista/cursor/', views.get_pedidos_by_estado_cliente_paginacion_cursor, name='Lista de Pedidos Cliente (DIA) PAGINADOR CURSOR'),

    path('empresa/sucursal/pedido/<str:estado>/cliente/lista/semana/', views.get_pedidos_by_estado_cliente_semana, name='Lista de Pedidos Cliente (SEMANA)'),
    path('empresa/sucursal/pedido/<str:estado>/cliente/lista/semana/cursor/', views.get_pedidos_by_estado_cliente_semana_paginacion_cursor, name='Lista de Pedidos Cliente (SEMANA) PAGINADOR CURSOR'),

    path('empresa/sucursal/pedido/<str:estado>/cliente/lista/rango/', views.get_pedidos_by_estado_cliente_rango, name='Lista de Pedidos Cliente (RANGO)'),
    path('empresa/sucursal/pedido/<str:estado>/cliente/lista/rango/cursor/', views.get_pedidos_by_estado_cliente_rango_paginacion_cursor, name='Lista de Pedidos Cliente (RANGO) PAGINADOR CURSOR'),

    path('empresa/sucursal/pedido/<int:id_pedido>/', views.get_pedido, name='Ver Pedido'),

    # REPARTIDOR
    path('empresa/repartidor/ciudad/<int:id_ciudad>/', views.repartidores_by_ciudad, name='Lista de Repartidores por Ciudad'),
    path('empresa/repartidor/disponible/', views.cambiar_disponibilidad_repartidor, name='Cambiar disponibilidad Repartidor'),
    path('empresa/repartidor/pedido/<int:id_pedido>/aceptar/', views.aceptar_pedido, name='Aceptar Pedido'),
    path('empresa/pedido/disponibles/dia/', views.get_pedidos_for_repartidor, name='Lista de Pedidos de todas las Sucursales - Repartidor'),
    path('empresa/repartidor/pedido/<str:estado>/dia/', views.get_pedidos_by_repartidor_dia, name='Lista de Pedidos de un Repartidor (DIA)'),
    path('empresa/repartidor/pedido/<str:estado>/dia/cursor/', views.get_pedidos_by_repartidor_dia_paginador_cursor, name='Lista de Pedidos de un Repartidor (DIA) PAGINADOR CURSOR'),
    
    path('empresa/repartidor/pedido/<str:estado>/semana/', views.get_pedidos_by_repartidor_semana, name='Lista de Pedidos de un Repartidor (SEMANA)'),
    path('empresa/repartidor/pedido/<str:estado>/semana/cursor/', views.get_pedidos_by_repartidor_semana_paginacion_cursor, name='Lista de Pedidos de un Repartidor (SEMANA) PAGINADOR CURSOR'),

    path('empresa/repartidor/pedido/<str:estado>/rango/', views.get_pedidos_by_repartidor_rango, name='Lista de Pedidos de un Repartidor (RANGO DE FECHAS)'),
    path('empresa/repartidor/pedido/<str:estado>/rango/cursor/', views.get_pedidos_by_repartidor_rango_paginacion_cursor, name='Lista de Pedidos de un Repartidor (RANGO DE FECHAS) PAGINADOR CURSOR'),

    # PAGINADORES CURSOR

    # CALIFICACION

    path('empresa/sucursal/pedido/<int:id_pedido>/calificar/cliente/', views.calificar_para_cliente, name='Calificar para Cliente'),
    path('empresa/sucursal/pedido/<int:id_pedido>/calificar/repartidor/', views.calificar_para_repartidor, name='Calificar para Repartidor'),
    path('empresa/sucursal/pedido/<int:id_pedido>/calificar/empresario/', views.calificar_para_empresa, name='Calificar para Empresa'),

    path('convert/', views.get_value_from_url, name='convert url'),
]