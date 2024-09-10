// Declare the variable only once
let deleteProductId = null;

// Correctly set deleteProductId to the provided productId
function showDeleteConfirmation(productId) {
    deleteProductId = productId;
    document.getElementById('delete-confirmation').style.display = 'block';
}

// Function to handle the cancellation of the delete action
function cancelDelete() {
    deleteProductId = null;
    document.getElementById('delete-confirmation').style.display = 'none';
}
