/**
 * Created by idrees on 12/15/2017.
 */

var ArzGlobalFunctionsModel = function () {
    var me = this;
    me.findIndex = function (list, value) {
        for (var i = 0; i < list.length; i++) {
            if (list[i].indexOf('value') != -1) {
                return i;
            }
        }
    }
    me.groupBy = function (data, key) {
        var sortedList = _(data).sortBy(key);
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
    me.max = function (data, key) {
        var result = _(data).max(function (scheme) {
            return parseFloat(scheme[key]);
        });
        return result[key];
    }
    me.min = function (data, key) {
        var result = _.min(data, function (scheme) {
            return parseFloat(scheme[key]);
        });
        return result[key];
    }

    me.geoJsonAttributeMin = function (data, key) {
        var currentVal = 0;
        var minVal = data[0].properties[key];

        for (var i = 0; i < data.length; i++) {
            currentVal = data[i].properties[key];
            if (currentVal < minVal) {
                minVal = currentVal;
            }
        }
        return minVal;
    }

    me.geoJsonAttributeMax = function (data, key) {
        var currentVal = 0;
        var maxVal = data[0].properties[key];

        for (var i = 0; i < data.length; i++) {
            currentVal = data[i].properties[key];
            if (currentVal > maxVal) {
                maxVal = currentVal;
            }
        }
        return maxVal;
    }

    me.fields = function (dataset) {
        var result = _.keys(dataset[0]);
        return result;
    }

    // me.getColumnsList = function(data){
    //     var columnsList = [];
    //     if (data.length > 0){
    //         var columnsIn = data[0];
    //         for(var key in columnsIn){
    //             columnsList.push(key);
    //         }
    //     }else{
    //         console.log("No columns");
    //     }
    //     return columnsList;
    // }

    me.getColumnsList = function (data) {
        var columns = [];
        var stringType = "string";
        var numberType = 'number';
        columns.push({xtype: 'rownumberer'});
        for (var key in data) {
            if (key === "extent" || key === "geojson" || key === "id" || key === "canal_type" || key === "gid") {
            }
            else {
                if (isNaN(parseFloat(data[key]))) {
                    columns.push({
                        dataIndex: key,
                        text: me.getColumnHeaderTitle(key),
                        width: 125,
                        exportStyle: {
                            alignment: {
                                horizontal: 'Right'
                            },
                            font: {
                                bold: true
                            },
                            format: 'Text'
                        },
                        filter: {
                            type: stringType,
                            itemDefaults: {
                                emptyText: 'Search for...'
                            }
                        }
                    })
                } else {
                    columns.push({
                        dataIndex: key,
                        text: me.getColumnHeaderTitle(key),
                        width: 100,
                        filter: numberType,
                        exportStyle: {
                            alignment: {
                                horizontal: 'Right'
                            },
                            font: {
                                bold: true
                            }
                        }
                    })
                }

            }
        }
        return columns;
    }

    me.getFieldsList = function (data) {
        var arrField = new Array();
        for (var key in data) {
            var obj = {};
            if (key === "extent" || key === "geojson" || key === "canal_type") {
            } else {
                obj.id = key;
                obj.name = key;
                arrField.push(obj);
            }
        }
        return arrField;
    }

    me.getColumnHeaderTitle = function (name) {
        var fullName = "";
        if (name == "name") {
            fullName = "Name";
            return fullName;
        } else if (name == "cca_ma") {
            fullName = "CCA (MA)";
            return fullName;
        } else if (name == "gca_ma") {
            fullName = "GCA (MA)";
            return fullName;
        } else if (name == "cca_geom_ma") {
            fullName = "CCA Geom";
            return fullName;
        } else if (name == "gca_geom_ma") {
            fullName = "GCA Geom";
            return fullName;
        } else if (name == "length") {
            fullName = "Canals Length (KM)";
            return fullName;
        } else if (name == "outlets") {
            fullName = "Outlets";
            return fullName;
        } else if (name == "acz_name") {
            fullName = "Agri Zone";
            return fullName;
        } else if (name == "cca_name") {
            fullName = "CCA";
            return fullName;
        } else if (name == "doab") {
            fullName = "Doab";
            return fullName;
        } else if (name == "basin") {
            fullName = "Basin";
            return fullName;
        } else if (name == "area_ha") {
            fullName = "Area (Hec)";
            return fullName;
        } else if (name == "cca_dam") {
            fullName = "CCA Dam";
            return fullName;
        } else if (name == "zone_name") {
            fullName = "Zone Name";
            return fullName;
        } else if (name == "circle_name") {
            fullName = "Circle Name";
            return fullName;
        } else if (name == "division_name") {
            fullName = "Division Name";
            return fullName;
        } else if (name == "area_acre") {
            fullName = "Area (Acre)";
            return fullName;
        } else if (name == "area_acre") {
            fullName = "Area (Acre)";
            return fullName;
        } else if (name == "district_name") {
            fullName = "District";
            return fullName;
        } else if (name == "zone") {
            fullName = "Zone";
            return fullName;
        } else if (name == "area_zone") {
            fullName = "Zone Total Area";
            return fullName;
        } else if (name == "zone_area") {
            fullName = "Zone Area";
            return fullName;
        } else if (name == "zone_area_percentage") {
            fullName = "Zone Area %age";
            return fullName;
        } else if (name == "circle") {
            fullName = "Circle";
            return fullName;
        } else if (name == "area_circle") {
            fullName = "Circle Total Area";
            return fullName;
        } else if (name == "circle_area") {
            fullName = "Circle Area";
            return fullName;
        } else if (name == "circle_area_percentage") {
            fullName = "Circle Area %age";
            return fullName;
        } else if (name == "division") {
            fullName = "Division";
            return fullName;
        } else if (name == "area_division") {
            fullName = "Division Total Area";
            return fullName;
        } else if (name == "division_area") {
            fullName = "Division Area";
            return fullName;
        } else if (name == "division_area_percentage") {
            fullName = "Division Area %age";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else if (name == "punjab_district_area") {
            fullName = "District Area";
            return fullName;
        } else {
            return name
        }
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
    me.getReportWhereClause = function (zone, circle, division) {
        var whereClause = {};
        if (zone == "" && circle == "" && division == "") {
            whereClause = {};
        }
        if (zone != "" && circle == "" && division == "") {
            whereClause.zone_name = zone;
        }
        if (zone != "" && circle != "" && division == "") {
            whereClause.zone_name = zone;
            whereClause.circle_name = circle;
        }
        if (zone != "" && circle != "" && division != "") {
            whereClause.zone_name = zone;
            whereClause.circle_name = circle;
            whereClause.division_name = division;
        }
        return whereClause;
    }
    me.getWhereClauseData = function (data, whereClause) {
        var filteredData = _.where(data, whereClause);
        return filteredData;
    }
    me.getDataArray = function (arrData) {
        var dataArray = new Array();
        for (var i = 0; i < arrData.length; i++) {
            var arrRecord = {};
            var record = arrData[i];
            arrRecord.id = record;
            arrRecord.name = record;
            dataArray.push(arrRecord);
        }
        return dataArray;
    }

    me.numberFormat = function (val, isDecimal) {
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

    me.getEmailForm = function (dataType, whereClause, filterArray) {
        var emailForm = Ext.create('Ext.form.Panel', {
            border: true,
            id: 'canalDataEmailForm',
            fieldDefaults: {
                labelWidth: 75
            },
            defaultType: 'textfield',
            bodyPadding: 15,
            items: [{
                fieldLabel: 'E-Mail Id:',
                id: 'emailid',
                name: 'emailid',
                allowBlank: false,
                anchor: '100%'  // anchor width by percentage
            }],
            bbar: [
                {
                    text: 'Send E-Mail',
                    handler: sendEMail
                }]
        });

        if (me.win != null) {
            me.win.destroy();
        }
        me.win = new Ext.window.Window({
            closable: true,
            resizable: true,
            draggable: true,
            title: 'Email Data',
            width: 350,
            height: 200,
            minWidth: 200,
            minHeight: 50,
            plain: true,
            layout: 'fit',
            items: emailForm,
            // buttons: [{
            //
            // },
            // {
            //     text: 'Cancel',
            // }
            // ]
        });
        function sendEMail() {
            var url = '';
            if (dataType == 'commanded_area' || dataType == 'district') {
                url = 'onlineemailservice';
            } else {
                url = '../onlineemailservice';
            }
            var emailId = Ext.getCmp('emailid').getValue();
            var params = {data_type: dataType, where_clause: whereClause, emailid: emailId, filters: filterArray};
            var box = Ext.MessageBox.wait('Please wait...', 'Loading Data');
            Ext.Ajax.timeout = 900000;
            Ext.Ajax.request({
                url: url,
                params: params,//Ext.JSON.encode(params),
                headers: {'X-CSRFToken': csrf_token},
                method: "POST",
                success: function (response) {
                    box.hide();
                    alert(response.responseText);
                    me.win.hide();
                },
                failure: function (res) {
                    box.hide();
                    alert(res.responseText);
                }
            });
        }

        me.win.show();

    }

    me.getSMSForm = function (dataType, whereClause, filterArray) {
        var emailForm = Ext.create('Ext.form.Panel', {
            border: true,
            id: 'canalDataSMSForm',
            fieldDefaults: {
                labelWidth: 75
            },
            defaultType: 'textfield',
            bodyPadding: 15,
            items: [{
                fieldLabel: 'Contact No:',
                id: 'contactNo',
                name: 'contactNo',
                allowBlank: false,
                anchor: '100%'  // anchor width by percentage
            }, {
                xtype: 'label',
                text: 'Sample Number: 923xxxxxxxxx',
                margin: '0 0 0 0'
            }]
        });

        if (me.win != null) {
            me.win.destroy();
        }

        me.win = new Ext.window.Window({
            closable: true,
            resizable: true,
            draggable: true,
            title: 'SMS Data Link',
            width: 350,
            height: 200,
            minWidth: 200,
            minHeight: 50,
            plain: true,
            layout: 'fit',
            items: emailForm,
            buttons: [{
                text: 'Send SMS',
                handler: sendSMS
            },
                // {
                //     text: 'Clear',
                // }
            ]
        });

        function sendSMS() {
            var url = '';
            if (dataType == 'commanded_area' || dataType == 'district') {
                url = 'onlinesmsservice';
            } else {
                url = '../onlinesmsservice';
            }
            var contactNo = Ext.getCmp('contactNo').getValue();
            var params = {data_type: dataType, where_clause: whereClause, contact_no: contactNo, filters: filterArray};
            var box = Ext.MessageBox.wait('Please wait...', 'Loading Data');
            Ext.Ajax.timeout = 900000;
            Ext.Ajax.request({
                url: url,
                params: params,//Ext.JSON.encode(params),
                headers: {'X-CSRFToken': csrf_token},
                method: "POST",
                success: function (response) {
                    box.hide();
                    var message = response.responseText;
                    if (message == 'OK') {
                        alert('SMS Sent');
                    } else {
                        alert(message);
                    }
                    me.win.hide();
                },
                failure: function (res) {
                    box.hide();
                    alert(res.responseText);
                }
            });
        }

        me.win.show();

    }

    me.getDataFromGridItems= function (gridItems) {
        var recordsCount = gridItems.length;
        var dataArray = new Array();
        for (var i = 0; i < recordsCount; i++) {
            var itemObject = gridItems.items[i].data;
            // delete recordObject.id;
            data ={}
            for (var key in itemObject){
                if(itemObject[key]){
                    data[key] = itemObject[key];
                }else {
                    data[key] = 0.0;
                }
            }
            dataArray.push(data);
        }
        return dataArray;
    }

    me.convertExtGridDataToJsonObj  = function (gridItems, columnsList) {
        var recordsCount = gridItems.length;
        var dataArray = new Array();

        keys = [];
        for (var i=1;i<columnsList.length;i++){
            keys.push(columnsList[i].dataIndex)
        }
        for (var i = 0; i < recordsCount; i++) {
            var itemObject = gridItems.items[i].data;
            // delete recordObject.id;
            data ={}
            for (var j=0; j<keys.length; j++){
                if(itemObject[keys[j]]){
                    data[keys[j]] = itemObject[keys[j]];
                }else {
                    data[keys[j]] = 0.0;
                }
            }
            dataArray.push(data);
        }
        return dataArray;
    }

    me.getParameterByName = function (name) {
        var url = window.location.href;
        name = name.replace(/[\[\]]/g, "\\$&");
        var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
            results = regex.exec(url);
        if (!results) return null;
        if (!results[2]) return '';
        return decodeURIComponent(results[2].replace(/\+/g, " "));
    }

    me.getUrlParamsList = function () {
        var url = window.location.href;
        var splittedUrl = url.split("?");
        if (splittedUrl.length > 0) {
            return splittedUrl[1];
        } else {
            return null;
        }
    }

    me.getGridFiltersList = function (grid) {
        var gridFilters = grid.getStore().getFilters(false);
        var filterItems = gridFilters.items;
        var filtersArray = [];
        Ext.Array.each(filterItems, function (item) {
            filter = {
                'operator': item.getOperator(),
                'property': item.getProperty(),
                'value': item.getValue()
            }
            Ext.Array.push(filtersArray, filter);
        });
        return JSON.stringify(filtersArray);
    }

    me.dimensionModelingGridTarget = null;
    me.analysisGridDialog = null;
    me.createPTGridDialog = function (data) {
        me.dimensionModelingGridTarget = $('<div id="dimension_modeling_grid_target"></div>')
        var div = $('<div style="margin-top: 20px;"></div>');
        div.append(me.dimensionModelingGridTarget);
        me.analysisGridDialog = new BootstrapDialog({
            size: BootstrapDialog.SIZE_WIDE,
            message: div,
            draggable: true,
            buttons: [
                {
                    label: 'Close',
                    cssClass: 'btn-primary',
                    action: function (dialogRef) {
                        dialogRef.close();
                    }
                }
            ]
        });
        me.analysisGridDialog.realize();
        me.analysisGridDialog.setTitle('Data Analysis (Dimension Modeling)');
        me.analysisGridDialog.setType(BootstrapDialog.TYPE_SUCCESS);
        me.analysisGridDialog.getModalHeader().css('height', '45');
        me.analysisGridDialog.open();
        me.createFlexMonsterPivotTable(data);
    }
    me.createFlexMonsterPivotTable = function (data) {
        me.dimensionModelingGridTarget.flexmonster({
            // container: container_id,
            componentFolder: "https://cdn.flexmonster.com/",
            toolbar: true,
            height: '100%',
            report: {
                dataSource: {
                    data: data
                },
            },
            // licenseKey: 'Z7HI-XG503S-5O4M4H-6F456Z-0A3E3Z-1X663C-5O4R35-4R'// for dch server
            licenseKey: 'Z7CJ-XF9J50-5J4J6X-2H136N-2L036W-1A0O01-6S5S6R-0W0T20-3C' // for localhost
        });
    }

    me.pivotTableWin = null;
    me.createPivotTableWindow = function (data) {
        var tablePanel = Ext.create('Ext.panel.Panel', {
            xtype: 'panel',
            headerCls: 'extPanel',
            id: 'fmPivotPanel',
            layout: 'fit',
            autoScroll: true,
            margin: '0 0 0 0',
        });
        me.pivotTableWin = new Ext.window.Window({
            closable: true,
            resizable: true,
            draggable: true,
            title: 'Pivot Table',
            width: 800,
            height: 500,
            minWidth: 400,
            minHeight: 250,
            plain: true,
            layout: 'fit',
            items: tablePanel
        });
        me.pivotTableWin.show();
        var panelDiv = Ext.getCmp('fmPivotPanel').body.dom;
        var flexmonster = new Flexmonster({
            container: panelDiv,
            componentFolder: "https://cdn.flexmonster.com/",
            toolbar: true,
            height: '100%',
            report: {
                dataSource: {
                    data: data
                }
            },

            licenseKey: 'Z7HI-XG503S-5O4M4H-6F456Z-0A3E3Z-1X663C-5O4R35-4R'// for dch server
            // licenseKey: 'Z7CJ-XF9J50-5J4J6X-2H136N-2L036W-1A0O01-6S5S6R-0W0T20-3C' // for localhost
        })
    }
    

    me.createPivotTableWindow = function (data, rows, columns, measures) {
        var tablePanel = Ext.create('Ext.panel.Panel', {
            xtype: 'panel',
            headerCls: 'extPanel',
            id: 'fmPivotPanel',
            layout: 'fit',
            autoScroll: true,
            margin: '0 0 0 0',
        });
        me.pivotTableWin = new Ext.window.Window({
            closable: true,
            resizable: true,
            draggable: true,
            title: 'Pivot Table',
            width: 800,
            height: 500,
            minWidth: 400,
            minHeight: 250,
            plain: true,
            layout: 'fit',
            items: tablePanel
        });
        me.pivotTableWin.show();
        var panelDiv = Ext.getCmp('fmPivotPanel').body.dom;
        var flexmonster = new Flexmonster({
            container: panelDiv,
            componentFolder: "https://cdn.flexmonster.com/",
            toolbar: true,
            height: '100%',
            report: {
                dataSource: {
                    data: data
                },
                "slice": {
                    "rows": rows,
                    "columns": columns,
                    "measures": measures
                },
            },

            licenseKey: 'Z7HI-XG503S-5O4M4H-6F456Z-0A3E3Z-1X663C-5O4R35-4R'// for dch server
            // licenseKey: 'Z7CJ-XF9J50-5J4J6X-2H136N-2L036W-1A0O01-6S5S6R-0W0T20-3C' // for localhost
        })
    }

}