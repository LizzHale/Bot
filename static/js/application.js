$(document).ready( function(){
    $("li.quote").on("click", function(event) {
        quote = $(this).find('blockquote')[0].innerHTML
        
        console.log("you clicked on this quote: " + quote)
        $.ajax({
            url: "/classifiers",
            data: {message:quote},
            method: "POST"
        }).done(function(data) {
            console.log("server sent us: " + data);
            $("#choices").slideToggle();
            $("#retrieved")[0].innerHTML = data;
            $("#retrieved").slideToggle();
        }).fail(function() {
            console.log("you failed")
        })
    });
    $("#retrieved").on("click", function() {
        $("#choices").slideToggle();
        $("#retrieved").slideToggle();
    });
});