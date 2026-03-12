class PermissionManager:

    ROLE_PERMISSIONS = {

        "Admin": {
            "employee_access": True,
            "payroll_access": True,
            "user_management_access": True,
            "view_own_payroll_only": False
        },

        "HR": {
            "employee_access": True,
            "payroll_access": True,
            "user_management_access": False,
            "view_own_payroll_only": False
        },

        "Employee": {
            "employee_access": False,
            "payroll_access": True,
            "user_management_access": False,
            "view_own_payroll_only": True
        }
    }

    @classmethod
    def has_permission(cls, role, permission_key):

        role_permissions = cls.ROLE_PERMISSIONS.get(role)

        if not role_permissions:
            return False

        return role_permissions.get(permission_key, False)
    
        def can_lock_payroll(self, role):
         return role in ["Admin", "Manager"]