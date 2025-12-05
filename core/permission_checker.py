"""
Permission Checker - REAL-TIME VERSION
Checks permissions directly from database on every operation.
When admin grants/revokes permission, it takes effect IMMEDIATELY.
"""

class PermissionChecker:
    """
    Real-time permission checker that queries the database on every check.
    This ensures that when admin changes permissions, they take effect immediately.
    """

    def __init__(self, db_manager, username: str, role: str):
        """
        Initialize the permission checker.

        Args:
            db_manager: DatabaseManager instance with active connection
            username: Current user's username
            role: Current user's role (admin, user, etc.)
        """
        self.db_manager = db_manager
        self.username = username
        self.role = role.lower() if role else 'user'
        self.is_admin = self.role in ['admin', 'superadmin']

        print(f"[PERMISSIONS] Checker initialized for {username} (role: {role}, admin: {self.is_admin})")

    def _check_permission(self, database_name: str, permission_type: str) -> bool:
        """
        Check if user has a specific permission on a database.
        Queries the database FRESH every time (real-time).

        Args:
            database_name: Name of the database
            permission_type: Type of permission (INSERT, DELETE, UPDATE, CREATE)

        Returns:
            True if user has permission, False otherwise
        """
        # Admins always have all permissions
        if self.is_admin:
            print(f"[PERMISSIONS] ✓ Admin bypass: {self.username} has {permission_type} on {database_name}")
            return True

        try:
            # Ensure connection is active
            if not self.db_manager or not self.db_manager.connection:
                print(f"[PERMISSIONS] ✗ No database connection")
                return False

            if not self.db_manager.connection.is_connected():
                self.db_manager.connect()

            cursor = self.db_manager.connection.cursor()

            # Query permissions table FRESH (real-time check)
            query = """
                SELECT COUNT(*) FROM backmeup_system.user_permissions 
                WHERE username = %s 
                AND database_name = %s 
                AND permission_type = %s
            """

            cursor.execute(query, (self.username, database_name, permission_type))
            result = cursor.fetchone()
            cursor.close()

            has_permission = result[0] > 0

            if has_permission:
                print(f"[PERMISSIONS] ✓ {self.username} has {permission_type} on {database_name}")
            else:
                print(f"[PERMISSIONS] ✗ {self.username} does NOT have {permission_type} on {database_name}")

            return has_permission

        except Exception as e:
            print(f"[PERMISSIONS] Error checking permission: {e}")
            # On error, deny permission for safety
            return False

    # ========== PERMISSION CHECK METHODS ==========

    def can_create_database(self) -> bool:
        """Check if user can create new databases (admin only)"""
        if self.is_admin:
            print(f"[PERMISSIONS] ✓ Admin {self.username} can create databases")
            return True
        print(f"[PERMISSIONS] ✗ {self.username} cannot create databases (not admin)")
        return False

    def can_drop_database(self, database_name: str) -> bool:
        """Check if user can drop a database"""
        return self._check_permission(database_name, 'DELETE')

    def can_create_table(self, database_name: str) -> bool:
        """Check if user can create tables in a database"""
        return self._check_permission(database_name, 'CREATE')

    def can_drop_table(self, database_name: str) -> bool:
        """Check if user can drop tables in a database"""
        return self._check_permission(database_name, 'DELETE')

    def can_insert(self, database_name: str) -> bool:
        """Check if user can insert data into a database"""
        return self._check_permission(database_name, 'INSERT')

    def can_update(self, database_name: str) -> bool:
        """Check if user can update data in a database"""
        return self._check_permission(database_name, 'UPDATE')

    def can_delete(self, database_name: str) -> bool:
        """Check if user can delete data from a database"""
        return self._check_permission(database_name, 'DELETE')

    def can_backup(self, database_name: str) -> bool:
        """Check if user can backup a database (all users can backup)"""
        # Everyone can create backups - it's a read operation
        print(f"[PERMISSIONS] ✓ {self.username} can backup {database_name}")
        return True

    def can_restore(self, database_name: str) -> bool:
        """Check if user can restore a database"""
        # Restore requires CREATE permission (creates/overwrites data)
        return self._check_permission(database_name, 'CREATE')

    def get_user_permissions(self, database_name: str = None) -> dict:
        """
        Get all permissions for current user (real-time).

        Args:
            database_name: Optional - filter by specific database

        Returns:
            Dictionary of permissions by database
        """
        if self.is_admin:
            return {"admin": True, "all_permissions": True}

        permissions = {}

        try:
            if not self.db_manager or not self.db_manager.connection:
                return permissions

            if not self.db_manager.connection.is_connected():
                self.db_manager.connect()

            cursor = self.db_manager.connection.cursor()

            if database_name:
                query = """
                    SELECT database_name, permission_type 
                    FROM backmeup_system.user_permissions 
                    WHERE username = %s AND database_name = %s
                """
                cursor.execute(query, (self.username, database_name))
            else:
                query = """
                    SELECT database_name, permission_type 
                    FROM backmeup_system.user_permissions 
                    WHERE username = %s
                """
                cursor.execute(query, (self.username,))

            for row in cursor.fetchall():
                db_name, perm_type = row
                if db_name not in permissions:
                    permissions[db_name] = []
                permissions[db_name].append(perm_type)

            cursor.close()

        except Exception as e:
            print(f"[PERMISSIONS] Error getting permissions: {e}")

        return permissions