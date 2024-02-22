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

document.addEventListener('DOMContentLoaded', function () {
    var navToggle = document.getElementById('navToggle');
    var navMenu = document.querySelector('.nav-menu');

    navToggle.addEventListener('click', function () {
        this.classList.toggle('is-active');
        navMenu.classList.toggle('nav-menu-open'); // Use a class to control the state
    });
});

