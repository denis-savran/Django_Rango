$(document).ready(function () {
    $('#like').click(function (event) {
        var cat_id = $(this).attr("data-cat_id");
        $.get('/rango/like_category/', {category_id: cat_id}, function (data) {
            $('#like_count').html(data);
            $('#like').hide();
        });
    });
});

$(document).ready(function () {
    $('#search-category').keyup(function () {
        var category_list, query;
        category_list = $('#side-bar-categories');

        query = $(this).val();
        if (query.length > 0) {
            $.get('/rango/suggest_category/', {starts_with: query}, function (data) {
                category_list.html(data);
            });
        }
        else {
            $.get('/rango/suggest_category/', function (data) {
                category_list.html(data);
            });
        }
    });
});

$(document).ready(function () {
    $('#search-input').keyup(function () {
        var search_suggestions, query;
        search_suggestions = $('#search-suggestions');

        query = $(this).val();
        if (query.length > 0) {
            $.get('/rango/suggest_search/', {q: query}, function (data) {
                search_suggestions.html(data);
                search_suggestions.show()
            });
        }
        else {
            search_suggestions.fadeOut('fast');
        }
    });
});

$(document).ready(function () {
    var search_input, suggestions, query;
    search_input = $('#search-input');
    suggestions = $('#search-suggestions');

    search_input.on('blur', function () {
        suggestions.fadeOut('fast');
    });
    search_input.on('focus', function () {
        query = search_input.val();
        if (query.length > 0) {
            suggestions.show()
        }
    });
    suggestions.hide()
});
