document.getElementById("crud").addEventListener("click", function() {
    goBack();
});

function goBack() {
    window.location.href = "{% url 'manage' %}";
}
