/**
 * Created by ather on 5/6/2017.
 */
var PivotTableVM = function(){
    var me = this;
    me.initialize = function(jsonData){
        var fields = {};
        for(var key in jsonData[0]){
            var fieldType = (isNaN(parseFloat(jsonData[0][key])) ? "string" : "number");
            fields[key] = {type:fieldType};
        }
        jsonData.splice(0,0,fields);
        var report = {
            dataSource: {
                data: jsonData
            },
            rows: [{uniqueName:"Sector"}],
            columns:[{uniqueName:"ADPYear"}],
            measures:[{uniqueName:"Allocation"}],
            expandAll: true,
            drillAll: true
        };
        var pivot = $("#pivotContainer").flexmonster({
            toolbar: true,
            report: report,
            height:'100%',
            licenseKey: "Z79D-XB0J2Z-1J4550-1S2A62"
        });
    }
}