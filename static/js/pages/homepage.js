// document.addEventListener('DOMContentLoaded', function () {
//     document.getElementById('navToggle').addEventListener('click', function () {
//         var navMenu = document.querySelector('.nav-menu');
//         if (navMenu.style.display === "none" || navMenu.style.display === "") {
//             navMenu.style.display = "block";
//         } else {
//             navMenu.style.display = "none";
//         }
//     });
// });

// document.addEventListener('DOMContentLoaded', function () {
//     var navToggle = document.getElementById('navToggle');
//     var navMenu = document.querySelector('.nav-menu');

//     navToggle.addEventListener('click', function () {
//         // Toggle the active state of the hamburger
//         this.classList.toggle('is-active');

//         // Toggle the nav menu
//         if (navMenu.style.transform === "translateX(0px)") {
//             navMenu.style.transform = "translateX(-100%)";
//         } else {
//             navMenu.style.transform = "translateX(0px)";
//         }
//     });
// });

// document.addEventListener('DOMContentLoaded', function () {
//     var navToggle = document.getElementById('navToggle');
//     var navMenu = document.querySelector('.nav-menu');

//     navToggle.addEventListener('click', function () {
//         // Toggle the active state of the hamburger
//         this.classList.toggle('is-active');

//         // Check if the navMenu is visible
//         if (navMenu.style.right === "0px" || navMenu.style.right === "") {
//             // Move the navMenu off-screen to the right
//             navMenu.style.right = "-250px";
//         } else {
//             // Move the navMenu to be flush with the right edge of the viewport
//             navMenu.style.right = "0px";
//         }
//     });
// });

// document.getElementById('toggleNav').addEventListener('click', function() {
//     document.getElementById('navMenu').classList.add('active');
// });
// document.getElementById('closeNav').addEventListener('click', function() {
//     document.getElementById('navMenu').classList.remove('active');
// });

// const toggleNav = document.getElementById('toggleNav');
// const navMenu = document.getElementById('navMenu');

// toggleNav.addEventListener('click', function() {
//     navMenu.classList.toggle('active');
//     // Toggle button icon between hamburger and 'X'
//     toggleNav.children[0].innerHTML = navMenu.classList.contains('active') ? '&times;' : '&#x2630;';
// });

// function toggleNav() {
//     const navMenu = document.getElementById('navMenu');
//     const toggleNavIcon = document.querySelector('.nav-toggle-icon');

//     // Check if the menu is currently active
//     const isMenuActive = navMenu.classList.contains('active');

//     // Toggle the active class on the nav menu
//     navMenu.classList.toggle('active');

//     // Change the toggle icon from hamburger to 'X' and vice versa
//     toggleNavIcon.textContent = isMenuActive ? '\u2630' : '\u00D7'; // Hamburger or 'X'
// }

// // Event listener for the toggle button
// document.getElementById('toggleNav').addEventListener('click', toggleNav);

// // Optional: Event listener for closing the menu by clicking the 'X'
// document.getElementById('closeNav').addEventListener('click', toggleNav);

document.addEventListener('DOMContentLoaded', function() {
    var toggleNav = document.getElementById('toggleNav');
    if (toggleNav) {
        toggleNav.addEventListener('click', function() {
            // Your toggle code here
            var navMenu = document.getElementById('navMenu');
            navMenu.classList.toggle('active');
            // Change the content of the toggle button appropriately
            this.textContent = navMenu.classList.contains('active') ? '×' : '☰';
        });
    } else {
        console.error('Element with ID "toggleNav" was not found.');
    }
});





