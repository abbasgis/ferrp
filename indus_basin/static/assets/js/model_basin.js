/**
 * Created by Shakir on 9/10/2018.
 */
/**
 * Created by Shakir on 2/13/2018.
 */
(function ($) {
    function fix_actions() {
        // $('.addlink').find('a').prop("href", "https://stackoverflow.com/");
        // $('.addlink').find('a').removeAttr("href");
        $(".addlink").on('click', function (event) {
            window.location.href = '/layers/upload/shp/?action=existing';
            return false;
            //(... rest of your JS code)
        });

        // $('.addlink').find('a').attr('href', '/admin/');
    };

    $(function () {
        fix_actions();
    });
})(django.jQuery);