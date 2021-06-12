
var mytoken;

function populateComboBox(sectors, scheme_names, token, user) {
    mytoken = token;
    if (user) {
        $('#row_radio').css("display", 'block');
    }
    $("#frmDetail :input").prop("disabled", true);
    for (var key in sectors) {
        $('#cmb_sectors').append('<option value=' + sectors[key].sec_id + ' >'
            + sectors[key].sec_name + '</option>');
    }
    $('#cmb_scheme').on('change', function (e) {
        $("#btnGet").prop('disabled', false);
    });
    $(".rButton").change(function () {
        switch ($(this).val()) {
            case 'view' :
                $('#cmb_scheme').empty();
                populateSectorData(true);
                enableDisableElements('view');
                break;
            case 'create' :
                enableDisableElements('create');
                break;
        }
    });
}

function enableDisableElements(checkBox) {
    if (checkBox == 'view') {
        $('#row_info_required').css("display", 'none');
        $('#rowAddNewScheme').css("display", "none");
        $("#s_name").prop('disabled', true);
        $("#gs_no").prop('disabled', true);
        $("#s_type").prop('disabled', true);
        $("#district").prop('disabled', true);
        $("#tehsil").prop('disabled', true);
        $("#main_sector").prop('disabled', true);
        $("#sec_name").prop('disabled', true);
        $("#approval_date").prop('disabled', true);
        $("#local_capital").prop('disabled', true);
        $("#revenue_total").prop('disabled', true);
        $("#allocation").prop('disabled', true);
        $("#exp_upto_june").prop('disabled', true);
        $("#foreign_aid").prop('disabled', true);
    } else {
        $('#row_info_required').css("display", "block");
        $('#rowAddNewScheme').css("display", "block");
        $('#btnWorkPlan').css("display", "none");
        $("#s_name").prop('disabled', false);
        $("#gs_no").prop('disabled', false);
        $("#s_type").prop('disabled', false);
        $("#district").prop('disabled', false);
        $("#tehsil").prop('disabled', false);
        $("#main_sector").prop('disabled', false);
        $("#sec_name").prop('disabled', false);
        $("#approval_date").prop('disabled', false);
        $("#local_capital").prop('disabled', false);
        $("#revenue_total").prop('disabled', false);
        $("#allocation").prop('disabled', false);
        $("#exp_upto_june").prop('disabled', false);
        $("#foreign_aid").prop('disabled', false);
    }
}

function populateSectorData(rbc) {
    $.get('/pp/getSectorNames?rbc=' + rbc, function (data) {
        data = JSON.parse(data);
        $('#cmb_sectors').empty();
        $('#cmb_sectors').append('<option> Select Sector. .</option>');
        for (var i = 0; i < data.length; i++) {
            $('#cmb_sectors').append('<option value=' + data[i].sec_id + ' >'
                + data[i].sec_name + '</option>');
        }
        $('.selectpicker').selectpicker('refresh');
    });
}

function uploadValues(data, url) {
    var request = $.ajax({
        url: url,
        type: 'post',
        dataType: "json",
        data: data
    });
    request.done(function (response) {
        if (response.message == 200) {
            var host = window.location.host;
            var port = window.location.port;
            var url = 'basic_info/?scheme=' + data.scheme_id;
            window.location.href = url
        } else if (response.message == 500) {
            alert('Failed to create Plan, Please Try Again Later or report the error to ferrp');
        } else {
            alert('Work Plan of this scheme does not exist, Please logIn to create workplan of this scheme');
        }
    });
    request.fail(function (jqXHR, textStatus) {
        alert("Request failed: " + textStatus);
    });
}

$("#btnAddNewScheme").click(function (event) {
    var params = {
        csrfmiddlewaretoken: mytoken,
        state: "inactive",
        'scheme_id': $("#gs_no").val(),
        's_name': $("#s_name").val(),
        'end_date': $("#end_date").val(),
        'start_date': $("#start_date").val(),
        'cost_total': $("#cost_total").val(),
        's_type': $("#s_type").val(),
        'district': $("#district").val(),
        'tehsil': $("#tehsil").val(),
        'main_sector': $("#main_sector").val(),
        'sec_name': $("#sec_name").val(),
        'approval_date': $("#approval_date").val(),
        'local_capital': $("#local_capital").val(),
        'revenue_total': $("#revenue_total").val(),
        'allocation': $("#allocation").val(),
        'exp_upto_june': $("#exp_upto_june").val(),
        'foreign_aid': $("#foreign_aid").val(),
    };
});

$("#btnWorkPlan").click(function (event) {
    $("#btnWorkPlan").prop('disabled', false);
    var rb_create = document.getElementById("rb_create");
    var rb_view = document.getElementById("rb_view");
    if (rb_create.checked) {
        $("s_name").addClass('disabled', false);
    }
    else if (rb_view.checked) {
        var scheme_id = $('#cmb_scheme option:selected').val();
        var params = {
            'scheme_id': scheme_id,
            csrfmiddlewaretoken: mytoken,
            state: "inactive",
            's_name': $("#s_name").val(),
            'end_date': $("#end_date").val(),
            'start_date': $("#start_date").val(),
            'cost_total': $("#cost_total").val(),
        };
        uploadValues(params, 'view_scheme_plan/');
    }

});

$('#cmb_sectors').on('change', function (e) {
    var rbc = (document.getElementById("rb_view")).checked;
    var sct_id = e.target.value;
    $("#btnGet").prop('disabled', true);
    $.get('getSchemeNames?sector_id=' + sct_id + '&rbc=' + rbc, function (data) {
        data = JSON.parse(data);
        $('#cmb_scheme').empty();
        $('#cmb_scheme').append('<option> Select scheme</option>');
        for (var i = 0; i < data.length; i++) {
            $('#cmb_scheme').append('<option value=' + data[i].gs_no + ' >'
                + data[i].s_name + '</option>');
        }
        $('.selectpicker').selectpicker('refresh');
    });
});

$('#cmb_scheme').on('change', function (e) {
    var scheme_id = e.target.value;
    getSchemeDetail();
});

function getSchemeDetail() {
    $('#btnWorkPlan').css("display", 'block');
    $('#row_info_required').css("display", 'block');
    $("#btnWorkPlan").prop('disabled', false);
    $("#btnViewWorkPlan").prop('disabled', false);
    var val = $('#cmb_scheme option:selected').val();
    $.get('getSchemeDetail?scheme_id=' + val, function (data) {
        var data = JSON.parse(data)[0];
        for (var key in data) {
            $("#" + key).val(data[key]);
        }
    });
}

$("#btnGet").click(function (event) {
    getSchemeDetail();
});
