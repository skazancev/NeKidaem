(function () {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $(document).ready(function (e) {

        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });
        $('.nav-link[href="' + location.pathname + '"]').addClass('active');
        $('.mark_read').click(function (e) {
            e.preventDefault();
            var self = this;
            $.ajax({
                url: '/blog/read/',
                type: 'post',
                data: {post_id: $(self).data('post')},
                success: function (data) {
                    if (data.status === 'ok') {
                        $(self).replaceWith('<span class="badge badge-secondary">Прочитано</span>')
                    }
                }
            })
        });
    });
})($);