var isDirty = true;
var raster_type = "single";
$(':radio[name="raster_type"]').change(function () {
    raster_type = this.value;
    var multiple = (raster_type == 'tile' ? true : false );
    $("#mul_file_field").attr("multiple", multiple)
});
$("#mul_file_field").change(function () {
    var files = this.files;
    var name = files[0].name.split(".")[0];
    $('#txt_raster_name').val(name);
    checkLayerName(name);
})
$('#txt_raster_name').change(function () {
    var name = this.value;
    checkLayerName(name);
})
var checkLayerName = function (layer_name) {
    var url = check_layer_name_url + "?layer_name=" + layer_name + " &layer_type=raster"
    callAJAX({url: url}, function (data) {
        isfound = data;
        var message = (isfound == true ? "Layer name already exist. Please change name." :
            "Layer name is fine")
        if (isfound == "true") {
            showAlert("Layer name already exist. Please change name", alert_info.error);
            isDirty = true;
        } else {
            isDirty = false;
            showAlert("Layer name is fine. You can upload file with this name.", alert_info.success);
        }

    })
}
// var progressbarModel = new ProgressBarModel();
// $("#btnExecute").click(function (event) {
//     var url = "";
//     callAJAX({url: url}, function (data) {
//         if (i + 1 == no_of_files) {
//             message = "Raster is uploaded successfully";
//             showAlert(message, alert_info.success);
//             progressbarModel.hideProgressBar();
//         }
//     });
// });
$("form#uploadFileForm").submit(function (event) {
    event.preventDefault();
    var url = this.action;
    isDirty = false;
    if (!isDirty) {
        var files = $("#mul_file_field")[0].files;
        var raster_name = $('#txt_raster_name').val();
        var project_id = $('#project_id').val();
        var dir_id = $('#dir_id').val();
        var no_of_files = files.length;
        var raster_srid = $('select[name=select_srid]').val();

        var filesize = 300;
        for (var i = 0; i < no_of_files; i++) {
            filesize += parseFloat(files[i].size);
            filesize = Math.round(filesize / 1024) + 1;
        }
        progressbarModel.initializeProgressBar(filesize);
        for (var i = 0; i < no_of_files; i++) {
            var file = files[i];

            showAlert("Uploading file " + (i + 1) + " out of " + no_of_files + ", having total file size " + filesize + " KB", alert_info.info);

            // progressbarModel.initializeProgressBarContinous();
            var data = new FormData();
            data.append('select_raster', file, file.name);
            data.append('raster_name', raster_name);
            data.append('project_id', project_id);
            data.append('dir_id', dir_id);
            data.append('raster_type', raster_type);
            data.append('no_of_files', no_of_files);
            data.append('raster_srid', raster_srid);
            data.append('file_index', i + 1);
            var params = {
                url: url,
                type: "POST",
                data: data,
                dataType: "json",
                processData: false,
                contentType: false,
                async: true,
                headers: {'X-CSRFToken': token},
            }
            callAJAX(params, function (data) {
                if (data.res == "200") {
                    message = "All file uploaded successfully.. Processing Rasters now...";
                    showAlert(message, alert_info.success);
                    processRaster(data.layer_name, data.table_name)
                    // progressbarModel.hideProgressBar();
                    //progressbarModel.initializeProgressBarContinous();
                } else if (data.res == "400") {
                    message = (i + 1) + " out of " + no_of_files + " has been uploaded"
                    showAlert(message, alert_info.info)
                    progressbarModel.resetProgressbar()
                } else {
                    message = "Failed to upload file. Contact your administrator for further action"
                    showAlert(message, alert_info.error)
                    progressbarModel.resetProgressbar()
                    // progressbarModel.hideProgressBar();
                }
            });
        }
    }
});
processRaster = function (layer_name, table_name) {
    var url = process_raster_url;
    var files = $("#mul_file_field")[0].files;
    var raster_name = $('#txt_raster_name').val();
    var project_id = $('#project_id').val();
    var dir_id = $('#dir_id').val();
    var no_of_files = files.length;
    var raster_srid = $('select[name=select_srid]').val();

    for (var i = 0; i < no_of_files; i++) {
        showAlert("Processing raster " + (i + 1) + " out of " + no_of_files + "...", alert_info.info);
        progressbarModel.resetProgressbar()
        var data = new FormData();
        data.append('raster_name', raster_name);
        data.append('project_id', project_id);
        data.append('dir_id', dir_id);
        data.append('raster_type', raster_type);
        data.append('no_of_files', no_of_files);
        data.append('raster_srid', raster_srid);
        data.append('table_name', table_name);
        data.append('file_name', files[i].name)
        data.append('file_index', (i + 1));
        var params = {
            url: url,
            type: "POST",
            data: data,
            dataType: "json",
            processData: false,
            contentType: false,
            async: true,
            headers: {'X-CSRFToken': token},
        }
        // progressbarModel.initializeProgressBarContinous();
        callAJAX(params, function (data) {
            if (data.res == 200) {
                progressbarModel.hideProgressBar()
                message = "All rasters processed successfully";
                showAlert(message, alert_info.success);
                window.location.href = view_layer_url + "?layer_name=" + data.table_name;
            } else if (data.res == "400") {
                // message = "Processing raster "+(i+1)+" out of "+no_of_files+"...";
                // showAlert(message, alert_info.info);
                progressbarModel.resetProgressbar();
            } else {
                message = "Error...";
                progressbarModel.hideProgressBar()
                showAlert(message, alert_info.error);
            }
        });

    }
}