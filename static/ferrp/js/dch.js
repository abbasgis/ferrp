/**
 * Created by ather on 12/12/2017.
 */
/**
 * Created by ather on 9/30/2017.
 **/
var theme = 'fresh';
$('.selectpicker').selectpicker({
    style: 'btn-primary',
    size: 4
});
$(":file").filestyle({buttonBefore: true, buttonName: "btn-primary"});
// alertClasses = {
//     'info': 'alert alert-success',     //'alert alert-info',
//     'error': 'alert alert-danger',
//     'warning': 'alert alert-warning',
//     'success': 'alert alert-success'
// }
// var showAlert = function (message, alertKey) {
//     if (!alertClasses[alertKey]) {
//         $('#msgContainer').html('<div class="' + alertClasses[alertKey.toLowerCase()] + '"><a class="close" data-dismiss="alert">×</a>' +
//             '<span><strong>' + alertKey + '! </strong>' + message + '</span></div>');
//     }
// }
alert_info = {
    'info': {name: "Information", class: 'alert alert-info'},
    'error': {name: "Error", class: 'alert alert-danger'},
    'warning': {name: "Warning", class: 'alert alert-warning'},
    'success': {name: "Success", class: 'alert alert-success'}
}
var showAlert = function (message, alert_info_obj) {
    $('#msgContainer').html('<div class="' + alert_info_obj.class + '"><a class="close" data-dismiss="alert">×</a>' +
        '<span><strong>' + alert_info_obj.name + '! </strong>' + message + '</span></div>')
}
var dialogTypes = {
    "default": BootstrapDialog.TYPE_DEFAULT,
    "info": BootstrapDialog.TYPE_SUCCESS,//BootstrapDialog.TYPE_PRIMARY,
    "primary": BootstrapDialog.TYPE_PRIMARY,
    "success": BootstrapDialog.TYPE_SUCCESS,
    "warning": BootstrapDialog.TYPE_WARNING,
    "error": BootstrapDialog.TYPE_DANGER
};
var showAlertDialog = function (message, dialogtype, buttons) {
    if (!buttons) buttons = [];
    // title = dialogtype.split("-")[1];
    // BootstrapDialog.show({
    var dialogRef = new BootstrapDialog({
        draggable: true,
        title: BootstrapDialog.DEFAULT_TEXTS[dialogtype],
        type: dialogtype,
        message: message,
        buttons: buttons
    });
    dialogRef.open();
    setTimeout(function () {
        dialogRef.close();
    }, 2000);
}
var ProgressBarModel = function () {
    var me = this;
    me.intervalId;
    me.intervalSize = 10;
    me.progressbarDiv = $('#myProgress'); //progressbarDiv;
    me.progressbar = $('#myBar');//progressbar;
    me.width = 1;
    me.initializeProgressBar = function (fileSize) {
        me.progressbarDiv.show();
        me.width = 1;
        me.intervalSize = Math.round(parseInt(fileSize) / 10); //(100 * fileSize)/100)
        me.intervalId = setInterval(me.updateProgressBarInfoText, me.intervalSize);
    }

    me.initializeProgressBarContinous = function () {
        me.progressbarDiv.show();
        me.width = 1;
        me.intervalSize = 1;
        me.intervalId = setInterval(me.updateProgressBarWithoutText, me.intervalSize);
    }
    me.resetProgressbar = function () {
        me.width = 5;
    }
    me.hideProgressBar = function () {
        clearInterval(me.intervalId);
        me.width = 1;
        me.progressbarDiv.hide();
    }
    me.updateProgressBarInfoText = function () {
        if (me.width >= 95) {
            clearInterval(me.intervalId);
        } else {
            me.width++;
            me.progressbar.css('width', me.width + '%');
            me.progressbar.text(me.width + '% completed');
        }
    }

    me.updateProgressBarWithoutText = function () {
        if (me.width == 99) me.width = 1;
        me.width++;
        me.progressbar.css('width', me.width + '%');
    }

    me.setProgressBarTextTo100 = function () {
        if (me.intervalId) {
            clearInterval(me.intervalId);
            me.progressbar.css('width', '100%');
            me.progressbar.text('upload completed');
        }
    }

}
// var callAJAX = function (params, callback) {
//     // params in the form of {url:url,post:post} ets
//     var delayInMilliseconds = 1000; //1 second
//     setTimeout(function () {
//         $.ajax(params).done(function (data) {
//             callback(data)
//         }).fail(function (error) {
//             try {
//                 console.log(error.responseText);
//                 showAlert(error.statusText, alert_info.error);
//             } catch (e) {
//                 console.log(e)
//             }
//         })
//             , delayInMilliseconds
//     })
// }
progressbarModel = null
// var formData = new FormData();
//
// formData.append("username", "Groucho");
// formData.append("accountnum", 123456);
// var params = {
//                url: url,
//                type: "POST",
//                data: formData,
//                dataType: "json",
//                processData: false,
//                contentType: false,
//                async: true,
//                headers: {'X-CSRFToken': token},
//            }

