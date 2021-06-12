/**
 * Created by ather on 3/23/2017.
 */
var AdpVM = function (info) {
    try {

        var me = this;
        me.panelHeader = ko.observable();
        me.panelBody = ko.observable();
        me.mainPnlBody = $('#mainpnlbody');
        me.navbar = $('#myNavbar');
        me.cmbYearsList = 'lstYears';
        me.schemesList = null;
        me.info = info;
        me.overviewModel = new OverviewModel(me);
        me.dimensionModel = null;
        me.treeGridModel = new TreeGridModel(me);
        me.filterSchemeModel = new FilterSchemesModel(me);

        me.alertClasses = {
            "info": 'alert alert-info', "danger": 'alert alert-danger',
            "warning": 'alert alert-warning', "success": 'alert alert-success'
        };

        me.removeAlert = function () {
            me.invokeAlert('info', 'Scheme List Table');
        }

        me.invokeAlert = function (type, text) {
            // me.alertText(text);
            $('#alertText').html(text);
            var aClass = (type == '' ? '' : me.alertClasses[type]);
            // me.alertClass(aClass);

            $('#alertClass').removeClass().addClass(aClass);
        }

        me.createPageElements = function () {
            me.setOverviewContents();
        }

        me.initialize = function (schemesList) {
            me.schemesList = schemesList;
            me.overviewModel.populateDataInInfoGraphicsAndGrid(me.schemesList);
            me.populateYearsList(me.schemesList);
            $('#lstYears').change(function () {
                $('#myPleaseWait').modal('show');
                me.setNewDataToJQXGrid();
            });
            $('#myPleaseWait').modal('hide');
        }
        me.setOverviewContents = function () {
            $('#btnFilter').removeClass('hidden');
            $('#btnClearFilter').removeClass('hidden');
            me.mainPnlBody.html('');
            me.overviewModel.initialize();
        }
        me.setDimensionModelingContents = function () {
            $('#btnFilter').addClass('hidden');
            $('#btnClearFilter').addClass('hidden');
            me.mainPnlBody.html('');
            me.dimensionModel = new DimensionModelingModel(me);
            me.dimensionModel.initialize();

        }
        me.openFilter = function () {
            // me.filterSchemeModel = new FilterSchemesModel(me);
            $('#sectorsList').html("");
            $('#districtsList').html("");
            me.filterSchemeModel.initialize();

            // getInfo();
            $('#myModal').modal('show');
        }
        me.getFilterSchemes = function () {
            $('#myModal').modal('hide');
            me.filterSchemeModel.applyFilter();
        }

        me.setNewDataToJQXGrid = function () {
            var yearName = $('#lstYears').val();
            var yearsData = me.filterSchemeModel.getYearData(yearName);
            me.treeGridModel.source.localdata = yearsData;
            $("#divSchemesList").jqxGrid('updatebounddata', 'cells');
            var records = $("#" + me.overviewModel.schemeDivId).jqxGrid('getrows');
            var statsObj = me.overviewModel.calculateRecordStats(records);
            me.overviewModel.setRecordStatsInInfoGraphics(statsObj);
            $('#myPleaseWait').modal('hide');
        }
        me.clearFilter = function () {
            me.filterSchemeModel.clearFilter();
            me.treeGridModel.clearFilterFromGrid();
            me.removeAlert();
        }

        me.populateYearsList = function (data) {
            var yearsList = me.getUniqueValues(data, 'Year');
            $.each(yearsList, function (key, value) {
                $('#' + me.cmbYearsList).append($('<option>', {value: value}).text(value));
            });
        }

        me.getUniqueValues = function (data, column) {
            var lookup = {};
            var items = data;
            var arrUniqueValues = [];
            for (var item, i = 0; item = items[i++];) {
                var key = item[column];
                if (!(key in lookup)) {
                    if (key) {
                        lookup[key] = 1;
                        arrUniqueValues.push(key);
                    }
                }
            }
            return arrUniqueValues;
        }

        me.numberFormat = function (val, isDecimal) {
            // var num = parseFloat(to)
            // var n = num.toString(), p = n.indexOf('.');
            // return n.replace(/\d(?=(?:\d{3})+(?:\.|$))/g, function($0, i){
            //     return p<0 || i<p ? ($0+',') : $0;
            // });
            var parts = val.toString().split(".");
            parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
            if (isDecimal) {
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
    } catch (err) {
        console.error(err.stack);
    }
}

var OverviewModel = function (adpVM) {
    var me = this;
    me.schemeDivId = 'divSchemesList';
    me.adpVM = adpVM;
    me.infoGraphics = adpVM.info.infoGraphics;
    me.infoGraphicInfo = adpVM.info.infoGraphicInfo;

    me.initialize = function () {
        adpVM.panelHeader('<span class="glyphicon glyphicon-book"></span>'); //ADP Overview

        var infoMainRow = me.createRowEl();
        for (var i = 0; i < me.infoGraphics.length; i++) {
            var pnl = me.createInfoPanel(me.infoGraphics[i]);
            infoMainRow.append(pnl);
        }
        var gridRow = me.createRowEl();
        var gridPnl = me.createSchemesGridPanel();

        gridRow.append(gridPnl);
        adpVM.mainPnlBody.append(infoMainRow);
        adpVM.mainPnlBody.append(gridRow);

        var records = me.setRecordStatsToZero();
        if(adpVM.schemesList){
            var statsObj = me.calculateRecordStats(adpVM.schemesList);
            me.populateDataInInfoGraphicsAndGrid(adpVM.schemesList);
        }
    }

    me.populateDataInInfoGraphicsAndGrid = function (schemesData) {
        adpVM.treeGridModel.createSchemesListGrid(schemesData);
        var records = $("#" + me.schemeDivId).jqxGrid('getrows');
        var statsObj = me.calculateRecordStats(records);
        me.setRecordStatsInInfoGraphics(statsObj);
    }

    me.createRowEl = function () {
        var row = '<div class="row"></div>';
        return $(row);
    }

    me.createMainHeading = function () {
        var mPnl = '<div class="row"> ' +
            '<h1 class="page-header" style="padding-left: 15px;">' +
            'Annual Development Programme (ADP 2016-17) Overview</BR><small id="pageHeaderText"></small> ' +
            '</h1> </div>';

        return $(mPnl);
    }

    me.createInfoPanel = function (infoGraphic) {
        var prefix = infoGraphic.id;
        var panel = '<div class="' + infoGraphic.class + '">' + //col-lg-6 col-md-6 col-sm-6 col-xs-12
            '<div class="panel ' + infoGraphic.PanelClass + '"> ' +
            '<div class="panel-heading" style="height: 120px;overflow: hidden;"> ' +
            '<div class="row"> ' +
            '<div class="col-xs-3"> ' +
            '<i class="fa fa-tasks fa-5x"></i> ' +
            //         '<i class="glyphicon glyphicon-tasks"></i>' +
            '</div> ' +
            '<div class="col-xs-9 text-right"> ' +
            '<div class="huge"></div> ' +
            '<div><h4>' + infoGraphic.Name + '<br/></h4>' +
            '<br/><h5>(Million PKR)</h5> ' +
            '</div></div> </div></div> ' +
            '<a href="#"> ' +
            '<div class="panel-footer" style="height: auto;overflow: auto;"> ';
        var table = '<table class="table table-striped">';
        for (var i = 0; i < me.infoGraphicInfo.length; i++) {
            // var infodiv = '<div><h5><b>' + me.infoGraphicInfo[i].name + '</b>: <label id="' + prefix + '_' + me.infoGraphicInfo[i].id + '">' + me.infoGraphicInfo[i].init + '</label></h5></div> ';
            // panel += infodiv;
            table += '<tr>';
            table += '<th>' + me.infoGraphicInfo[i].name + '</th>';
            table += '<td><label class="infolabel" id="' + prefix + '_' + me.infoGraphicInfo[i].id + '" /></td>';
            table += '</tr>';
        }
        panel += table;
        panel += '<div class="clearfix"></div> </div> </a> </div></div>';
        return $(panel);
    }

    me.createSchemesGridPanel = function () {
        var pnl = ' <div class="col-lg-12"> ' +
            '<div class="panel panel-primary"> ' +
            // '<div class="panel-heading" style="height:50px">Scheme List Table</div>' +
            '<div class="panel-body"> ' +
            '<div class="alert alert-info" id="alertClass"> ' +  //data-bind="css: alertClass"
            '<a href="#" data-bind="click: removeAlert" class="close"  aria-label="close">x</a>' +
            '<span id="alertText">Scheme List Table</span> </div>' +  //
            '<div style="height: 600px;" id="' + me.schemeDivId + '" class="col-lg-12"></div> ' +
            '</div> </div>';

        // var kopnl = $(pnl)[0];
        // ko.cleanNode(kopnl);
        // ko.applyBindings(adpVM, kopnl);
        return $(pnl);
    }

    me.setRecordStatsToZero = function () {
        var statsObj = {};
        try {
            for (var i = 0; i < me.infoGraphics.length; i++) {
                var prefix = me.infoGraphics[i].id;
                for (var j = 0; j < me.infoGraphicInfo.length; j++) {
                    var key = prefix + '_' + me.infoGraphicInfo[j].id;
                    // me.fillInfoGraphicValue(key,'0');
                    statsObj[key] = 0;
                }
            }
        } catch (err) {
            console.error(err.stack);
        }
        return statsObj;
    }

    me.setRecordStatsInInfoGraphics = function (recordsStats) {

        try {
            // var records = $("#" + me.schemeDivId).jqxGrid('getrows');
            //
            // var statsObj = me.calculateRecordStats(records);
            for (var i = 0; i < me.infoGraphics.length; i++) {
                var prefix = me.infoGraphics[i].id;
                for (var j = 0; j < me.infoGraphicInfo.length; j++) {
                    var key = prefix + '_' + me.infoGraphicInfo[j].id;
                    var val = 0;
                    if (recordsStats[key]) {
                        var val = recordsStats[key]
                    }
                    me.fillInfoGraphicValue(key, val);
                }
            }
        } catch (err) {
            console.error(err.stack);
        }
    }

    me.fillInfoGraphicValue = function (key, val) {
        var label = $('#' + key);
        if (label) {
            var isDecimal = true;
            if (key.indexOf("count") != -1) isDecimal = false;
            val = adpVM.numberFormat(val, isDecimal);
            // statsObj[prefix + "_utilization_wrt_release"] +="%";
            // statsObj[prefix+"_utilization_wrt_allocation"] +="%";
            if (key.indexOf("wrt") != -1) val += "%";
            label.text(val);
        }
    }

    me.calculateRecordStats = function (records) {
        var statsObj = me.setRecordStatsToZero();
        try {
            // var prefixKey={"ALL SCHEMES":"all", "NEW SCHEMES":"ns", "ON-GOING SCHEMES":"ogs", "OTHER DEVELOPMENT PROGRAM":"odp", "NEW INDUCTED":"ni"};
            var prefixKey = me.adpVM.info.prefixKey;
            for (var i = 0; i < records.length; i++) {
                var record = records[i];
                if (record["Type"].toUpperCase() != '') {
                    var prefix = prefixKey[record["Type"].toUpperCase()];
                    statsObj["all_count"] += 1;
                    statsObj[prefix + "_count"] += 1;
                    for (var j = 0; j < me.infoGraphicInfo.length; j++) {
                        if (me.infoGraphicInfo[j].recordKey) {
                            var value = parseFloat(record[me.infoGraphicInfo[j].recordKey]);///1000000;
                            if (isNaN(value)) value = 0;
                            statsObj["all_" + me.infoGraphicInfo[j].id] += value;
                            statsObj[prefix + "_" + me.infoGraphicInfo[j].id] += value;
                        }
                    }
                }
            }
            // for(var key in prefixKey){
            //     var prefix = prefixKey[key];
            //     if(statsObj[prefix+"_release"]==0) {
            //         statsObj[prefix + "_utilization_wrt_release"] = 0;
            //     }else{
            //         statsObj[prefix + "_utilization_wrt_release"] = statsObj[prefix + "_utilization"] / statsObj[prefix+"_release"] * 100;
            //     }
            //     if(statsObj[prefix+"_allocation"]==0){
            //         statsObj[prefix+"_utilization_wrt_allocation"] = 0;
            //     }else{
            //         statsObj[prefix+"_utilization_wrt_allocation"] = statsObj[prefix+"_utilization"]/statsObj[prefix+"_allocation"]*100;
            //     }
            // }

        } catch (err) {
            console.error(err.stack);
        }
        return statsObj;
    }
}

var FilterSchemesModel = function (adpVM) {
    var me = this;
    me.cmbYearsList = $("#lstYears");
    me.cmbSectorList = $("#sectorsList");
    me.cmbDistrictList = $("#districtsList");
    me.sliderCostRange = $("#totalCostRange");
    me.sliderAllocationRange = $("#totalAllocationRange")
    var costField = "Total_Cost";
    var allocationField = "Allocation";
    me.initialize = function () {
        try {
            var fields = me.fields();
            var costIndex = me.findIndex(fields, 'Total_Cost');
            var allocationIndex = me.findIndex(fields, 'Allocation');
            var sectorGroup = me.groupBy('Sector');
            var districtGroup = me.groupBy('District');
            me.cmbSectorList
                .append($('<option>', {value: '-1'})
                    .text('All Sectors'));
            me.cmbDistrictList
                .append($('<option>', {value: '-1'})
                    .text('All Districts'));
            $.each(sectorGroup, function (key, value) {
                me.cmbSectorList
                    .append($('<option>', {value: key})
                        .text(key));
            });
            $.each(districtGroup, function (key, value) {
                me.cmbDistrictList
                    .append($('<option>', {value: key})
                        .text(key));
            });
            me.minCostValue = parseFloat(me.min(costField));
            me.maxCostValue = parseFloat(me.max(costField));
            me.minAllocationValue = parseFloat(me.min(allocationField));
            me.maxAllocationValue = parseFloat(me.max(allocationField));
            me.sliderCostRange.bootstrapSlider({
                id: "costSlideer",
                min: me.minCostValue,
                max: me.maxCostValue,
                range: true
            })
            me.sliderAllocationRange.bootstrapSlider({
                id: "allocationSlider",
                min: me.minAllocationValue,
                max: me.maxAllocationValue,
                range: true
            })
        } catch (err) {
            console.error(err.stack);
        }
    }

    me.filterInformation = 'Filter applied on ';
    me.clearFilter = function () {
        me.sliderCostRange.bootstrapSlider('setValue', [me.minCostValue, me.maxCostValue]);
        me.sliderAllocationRange.bootstrapSlider('setValue', [me.minAllocationValue, me.maxAllocationValue]);
        me.cmbSectorList.val("-1");
        me.cmbDistrictList.val("-1");
        // me.cmbYearsList.val("-1");

    }
    me.applyFilter = function (sector, district) {
        $("#divSchemesList").jqxGrid('clearfilters');

        me.applySectorFilter();
        me.applyDistrictFilter();

        me.applyCostFilter();
        me.applyAllocationFilter();

        $("#divSchemesList").jqxGrid('applyfilters');

        var records = $("#" + adpVM.overviewModel.schemeDivId).jqxGrid('getrows');
        var statsObj = adpVM.overviewModel.calculateRecordStats(records);
        adpVM.overviewModel.setRecordStatsInInfoGraphics(statsObj);

    }
    me.applyAllocationFilter = function () {
        var maxValue = me.sliderAllocationRange.data().bootstrapSlider.options.max;
        var minValue = me.sliderAllocationRange.data().bootstrapSlider.options.value;
        var range = me.sliderAllocationRange.bootstrapSlider("getValue");
        var minAlloc = range[0];
        var maxAlloc = range[1];
        if (parseInt(minAlloc) != parseInt(minValue) || parseInt(maxAlloc) != parseInt(maxValue)) {
            var allocFilterGroup = new $.jqx.filter();
            var alloc_operator;

            allocFilterGroup.operator = 'and';
            alloc_operator = 0;

            var filterMinValue = minAlloc;
            var filterMinCondition = 'GREATER_THAN_OR_EQUAL';
            var filterMaxValue = maxAlloc;
            var filterMaxCondition = 'LESS_THAN_OR_EQUAL';

            var costMinFilter = allocFilterGroup.createfilter('numericfilter', filterMinValue, filterMinCondition);
            var costMaxFilter = allocFilterGroup.createfilter('numericfilter', filterMaxValue, filterMaxCondition);

            allocFilterGroup.addfilter(alloc_operator, costMinFilter);
            allocFilterGroup.addfilter(alloc_operator, costMaxFilter);
            $("#divSchemesList").jqxGrid('addfilter', 'Allocation', allocFilterGroup);
            me.filterInformation += "Allocation Range =  " + range[0] + "-" + range[1] + ";";
        }
    }

    me.applyCostFilter = function () {
        var maxValue = me.sliderCostRange.data().bootstrapSlider.options.max;
        var minValue = me.sliderCostRange.data().bootstrapSlider.options.value;
        var range = me.sliderCostRange.bootstrapSlider("getValue");
        var minCost = range[0];
        var maxCost = range[1];
        if (parseInt(minCost) != parseInt(minValue) || parseInt(maxCost) != parseInt(maxValue)) {
            var costFilterGroup = new $.jqx.filter();
            var cost_operator;

            costFilterGroup.operator = 'and';
            cost_operator = 0;

            var filterMinValue = minCost;
            var filterMinCondition = 'GREATER_THAN_OR_EQUAL';
            var filterMaxValue = maxCost;
            var filterMaxCondition = 'LESS_THAN_OR_EQUAL';

            var costMinFilter = costFilterGroup.createfilter('numericfilter', filterMinValue, filterMinCondition);
            var costMaxFilter = costFilterGroup.createfilter('numericfilter', filterMaxValue, filterMaxCondition);

            costFilterGroup.addfilter(cost_operator, costMinFilter);
            costFilterGroup.addfilter(cost_operator, costMaxFilter);
            $("#divSchemesList").jqxGrid('addfilter', 'Total_Cost', costFilterGroup);
            me.filterInformation += "Cost Range =  " + range[0] + "-" + range[1] + ";";
        }
    }

    me.applyDistrictFilter = function () {
        var districtFilterGroup = new $.jqx.filter();
        var districtName = me.cmbDistrictList.val();
        var district_operator = null;
        if (districtName != '-1') {
            districtFilterGroup.operator = 'and';
            district_operator = 0;
            var filtervalue = districtName;
            var filtercondition = 'equal';
            var districtFilter1 = districtFilterGroup.createfilter('stringfilter', filtervalue, filtercondition);
            districtFilterGroup.addfilter(district_operator, districtFilter1);
            $("#divSchemesList").jqxGrid('addfilter', 'District', districtFilterGroup);
            me.filterInformation += "district =  " + districtName + ";";
        }
    }

    me.applySectorFilter = function () {
        var sectorFilterGroup = new $.jqx.filter();
        var sectorName = me.cmbSectorList.val();
        var sector_operator = null;
        if (sectorName != '-1') {
            sectorFilterGroup.operator = 'and';
            sector_operator = 0;
            var filtervalue = sectorName;
            var filtercondition = 'equal';
            var sectorFilter1 = sectorFilterGroup.createfilter('stringfilter', filtervalue, filtercondition);
            sectorFilterGroup.addfilter(sector_operator, sectorFilter1);
            $("#divSchemesList").jqxGrid('addfilter', 'Sector', sectorFilterGroup);
            me.filterInformation += "sector =  " + sectorName + ";";
        }
    }

    me.getYearData = function (year) {
        if (year != '-1') {
            var groupByData = me.groupBy('Year');
            for (var key in groupByData) {
                if (key == year) {
                    return groupByData[key];
                }
            }
        }else {
            return adpVM.schemesList;
        }
    }
    me.findIndex = function (list, value) {
        for (var i = 0; i < list.length; i++) {
            if (list[i].indexOf('value') != -1) {
                return i;
            }
        }
    }
    me.groupBy = function (key) {
        var sortedList = _(adpVM.schemesList).sortBy(key);
        var result = _(sortedList).groupBy(function (scheme) {
            if (scheme[key] != null) {
                var res = scheme[key].split(",");
                var value = null;
                if (res.length > 1) {
                    value = "Multiple-" + key;
                } else {
                    value = scheme[key].trim();
                }
                return value;
            }
        });
        return result;
    }
    me.max = function (key) {
        var result = _(adpVM.schemesList).max(function (scheme) {
            return parseFloat(scheme[key]);
        });
        return result[key];
    }
    me.min = function (key) {
        var result = _.min(adpVM.schemesList, function (scheme) {
            return parseFloat(scheme[key]);
        });
        return result[key];
    }
    me.fields = function (dataset) {
        if (!dataset) dataset = adpVM.schemesList[0];
        var result = _.keys(dataset);
        return result;
    }
}

