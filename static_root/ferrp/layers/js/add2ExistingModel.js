/**
 * Created by Dr. Ather Ashraf on 8/18/2018.
 */
$("#selApp").on('change', function (e) {
    var app_key = $(this).find("option:selected").val();
    var models = appList[app_key];
    $('#selModel').find('option').remove().end().append('<option value="-1">Select Model</option>');
    if (models) {
        for (var i = 0; i < models.length; i++) {
            $('#selModel').append('<option value="' + models[i] + '">' + models[i] + '</option>');
        }
    }
})
$('#selModel').on('change', function (e) {
    var appLabel = $("#selApp").find("option:selected").val();
    var modelName = $(this).find("option:selected").val();
    var url = "/get_model_fields/?appLabel=" + appLabel + "&modelName=" + modelName;
    var params = {
        url: url,
        type: "GET",
        // data: formData,
        dataType: "json",
        processData: false,
        contentType: false,
        async: true,

    }
    callAJAX(params, function (data) {
        // alert(data)
        $('#tblFiledMapping > tbody').empty("");
        for (var key in data) {
            var tr = $('<tr></tr>');
            var fieldName = data[key];
            var select = $('<select id="sel' + fieldName + '" class="selLayerField form-control"></select>')
            var option = $('<option value="-1">Select Layer Field</option>')
            select.append(option);
            for (key in lyrFieldList) {
                var lyrFieldName = lyrFieldList[key];
                var option = $('<option value="' + lyrFieldName + '">' + lyrFieldName + '</option>');
                select.append(option)
            }
            tr.append('<td class="cellValue">' + fieldName + '</td>');
            var td = $('<td></td>');
            td.append(select)
            tr.append(td);
            // var missingExtention = me.missingShpExtention(fileList[key], tr);
            $('#tblFiledMapping > tbody:last-child').append(tr);
        }
    })
})

var progressbarModel = new ProgressBarModel();
$("form#fileParametersform").submit(function (event) {
    event.preventDefault()
    progressbarModel.initializeProgressBarContinous();
    var mapping = {}
    $('#tblFiledMapping > tbody > tr').each(function () {
        // $(this).find('td').each(function () {
        // do your cool stuff
        var tds = $(this).find('td');
        var modelField = tds[0].innerHTML;
        var layerField = $('#sel' + modelField).find("option:selected").val();
        mapping[modelField] = layerField
        // });
    });
    // alert(JSON.stringify(mapping));
    var srid = $('#txtSrid').val()
    var appLabel = $("#selApp").find("option:selected").val();
    var modelName = $('#selModel').find("option:selected").val();
    var formData = new FormData();
    formData.append("mapping", JSON.stringify(mapping));
    formData.append("srid", srid);
    formData.append("fileName", fileName);
    formData.append("appLabel",appLabel);
    formData.append("modelName",modelName);
    // var url = $('#fileParametersform').attr('action')
    var params = {
        url: urlMapping,
        type: "POST",
        data: formData,
        dataType: "json",
        processData: false,
        contentType: false,
        async: true,
        headers: {'X-CSRFToken': csrfToken},
    }
    callAJAX(params, function (data) {
        window.location.href = urlViewLayer + "?layer_name="+data.layerName
    })
});