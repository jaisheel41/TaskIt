document.addEventListener('DOMContentLoaded', function() {
    var toggleNav = document.getElementById('toggleNav');
    if (toggleNav) {
        toggleNav.addEventListener('click', function() {
            
            var navMenu = document.getElementById('navMenu');
            navMenu.classList.toggle('active');
            // the content of the toggle button
            this.textContent = navMenu.classList.contains('active') ? '×' : '☰';
        });
    } else {
        console.error('Element with ID "toggleNav" was not found.');
    }
});





