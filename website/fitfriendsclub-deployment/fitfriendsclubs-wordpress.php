<?php
/**
 * Plugin Name: FitFriendsClubs Integration
 * Plugin URI: https://fitfriendsclub-api.darnellroy2.workers.dev
 * Description: Complete WordPress integration for FitFriendsClubs API with clubs, trails, and dashboard functionality
 * Version: 1.0.0
 * Author: FitFriendsClubs
 * License: GPL v2 or later
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

class FitFriendsClubsPlugin {
    
    public function __construct() {
        add_action('init', array($this, 'init'));
        add_action('wp_enqueue_scripts', array($this, 'enqueue_scripts'));
        add_action('admin_menu', array($this, 'admin_menu'));
        register_activation_hook(__FILE__, array($this, 'activate'));
        register_deactivation_hook(__FILE__, array($this, 'deactivate'));
    }
    
    public function init() {
        // Register shortcodes
        add_shortcode('fitfriendsclubs-dashboard', array($this, 'dashboard_shortcode'));
        add_shortcode('fitfriendsclubs-clubs', array($this, 'clubs_shortcode'));
        add_shortcode('fitfriendsclubs-trails', array($this, 'trails_shortcode'));
        add_shortcode('fitfriendsclubs-test', array($this, 'test_shortcode'));
    }
    
    public function enqueue_scripts() {
        // Enqueue CSS
        wp_enqueue_style('fitfriendsclubs-css', plugin_dir_url(__FILE__) . 'assets/fitfriendsclubs.css', array(), '1.0.0');
        
        // Enqueue JavaScript
        wp_enqueue_script('fitfriendsclubs-js', plugin_dir_url(__FILE__) . 'assets/fitfriendsclubs.js', array('jquery'), '1.0.0', true);
        
        // Localize script with AJAX URL and settings
        wp_localize_script('fitfriendsclubs-js', 'fitfriendsclubs_ajax', array(
            'ajax_url' => admin_url('admin-ajax.php'),
            'nonce' => wp_create_nonce('fitfriendsclubs_nonce'),
            'api_url' => get_option('fitfriendsclubs_api_url', 'https://fitfriendsclub-api.darnellroy2.workers.dev'),
            'debug_mode' => get_option('fitfriendsclubs_debug', '1'),
            'auto_load' => get_option('fitfriendsclubs_autoload', '1')
        ));
    }
    
    public function dashboard_shortcode($atts) {
        $atts = shortcode_atts(array(
            'auto_load' => 'true'
        ), $atts);
        
        ob_start();
        ?>
        <div id="fitfriendsclubs-dashboard-container" class="fitfriendsclubs-container">
            <div id="ff-loading-indicator" class="ff-loading" style="display:none;">
                <div class="ff-load"></div>
                <p>Loading dashboard...</p>
            </div>
            <div id="ff-dashboard-content">
                <h3>FitFriendsClubs Dashboard</h3>
                <div id="ff-status-display" class="ff-status-container">
                    <span id="ff-connection-status">Connecting...</span>
                </div>
                <button id="ff-test-button" class="button button-primary">Test API Connection</button>
                <div id="ff-test-results" class="ff-results"></div>
                <div id="ff-dashboard-stats">
                    <div class="ff-stat-card">
                        <h4>System Status</h4>
                        <div id="ff-system-status">Checking...</div>
                    </div>
                    <div class="ff-stat-card">
                        <h4>Total Clubs</h4>
                        <div id="ff-club-count">Loading...</div>
                    </div>
                    <div class="ff-stat-card">
                        <h4>Total Trails</h4>
                        <div id="ff-trail-count">Loading...</div>
                    </div>
                </div>
            </div>
        </div>
        <script>
        jQuery(document).ready(function($) {
            if (typeof window.FitFriendsClubs !== 'undefined') {
                window.FitFriendsClubs.initDashboard();
            }
        });
        </script>
        <?php
        return ob_get_clean();
    }
    
    public function clubs_shortcode($atts) {
        $atts = shortcode_atts(array(
            'limit' => '10',
            'show_details' => 'true'
        ), $atts);
        
        ob_start();
        ?>
        <div id="fitfriendsclubs-clubs-container" class="fitfriendsclubs-container">
            <div id="ff-clubs-loading" class="ff-loading" style="display:none;">
                <div class="ff-load"></div>
                <p>Loading clubs...</p>
            </div>
            <div id="ff-clubs-content">
                <h3>Fitness Clubs</h3>
                <div id="ff-clubs-list" class="ff-clubs-grid"></div>
            </div>
        </div>
        
        <!-- Club Details Modal -->
        <div id="ff-club-modal" class="ff-modal" style="display:none;">
            <div class="ff-modal-content">
                <span class="ff-close" id="ff-club-close">&times;</span>
                <h3 id="ff-club-title">Club Details</h3>
                <div id="ff-club-details">
                    <p><strong>Category:</strong> <span id="ff-club-category"></span></p>
                    <p><strong>Equipment:</strong> <span id="ff-club-equipment"></span></p>
                    <p><strong>Location:</strong> <span id="ff-club-location"></span></p>
                    <p><strong>Members:</strong> <span id="ff-club-members"></span></p>
                    <div id="ff-club-description"></div>
                </div>
            </div>
        </div>
        
        <script>
        jQuery(document).ready(function($) {
            if (typeof window.FitFriendsClubs !== 'undefined') {
                window.FitFriendsClubs.loadClubs(<?php echo intval($atts['limit']); ?>);
            }
        });
        </script>
        <?php
        return ob_get_clean();
    }
    
    public function trails_shortcode($atts) {
        $atts = shortcode_atts(array(
            'limit' => '10',
            'difficulty' => 'all'
        ), $atts);
        
        ob_start();
        ?>
        <div id="fitfriendsclubs-trails-container" class="fitfriendsclubs-container">
            <div id="ff-trails-loading" class="ff-loading" style="display:none;">
                <div class="ff-load"></div>
                <p>Loading trails...</p>
            </div>
            <div id="ff-trails-content">
                <h3>Virtual Trails</h3>
                <div id="ff-trails-list" class="ff-trails-grid"></div>
            </div>
        </div>
        
        <!-- Trail Details Modal -->
        <div id="ff-trail-modal" class="ff-modal" style="display:none;">
            <div class="ff-modal-content">
                <span class="ff-close" id="ff-trail-close">&times;</span>
                <h3 id="ff-trail-title">Trail Details</h3>
                <div id="ff-trail-details">
                    <p><strong>Location:</strong> <span id="ff-trail-location"></span></p>
                    <p><strong>Difficulty:</strong> <span id="ff-trail-difficulty" class="ff-badge"></span></p>
                    <p><strong>Distance:</strong> <span id="ff-trail-distance"></span></p>
                    <p><strong>Est. Time:</strong> <span id="ff-trail-time"></span></p>
                    <p><strong>Elevation:</strong> <span id="ff-trail-elevation"></span></p>
                    <div id="ff-trail-description"></div>
                </div>
            </div>
        </div>
        
        <script>
        jQuery(document).ready(function($) {
            if (typeof window.FitFriendsClubs !== 'undefined') {
                window.FitFriendsClubs.loadTrails(<?php echo intval($atts['limit']); ?>, '<?php echo esc_js($atts['difficulty']); ?>');
            }
        });
        </script>
        <?php
        return ob_get_clean();
    }
    
    public function test_shortcode($atts) {
        ob_start();
        ?>
        <div id="fitfriendsclubs-test-container" class="fitfriendsclubs-container">
            <h3>FitFriendsClubs API Test</h3>
            <button id="ff-run-test" class="button button-primary">Run Full Test</button>
            <div id="ff-test-output" class="ff-test-results"></div>
        </div>
        
        <script>
        jQuery(document).ready(function($) {
            jQuery('#ff-run-test').on('click', function() {
                if (typeof window.FitFriendsClubs !== 'undefined') {
                    window.FitFriendsClubs.runTest();
                }
            });
        });
        </script>
        <?php
        return ob_get_clean();
    }
    
    public function admin_menu() {
        add_options_page(
            'FitFriendsClubs Settings',
            'FitFriendsClubs',
            'manage_options',
            'fitfriendsclubs-settings',
            array($this, 'admin_page')
        );
    }
    
    public function admin_page() {
        if (isset($_POST['submit'])) {
            update_option('fitfriendsclubs_api_url', sanitize_url($_POST['api_url']));
            update_option('fitfriendsclubs_debug', sanitize_text_field($_POST['debug_mode']));
            update_option('fitfriendsclubs_autoload', sanitize_text_field($_POST['auto_load']));
            echo '<div class="notice notice-success"><p>Settings saved!</p></div>';
        }
        
        $api_url = get_option('fitfriendsclubs_api_url', 'https://fitfriendsclub-api.darnellroy2.workers.dev');
        $debug_mode = get_option('fitfriendsclubs_debug', '1');
        $auto_load = get_option('fitfriendsclubs_autoload', '1');
        ?>
        <div class="wrap">
            <h1>FitFriendsClubs Settings</h1>
            <form method="post" action="">
                <table class="form-table">
                    <tr>
                        <th scope="row">API URL</th>
                        <td><input type="url" name="api_url" value="<?php echo esc_attr($api_url); ?>" class="regular-text" /></td>
                    </tr>
                    <tr>
                        <th scope="row">Debug Mode</th>
                        <td>
                            <select name="debug_mode">
                                <option value="1" <?php selected($debug_mode, '1'); ?>>Enabled</option>
                                <option value="0" <?php selected($debug_mode, '0'); ?>>Disabled</option>
                            </select>
                        </td>
                    </tr>
                    <tr>
                        <th scope="row">Auto Load Content</th>
                        <td>
                            <select name="auto_load">
                                <option value="1" <?php selected($auto_load, '1'); ?>>Enabled</option>
                                <option value="0" <?php selected($auto_load, '0'); ?>>Disabled</option>
                            </select>
                        </td>
                    </tr>
                </table>
                <?php submit_button(); ?>
            </form>
            
            <h2>Shortcodes</h2>
            <p>Use these shortcodes to display FitFriendsClubs content:</p>
            <ul>
                <li><code>[fitfriendsclubs-dashboard]</code> - Dashboard with API status and stats</li>
                <li><code>[fitfriendsclubs-clubs limit="10"]</code> - Display fitness clubs</li>
                <li><code>[fitfriendsclubs-trails limit="8" difficulty="all"]</code> - Display virtual trails</li>
                <li><code>[fitfriendsclubs-test]</code> - API test interface</li>
            </ul>
            
            <h2>Test API Connection</h2>
            <button id="admin-test-api" class="button button-secondary">Test API</button>
            <div id="admin-test-results"></div>
            
            <script>
            jQuery(document).ready(function($) {
                $('#admin-test-api').on('click', function() {
                    var button = $(this);
                    button.prop('disabled', true).text('Testing...');
                    
                    $.ajax({
                        url: '<?php echo esc_js($api_url); ?>',
                        method: 'GET',
                        timeout: 10000,
                        success: function(response) {
                            $('#admin-test-results').html('<div class="notice notice-success"><p>✅ API Connection Successful!</p></div>');
                        },
                        error: function() {
                            $('#admin-test-results').html('<div class="notice notice-error"><p>❌ API Connection Failed</p></div>');
                        },
                        complete: function() {
                            button.prop('disabled', false).text('Test API');
                        }
                    });
                });
            });
            </script>
        </div>
        <?php
    }
    
    public function activate() {
        // Set default options
        add_option('fitfriendsclubs_api_url', 'https://fitfriendsclub-api.darnellroy2.workers.dev');
        add_option('fitfriendsclubs_debug', '1');
        add_option('fitfriendsclubs_autoload', '1');
    }
    
    public function deactivate() {
        // Clean up if needed
    }
}

// Initialize the plugin
new FitFriendsClubsPlugin();
?>