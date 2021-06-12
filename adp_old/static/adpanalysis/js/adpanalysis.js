/**
 * Created by idrees on 5/3/2017.
 */
var schemesStats = null;
var pwHeight = 100;
$(document).ready(function(){
    try {
        //$('#myPleaseWait').modal('show');
        resizeContent();
        waitingDialog.show();
        waitingDialog.progress(0);
        var adpanalysis = new AdpAnalysisVM();
        schemesStats = JSON.parse(localStorage.getItem("adpstats"));

        if(!schemesStats){
            $.ajax({
                type: 'GET',
                dataType: 'text',
                url: 'adpstats',
                cache: false,
                timeout: 9000000,
                error: function (xhr, ajaxOptions, thrownError) {
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
                    schemesStats = eval('(' + JXG.decompress(data) + ')');
                    adpanalysis.initialize(schemesStats);
                }
            });

        }else{
            waitingDialog.hide();
            var decompressSchemesList = JSON.parse(eval('(' + JXG.decompress(schemesStats) + ')'));
            adpanalysis.initialize(decompressSchemesList);
        }
        $(window).resize(function () {
            resizeContent();
        });
    }catch(err){
        waitingDialog.hide();
        console.error(err.stack);
    }
});

function cacheData(){
    $('#myPleaseWait').modal('show');
    try {
        //localStorage.clear();
        localStorage.setItem("adpstats", JSON.stringify(schemesStats));
        $('#myPleaseWait').modal('hide');
    }catch(e){
        localStorage.clear();
        localStorage.setItem("adpstats", JSON.stringify(schemesStats));
        $('#myPleaseWait').modal('hide');
        console.error(e.stack);
    }
}

function getMapGeoJson(){
    localStorage.clear();
    var geoJson = localStorage.getItem("adpmap");
    var success = false;
    if (!geoJson) {

        $.ajax('adpanalysis/adpmap', {
            success: function(data) {
                geoJson = data;
                try {
                    localStorage.setItem("adpmap","");
                    localStorage.setItem("adpmap", geoJson);
                }catch(e){
                    console.error(e.stack);
                }
            },
            error: function() {
                //$('#notification-bar').text('An error occurred');
            }
        });


    }
    return geoJson;
}


function resizeContent() {
    var bodyheight =   $('body').height(); //- $("#topnavbar").height();
    //var filterDivHeight =$('#filterDiv').height();
    var navBarHeaderHeight =$('#base_nav').height();
    var footnoteHeight =$('#footnote').height();
    pwHeight = bodyheight - navBarHeaderHeight - footnoteHeight;

    $('#wrap').height(pwHeight);

}