var logSent = false;

// Collect browser and OS information using UAParser.js
var parser = new UAParser();
var result = parser.getResult();

var browserInfo = {
    userAgent: navigator.userAgent,
    browserName: result.browser.name || 'Unknown Browser',
    browserVersion: result.browser.version || 'Unknown Version',
    platform: result.os.name + " " + result.os.version || 'Unknown Platform',
    device: result.device.model || 'Unknown Device',
    plugins: [],
    user_id: ''  // We'll set this after fetching the user_id cookie
};

// Collect plugins information
for (var i = 0; i < navigator.plugins.length; i++) {
    browserInfo.plugins.push(navigator.plugins[i].name);
}

// Get the user_id from cookies
var userIdCookie = document.cookie.split('; ').find(row => row.startsWith('user_id='));
if (userIdCookie) {
    browserInfo.user_id = userIdCookie.split('=')[1];
} else {
    browserInfo.user_id = 'Unknown User';
}

console.log("Collected browser info: ", browserInfo);

if (!logSent) {
    fetch('/log_browser_info', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(browserInfo)
    })
    .then(() => {
        logSent = true;  // Set logSent to true to prevent further logs
        console.log("Browser info logged successfully.");
    })
    .catch(error => {
        console.error('Error logging browser info:', error);
    });
}
function saveAssignments() {
    var assignments = [];
    $('#logTableBody select').each(function() {
        var logId = $(this).data('log-id');
        var selectedModuleIds = $(this).val() || [];
        assignments.push({ logId: logId, moduleIds: selectedModuleIds });
    });

    $.ajax({
        url: '/assign_modules',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(assignments),
        success: function(response) {
            if (response.success) {
                console.log("Assignments saved successfully.");
                $('#successMessage').show().delay(3000).fadeOut();
            } else {
                console.log("Duplicate log detected, not saved.");
                $('#errorMessage').text(response.message).show().delay(3000).fadeOut();
            }
        }
    });
}
