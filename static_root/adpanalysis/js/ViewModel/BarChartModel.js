/**
 * Created by idrees on 5/5/2017.
 */
var BarChartModel = function(parentModel, schemeStats){
    var me = this;
    me.aaVM = parentModel;
    me.statsModel = new StatsModel(me);
    me.schemeStats = schemeStats;
    me.xAxisUniqueValues = null;
    me.columnUniqueValues = null;
    me.dataColumn = [];
    me.groupcolumn = [];

    me.createBarChartView = function(dataDivId){

        var table = $('<table class="table mytable" ></table>');

        var trfields = $('<tr class="tablerowone"></tr>');
        var tdFacts = $('<td id="tdFacts"><label >Y Field</label></td>');
        var tdXDim = $('<td id="tdXDim"><label >X Field</label></td>');
        var tdXDimUniqueValues = $('<div id="tdXDimUniqueValues"></div>');
        var tdYDim = $('<div id="tdYDim"><label>Column Field</label></div>');
        var tdYDimUniqueValues = $('<div id="tdYDimUniqueValues"></div>');

        tdFacts.append(me.createComboBox('cmbFacts', 'Fact'));
        tdFacts.append(me.createComboBox('cmbFactsColumns', 'Fact Column'));
        tdXDim.append(me.createComboBox('cmbXDim', 'X Field'));
        tdXDim.append(tdXDimUniqueValues);
        //tdXDim.append(me.createComboBox('cmbXDimUniqueValues', 'Column Field Data'));
        tdYDim.append(me.createComboBox('cmbGroupDim', 'Group Field'));
        tdYDim.append(tdYDimUniqueValues);
        //tdYDim.append(me.createComboBox('cmbYDimUniqueValues', 'Row Field Data'));

        trfields.append(tdFacts);
        trfields.append(tdXDim);
        trfields.append(tdYDim);
        table.append(trfields);

        var trSecond = $('<tr class="tablerowtwo"></tr>');
        var tdChart = $('<td id="tdBarChart" colspan="3"></td>');
        trSecond.append(tdChart);
        table.append(trSecond);
        $('#'+dataDivId).html('');
        $('#'+dataDivId).append(table);
        me.populateComboes();
        //me.populateComboes();
        me.selectComboesDataOnPageLoad();
        var data = me.createChartData('Allocation', 'Main_Sector', 'Year');
        var distList = me.statsModel.getUniqueValues(me.schemeStats, 'Main_Sector');
        me.createBarChart(data, distList, 'Allocation', 'Main_Sector Year Allocation');
        var ddlXAxisUniqueValues = me.xAxisDropDownListWithCheckBoxes(me.xAxisUniqueValues);
        var ddlColumnsUniqueValues = me.columnsDropDownListWithCheckBoxes(me.columnUniqueValues);

        $('#tdXDimUniqueValues').append(ddlXAxisUniqueValues);
        $('#tdYDimUniqueValues').append(ddlColumnsUniqueValues);
        $('#xAxisDDL').multiselect({
            enableFiltering: true,
            maxHeight: 400,
            includeSelectAllOption: true,
            onDropdownHide: function(event) {
                var factColumnName = $('#cmbFactsColumns').find("option:selected").text();
                var dataColumnName = $('#cmbXDim').find("option:selected").text();
                var groupColumnName = $('#cmbGroupDim').find("option:selected").text();
                var data = me.createChartDataTest(factColumnName, dataColumnName, groupColumnName, me.dataColumn, me.groupcolumn);
                me.createBarChart(data, me.dataColumn, factColumnName, dataColumnName + ' ' + groupColumnName + ' ' + factColumnName);
            },
            onChange: function(option, checked) {
                var selected = [];
                $('#xAxisDDL option:selected').each(function() {
                    selected.push([$(this).val(), $(this).data('order')]);
                });

                selected.sort(function(a, b) {
                    return a[1] - b[1];
                });

                var text = '';
                me.dataColumn = [];
                for (var i = 0; i < selected.length; i++) {
                    text += selected[i][0] + ', ';
                    me.dataColumn.push(selected[i][0]);
                }
                text = text.substring(0, text.length - 2);

                //alert(text);
            }
        });
        $('#columnsDDL').multiselect({
            enableFiltering: true,
            maxHeight: 400,
            includeSelectAllOption: true,
            onDropdownHide: function(event) {
                var factColumnName = $('#cmbFactsColumns').find("option:selected").text();
                var dataColumnName = $('#cmbXDim').find("option:selected").text();
                var groupColumnName = $('#cmbGroupDim').find("option:selected").text();
                var data = me.createChartDataTest(factColumnName, dataColumnName, groupColumnName, me.dataColumn, me.groupcolumn);
                me.createBarChart(data, me.dataColumn, factColumnName, dataColumnName + ' ' + groupColumnName + ' ' + factColumnName);
            },
            onChange: function(option, checked) {
                var selected = [];
                $('#columnsDDL option:selected').each(function() {
                    selected.push([$(this).val(), $(this).data('order')]);
                });

                selected.sort(function(a, b) {
                    return a[1] - b[1];
                });
                me.groupcolumn = [];
                for (var i = 0; i < selected.length; i++) {
                    me.groupcolumn.push(selected[i][0]);
                }
            }
        });

        me.comboesOnChange();
    }

    me.createBarChart = function(data, sectorsList, yLabel, label){
        var barchart =  Highcharts.chart('tdBarChart', {
            chart: {
                type: 'column'
            },
            title: {
                text: label
            },
            xAxis: {
                categories: sectorsList
            },
            yAxis: {
                min: 0,
                title: {
                    text: yLabel+'(Million PKR)'
                }
            },
            tooltip: {
                headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
                pointFormat: '<tr><td style="color:{series.color};padding:0; font-size:10px;">{series.name}: </td>' +
                '<td style="padding:0; font-size:10px;"><b>{point.y:.1f}Million PKR</b></td></tr>',
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
            //height:'100%',
            //width:'100%',
            series: data
        });
    }

    me.populateComboes = function(){

        var data = me.schemeStats;
        var columnsList = me.statsModel.getColumnsList(data);
        var sumColumnsList = me.sumFactColumnsList();
        var countColumnsList = me.countFactColumnsList();

        var cmbFacts = $('#cmbFacts');
        var cmbFactsColumns = $('#cmbFactsColumns');
        var cmbXDim = $('#cmbXDim');
        var cmbGroupDim = $('#cmbGroupDim');

        cmbFacts.empty();
        cmbFactsColumns.empty();
        cmbXDim.empty();
        cmbGroupDim.empty();

        cmbFacts.append('<option value="1">Sum</option>');
        cmbFacts.append('<option value="2">Count</option>');

        //$('#cmbFacts').change(function(){
        //    var cmbFactValue = $('#cmbFacts option:selected').val();
        //    $('#cmbFactsColumns').empty();
        //    $('#cmbFactsColumns').append('<option value="Select Fact Column">Select Fact Column</option>');
        //    if(cmbFactValue == "1"){
        //        $.each(sumColumnsList, function(index, value) {
        //            $('#cmbFactsColumns').append('<option value="' + value +'">' + value + '</option>');
        //        });
        //    }if(cmbFactValue == "2"){
        //        $.each(countColumnsList, function(index, value) {
        //            $('#cmbFactsColumns').append('<option value="' + value +'">' + value + '</option>');
        //        });
        //    }else{
        //        $('#cmbFactsColumns').empty();
        //        $('#cmbFactsColumns').append('<option value="Select Fact Column">Select Fact Column</option>');
        //    };
        //});

        $.each(sumColumnsList, function(index, value) {
            cmbFactsColumns.append('<option value="' + value +'">' + value + '</option>');
        });

        $.each(countColumnsList, function(index, value) {
            cmbXDim.append('<option value="' + value +'">' + value + '</option>');
        });
        $.each(countColumnsList, function(index, value) {
            cmbGroupDim.append('<option value="' + value +'">' + value + '</option>');
        });
    }

    me.createChartData = function(factField, dataField, groupByField){
        var data = me.schemeStats;
        var factFieldSum = 0;
        var dataFieldsList = me.statsModel.getUniqueValues(data, dataField);
        var groupByFieldList = me.statsModel.getUniqueValues(data, groupByField);
        me.xAxisUniqueValues = dataFieldsList;
        me.columnUniqueValues = groupByFieldList;

        var finalArray = [];
        var dataFieldName = "";
        var groupData = _.groupBy(data, groupByField);

        for(var i = 0; i<groupByFieldList.length; i++){
            var dRecord = new Array();
            var groupName = groupByFieldList[i];
            var groupByRecord = groupData[groupName];
            var dataFieldGroupData = _.groupBy(groupByRecord, dataField);
            for(var k = 0; k<dataFieldsList.length; k++){

                factFieldSum = 0;
                dataFieldName = dataFieldsList[k];
                var dataFieldRecord = dataFieldGroupData[dataFieldName];
                if(dataFieldRecord){
                    for(var l = 0; l<dataFieldRecord.length; l++){
                        factFieldSum += (isNaN(dataFieldRecord[l][factField]) ? 0 : dataFieldRecord[l][factField]);
                    }
                }
                dRecord.push(factFieldSum);
            }
            finalArray.push({name:groupName, data:dRecord});
        }
        return finalArray;

    }

    me.createChartDataTest = function(factField, dataField, groupByField, dataFieldsList, groupByFieldList){
        var data = me.schemeStats;
        var factFieldSum = 0;
        me.xAxisUniqueValues = dataFieldsList;
        me.columnUniqueValues = groupByFieldList;

        var finalArray = [];
        var dataFieldName = "";
        var groupData = _.groupBy(data, groupByField);

        for(var i = 0; i<groupByFieldList.length; i++){
            var dRecord = new Array();
            var groupName = groupByFieldList[i];
            var groupByRecord = groupData[groupName];
            var dataFieldGroupData = _.groupBy(groupByRecord, dataField);
            for(var k = 0; k<dataFieldsList.length; k++){

                factFieldSum = 0;
                dataFieldName = dataFieldsList[k];
                var dataFieldRecord = dataFieldGroupData[dataFieldName];
                if(dataFieldRecord){
                    for(var l = 0; l<dataFieldRecord.length; l++){
                        factFieldSum += (isNaN(dataFieldRecord[l][factField]) ? 0 : dataFieldRecord[l][factField]);
                    }
                }
                dRecord.push(factFieldSum);
            }
            finalArray.push({name:groupName, data:dRecord});
        }
        return finalArray;

    }

    me.selectComboesDataOnPageLoad = function(){
        $('[name=cmbFacts]').val( 1 );
        $('[name=cmbFactsColumns] option').filter(function() {
            return ($(this).text() == 'Allocation'); //To select Blue
        }).prop('selected', true);
        $('[name=cmbXDim] option').filter(function() {
            return ($(this).text() == 'Main_Sector'); //To select Blue
        }).prop('selected', true);
        $('[name=cmbGroupDim] option').filter(function() {
            return ($(this).text() == 'Year'); //To select Blue
        }).prop('selected', true);
    }

    me.createComboBox = function(id, text){
        var combo = '<select id="'+id+'" name="'+id+'" class="form-control" style="margin:2px;">'+
            '<option value="-1">Select '+text+'</option>'+
            '</select>';
        return $(combo);
    }

    me.sumFactColumnsList = function(){
        var columnsList = [];
        columnsList.push('Schemes');
        columnsList.push('Total_Cost');
        columnsList.push('Allocation');
        columnsList.push('Local_Capital');
        columnsList.push('Local_Revenue');
        columnsList.push('Total_Capital');
        columnsList.push('Total_Revenue');
        columnsList.push('Foreign_Aid_Capital');
        columnsList.push('Foreign_Aid_Revenue');
        columnsList.push('Foreign_Aid_Total');
        columnsList.push('Projection_One');
        columnsList.push('Projection_Two');
        columnsList.push('Throw_Forward');
        return columnsList;
    }

    me.countFactColumnsList = function(){
        var columnsList = [];
        columnsList.push('Year');
        columnsList.push('Type');
        columnsList.push('Main_Sector');
        columnsList.push('Sector');
        columnsList.push('District');
        return columnsList;
    }

    me.comboesOnChange = function(){
        $('#cmbFactsColumns').change(function(){

            var factColumnName = $(this).find("option:selected").text();
            var dataColumnName = $('#cmbXDim').find("option:selected").text();
            var groupColumnName = $('#cmbGroupDim').find("option:selected").text();
            var data = me.createChartDataTest(factColumnName, dataColumnName, groupColumnName, me.dataColumn, me.groupcolumn);
            me.createBarChart(data, me.dataColumn, factColumnName, dataColumnName + ' ' + groupColumnName + ' ' + factColumnName);
        });

        $('#cmbXDim').change(function(){
            var factColumn = $('#cmbFactsColumns').find("option:selected").text();
            var dataColumn = $(this).find("option:selected").text();
            var groupColumn = $('#cmbGroupDim').find("option:selected").text();
            var data = me.createChartData(factColumn, dataColumn, groupColumn);
            var distList = me.statsModel.getUniqueValues(me.schemeStats, dataColumn);
            me.createBarChart(data, distList, factColumn, dataColumn + ' ' + groupColumn + ' ' + factColumn);
            $('#tdXDimUniqueValues').html('');
            var ddlXAxisUniqueValues = me.xAxisDropDownListWithCheckBoxes(me.xAxisUniqueValues);
            $('#tdXDimUniqueValues').append(ddlXAxisUniqueValues);
            $('#xAxisDDL').multiselect({
                enableFiltering: true,
                includeSelectAllOption: true,
                maxHeight: 400,
                onDropdownHide: function(event) {
                    var factColumnName = $('#cmbFactsColumns').find("option:selected").text();
                    var dataColumnName = $('#cmbXDim').find("option:selected").text();
                    var groupColumnName = $('#cmbGroupDim').find("option:selected").text();
                    var data = me.createChartDataTest(factColumnName, dataColumnName, groupColumnName, me.dataColumn, me.groupcolumn);
                    me.createBarChart(data, me.dataColumn, factColumnName, dataColumnName + ' ' + groupColumnName + ' ' + factColumnName);
                },
                onChange: function(option, checked) {
                    var selected = [];
                    $('#xAxisDDL option:selected').each(function() {
                        selected.push([$(this).val(), $(this).data('order')]);
                    });

                    selected.sort(function(a, b) {
                        return a[1] - b[1];
                    });
                    me.dataColumn = [];
                    for (var i = 0; i < selected.length; i++) {
                        me.dataColumn.push(selected[i][0]);
                    }
                }
            });
        });

        $('#cmbGroupDim').change(function(){
            var factColumn = $('#cmbFactsColumns').find("option:selected").text();
            var dataColumn = $('#cmbXDim').find("option:selected").text();
            var groupColumn = $(this).find("option:selected").text();
            var data = me.createChartData(factColumn, dataColumn, groupColumn);
            var distList = me.statsModel.getUniqueValues(me.schemeStats, dataColumn);
            me.createBarChart(data, distList, factColumn, dataColumn + ' ' + groupColumn + ' ' + factColumn);

            $('#tdYDimUniqueValues').html('');
            var ddlColumnsUniqueValues = me.columnsDropDownListWithCheckBoxes(me.columnUniqueValues);
            $('#tdYDimUniqueValues').append(ddlColumnsUniqueValues);
            $('#columnsDDL').multiselect({
                enableFiltering: true,
                maxHeight: 400,
                includeSelectAllOption: true,
                onDropdownHide: function(event) {
                    var factColumnName = $('#cmbFactsColumns').find("option:selected").text();
                    var dataColumnName = $('#cmbXDim').find("option:selected").text();
                    var groupColumnName = $('#cmbGroupDim').find("option:selected").text();
                    var data = me.createChartDataTest(factColumnName, dataColumnName, groupColumnName, me.dataColumn, me.groupcolumn);
                    me.createBarChart(data, me.dataColumn, factColumnName, dataColumnName + ' ' + groupColumnName + ' ' + factColumnName);
                },
                onChange: function(option, checked) {
                    var selected = [];
                    $('#columnsDDL option:selected').each(function() {
                        selected.push([$(this).val(), $(this).data('order')]);
                    });

                    selected.sort(function(a, b) {
                        return a[1] - b[1];
                    });
                    me.groupcolumn = [];
                    for (var i = 0; i < selected.length; i++) {
                        me.groupcolumn.push(selected[i][0]);
                    }
                }
            });
        });
    }

    me.createCheckBox = function(displayText){
        var checkBox = '<li><a href="#" class="small" data-value="'+displayText+'" tabIndex="-1"><input type="checkbox"/>&nbsp;'+displayText+'</a></li>';
        return checkBox;
    }

    me.xAxisDropDownListWithCheckBoxes = function(dataList){
        var dropdownList = $('<select id="xAxisDDL" multiple="multiple"</select>');
        me.dataColumn = [];
        for(var i = 0; i<dataList.length; i++){
            var text = dataList[i];
            me.dataColumn.push(text);
            dropdownList.append('<option value="'+text+'" selected="true">'+text+'</option>');
        }
        return dropdownList;
    }

    me.columnsDropDownListWithCheckBoxes = function(dataList){
        var dropdownList = $('<select id="columnsDDL" multiple="multiple"></select>');
        me.groupcolumn = [];
        for(var i = 0; i<dataList.length; i++){
            var text = dataList[i];
            me.groupcolumn.push(text);
            dropdownList.append('<option value="'+text+'" selected="true">'+text+'</option>');
        }
        return dropdownList;
    }
}