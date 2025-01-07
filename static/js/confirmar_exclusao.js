let deleteUrl = "";

function showDeleteToast(url) {
    deleteUrl = url;
    const toastElement = document.getElementById('deleteToast');
    const toast = new bootstrap.Toast(toastElement);
    toast.show();
}

document.getElementById('confirmDeleteBtn').addEventListener('click', function () {
    if (deleteUrl) {
        window.location.href = deleteUrl;
    }
});