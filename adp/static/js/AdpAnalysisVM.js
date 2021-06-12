/**
 * Created by idrees on 11/13/2018.
 */


var schemesList;
$(document).ready(function () {
    try {
        resizeContent();
        waitingDialog.show();
        waitingDialog.progress(0);

        var analysisModel = new AnalysisModel();
        var dimensionalModel = new DimensionModel(analysisModel);
        ko.applyBindings(analysisModel);
        schemesList = JSON.parse(localStorage.getItem("adp_schemes"));
        if(!schemesList){
            $.ajax({
                type: 'GET',
                dataType: 'text',
                url: 'adp_schemes',
                cache: false,
                timeout: 9000000,
                error: function (xhr, ajaxOptions, thrownError) {
                    waitingDialog.hide();
                    alert(xhr.responseText);
                    alert(thrownError);
                },
                xhr: function () {
                    var xhr = new window.XMLHttpRequest();
                    xhr.addEventListener("progress", function (evt) {
                        var message;
                        if (evt.lengthComputable) {
                            var progress = ((100*evt.loaded)/(evt.total)).toFixed(0);
                            message = progress + "% downloaded."
                        }else{
                            if(evt.loaded < 1024){
                                message = evt.loaded +" bytes downloaded.";
                            }else if(evt.loaded < 1024*1024){
                                var progress = (evt.loaded/1024).toFixed(2);
                                message = progress +" KB downloaded.";
                            }else{
                                var progress = (evt.loaded/(1024 * 1024)).toFixed(2);
                                message = progress +" MB downloaded.";
                            }
                        }
                        waitingDialog.message(message)
                        waitingDialog.progress(100);
                    }, false);
                    return xhr;
                },
                success: function (data) {
                    waitingDialog.hide();
                    schemesList = eval('(' + JXG.decompress(data) + ')');
                    dimensionalModel.initialize();

                    // alert('Data loaded from server');
                }
            });
        }else{
            waitingDialog.hide();
            dimensionalModel.initialize();
            // alert('Data loaded from local storage');
        }
        $(window).resize(function () {
            resizeContent();
        });
    } catch (err) {
        console.error(err.stack);
    }
});


function resizeContent() {
    var navbarHeight = $('#base_nav').height();
    var footnoteHeight = $('#footnote').height();
    height = $('body').height() - (navbarHeight + footnoteHeight);
    $('div#mainpanel').height(height);
}

function cacheData(){
    $('#myPleaseWait').modal('show');
    try {
        localStorage.removeItem("adp_schemes");
        localStorage.setItem("adp_schemes", JSON.stringify(schemesList));
        $('#myPleaseWait').modal('hide');
    }catch(e){
        $('#myPleaseWait').modal('hide');
        console.error(e.stack);
    }
}

function clearChache(){
    $('#myPleaseWait').modal('show');
    try {
        localStorage.clear();
        localStorage.removeItem("adp_schemes");
        $('#myPleaseWait').modal('hide');
    }catch(e){
        $('#myPleaseWait').modal('hide');
        console.error(e.stack);
    }
}

 function numberFormat(val,isDecimal){
    var parts = val.toString().split(".");
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    if(isDecimal) {
        if (!parts[1]) {
            parts.push('00');
        } else {
            if (parts[1].length > 2) {
                parts[1] = parts[1].substring(0, 2);
            }
        }
    }
    return parts.join(".");
}