$(document).ready( function(){
    $("li.quote").on("click", function(event) {
        quote = $(this).find('blockquote')[0].innerHTML
        $("#choices").slideToggle();
        $("#quote_loading").slideToggle();
        $.ajax({
            url: "/classifiers/compare",
            data: {message:quote},
            method: "POST"
        }).done(function(data) {
            console.log("server sent us: " + data);
            $("#retrieved")[0].innerHTML = data;
            $("#quote_loading").slideToggle();
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
        $("#fisher_submit").slideToggle();
        $("#stats_loading").slideToggle();
        $.ajax({
            url: "/classifiers/stats",
            data: {stats:message},
            method: "POST"
        }).done(function(data) {
            console.log("server sent us: " + data);
            $("#fisher_details")[0].innerHTML = data;
            $("#stats_loading").slideToggle();
            $("#fisher_details").slideToggle();
        }).fail(function(){
            console.log("you failed");
        })
    });
    $("#fisher_details").on("click", function() {
        $("#fisher_submit").slideToggle();
        $("#fisher_details").slideToggle();
    });
});