var setMissingParams = function (params, isAsync) {
    if (!params["type"]) {
        params["type"] = "GET";
    }
    if (!params["dataType"]) {
        params["dataType"] = "json";
    }
    if (!params["processData"]) {
        params["processData"] = false;
    }
    if (!params["contentType"]) {
        params["contentType"] = false;
    }

    if (!params["async"]) {
        params["async"] = isAsync;
    }
    return params;
}
var callSJAX = function (params) {
    var params = setMissingParams(params, false);
    $.ajaxSetup({async: false});
    var remote = $.ajax(params).responseText;
    return remote;
}
var callAJAX = function (params, callback) {
    // params in the form of {url:url,post:post} ets
    var params = setMissingParams(params, true);
    if ($("#waiting-div").length) $("#waiting-div").css('visibility', 'visible');
    var delayInMilliseconds = 1000; //1 second
    setTimeout(function () {
        $.ajax(params).done(function (data) {
            if ($("#waiting-div").length) $("#waiting-div").css('visibility', 'hidden');
            try {
                if (data.is_redirect) {
                    window.location.href = data.url
                }
            } catch (e) {
                console.log(e)
            }
            callback(data)
        }).fail(function (error, texStatus) {
            // console.log(error.responseText);
            if ($("#waiting-div").length) $("#waiting-div").css('visibility', 'hidden');
            console.log(texStatus)
            errorMsg = "Fail to perform your request."
            showAlertDialog(errorMsg, dialogTypes.error);
            if (progressbarModel != null)
                progressbarModel.hideProgressBar()
        })
            , delayInMilliseconds
    })
}
resampleHermite = function (canvas, width, height) {
    var HERMITE = new Hermite_class();
//default resize
    HERMITE.resample(canvas, width, height);
//more options
//     HERMITE.resample(canvas, width, height, true, finish_handler); //true=resize canvas
//single core
//     HERMITE.resample_single(canvas, width, height);
// resize image to 300x100
//     HERMITE.resize_image('image_id', newWidth, newHeight);
//resize image to 50%
//     HERMITE.resize_image('image_id', null, null, 50);
}

var validation = {
    isEmailAddress: function (str) {
        var pattern = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
        return pattern.test(str);  // returns a boolean
    },
    isNotEmpty: function (str) {
        var pattern = /\S+/;
        return pattern.test(str);  // returns a boolean
    },
    isNumber: function (str) {
        var pattern = /^-?\d+\.?\d*$/; ///^\d+$/;
        return pattern.test(str);  // returns a boolean
    },
    isSame: function (str1, str2) {
        return str1 === str2;
    }
};

var getRemainingBodyHeight = function (isHeaderAvalilable, isFooterAvailable, cushion, minHeight) {
    var cushion = (cushion) ? cushion : 15;
    minHeight = (minHeight) ? minHeight : 400;
    var width = $(window).width();
    var height = $(window).height();
    var navbar_height = $("#base_nav").height();
    var header_height = (isHeaderAvalilable == true) ? $("#header").height() : 0;
    var footer_heght = (isFooterAvailable == true) ? $("#footer").height() : 0;
    var rem_height = height - (navbar_height + header_height + footer_heght + cushion);
    rem_height = (rem_height > minHeight ? rem_height : minHeight);
    return rem_height;
};
var getPanelBodyHeight = function (pnlId, remHeight) {
    var targetPanel = $('#' + pnlId);
    var panelHeadingHeight = $('#' + pnlId + ' .panel-heading').height()
    var panelFooterHeight = $('#' + pnlId + ' .panel-footer').height()
    var bodyHeight = remHeight - (panelFooterHeight + panelHeadingHeight);
    return bodyHeight;
}

var correctString2JSON = function (s) {
    var s = s.replace(/\\n/g, "\\n")
        .replace(/\\'/g, "\\'")
        .replace(/\\"/g, '\\"')
        .replace(/\\&/g, "\\&")
        .replace(/\\r/g, "\\r")
        .replace(/\\t/g, "\\t")
        .replace(/\\b/g, "\\b")
        .replace(/\\f/g, "\\f");
// remove non-printable and other non-valid JSON chars
    s = s.replace(/[\u0000-\u0019]+/g, "");
    return s
}