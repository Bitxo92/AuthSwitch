/*
this file  defines the permissions used for the frontend rbac. Each permission consists of a string that follows the format: <resource>-<action>. 
The resource is the name of the resource being accessed, meaning the page(for example: "gestion_usuarios"), 
and the action is the type of access being granted(for example: "access", "create", "update", "delete"). 
For example, the permission "gestion_usuarios-access" grants access to the "gestion_usuarios" resource, 
while a permission like "gestion_usuarios-create" would grant the ability to create new user in the "gestion_usuarios" resource. 
This structure allows for fine-grained control over user access to different parts of the application. 
*/
export const PERMISSIONS = {
  GESTION_USUARIOS: {
    ACCESS: "gestion_usuarios-access",
    CREATE: "gestion_usuarios-create",
    UPDATE: "gestion_usuarios-update",
    DELETE: "gestion_usuarios-delete",
  },
}
