/**
 * Created by idrees on 1/11/2018.
 */
// var appData = mail_data;
// alert(appData);

Ext.Loader.setConfig({enabled: true});
// Ext.Loader.setPath('Ext.ux', '/static/Extjs-6.2.0/packages/ux/classic/src');

Ext.require([
    'Ext.Viewport',
    'Ext.grid.Panel',
    'Ext.panel.Panel',
    'Ext.container.Container',
]);

Ext.application({
    name:'IIMS',
    launch:function () {
        var me = this;
        var renderDiv = Ext.get('irrigationDashboard');
        var heightWin = window.innerHeight;
        var panel = Ext.create('Ext.panel.Panel', {
            height: heightWin - 105,
            minHeight: 400,
            minWidth: 350,
            autoScroll: true,
            border: false,
            bodyStyle: {
                backgroundColor: 'transparent'
            },
            layout: 'border',
            items: [
                {
                    autoHeight: true,
                    bodyStyle: {
                        backgroundColor: 'transparent'
                    },
                    border: false,
                    region: 'center',
                    layout: {
                        type: 'hbox',
                        align: 'stretch'
                    },
                    items: [
                        {
                            layout: 'fit',
                            padding:'0 0 0 0',
                            flex:1,
                            items:[
                                {
                                    region:'center',
                                    height:'100%',
                                    layout:'fit',
                                    items:[
                                        {
                                            xtype: 'panel',
                                            titleAlign:'center',
                                            border:false,
                                            headerCls: 'extPanel',
                                            id: 'pnlIrrigationData',
                                            layout: 'fit',
                                        }
                                    ]

                                }
                            ]
                        }

                    ]
                }
            ],
            renderTo: renderDiv,
            listeners: {
                resize: function (pnl, width, height, oldWidth, oldHeight, eOpts) {

                }
            }
        });

        var appFunctions = new AppCommonFunction();
        appFunctions.getParamsDataPanel();
        // appFunctions.createDataPanel();

        Ext.EventManager.onWindowResize(function () {
            var widthWin = window.innerWidth - 15;
            var heightWin = window.innerHeight;
            panel.setHeight(heightWin - 105);
            panel.setWidth(widthWin - 20);
        });
    }
});

