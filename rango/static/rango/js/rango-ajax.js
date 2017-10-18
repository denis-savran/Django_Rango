$(document).ready(function () {
    $('#like').click(function (event) {
        var cat_id = $(this).attr("data-cat_id");
        $.get('/rango/like_category/', {category_id: cat_id}, function (data) {
            $('#like_count').html(data);
            $('#like').hide();
        });
    });
});