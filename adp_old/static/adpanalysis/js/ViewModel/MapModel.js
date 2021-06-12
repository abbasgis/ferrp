/**
 * Created by idrees on 5/10/2017.
 */
var MapModel = function (data, geoJson) {

    var me = this;
    me.schemesStats = data;
    me.geoJson = geoJson[0].row_to_json;//JSON.parse(geoJson);
    me.districtsList = null;
    me.columnsList = null;
    me.statsModel = new StatsModel(me);

    me.createMapView = function (dataDivId) {
        var table = $('<table class="table mytable" ></table>');

        var trFields = $('<tr class="tablerowone"></tr>');
        var tdYear = $('<td id="tdYear"><label >Data Selection</label></td>');
        var tdColumns = $('<td id="tdColumns"><label>Where Clause</label></td>');

        tdYear.append(me.createComboBox('cmbYear', 'Year'));
        tdYear.append(me.createComboBox('cmbColumns', 'Column'));

        tdColumns.append(me.createComboBox('cmbType', 'Type'));
        tdColumns.append(me.createComboBox('cmbSector', 'Sector'));

        trFields.append(tdYear);
        trFields.append(tdColumns);

        var trMap = $('<tr class="tablerowtwo"></tr>');
        var tdMap = $('<td id="tdMap" colspan="2"></td>');
        trMap.append(tdMap);

        table.append(trFields);
        table.append(tdMap);
        $('#' + dataDivId).html('');
        $('#' + dataDivId).append(table);

        me.populateComboes();
        me.selectComboValuesOnPageLoad();
        var whereClause = me.getWhereClause("<--All Types-->", "<--All Sectors-->");
        me.createHighMap('Allocation', '2015-16', whereClause);
        me.comboesOnChange();
    }

    me.selectComboValuesOnPageLoad = function(){
        $('[name=cmbYear] option').filter(function() {
            return ($(this).text() == '2015-16');
        }).prop('selected', true);
        $('[name=cmbColumns] option').filter(function() {
            return ($(this).text() == 'Allocation');
        }).prop('selected', true);
        //$('[name=cmbType] option').filter(function() {
        //    return ($(this).text() == 'NEW SCHEMES');
        //}).prop('selected', true);
        //$('[name=cmbSector] option').filter(function() {
        //    return ($(this).text() == 'Roads');
        //}).prop('selected', true);
    }

    me.createComboBox = function (id, text) {
        var combo = '<select id="' + id + '" name="' + id + '" class="form-control" style="margin:2px;">' +
            '<option value="-1">Select ' + text + '</option>' +
            '</select>';
        return $(combo);
    }

    me.populateComboes = function () {
        var data = me.schemesStats;
        var columnsList = me.statsModel.getColumnsList(data);
        var yearsList = me.statsModel.getUniqueValues(data, "Year");
        var typeList = me.statsModel.getUniqueValues(data, "Type");
        var sectorList = me.statsModel.getUniqueValues(data, "Sector");

        var cmbYear = $('#cmbYear');
        var cmbColumns = $('#cmbColumns');
        var cmbType = $('#cmbType');
        var cmbSector = $('#cmbSector');

        cmbYear.empty();
        cmbColumns.empty();
        cmbType.empty();
        cmbSector.empty();

        cmbColumns.append('<option value="-1"><--Select Column--></option>');
        $.each(columnsList, function (index, value) {
            cmbColumns.append('<option value="' + value + '">' + value + '</option>');
        });

        cmbYear.append('<option value="-1"><--All Years--></option>');
        $.each(yearsList, function (index, value) {
            cmbYear.append('<option value="' + value + '">' + value + '</option>');
        });

        cmbType.append('<option value="-1"><--All Types--></option>');
        $.each(typeList, function (index, value) {
            cmbType.append('<option value="' + value + '">' + value + '</option>');
        });

        cmbSector.append('<option value="-1"><--All Sectors--></option>');
        $.each(sectorList, function (index, value) {
            cmbSector.append('<option value="' + value + '">' + value + '</option>');
        });
    }

    me.createHighMap = function (fact, year, whereClause) {

        var factStats = me.mapData(year, fact, whereClause);
        try {
            Highcharts.mapChart('tdMap', {

                chart: {
                    borderWidth: 2
                },
                title: {
                    text:  fact + ' ' + year
                },
                legend: {
                    layout: 'horizontal',
                    borderWidth: 0,
                    backgroundColor: 'rgba(255,255,255,0.3)',
                    floating: true,
                    align:'right',
                    verticalAlign: 'bottom'
                },
                mapNavigation: {
                    enabled: true
                },
                colorAxis: {
                    min: 1,
                    type: 'logarithmic',
                    minColor: '#EEEEFF',
                    maxColor: '#002020  ',
                    stops: [
                        [0, '#EEEEFF'],
                        [0.4, '#00F000'],
                        [0.8, '#007000'],
                        [1, '#001800']
                    ]
                },
                series: [{
                    animation: {
                        duration: 500
                    },
                    data: factStats,
                    mapData: me.geoJson,
                    joinBy: ['name', 'code'],
                    dataLabels: {
                        enabled: true,
                        color: '#FFFFFF',
                        format: '{point.code}'
                    },
                    name: fact + ' ' + year,
                    tooltip: {
                        pointFormat: '{point.name}: {point.value} PKR Million'
                    }
                }]
            });
        } catch (err) {
            console.error(err.stack);
        }
    }

    me.mapData = function (year, fact, whereClause) {
        var data = me.schemesStats;
        var yearData = null;
        var yearsGroup = null;
        if(year == '<--All Years-->'){
            yearData = data;
        }else{
            yearsGroup = me.statsModel.groupBy(data, 'Year');
            yearData = yearsGroup[year];
        }
        var typeSectorData = _.where(yearData, whereClause);
        var districtsGroup = me.statsModel.groupBy(typeSectorData, 'District');
        var districtsList = me.statsModel.getUniqueValues(typeSectorData, "District");

        //var sectorTypeDistrictsGroup = _.where(districtsGroup, "Sector=");
        var output = [];
        for (var i = 0; i<districtsList.length; i ++){
            var key = districtsList[i];
            if(key == "Multiple Districts" || key == "Unknown" || key == "Punjab" || key == "Islamabad" || key == "Karachi" || key == "Balochistan"){

            }else{
                var districtArray = districtsGroup[key];
                var factVal = 0;
                for(var j=0;j<districtArray.length;j++){
                    factVal += (isNaN(districtArray[j][fact]) ? 0 : districtArray[j][fact]);
                }
                if(factVal == 0) factVal = 0.0000001;
                var obj = {};
                obj.code = key;
                obj.value = factVal;
                output.push(obj);
            }
        }
        return output;
    }

    me.comboesOnChange = function(){
        $('#cmbYear').change(function(){
            var year = $(this).find("option:selected").text();
            var fact = $('#cmbColumns').find("option:selected").text();
            var type = $('#cmbType').find("option:selected").text();
            var sector = $('#cmbSector').find("option:selected").text();
            var whereClause = me.getWhereClause(type, sector);
            me.createHighMap(fact, year, whereClause);
        });

        $('#cmbColumns').change(function(){
            var fact = $(this).find("option:selected").text();
            var year = $('#cmbYear').find("option:selected").text();
            var type = $('#cmbType').find("option:selected").text();
            var sector = $('#cmbSector').find("option:selected").text();
            var whereClause = me.getWhereClause(type, sector);
            me.createHighMap(fact, year, whereClause);
        });

        $('#cmbType').change(function(){
            var type = $(this).find("option:selected").text();
            var year = $('#cmbYear').find("option:selected").text();
            var fact = $('#cmbColumns').find("option:selected").text();
            var sector = $('#cmbSector').find("option:selected").text();
            var whereClause = me.getWhereClause(type, sector);
            me.createHighMap(fact, year, whereClause);
        });

        $('#cmbSector').change(function(){
            var sector = $(this).find("option:selected").text();
            var year = $('#cmbYear').find("option:selected").text();
            var type = $('#cmbType').find("option:selected").text();
            var fact = $('#cmbColumns').find("option:selected").text();
            var whereClause = me.getWhereClause(type, sector);
            me.createHighMap(fact, year, whereClause);
        });
    }

    me.getWhereClause = function(type, sector){
        var whereClause = {};
        if(type == "<--All Types-->" && sector == "<--All Sectors-->"){
            whereClause = {};
        }if(type != "<--All Types-->" && sector != "<--All Sectors-->"){
            whereClause.Type = type;
            whereClause.Sector = sector;
        }if(type == "<--All Types-->" && sector != "<--All Sectors-->"){
            whereClause.Sector = sector;
        }if(type != "<--All Types-->" && sector == "<--All Sectors-->"){
            whereClause.Type = type;
        }
        return whereClause;
    }

}