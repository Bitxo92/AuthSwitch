"""
authswitch - RBAC Template

Este módulo contiene la plantilla de roles y permisos para el realm main.
"""
from tai_api.rbac import source, role, app_permission, rls
# Importa las constantes de permisos de API generados para las tablas y vistas
# from api.rbac.tables.main import *

# Carga los permisos de API desde los schemas de la base de datos
# Ajusta el parámetro dbschemas con los nombres de los schemas que contienen tablas/vistas de las que quieras generar permisos
# Luego ejecutar tai-api generate
source(realm_name="main", dbschemas=[])

role(
    name="Administrador",
    description="Rol de administrador con todos los permisos",
    api_permissions=[
        "sudo",
        "main-admin",
    ],
)

"""
INSTRUCCIONES

# Definición de permisos de aplicación (custom, no vinculados a tablas)

all_permissions = app_permission(
    name="all_permissions",
    description="Permiso para realizar todas las acciones.",
)

view_data = app_permission(
    name="view_data",
    description="Permiso para visualizar los datos de las vistas.",
)

# Definición de roles (agrupan permisos de API y/o de aplicación)
# Los permisos de API se pueden referenciar:
#   1.  Usando las clases importadas de tables.
#           api_permissions=[Usuario.READ, Post.CREATE]
#   2.  Usando strings con el nombre del permiso.
#           api_permissions=['usuario-read', 'post-create']
# Los permisos de APP se pueden referenciar:
#   1.  Usando las variables definidas en este archivo:
#           app_permissions=[view_data]
#   2.  Usando strings con el nombre del permiso:
#           app_permissions=['view_data']

viewer = role(
    name="viewer",
    description="Rol de lectura para vistas",
    app_permissions=[view_data],
)

reader = role(
    name="reader",
    description="Rol de lectura para vistas",
    app_permissions=['view_data'],
    subroles=[viewer],
)
"""