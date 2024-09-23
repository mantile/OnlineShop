document.addEventListener("DOMContentLoaded", function() {
    var menu = document.querySelector('.main-menu');
    var sticky = menu.offsetTop;

    function checkScroll() {
        if (window.pageYOffset > sticky) {
            menu.classList.add("fixed");
        } else {
            menu.classList.remove("fixed");
        }
    }

    // Привязка обработчика события прокрутки
    document.addEventListener("scroll", checkScroll);
});