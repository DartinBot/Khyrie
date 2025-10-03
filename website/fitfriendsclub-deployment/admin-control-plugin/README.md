# Site Admin Control Plugin

## ⚠️ **IMPORTANT SECURITY WARNING** ⚠️

**This plugin grants FULL administrative access to your WordPress site. Only use this if:**
- You are locked out of your own site
- You need emergency administrative access
- You understand the security implications

**DO NOT** use this plugin on production sites without removing it after regaining access.

## 📁 Installation Instructions

### Method 1: Upload via WordPress Admin (if you have any access)
1. Zip the `admin-control-plugin` folder
2. Go to WordPress Admin → Plugins → Add New → Upload Plugin
3. Upload the zip file and activate

### Method 2: FTP/File Manager Upload
1. Upload the entire `admin-control-plugin` folder to `/wp-content/plugins/`
2. Go to WordPress Admin → Plugins
3. Find "Site Admin Control" and click "Activate"

### Method 3: Emergency Access (if completely locked out)
1. Upload the folder via FTP to `/wp-content/plugins/`
2. Add this line to your theme's `functions.php`:
   ```php
   // Emergency activation
   include_once(WP_PLUGIN_DIR . '/admin-control-plugin/site-admin-control.php');
   ```

## 🔧 Configuration

**BEFORE ACTIVATING**, edit `site-admin-control.php` and change these lines:

```php
$this->admin_email = 'your-email@example.com'; // CHANGE TO YOUR EMAIL
$this->admin_username = 'admin'; // CHANGE TO YOUR DESIRED USERNAME
```

## ✨ What This Plugin Does

### 🔑 **Access Control**
- Creates a new admin user automatically
- Grants full administrator privileges to any logged-in user
- Bypasses capability checks
- Forces admin role on login

### 🛠️ **Site Editing Permissions**
- Enables theme editing
- Enables plugin editing
- Allows file uploads
- Grants all WordPress capabilities

### 👤 **User Management**
- Creates emergency admin account
- Grants super admin on multisite
- Allows promoting other users to admin

### 📊 **Admin Dashboard**
- Adds "Site Control" menu in WordPress admin
- Shows current user capabilities
- Provides quick action buttons
- Displays system information

## 🚀 After Installation

1. **Check your email** - You'll receive login credentials for the new admin user
2. **Login** with the new credentials
3. **Go to Site Control** menu in WordPress admin
4. **Verify permissions** - You should see ✅ for all capabilities

## 🔒 Security Features Bypassed

- File editing restrictions
- Capability checks
- User role limitations
- Plugin/theme installation blocks
- Maintenance mode (if active)

## ⚡ Quick Actions Available

After activation, you'll have access to:
- **Theme Editor** - Edit theme files directly
- **Plugin Editor** - Edit plugin files directly  
- **User Management** - Add/remove/modify users
- **Plugin Management** - Install/activate/deactivate plugins
- **Theme Management** - Install/activate themes

## 🛡️ Post-Access Security Steps

**IMPORTANT:** After regaining access to your site:

1. **Change all passwords** for important accounts
2. **Remove this plugin** - Deactivate and delete it
3. **Review user accounts** - Remove any unnecessary admin users
4. **Check for security issues** that caused the lockout
5. **Implement proper backup procedures**

## 🆘 Emergency Functions

If the plugin doesn't work normally, add this to your theme's `functions.php`:

```php
// Emergency admin creation
add_action('init', function() {
    if (!username_exists('emergency_admin')) {
        $user_id = wp_create_user('emergency_admin', 'TempPass123!', 'admin@yoursite.com');
        if (!is_wp_error($user_id)) {
            $user = new WP_User($user_id);
            $user->set_role('administrator');
            if (is_multisite()) {
                grant_super_admin($user_id);
            }
        }
    }
});
```

## 🔍 Troubleshooting

### Plugin Not Appearing?
- Check file permissions (folders: 755, files: 644)
- Verify the folder is in `/wp-content/plugins/`
- Check WordPress error logs

### Still Can't Access?
- Try the emergency function above
- Contact your hosting provider
- Use WordPress CLI if available
- Restore from backup

### Capabilities Not Working?
- Clear any caching
- Try logging out and back in
- Check if other security plugins are interfering

## ⚠️ **REMOVE AFTER USE**

This plugin is designed for **emergency access only**. Remove it immediately after:
- Regaining administrative access
- Fixing the underlying issue
- Securing your site properly

**File Locations to Remove:**
- `/wp-content/plugins/admin-control-plugin/` (entire folder)
- Any emergency code added to `functions.php`

## 📝 Legal Disclaimer

This plugin is provided "as-is" for legitimate site recovery purposes only. Users are responsible for:
- Using it only on sites they own or have permission to access
- Removing it after regaining access
- Any security implications of its use
- Complying with applicable laws and terms of service

Use responsibly and only when necessary! 🛡️