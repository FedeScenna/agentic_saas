// Main JavaScript file for Business Insights SaaS Platform

// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide flash messages after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Copy API key to clipboard
    var copyApiKeyBtn = document.getElementById('copy-api-key');
    if (copyApiKeyBtn) {
        copyApiKeyBtn.addEventListener('click', function() {
            var apiKeyInput = document.getElementById('api-key');
            apiKeyInput.select();
            document.execCommand('copy');
            
            // Show copied message
            var originalText = this.innerHTML;
            this.innerHTML = '<i class="fas fa-check"></i> Copied!';
            this.classList.remove('btn-outline-primary');
            this.classList.add('btn-success');
            
            // Reset button after 2 seconds
            setTimeout(function() {
                copyApiKeyBtn.innerHTML = originalText;
                copyApiKeyBtn.classList.remove('btn-success');
                copyApiKeyBtn.classList.add('btn-outline-primary');
            }, 2000);
        });
    }

    // Toggle password visibility
    var togglePasswordBtns = document.querySelectorAll('.toggle-password');
    togglePasswordBtns.forEach(function(btn) {
        btn.addEventListener('click', function() {
            var passwordInput = document.querySelector(this.getAttribute('data-target'));
            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
                this.innerHTML = '<i class="fas fa-eye-slash"></i>';
            } else {
                passwordInput.type = 'password';
                this.innerHTML = '<i class="fas fa-eye"></i>';
            }
        });
    });

    // Confirm deletion modals
    var confirmDeleteBtns = document.querySelectorAll('[data-confirm="true"]');
    confirmDeleteBtns.forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    });
}); 