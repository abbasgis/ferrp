/**
 * Created by idrees on 5/3/2017.
 */

var AdpAnalysisVM = function(){
    var me = this;
    me.containerDivId = 'containerDiv';
    me.schemesStats = null;
    me.districtStats = null;
    me.sectorStats = null;
    me.barChartModel = null;
    me.mapModel = null;
    me.statsModel = new StatsModel();
    me.dimensionModel = null;
    me.geoJson = null;

    me.initialize = function(schemesStats){
        try{
            me.schemesStats = schemesStats;
            me.barChartModel = new BarChartModel(me, me.schemesStats);
            me.dimensionModel = new TabularDataModel(me.schemesStats);
            me.tabularDataActivity();
            $('#myPleaseWait').modal('hide');
        }catch(err){
            $('#myPleaseWait').modal('hide');
            console.error(err.stack);
        }
    }

    me.barChartActivity = function(){
        me.barChartModel.createBarChartView(me.containerDivId);
    }

    me.tabularDataActivity = function(){
        var containerDiv = $('#' + me.containerDivId);
        containerDiv.html('');
        me.dimensionModel.initialize(containerDiv);
    }

    me.mapActivity = function(){
        me.mapModel.createMapView(me.containerDivId);
    }

    $('#aSectorTabularData').click(function(){
        $('#myPleaseWait').modal('show');
        me.tabularDataActivity();
        $('#myPleaseWait').modal('hide');
    });

    $('#aSectorChartData').click(function(){
        $('#myPleaseWait').modal('show');
        me.barChartActivity();
        $('#myPleaseWait').modal('hide');
    });

    $('#aMap').click(function(){
        me.geoJson = JSON.parse(localStorage.getItem("adpmap"));
        if(!me.geoJson){
            waitingDialog.show();
            waitingDialog.progress(0);
            $.ajax({
                type: 'GET',
                dataType: 'text',
                url: '../adpanalysis/adpmap',
                cache: false,
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
                success: function (json) {
                    waitingDialog.hide();
                    try{
                        me.geoJson = localStorage.setItem("adpmap", JSON.stringify(json));
                        var geojsondata = eval('(' + JXG.decompress(json) + ')');
                        me.mapModel = new MapModel(me.schemesStats, geojsondata);
                        me.mapActivity();
                    }catch(err){
                        console.log(err.stack);
                    }
                }
            });
        }else{
            $('#myPleaseWait').modal('show');
            try{
                var geojsondata = eval('(' + JXG.decompress(me.geoJson) + ')');
                // var geojsondata = eval('(' + me.geoJson + ')');
                me.mapModel = new MapModel(me.schemesStats, geojsondata);
                me.mapActivity();
                $('#myPleaseWait').modal('hide');
            }catch(err){
                $('#myPleaseWait').modal('hide');
                console.error(err.stack);
            }

        }
    });

}
