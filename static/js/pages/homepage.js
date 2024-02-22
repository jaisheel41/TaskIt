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

document.addEventListener('DOMContentLoaded', function () {
    var navToggle = document.getElementById('navToggle');
    if(navToggle) {
        navToggle.addEventListener('click', function () {
            var navMenu = document.querySelector('.nav-menu');
            if (navMenu.style.display === "none" || navMenu.style.display === "") {
                navMenu.style.display = "block";
            } else {
                navMenu.style.display = "none";
            }
        });
    }
});
