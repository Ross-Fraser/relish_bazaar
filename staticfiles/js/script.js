window.addEventListener('DOMContentLoaded', function() {
    alert("JavaScript is loaded correctly!");
});

window.addEventListener('DOMContentLoaded', function() {
    // Check if the current URL matches the Manage Products page
if (window.location.pathname === '/manage/') {
    alert("Manage Products page detected!");
    window.addEventListener('beforeunload', function (e) {
        var confirmationMessage = "Are you sure you want to leave this page?";
        e.preventDefault();
        e.returnValue = confirmationMessage; directly
        return confirmationMessage;
    });
}
});
