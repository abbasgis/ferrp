/**
 * Created by ather on 10/14/2017.
 */

var UploadFileModel = function (progressbarModel, urlUpload) {
    var me = this;
    me.reqExt = ['shp', 'shx', 'dbf', 'prj'];
    me.submitButton = $('#btnSubmit');
    me.addToExisitingButton = $('#btnExistingModel')
    me.isDirty = false;
    me.selRow;
    me.fileName;
    me.progressbarModel = progressbarModel;
    me.urlUpload = urlUpload;
    me.mulFileFieldChange = function (input) {
        var files = input.get(0).files;
        var numFiles = input.get(0).files ? input.get(0).files.length : 1;
        var fileList = {}
        $("#tblFiles > tbody").empty();
        for (i = 0; i < numFiles; i++) {
            var fileNameParts = files[i].name.split(".");
            var name = fileNameParts[0], extension = fileNameParts[1];
            for (var j = 2; j < fileNameParts.length; j++) extension += "." + fileNameParts[j];
            if (!fileList[name]) fileList[name] = [];
            fileList[name].push(extension);
        }
        for (var key in fileList) {
            var tr = $('<tr></tr>');
            var fname = fileList[key];
            tr.append('<td><input type="radio" name="optUpFile" onchange="handleRadioChange(this)"></td><td name="fname">' + key + '</td>');
            var missingExtention = me.missingShpExtention(fileList[key], tr);
            $('#tblFiles > tbody:last-child').append(tr);
        }
        showAlert("Please select any file to upload", alert_info.info);
    }

    me.missingShpExtention = function (fileExts, row) {
        var res = [];
        // var fileExts = fileList[key];

        for (var i = 0; i < me.reqExt.length; i++) {
            var td = $('<td name="' + me.reqExt[i] + '"></td>');
            var a = fileExts.indexOf(me.reqExt[i]);
            if (a == -1) {
                res.push(me.reqExt[i]);
                td.html('No')
                td.css('color', 'red');
            } else {
                td.html('Yes')
                td.css('color', 'green');
            }
            row.append(td);
        }
        return res;
    }

    me.handleRadioChange = function (rdo) {
        me.isDirty = false;
        me.selRow = $(rdo).parents('tr'); //.index();
        var fileExt = [];
        var fileName = "";

        $(me.selRow).find("td").each(function () {
            if ($(this).attr('name') == "fname") me.fileName = $(this).html();
            if ($(this).html() == 'No') {
                fileExt.push($(this).attr('name'));
                me.isDirty = true;
            }
        });
        var alertKey = alert_info.info;
        var message = "Click on submit button to upload file...";
        if (me.isDirty) {
            if (fileExt[0] == 'prj') {
                alertKey = alert_info.warning;
                message = "Prj file of " + fileName + ".shp  is missing.If it is not available, click on submit button to upload it. ";
                me.isDirty = false;
            } else {
                alertKey = alert_info.error;
                message = "You cannot upload " + fileName + ".shp because important files are missing.";
                rdo.checked = false;

            }
        }
        me.submitButton.attr('disabled', me.isDirty);
        me.addToExisitingButton.attr('disabled', me.isDirty);
        showAlert(message, alertKey);
    }

    me.uploadShapefile = function (csrftoken, nextURL, project_id, dir_id) {
        if (!me.selRow) {
            var message = "You can upload only one file at a time. Please select any file for uploading by clicking on radio button";
            // showAlert(message, alert_info.warning);
            showAlertDialog(message, dialogTypes.warning);
        } else {
            if (!me.isDirty) {
                var data = new FormData();
                var filesize = 0;
                $.each($('#mulFileField')[0].files, function (i, file) {
                    if (file.name.indexOf(me.fileName) != -1) {
                        data.append('file_field', file, file.name);
                        filesize += parseFloat(file.size);
                    }
                });
                filesize = Math.round(filesize / 1024) + 1;
                showAlert("Uploading file of size " + filesize + " KB", alert_info.info);
                me.progressbarModel.initializeProgressBar(filesize);
                $.ajax({
                    url: me.urlUpload,
                    type: "POST",
                    data: data,
                    processData: false,
                    contentType: false,
                    headers: {'X-CSRFToken': csrftoken},
                    success: function (response) {
                        me.progressbarModel.hideProgressBar();
                        var shapefileName = response;
                        nextURL += "?file_name=" + shapefileName + "&project_id=" + project_id + "&dir_id=" + dir_id;
                        window.location.href = nextURL;
                    },
                    error: function (jqXHR, textStatus, errorMessage) {

                        console.log(jqXHR.responseText); // Optional
                        showAlert(errorMessage, alert_info.error);
                        me.progressbarModel.setProgressBarTextTo100();
                    }
                });
            }
        }
    }

    // me.submitForm = function (csrftoken, url) {
    //     if (!me.selRow) {
    //         var message = "You can upload only one file at a time. Please select any file for uploading by clicking on radio button";
    //         // showAlert(message, alert_info.warning);
    //         showAlertDialog(message, dialogTypes.warning);
    //     } else {
    //         me.uploadShapefile(csrftoken, url)
    //     }
    //
    // }
    // me.add2ExistingModel = function (csrftoken, url) {
    //     if (!me.selRow) {
    //         var message = "You can upload only one file at a time. Please select any file for uploading by clicking on radio button";
    //         // showAlert(message, alert_info.warning);
    //         showAlertDialog(message, dialogTypes.warning);
    //     } else {
    //         me.uploadShapefile(csrftoken, url)
    //     }
    // }

}




