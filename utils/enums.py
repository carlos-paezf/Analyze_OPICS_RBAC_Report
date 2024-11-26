from enum import Enum


# The class `RBACKeys` defines enumerated keys related to government, groups, transactions, profiles,
# and user permissions.
class RBAC_Keys(str, Enum):
    GOVERNMENT = "gobierno"
    GROUPS = "grupos"
    GROUP_TRANSACTION = "grupo-transaccion"
    PROFILES = "perfiles"
    PROFILES_GROUPS = "perfil-grupo"
    PROFILES_USERS = "perfil-usuario"


class RUGAR_Keys(str, Enum):
    OPERATOR_ID = "OperatorID: "
    OPERATOR_NAME = "Operator Name: "
    GROUPS = "Groups:"


# The class `OPICSKeys` defines enumeration constants for keys related to user information in OPICS.
class OPICS_Keys(str, Enum):
    USER = "usuario_opics"
    USERNAME = "nombre_del_usuario"
    GROUPS = "grupos"


# The class RBAC_Profile_Keys_Enum defines enumeration keys for various attributes related to RBAC
# profiles.
class RBAC_Profile_Keys(str, Enum):
    PROFILE = "perfil"
    DESCRIPTION = "descripcion_del_perfil"
    ROLE_TYPE = "tipo_role_admin/operativo"
    USER_TYPE = "tipo_de_usuariointerno/externo"
    CRITICALITY = "criticidad_del_privilegio"
    IN_USE = "en_uso",
    WITHDRAWAL_DATE = "fecha__retiro"
    EXCLUSIVE_OF_ANOTHER_PROFILE = "excluyente_de_otro_perfil"


class RBAC_Profile_Group_Keys(str, Enum):
    PROFILE = "perfil"
    GROUPS = "grupos"