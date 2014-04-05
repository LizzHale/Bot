$(document).ready( function(){
    $("li.quote").on("click", function(event) {
        quote = $(this).find('blockquote')[0].innerHTML
        $.ajax({
            url: "/classifiers/compare",
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
    $(".btn").on("click", function(event) {
        event.preventDefault();
        message = $("textarea").val();
        console.log(message)
        $.ajax({
            url: "/classifiers/stats",
            data: {stats:message},
            method: "POST"
        }).done(function(data) {
            console.log("server sent us: " + data);
            $("#fisher_submit").slideToggle();
            $("#fisher_details")[0].innerHTML = data;
            $("#fisher_details").slideToggle();
        }).fail(function(){
            console.log("you failed");
        })
    });
});