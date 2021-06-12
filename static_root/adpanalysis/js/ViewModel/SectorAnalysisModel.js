/**
 * Created by idrees on 5/3/2017.
 */
var SectorAnalysisModel = function(aaVM, schemesList){
    var me = this;
    me.aaVM = aaVM;
    me.schemesList = schemesList;
    me.csvColumns = null;
    //me.sectorColumnsList = null;
    me.sectorsList = null;
    //me.yearsList = null;

    me.initialize = function(){
        me.sectorColumnsList = me.getSectorColumnsList();
        me.yearsList = me.getYearsList();
    }

    me.createBarChart = function(data, sectorsList){
       var barchart =  Highcharts.chart(me.aaVM.containerDivId, {
            chart: {
                type: 'column'
            },
            title: {
                text: 'Yearly Sector Allocation'
            },
            subtitle: {
                text: 'Source: www.pndpunjab.gov.pk'
            },
            xAxis: {
                categories: sectorsList,
                crosshair: true
            },
            yAxis: {
                min: 0,
                title: {
                    text: 'Amount (Million PKR)'
                }
            },
            tooltip: {
                headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
                pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                '<td style="padding:0"><b>{point.y:.1f} mm</b></td></tr>',
                footerFormat: '</table>',
                shared: true,
                useHTML: true
            },
            plotOptions: {
                column: {
                    pointPadding: 0.2,
                    borderWidth: 0
                }
            },
            series: data
        });
    }

    me.createTabularData = function(){
        var panelDiv = $('<div id="panelbody" class="panel-body" style="overflow:scroll"> </div>');
        //$('#'+me.aaVM.containerDivId).html(panelDiv);
        var columnsList = [
            {name:0}
        ];
        var i = 0;

        for (var key in me.schemesList[0]){
            var field = {};
            field.name = key;
            field.caption = key;
            var aggFun = (isNaN(parseFloat(me.schemesList[0][key])) ? "count" : "sum");
            field.dataSettings = {
                aggregateFunc: aggFun,
                formatFunc: function(value) {
                    if(aggFun == "sum") {
                        //var val = parseFloat(value);
                        //var value = (isNaN(val) ? 0 : val);
                        return Number(value).toFixed(2);
                    }else{
                        return value;
                    }
                }
            }
            columnsList.push(field);
            i++;
        }
        //var data = [];
        //for(var i = 0; i<me.sectorsList.length; i++){
        //    var sector = new Array();
        //    for (var key in me.sectorsList[i]){
        //        var value = parseFloat(me.sectorsList[i][key]);
        //        value = (isNaN(value) ? me.sectorsList[i][key] : value);
        //        sector.push(value);
        //    }
        //    data.push(sector);
        //}


        var config = {
            dataSource: me.schemesList,
            dataHeadersLocation: 'columns',
            theme: 'blue',
            toolbar: {
                visible: true
            },
            grandTotal: {
                rowsvisible: true,
                columnsvisible: true
            },
            subTotal: {
                visible: true,
                collapsed: true
            },
            //fields: [
            //    { name: '0', caption: 'Year' },
            //    { name: '1', caption: 'Sector' },
            //    //{ name: '2', caption: 'Schemes', sort: { order: 'asc' } },
            //    //{ name: '3', caption: 'Class' },
            //    //{ name: '4', caption: 'Category', sort: { order: 'desc' } },
            //    //{ name: '5', caption: 'Quantity' },
            //    {
            //        name: '2',
            //        caption: 'Local Capital',
            //        dataSettings: {
            //            aggregateFunc: 'sum',
            //            formatFunc: function(value) {
            //                var val = parseFloat(value);
            //                var value = (isNaN(val) ? 0 : val);
            //                return Number(value).toFixed(2);
            //            }
            //        }
            //    }
            //],
            fields :columnsList,
            rows    : [ 'Sector' ],
            columns : [ 'Year'],
            data    : [ 'Allocation'],
            //preFilters : {
            //    'Manufacturer': { 'Matches': /n/ },
            //    'Amount'      : { '>':  40 }
            //}
            //width: 400,
            height: 400
        };

        // instantiate and show the pivot grid
        var orbObj = new orb.pgridwidget(config);
        orbObj.render(document.getElementById(me.aaVM.containerDivId));

    }

    me.populateYearsData = function(){
        $year = $("#cmbSectorChartYearsList");
        var yearsList = me.yearsList;
        $.each(yearsList, function(index, value) {
            $year.append('<option value="' + value +'">' + value + '</option>');
        });
    }
    me.populateColumnNameData = function(){
        var cmbXFields = $("#xFieldList");
        var columnsList = me.sectorColumnsList;
        $.each(columnsList, function(index, value) {
            cmbXFields.append('<option value="' + value +'">' + value + '</option>');
        });
        var cmbYFields = $("#yFieldList");
        $.each(columnsList, function(index, value) {
            cmbYFields.append('<option value="' + value +'">' + value + '</option>');
        });
    }




    me.createSectorChartFilters = function(){
        var filterComps = '<div class="col-lg-12" style="padding-top: 10px;">'+
            '<div class="col-md-3">'+
                '<label for="sectorChartYearsList">Select Bar Data:</label>'+
                '<select id="cmbSectorChartYearsList" name="sectorChartYearsList" class="form-control">'+
                    '<option value="-1">Select Year</option>'+
                '</select>'+
            '</div>'+
            '<div class="col-md-3">'+
                '<label for="xFieldList">X Field:</label>'+
                '<select id="xFieldList" name="xFieldList" class="form-control">'+
                    '<option value="-1">Select X Field</option>'+
                '</select>'+
            '</div>'+
            '<div class="col-md-3">'+
                '<label for="yFieldList">Y Field:</label>'+
                '<select id="yFieldList" name="yFieldList" class="form-control">'+
                    '<option value="-1">Select Y Field</option>'+
                '</select>'+
            '</div>'+
            '<label for="btnGetSectorTable">Get Data Table:</label><button id="btnGetSectorTable" class="btn btn-primary col-md-3">Get Table</button>'+
        '</div>';
        return $(filterComps);
    }

    me.getYearlySectorAggregates = function(year){
        var data = me.schemesList;
        var arrAllocation = [], arrCost = [], arrFAid = [];
        var yearlySectorAggregates = [];
        var yearData = _.where(data, {Year:year});
        me.sectorsList = me.getSectorsList(yearData);
        var sectorAggregates = _.groupBy(yearData, "Sector");
        for(var i = 0; i< me.sectorsList.length; i++){
            var allocation = 0, total_cost = 0, foreign_cost = 0;
            var fact = new Array();
            var key = _.where(yearData, {Sector:me.sectorsList[i]});
            for (var k in key){
                allocation += (isNaN(key[k]["Allocation"]) ? 0 : key[k]["Allocation"]);
                total_cost += (isNaN(key[k]["Total Cost"]) ? 0 : key[k]["Total Cost"]);
                foreign_cost += (isNaN(key[k]["Foreign Aid Total"]) ? 0 : key[k]["Foreign Aid Total"]);
            }
            fact["Allocation"] = allocation;
            fact["Total Cost"] = total_cost;
            fact["Foreign Aid Total"] = foreign_cost;
            arrAllocation.push(allocation);
            arrCost.push(total_cost);
            arrFAid.push(foreign_cost);
            //yearlySectorAggregates.push({name:me.sectorsList[i], data:fact});
        }
        yearlySectorAggregates.push({name:"Allocation", data:arrAllocation});
        yearlySectorAggregates.push({name:"Total Cost", data:arrCost});
        yearlySectorAggregates.push({name:"Foreign Aid", data:arrFAid});
        return yearlySectorAggregates;
    }

    me.createChartData = function(factField, dataField, groupByField){

    }

    me.getYearSectorChart = function(year){
        var data = me.getYearlySectorAggregates(year);
        me.createBarChart(data, me.sectorsList);
    }

    me.getSectorColumnsList = function(){
        var sectorsColumnsList = [];
        var sectorJson = me.schemesList;
        if (sectorJson.length > 0){
            var columnsIn = sectorJson[0];
            var i = 0;
            for(var key in columnsIn){
                sectorsColumnsList.push(key);
                i++;
            }
        }else{
            console.log("No columns");
        }
        return sectorsColumnsList;
    }

    me.getYearsList = function(){
        var lookup = {};
        var items = me.schemesList;
        var arrYears = [];

        for (var item, i = 0; item = items[i++];) {
            var year = item["Year"];

            if (!(year in lookup)) {
                lookup[year] = 1;
                arrYears.push(year);
            }
        }
        return arrYears;
    }

    me.getSectorsList = function(data){
        var lookup = {};
        var items = data;
        var arrSectors = [];

        for (var item, i = 0; item = items[i++];) {
            var year = item["Sector"];

            if (!(year in lookup)) {
                lookup[year] = 1;
                arrSectors.push(year);
            }
        }
        return arrSectors;
    }

}
