$(document).ready( function(){
    $("button#next").on("click", function(event) {
        $("img").slideToggle();
        $("#example").slideToggle();
    });
    $(".classifier").on("click", function() {
        $("img").slideToggle();
        $("#description").slideToggle();
    });
});