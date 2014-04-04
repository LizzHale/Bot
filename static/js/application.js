$(document).ready( function(){
    $("li.quote").on("click", function(event) {
        $("#choices").slideToggle();
        $("#retrieved").slideToggle();
    });
    $("#retrieved").on("click", function() {
        $("#choices").slideToggle();
        $("#retrieved").slideToggle();
    });
});