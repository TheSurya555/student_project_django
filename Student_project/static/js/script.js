// JavaScript to change navbar background on scroll
window.addEventListener('scroll', function() {
    var navbar = document.querySelector('.nav');
    if (window.scrollY > 50) { // Adjust the scroll value to your preference
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});
