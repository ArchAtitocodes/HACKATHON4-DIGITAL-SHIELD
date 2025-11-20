/**
 * Client-Side Session Manager
 * Handles session expiry warnings and cleanup
 * Privacy-focused: No data stored in localStorage
 */

'use strict';

(function() {
    // Session configuration
    const SESSION_TIMEOUT = 5 * 60 * 1000; // 5 minutes in milliseconds
    const WARNING_TIME = 60 * 1000; // Warn 1 minute before expiry
    
    let lastActivityTime = Date.now();
    let timeoutWarningShown = false;
    let sessionTimer = null;
    let warningTimer = null;
    
    /**
     * Initialize session monitoring
     */
    function initializeSession() {
        // Track user activity
        const activityEvents = ['mousedown', 'keydown', 'scroll', 'touchstart'];
        activityEvents.forEach(event => {
            document.addEventListener(event, resetSessionTimer, { passive: true });
        });
        
        // Start session timers
        startSessionTimers();
        
        // Handle page unload (clear session)
        window.addEventListener('beforeunload', handlePageUnload);
    }
    
    /**
     * Start session expiry timers
     */
    function startSessionTimers() {
        clearSessionTimers();
        
        // Set warning timer (4 minutes)
        warningTimer = setTimeout(() => {
            showTimeoutWarning();
        }, SESSION_TIMEOUT - WARNING_TIME);
        
        // Set session expiry timer (5 minutes)
        sessionTimer = setTimeout(() => {
            endSession();
        }, SESSION_TIMEOUT);
    }
    
    /**
     * Clear all session timers
     */
    function clearSessionTimers() {
        if (sessionTimer) {
            clearTimeout(sessionTimer);
            sessionTimer = null;
        }
        if (warningTimer) {
            clearTimeout(warningTimer);
            warningTimer = null;
        }
    }
    
    /**
     * Reset session timer on user activity
     */
    function resetSessionTimer() {
        lastActivityTime = Date.now();
        timeoutWarningShown = false;
        hideTimeoutWarning();
        startSessionTimers();
    }
    
    /**
     * Show timeout warning to user
     */
    function showTimeoutWarning() {
        if (timeoutWarningShown) return;
        
        timeoutWarningShown = true;
        
        // Only show warning on chatbot page
        if (window.location.pathname === '/chatbot') {
            const statusText = document.getElementById('status-text');
            if (statusText) {
                statusText.textContent = 'Session expiring in 1 minute - Click anywhere to continue';
                statusText.style.color = '#f59e0b';
            }
        }
    }
    
    /**
     * Hide timeout warning
     */
    function hideTimeoutWarning() {
        if (!timeoutWarningShown) return;
        
        if (window.location.pathname === '/chatbot') {
            const statusText = document.getElementById('status-text');
            if (statusText) {
                statusText.textContent = 'Safe, private guidance';
                statusText.style.color = '';
            }
        }
    }
    
    /**
     * End session due to inactivity
     */
    function endSession() {
        // Call API to end session
        fetch('/api/chatbot/end', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        }).catch(() => {
            // Fail silently - privacy is maintained regardless
        });
        
        // Redirect to home with message
        if (window.location.pathname === '/chatbot') {
            alert('Your session has ended due to inactivity. This protects your privacy.');
            window.location.href = '/';
        }
    }
    
    /**
     * Handle page unload - clear session
     */
    function handlePageUnload() {
        if (window.location.pathname === '/chatbot') {
            // Send beacon to end session (non-blocking)
            if (navigator.sendBeacon) {
                navigator.sendBeacon('/api/chatbot/end');
            }
        }
    }
    
    /**
     * Explicitly end session (called by end button)
     */
    window.endChatbotSession = function() {
        clearSessionTimers();
        
        fetch('/api/chatbot/end', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(() => {
            window.location.href = '/';
        })
        .catch(() => {
            window.location.href = '/';
        });
    };
    
    // Initialize on page load
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initializeSession);
    } else {
        initializeSession();
    }
})();