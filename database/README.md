# Database Setup Instructions

## Creating the Users Table

Before running the application, you need to create the users table in your MySQL database.

### Option 1: Using MySQL Command Line

1. Open MySQL command line or MySQL Workbench
2. Run the SQL script:

```bash
mysql -u root -p < create_users_table.sql
```

Or in MySQL Workbench:
- Open the `create_users_table.sql` file
- Execute the script (F9 or Execute button)

### Option 2: Using phpMyAdmin

1. Open phpMyAdmin in your browser
2. Select the `backmeup_system` database (or create it if it doesn't exist)
3. Go to the "SQL" tab
4. Copy and paste the contents of `create_users_table.sql`
5. Click "Go" to execute

### Default Admin Account

After running the script, a default admin account will be created:

- **Username:** `admin`
- **Password:** `admin123`
- **Email:** `admin@backmeup.com`

**Important:** Change the default password after first login for security!

### Database Structure

The `users` table contains the following fields:

- `id` - Primary key (auto-increment)
- `username` - Unique username (required)
- `email` - Unique email address (required)
- `password` - User password (stored as plain text - use hashing in production!)
- `full_name` - User's full name (optional)
- `created_at` - Account creation timestamp
- `last_login` - Last login timestamp
- `is_active` - Account status (TRUE/FALSE)
- `role` - User role (default: 'user', admin: 'admin')

### Security Note

⚠️ **Important:** This implementation uses plain text passwords for simplicity. In a production environment, you should:

1. Use password hashing (bcrypt, argon2, etc.)
2. Implement password reset functionality
3. Add email verification
4. Use prepared statements (already implemented)
5. Add rate limiting for login attempts
6. Implement session management

### Troubleshooting

If you encounter errors:

1. **Database doesn't exist:** The script will create it automatically
2. **Table already exists:** The script uses `CREATE TABLE IF NOT EXISTS`, so it's safe to run multiple times
3. **Connection refused:** Make sure MySQL/XAMPP is running
4. **Access denied:** Check your MySQL root password in the application configuration

