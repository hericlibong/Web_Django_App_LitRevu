// scripts.js

document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll('.toggleDescription').forEach(function(element) {
        element.addEventListener('click', function(event) {
            event.preventDefault();  // Empêcher le lien de ramener en haut de la page
            toggleDescription(this.getAttribute('data-index'));
        });
    });
    document.querySelectorAll('.toggleReview').forEach(function(element) {
        element.addEventListener('click', function(event) {
            event.preventDefault();  // Empêcher le lien de ramener en haut de la page
            toggleReview(this.getAttribute('data-index'));
        });
    });
});

function toggleDescription(index) {
    var shortText = document.getElementById('shortDescription' + index);
    var fullText = document.getElementById('fullDescription' + index);
    shortText.classList.toggle('collapse');
    fullText.classList.toggle('collapse');
}

function toggleReview(index) {
    var shortText = document.getElementById('shortReview' + index);
    var fullText = document.getElementById('fullReview' + index);
    shortText.classList.toggle('collapse');
    fullText.classList.toggle('collapse');
}

