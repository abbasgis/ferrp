/**
 * Created by Shakir on 1/1/2019.
 */

var SideNavManager = function () {
    var me = this;
    me.manageSections = function (section) {
        if (section === '') {
            section = 1
        } else {
            section = parseInt(section);
        }
        var section1 = $("#section-one");
        var section2 = $("#section-two");
        if (section === 1) {
            section2.hide();
            section1.show();
        } else if (section === 2) {
            section1.hide();
            section2.show();
        }
        section1.click(function () {
            section2.hide();
            section1.show();
        });
        section2.click(function () {
            section1.hide();
            section2.show();
        });
        var lat = 31.550243;
        var long = 74.352940;
        var url = 'https://maps.google.com/maps?q=' + lat + ',' + long + '&t=&z=13&ie=UTF8&iwloc=&output=embed';
        var el = document.getElementById('gmap_canvas');
        if(el){
         el.src = url;
        }

    }
};

