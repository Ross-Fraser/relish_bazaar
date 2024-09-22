window.addEventListener('DOMContentLoaded', function() {
});

window.addEventListener('DOMContentLoaded', function() {
    // Check if the current URL matches the Manage Products page
if (window.location.pathname === '/manage/') {
    window.addEventListener('beforeunload', function (e) {
        var confirmationMessage = "Are you sure you want to leave this page?";
        return confirmationMessage;
    });
}
});
