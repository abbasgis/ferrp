/**
 * Created by idrees on 11/6/2017.
 */

var ArzOverviewModel = function () {
    var me = this;
    me.statFunctions = new ArzGlobalFunctionsModel();
    me.createPopup = function (data) {
        var totalLength = 0.0, length = 0.0;
        canalTypeDataArray = [];
        canalTypeDataArray.splice(0,canalTypeDataArray.length)
        for (var i = 0; i < data.length; i++){
            var record = {};
            var value = (data[i]["length"]);
            length = (isNaN(parseFloat(value)) ? 0 : parseFloat(value));;
            record.varables = me.getFullNameFromCanalType(data[i].canal_type);
            record.content = me.statFunctions.numberFormat(length, true);
            canalTypeDataArray.push(record);
            totalLength += length;
        }
        var formattedTotalLength = me.statFunctions.numberFormat(totalLength, true);
        $("#canalsLength").text(formattedTotalLength);
    }

    me.getFullNameFromCanalType = function (shortName) {
        var fullName = "";
        if(shortName == "L-Ch"){
            fullName = "Link Canal";
        // }else if(shortName == "M"){
        //     fullName = "Minor Canal";
        // }else if(shortName == "Lift-Ch"){
        //     fullName = "Lift Channel";
        // }else if(shortName == "B"){
        //     fullName = "Branch Canal";
        // }else if(shortName == "C"){
        //     fullName = "Main Canal";
        }else if(shortName == "D"){
            fullName = "Distributary";
        }else if(shortName == "S/M"){
            fullName = "Sub Minor";
        }else if(shortName == "E"){
            fullName = "Escape";
        }else if(shortName == "Ch"){
            fullName = "New/Lift Channel";
        }else if(shortName == "F"){
            fullName = "Feeder";
        }else if(shortName == "H-L-Ch"){
            fullName = "High Level Channel";
        }else if(shortName == "ML"){
            fullName = "Main Line";
        }else if(shortName == ""){
            fullName = "Others";
        }else if(shortName == " "){
            fullName = "Others";
        }else if(shortName == "BC"){
            fullName = "Branch Canal";
        }else if(shortName == "M"){
            fullName = "Minor";
        }else if(shortName == "MC"){
            fullName = "Main Canal";
        }else if(shortName == "SM"){
            fullName = "Sub Minor";
        }else {
            fullName = shortName;
        }
        return fullName;
    }

    me.getGrossCommandedAreaArray = function (data) {
        var totalArea = 0.0, area = 0.0;
        grossCommandedAreaArray = [];
        grossCommandedAreaArray.splice(0,grossCommandedAreaArray.length);
        for (var i = 0; i < data.length; i++){
            var record = {};
            var value = (data[i].gca_geom_ma);
            area =  (isNaN(parseFloat(value)) ? 0 : parseFloat(value));
            record.varables = data[i].name;
            record.content = me.statFunctions.numberFormat(area, true);
            grossCommandedAreaArray.push(record);
            totalArea += area;
        }
        var formattedTotalArea = me.statFunctions.numberFormat(totalArea, true);
        $("#grossCommandedArea").text(formattedTotalArea);
    }

    me.getCultivableCommandedAreaArray = function (data) {
        var totalArea = 0.0, area = 0.0;
        cultivableCommandedAreaArray = [];
        cultivableCommandedAreaArray.splice(0,cultivableCommandedAreaArray.length);
        for (var i = 0; i < data.length; i++){
            var record = {};
            var value = (data[i].cca_geom_ma)
            area =  (isNaN(parseFloat(value)) ? 0 : parseFloat(value));;
            record.varables = data[i].name;
            record.content = me.statFunctions.numberFormat(area, true);
            cultivableCommandedAreaArray.push(record);
            totalArea += area;
        }
        var formattedTotalArea = me.statFunctions.numberFormat(totalArea, true);
        $("#cultivableCommandedArea").text(formattedTotalArea);
    }

    me.getWaterTableStatsArray = function (data) {

        waterTableStatsArray = [];
        waterTableStatsArray.splice(0,waterTableStatsArray.length);
        if(data){
            waterTableStatsArray = [
                {
                    varables: me.getFullNameFromWTStats("min"),
                    content:  parseFloat((data[0].min))
                },
                {
                    varables: me.getFullNameFromWTStats("max"),
                    content:  parseFloat((data[0].max))
                },
                {
                    varables: me.getFullNameFromWTStats("avg"),
                    content:  parseFloat((data[0].avg))
                },
                {
                    varables: me.getFullNameFromWTStats("std"),
                    content:  parseFloat((data[0].stdev))
                }
            ]
            var statsTotal = (parseFloat((data[0].max)))
            $("#cultivableCommandedArea").text(statsTotal + " ft. Max");

        }else {
            $("#cultivableCommandedArea").text("No Data");
        }

    }

    me.getFullNameFromWTStats = function (shortName) {
        var fullName = "";
        if(shortName == "min"){
            fullName = "Minimum Depth";
        }else if(shortName == "max"){
            fullName = "Maximum Depth";
        }else if(shortName == "avg"){
            fullName = "Average Depth";
        }else if(shortName == "std"){
            fullName = "Std. Dev. Depth";
        }
        return fullName;
    }

}