var AppCommonFunction = function () {
    var me = this
    me.globalFunctions = null;
    me.gridColumns = null;
    
    me.getColumnsList = function (dataType, whereClause) {
        me.gridColumns = new ArzGridColumns();
        var level = whereClause.split('=')[0].trim();
        if(dataType == 'commanded_area'){
            return me.gridColumns.getCommandedAreaColumnsList(level)
        }if(dataType == 'district'){
            return me.gridColumns.getCommandedAreaDistrictsColumnsList(level)
        }if(dataType == 'canal'){
            return me.gridColumns.getCanalsColumnsList()
        }if(dataType == 'canal_l_section'){
            return me.gridColumns.getLSectionColumnsList()
        }if(dataType == 'canal_gauges'){
            return me.gridColumns.getGaugesColumnsList()
        }if(dataType == 'canal_gates'){
            return me.gridColumns.getGatesColumnsList()
        }if(dataType == 'canal_row'){
            return me.gridColumns.getROWColumnsList()
        }if(dataType == 'canal_structure'){
            return me.gridColumns.getStructureColumnsList()
        }if(dataType == 'dams'){
            return me.gridColumns.getHeadWorkColumnsList()
        }if(dataType == 'discharge'){
            return me.gridColumns.getHeadWorkDischargeColumnsList()
        }if(dataType == 'ground_water'){
            return me.gridColumns.getGroundWaterColumnsList()
        }
    }

    me.getParamsDataPanel = function () {
        me.globalFunctions = new ArzGlobalFunctionsModel();

        var dataType = me.globalFunctions.getParameterByName('data_type');
        var whereClause = me.globalFunctions.getParameterByName('where_clause');
        var params = me.globalFunctions.getUrlParamsList();
        var columnsList = me.getColumnsList(dataType, whereClause);

        var box = Ext.MessageBox.wait('Please wait...', 'Loading Data');
        var url = 'mailsmsdata?' + params;
        Ext.Ajax.timeout = 900000;
        Ext.Ajax.request({
            url: url,
            method: "GET",
            success: function (response) {
                box.hide();
                var respText = response.responseText;
                var respnseText = eval('(' + JXG.decompress(respText) + ')');
                if (respnseText != "false") {
                    var data = respnseText;
                    me.data = data;
                    me.createDataPanel(data,dataType, columnsList);
                }
            },
            failure: function (res) {
                box.hide();
            }
        });


    }

    me.createDataPanel = function (data, dataType, columnsList) {

        var store = Ext.create('Ext.data.Store', {
            id:'appDataStore',
            fields: me.getFieldsList(data[0]),
            data:data
        });

        var gridPanel = Ext.create('Ext.grid.Panel', {
            id:'appDataPanel',
            store: store,
            titleAlign:'center',
            title: me.getTableTitle(dataType) + " Data Table",
            stripeRows: true,
            columnLines: true,
            plugins:'gridfilters',
            autoScroll: true,
            bbar:[
                {
                    tooltip: 'Show pivot table',
                    text: 'PT',
                    cls:'btnPT',
                    handler: function () {
                        var ptData = gridPanel.getStore().data;
                        var gridData = me.globalFunctions.getDataFromGridItems(ptData);
                        me.globalFunctions.createPivotTableWindow(gridData);
                    }
                },'-',
                {
                    tooltip:   'Export to Excel',
                    icon: imgPath + 'EXCLE.png',
                    handler: function () {
                        var data = gridPanel.getStore().data;
                        var exportData = me.globalFunctions.getDataFromGridItems(data);
                        alasql("SELECT * INTO XLSX('data_table.xlsx',{headers:true}) FROM ? ",[exportData]);
                    }
                }
            ],
            columns: columnsList,
        });
        var dataPanel = Ext.getCmp("pnlIrrigationData");
        dataPanel.removeAll();
        dataPanel.add(gridPanel);
    }

    me.getTableTitle = function (name) {
        if(name == 'canal'){
            return '';
        }if(name == 'canal_l_section'){
            return 'L Section';
        }if(name == 'canal_gates'){
            return 'Gates';
        }if(name == 'canal_guages'){
            return 'Guages';
        }if(name == 'canal_row'){
            return 'Right of way';
        }if(name == 'canal_structure'){
            return 'Structure';
        }if(name == 'commanded_area'){
            return 'Commanded Area';
        }if(name == 'district'){
            return 'District';
        }if(name == 'dams'){
            return 'Dams and Barages';
        }if(name == 'ground_water'){
            return 'Ground Water';
        }if(name == 'canal'){
            return '';
        }else {
            return '';
        }
    }

    me.getColumnHeaderTitle = function (name) {
        var fullName = "";
        if(name == "name"){
            fullName = "Name";
            return fullName;
        }else if(name == "cca_ma"){
            fullName = "CCA (MA)";
            return fullName;
        }else if(name == "gca_ma"){
            fullName = "GCA (MA)";
            return fullName;
        }else if(name == "cca_geom_ma"){
            fullName = "CCA Geom";
            return fullName;
        }else if(name == "gca_geom_ma"){
            fullName = "GCA Geom";
            return fullName;
        }else if(name == "length"){
            fullName = "Canals Length (KM)";
            return fullName;
        }else if(name == "outlets"){
            fullName = "Outlets";
            return fullName;
        }else if(name == "acz_name"){
            fullName = "Agri Zone";
            return fullName;
        }else if(name == "cca_name"){
            fullName = "CCA";
            return fullName;
        }else if(name == "doab"){
            fullName = "Doab";
            return fullName;
        }else if(name == "basin"){
            fullName = "Basin";
            return fullName;
        }else if(name == "area_ha"){
            fullName = "Area (Hec)";
            return fullName;
        }else if(name == "cca_dam"){
            fullName = "CCA Dam";
            return fullName;
        }else if(name == "zone_name"){
            fullName = "Zone Name";
            return fullName;
        }else if(name == "circle_name"){
            fullName = "Circle Name";
            return fullName;
        }else if(name == "division_name"){
            fullName = "Division Name";
            return fullName;
        }else if(name == "area_acre"){
            fullName = "Area (Acre)";
            return fullName;
        }else if(name == "area_acre"){
            fullName = "Area (Acre)";
            return fullName;
        }else if(name == "district_name"){
            fullName = "District";
            return fullName;
        }else if(name == "zone"){
            fullName = "Zone";
            return fullName;
        }else if(name == "area_zone"){
            fullName = "Zone Total Area";
            return fullName;
        }else if(name == "zone_area"){
            fullName = "Zone Area";
            return fullName;
        }else if(name == "zone_area_percentage"){
            fullName = "Zone Area %age";
            return fullName;
        }else if(name == "circle"){
            fullName = "Circle";
            return fullName;
        }else if(name == "area_circle"){
            fullName = "Circle Total Area";
            return fullName;
        }else if(name == "circle_area"){
            fullName = "Circle Area";
            return fullName;
        }else if(name == "circle_area_percentage"){
            fullName = "Circle Area %age";
            return fullName;
        }else if(name == "division"){
            fullName = "Division";
            return fullName;
        }else if(name == "area_division"){
            fullName = "Division Total Area";
            return fullName;
        }else if(name == "division_area"){
            fullName = "Division Area";
            return fullName;
        }else if(name == "division_area_percentage"){
            fullName = "Division Area %age";
            return fullName;
        }else if(name == "punjab_district_area"){
            fullName = "District Area";
            return fullName;
        }else {
            return name
        }
    }

    // me.getColumnsList = function (data) {
    //     var columns = [];
    //     var stringType = "string";
    //     var numberType = 'number';
    //     for (var key in data) {
    //         if (key === "extent" || key === "geojson" || key === "id"  ||  key === "canal_type") {
    //         }
    //         else {
    //             if(isNaN(parseFloat(data[key]))){
    //                 columns.push({
    //                     dataIndex: key,
    //                     text: me.getColumnHeaderTitle(key),
    //                     width:100,
    //                     exportStyle: {
    //                         alignment: {
    //                             horizontal: 'Right'
    //                         },
    //                         font: {
    //                             bold: true
    //                         },
    //                         format: 'Text'
    //                     },
    //                     filter: {
    //                         type:stringType,
    //                         itemDefaults: {
    //                             emptyText: 'Search for...'
    //                         }
    //                     }
    //                 })
    //             }else {
    //                 columns.push({
    //                     dataIndex: key,
    //                     text: me.getColumnHeaderTitle(key),
    //                     width:80,
    //                     filter: numberType,
    //                     exportStyle: {
    //                         alignment: {
    //                             horizontal: 'Right'
    //                         },
    //                         font: {
    //                             bold: true
    //                         }
    //                     }
    //                 })
    //             }
    //
    //         }
    //     }
    //     return columns;
    // }

    // me.getComboStore = function (storeId) {
    //     var fieldStore = Ext.create('Ext.data.Store', {
    //         fields: [
    //             {name: 'id', type: 'string'},
    //             {name: 'name', type: 'string'}
    //         ],
    //         id: storeId,
    //         data:[]
    //     });
    //     return fieldStore;
    // }

    me.getFieldsList = function (data) {
        var arrField = new Array();
        for (var key in data) {
            var obj = {};
            if(key === "extent" || key === "geojson" ||  key === "canal_type"){
            }else {
                obj.id = key;
                obj.name = key;
                arrField.push(obj);
            }
        }
        return arrField;
    }
}

