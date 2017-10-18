$(document).ready(function () {
    $("#about-btn").click(function (event) {
        var msg_element = $("#msg");
        var msgstr = msg_element.html();
        msgstr = msgstr + "ooo";
        msg_element.html(msgstr);
    });
});

$(document).ready(function () {
    $("#about-btn").hover(function () {
        $(this).addClass('btn-primary')
    },
    function () {
        $(this).removeClass('btn-primary')
    });
});

$(document).ready(
    function () {
        $("p").hover(
            function () {
                $(this).css('color', 'red');
            },
            function () {
                $(this).css('color', 'blue');
            });
    });
