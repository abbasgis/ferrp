// this function execute when the choropleth style dialogue loads
$('#choropleth_map').on('click', function () {

    var params = {
        url: layer_columns_names,
        type: "POST",
        data: {'layername': layertype},
        dataType: 'json',
        headers: {'X-CSRFToken': token}
    };

    callAJAX(params, function (response) {

        // alert(response);

        if (response.length != 0) {

            $('#column_name').empty();
            $('#column_name').append('<option value="" selected="selected" disabled="disabled">Select a Column</option>');

            $.each(response, function (index, item) {
                $('#column_name').append('<option value=' + item.column_name + ' >'
                    + item.column_name + '</option>');
            });
            $('#chloropethmap').modal('show');
        }
        else {
            $('#msg_model_head').empty();
            $('#msg_model_head').append('<h3 class="modal-title">No Result Found</h3>');
            $('#msg_model_head').css("background-color", "#FF5555");
            $('#msg_model_body').empty();
            $('#msg_model_body').append('No Result Found from this layer');
            $('#msg_model').modal('show');
        }
    });
});

// this function execute when Column Name is selected from the dropdownlist

$('#column_name').on('change', function () {
    // alert( this.value );
    var params = {
        url: get_columns_names,
        type: "POST",
        data: {'layername': layertype, 'col_name': this.value},
        dataType: 'json',
        headers: {'X-CSRFToken': token}
    };

    callAJAX(params, function (response) {
        //alert(response);
        $("#set_cloro_prop").prop('disabled', false);
        $("#chloro_submit").prop('disabled', false);
        $('#max').val(response[0].maximum);
        $('#min').val(response[0].minimum);

    })
});

// this function execute when the choropleth style dialogue submits.
$('#chloro_submit').on('click', function () {

    data_max = parseInt($('#max').val());
    data_min = parseInt($('#min').val());
    var high_val = $('#high').val();
    var mid_val = $('#mid').val();
    var low_val = $('#low').val();
    var no_of_classes = $('#colorful').val();
    color_arr = [];
    classes_arr = [];

    var colors = [high_val, mid_val, low_val];
    steps = parseInt(no_of_classes);
    var grad = tinygradient(colors);

    // intval = (max - min)/ (cls);
    var interval = Math.round((data_max - data_min) / no_of_classes);

    grad.rgb(steps + 1).forEach(function (color) {
        color_arr.push(color.toHexString());
    });


    var params = {
        url: get_chloropeth_geojson,
        type: "POST",
        data: {'layername': layertype},
        dataType: 'json',
        headers: {'X-CSRFToken': token}
    };

    callAJAX(params, function (response) {
        // alert(response);
        // response["chloro_geojson"]
        if (response != []) {
            if (edmap.hasLayer(LandView.baselayer)) {
                edmap.removeLayer(LandView.baselayer);
            }


            for (var i = 0; i < steps; i++) {
                if (classes_arr.length == 0) {
                    val = data_max;
                    classes_arr.push(val);
                }
                val = val - interval;
                classes_arr.push(val);
            }


            LandView.baselayer = L.geoJson(response["chloro_geojson"], {
                style: LandView.new_style
                // onEachFeature: onEachFeature
            }).addTo(edmap);

            LandView.create_legend();
            $('#chloropethmap').modal('hide');
        }

    });
});




  me.new_style = function (feature) {

        return {
            weight: 2,
            opacity: 1,
            color: 'white',
            dashArray: '3',
            fillOpacity: 0.7,
            fillColor: me.get_Color(feature.properties.pop_density, color_arr)
            //fillColor: function(feature){}
        };
    }
    me.get_Color = function (d, color_arr) {


        for (var k = 0; k < steps + 1; k++) {

            if (d >= classes_arr[k]) {
                return color_arr[k];
                break;
            }
        }
        if (d < 10) {
            return '#000000'
        }

    }
    me.create_legend = function () {


        if (legend != '') {
            edmap.removeControl(legend);
        }


        legend = '';
        legend = L.control({position: 'bottomright'});
        legend.onAdd = function (map) {

            var div = L.DomUtil.create('div', 'info legend'),
                grades = classes_arr,
                labels = [],
                from, to;

            for (var i = 0; i < grades.length; i++) {
                from = grades[i];
                to = grades[i + 1];

                labels.push(
                    '<i style="background:' + me.get_Color(from + 1, color_arr) + '"></i> ' +
                    from + (to ? '&ndash;' + to : '+'));
            }

            div.innerHTML = labels.join('<br>');
            return div;
        };

        legend.addTo(edmap);

    }
