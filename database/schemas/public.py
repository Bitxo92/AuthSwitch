# -*- coding: utf-8 -*-
"""
Fuente principal para la definición de esquemas y generación de modelos CRUD.
Usa el contenido de tai_sql para definir tablas, relaciones, vistas y generar automáticamente modelos y CRUDs.
Usa tai_sql.generators para generar modelos y CRUDs basados en las tablas definidas.
Ejecuta por consola tai-sql generate para generar los recursos definidos en este esquema.
"""
from __future__ import annotations
from tai_sql import *
from tai_sql.generators import *


# Configurar el datasource
datasource(
    provider=env('MAIN_DATABASE_URL'), # Además de env, también puedes usar (para testing) connection_string y params
    schema='public', # Esquema del datasource
    syntax='v2', # Sintaxis V2: col[type], onetomany[Model], manytoone[Model]
    operative_fields=False, # Añade created_at, updated_at, created_by, updated_by a todas las tablas
)

# Configurar los generadores
generate(
    PythonClientGenerator(
        output_dir=[
            'database/database', # Directorio donde se generará el cliente python
            # Añade más directorios aquí
        ]
    ),
    ERDiagramGenerator(
        output_dir=[
            'database/diagrams', # Directorio donde se generará el diagrama
            # Añade más directorios aquí
        ],
        theme='classic',
        format='svg'
    )
)

# Definición de tablas y relaciones

# Ejemplo de definición de tablas y relaciones. Eliminar estos modelos y definir los tuyos propios.
class Usuario(Table):
    """Tabla que almacena información de los usuarios del sistema"""
    __tablename__ = "usuario"

    id: col[int] = column(primary_key=True, autoincrement=True)
    name: col[str] = column(unique=True, description='Nombre del usuario')
    pwd: col[str] = column(encrypt=True) # Contraseña encriptada
    email: col[str | None] # Nullable
    last_post_date: col[datetime | None] # Nullable, se actualizará con un trigger al crear un nuevo post

    posts: onetomany[Post] # Relación one-to-many (implícita) con la tabla Post

    def feed(self) -> List[Usuario]:
        """Datos iniciales para poblar la tabla. Ejecutar con: tai-sql feed"""
        return [
            Usuario(
                name="John Doe",
                pwd="hashed_password",
                email="john.doe@example.com",
                posts=[
                    Post(title="First Post", content="Hello World!", comments=[
                        Comment(content="Great post!"),
                        Comment(content="Thanks for sharing"),
                    ]),
                    Post(title="Second Post", content="Another day, another post"),
                ],
            ),
            Usuario(
                name="Jane Smith",
                pwd="hashed_password",
                email="jane.smith@example.com",
                posts=[
                    Post(title="Jane's Post", content="My first post here"),
                ],
            ),
        ]


class ContentType(Enum):
    """Tipos de contenido para los posts"""
    TEXT = 'text'
    IMAGE = 'image'
    VIDEO = 'video'


class Post(Table):
    """Tabla que almacena los posts de los usuarios"""
    __tablename__ = "post"

    id: col[bigint] = column(primary_key=True, autoincrement=True) # Tipo bigint para PostgreSQL
    title: col[str] = column(default='Post Title') # Valor por defecto
    content: col[str] = column(description='Contenido del post')
    content_type: col[ContentType] = column(default=ContentType.TEXT) # Tipo de contenido con valor por defecto
    timestamp: col[datetime] = column(default=datetime.now, description='Fecha y hora del post') # Timestamp con generador de valor por defecto
    author_id: col[int]

    comments: onetomany[Comment]

    author: manytoone[Usuario] = relation(fields=['author_id'], references=['id'], backref='posts') # Relación many-to-one con la tabla User

    @on_create(timing='after')
    def modify_user_last_post_date(self, t: TriggerAPI):
        """Trigger que actualiza el campo last_post_date del usuario al crear un nuevo post"""
        t.update(Usuario, self.author_id, last_post_date=self.timestamp)


class Comment(Table):
    """Tabla que almacena los comentarios de los posts"""
    __tablename__ = "comment"

    id: col[int] = column(primary_key=True, autoincrement=True)
    content: col[str] = column(description='Contenido del comentario')
    post_id: col[bigint]

    post: manytoone[Post] = relation(fields=['post_id'], references=['id'], backref='comments') # Relación many-to-one con la tabla Post


# Definición de vistas

class UserStats(View):
    """Vista que muestra estadísticas de usuarios y sus posts"""
    __tablename__ = "user_stats"
    __query__ = query('user_stats.sql') # Esto es necesario para usar tai-sql push

    user_id: col[int]
    user_name: col[str]
    post_count: col[int]