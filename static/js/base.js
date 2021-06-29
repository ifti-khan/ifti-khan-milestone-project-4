$(document).ready(function () {
    // This is for the copyright year located in the footer 
    //and will auto update when the year date changes
    $("#copyright-footerYear").text(new Date().getFullYear());

    //This block of code is for floating scroll button located bottom right, 
    //so when a user scrolls down a certain amount it will become visible and 
    //if they scroll up a certain amount, the button will not be visible.
    let topButton = $('#back-to-top-btn');
    $(window).scroll(function () {
        if ($(window).scrollTop() > 50) {
            topButton.addClass('visible');
        } else {
            topButton.removeClass('visible');
        }
    });

    //This is part of the floating scroll button, so when a user clicks the button 
    //it will take the user back to the top of the page.
    topButton.on('click', function (event) {
        event.preventDefault();
        $('html, body').scrollTop(0);
    });

});