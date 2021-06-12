/**
 * Created by Mariam on 1/29/2019.
 */
/**
 * Created by Mariam on 10/18/2018.
 */
var MHVRAModel = function (mapInfo) {
    var me = this;
    me.olMapModel = null;
    me.gridEL = $("#grid");
    me.initialize = function () {
        me.olMapModel = new OLMapModel(mapInfo.extent, "map", "layerSwitcher", null, mapInfo.csrfToken, null);
        me.olMapModel.initialize();
        me.createMapToolbar(mapInfo);
        // if(){}
        // me.create_jqx_grid();
        // var data = [{
        //     "category": ".",
        //     "design_criteria": "",
        //     "value_mhvra": "",
        //     "value_unit": "",
        //     "vulnerability": "",
        //     "damage": "",
        //     "order_address": "",
        //     "risk": "",
        //     "qualitative_measure": "",
        //     "probability": "",
        //     "cost_impact": ""
        //
        // }];
        // me.updateGridDataWithLocalData(data);
    };
    me.createMapToolbar = function (mapInfo) {
        me.toolbarModel = new JQXToolbarModel("10%", mapInfo, me);
        var navbar = me.toolbarModel.navbar;
        var navbarSeq = [navbar.addLayer, navbar.fullExtent, navbar.pan, navbar.zoom2Rect, navbar.zoomIn, navbar.zoomOut, navbar.zoom2Prev, navbar.zoom2Next,
            navbar.spacebar, navbar.zoom2Selection, navbar.clearSelection, navbar.identifier, navbar.spacebar, navbar.project_location
        ];
        me.siteSelModel = new SiteSelectionModel(mapInfo, me);
        me.siteSelModel.init();
        me.toolbarModel.initialize(me, navbarSeq);
    };
    me.showMHVRAStatsOfMarkedLocation = function (long, lat) {
        var url = '/dia/get_hazard_flood_data/?lat=' + lat + '&long=' + long;
        var params = {
            url: url,
            type: "GET",
            // data: data,
            // dataType: "json",
            processData: false,
            contentType: false,
            async: true
            // headers: {'X-CSRFToken': token},
        };
        // var data = callSJAX(params);
        callAJAX(params, function (response) {
            me.updateGridDataWithLocalData(response)

        })
    }
    me.create_jqx_grid = function () {
        var source = {
            datatype: "json",
            datafields: [
                {name: 'category', type: 'string'},
                {name: 'design_criteria', type: 'string'},
                {name: 'value_mhvra', type: 'number'},
                {name: 'value_unit', type: 'string'},
                {name: 'vulnerability', type: 'number'},
                {name: 'damage', type: 'number'},
                {name: 'order_address', type: 'string'},
                {name: 'risk', type: 'number'},
                {name: 'qualitative_measure', type: 'number'},
                {name: 'probability', type: 'number'},
                {name: 'cost_impact ', type: 'number'}

            ]

        };
        var dataAdapter = new $.jqx.dataAdapter(source, {
            loadComplete: function () {
            }
        });
        // create grid.
        me.gridEL.jqxGrid(
            {
                width: '100%',
                source: dataAdapter,
                // pageable: true,
                // autorowheight: true,
                altrows: true,
                groupable: true,
                groups: ['category'],
                columnsresize: true,
                columns: [
                    {
                        text: 'Category',
                        columngroup: 'NATURAL',
                        cellsalign: 'center',
                        align: 'center',
                        datafield: 'category',
                        width: 100
                    },
                    {
                        text: 'Design Criteria (dc)',
                        columngroup: 'NATURAL',
                        datafield: 'design_criteria',
                        cellsalign: 'center',
                        align: 'center',
                        width: 140
                    },
                    {
                        text: 'Value MHVRA',
                        columngroup: 'NATURAL',
                        cellsalign: 'center',
                        align: 'center',
                        cellsformat: 'd',
                        datafield: 'value_mhvra',
                        width: 100
                    },
                    {
                        text: 'Value Unit',
                        columngroup: 'NATURAL',
                        datafield: 'value_unit',
                        cellsformat: 'd',
                        cellsalign: 'center',
                        align: 'center',
                        width: 100
                    },
                    {
                        text: 'Damage (D) Km2',
                        columngroup: 'RISK ASSESSMENT',
                        cellsalign: 'center',
                        align: 'center',
                        datafield: 'damage',
                        width: 170
                    },
                    {
                        text: 'Vulnerability',
                        columngroup: 'RISK ASSESSMENT',
                        datafield: 'vulnerability',
                        cellsformat: 'd',
                        cellsalign: 'center',
                        align: 'center',
                        width: 100
                    },
                    {
                        text: 'Risk R (class)',
                        columngroup: 'RISK ASSESSMENT',
                        cellsalign: 'center',
                        align: 'center',
                        datafield: 'risk',
                        width: 120
                    },
                    {
                        text: 'Qualitative Measure',
                        columngroup: 'RISK ASSESSMENT',
                        datafield: 'qualitative_measure',
                        cellsformat: 'd',
                        cellsalign: 'center',
                        align: 'center',
                        width: 140
                    },
                    {
                        text: 'Probability (p)',
                        columngroup: 'RISK ASSESSMENT',
                        datafield: 'probability',
                        cellsformat: 'd',
                        align: 'center',
                        cellsalign: 'center',
                        width: 130
                    },

                ],
                columngroups: [
                    {text: 'RISK ASSESSMENT', align: 'center', name: 'RISK ASSESSMENT'},
                    {text: 'NATURAL HAZARD IDENTIFICATION', align: 'center', name: 'NATURAL'}


                ]
            });
    }
    me.updateGridDataWithLocalData = function (data) {
        if ((data[0].category) === '') {
            alert("Please select location again");
        }
        var adapter = me.gridEL.jqxGrid('source');
        var source =
            {
                datatype: "json",
                datafields: adapter._source.datafields,
                localdata: data
            };
        var dataAdapter = new $.jqx.dataAdapter(source);
        dataAdapter.dataBind();
        me.gridEL.jqxGrid({source: dataAdapter});
        me.gridEL.jqxGrid('updatebounddata');
    };

};
var updateDIAGridDataWithLocalData = function (data) {
    console.log("in grid data function", data)
    // if ((data[0].category) === '') {
    //     alert("Please select location again");
    // }
    var adapter = $("#project_list_grid").jqxGrid('source');
    var source =
        {
            datatype: "json",
            datafields: adapter._source.datafields,
            localdata: data
        };
    var dataAdapter = new $.jqx.dataAdapter(source);
    dataAdapter.dataBind();
    $("#project_list_grid").jqxGrid({source: dataAdapter});
    $("#project_list_grid").jqxGrid('updatebounddata');
};
function get_dia_data_list() {
    var me = this;
    var url = '/dia/get_dia_data/';
    var params = {
        url: url,
        type: "GET",
        // data: data,
        // dataType: "json",
        processData: false,
        contentType: false,
        async: true
        // headers: {'X-CSRFToken': token},
    };
    // var data = callSJAX(params);
    callAJAX(params, function (response) {
        console.log(response)
        me.updateDIAGridDataWithLocalData(response)

    })
}

// var ProjectListGrid = function (user) {
//     var me = this;
//     me.projectGridEl = $("#project_list_grid");
//     // me.get_dia_data_list();
//     var source =
//         {
//             datafields: [
//                 {name: 'project_id', type: 'string'},
//                 {name: 'project_name', type: 'string'},
//                 {name: 'created_by', type: 'string'},
//                 {name: 'date', type: 'date'},
//             ],
//             datatype: "json"
//         };
//     var dataAdapter = new $.jqx.dataAdapter(source);
//      me.projectGridEl.jqxGrid(
//         {
//             width: '100%',
//             source: dataAdapter,
//             sortable: true,
//             pageable: true,
//             showtoolbar: true,
//             columnsresize: true,
//             columnsreorder: true,
//             showfilterrow: true,
//             filterable: true,
//             selectionmode: 'singlerow',
//             rendertoolbar: function (statusbar) {
//                 var container = $("<div style='overflow: hidden; position: relative; margin: 5px;'></div>");
//                 var addButton = $("<div style='float: left; margin-left: 5px;'><span style='position: relative; margin-top: 2px; width: 40px;' class='glyphicon glyphicon-plus'><span style='margin-left: 4px; position: relative; top: -3px;'>Add</span></span></div>");
//                 var editButton = $("<div style='float: left; margin-left: 5px;'><span style='position: relative; margin-top: 2px; width: 40px;' class='glyphicon glyphicon-pencil'><span style='margin-left: 4px; position: relative; top: -3px;'>Edit</span></span></div>");
//                 var viewButton = $("<div style='float: left; margin-left: 5px;'><span style='position: relative; margin-top: 2px; width: 40px;' class='glyphicon glyphicon-eye-open'><span style='margin-left: 4px; position: relative; top: -3px;'>View</span></span></div>");
//                 if (user != null) {
//                     container.append(addButton);
//                     container.append(editButton);
//                     container.append(viewButton);
//                 }
//                 else {
//                     container.append(viewButton);
//                     console.log("user is null");
//                 }
//                 statusbar.append(container);
//                 addButton.jqxButton({width: 60, height: 20});
//                 editButton.jqxButton({width: 65, height: 20});
//                 viewButton.jqxButton({width: 65, height: 20});
//                 addButton.click(function (event) {
//                     var url = 'http://pcupiupnd.info/projects/';
//                     window.location.href = url;
//                 });
//                 // delete selected row.
//                 editButton.click(function (event) {
//                     var selectedrowindex = me.projectGridEl.jqxGrid('getselectedrowindex');
//                     if (selectedrowindex !== -1) {
//                         var rowData = me.projectGridEl.jqxGrid('getrowdata', selectedrowindex);
//                         var url = '//view_dia_add_data/?project_id=' + rowData.project_id;
//                         window.location.href = url;
//                     } else {
//                         alert("Please select any row from below table");
//                     }
//                 });
//                 // view grid data.
//                 viewButton.click(function (event) {
//                     var selectedrowindex = me.projectGridEl.jqxGrid('getselectedrowindex');
//                     if (selectedrowindex !== -1) {
//                         var rowData = me.projectGridEl.jqxGrid('getrowdata', selectedrowindex);
//                         var url = '/dia/view_dia_add_data/?project_id=' + rowData.project_id;
//                         window.location.href = url;
//                     } else {
//                         alert("Please select any row from below table");
//                     }
//
//                 });
//
//             },
//             columns: [
//                 {
//                     text: 'Project Name',
//                     datafield: 'project_name',
//                     cellsrenderer: function (row, column, value) {
//                         var rowData = me.projectGridEl.jqxGrid('getrowdata', row);
//                         var url = '/dia/view_dia_add_data/?project_id=' + rowData.project_id;
//                         return '<a href="' + url + '">' + value + '</a>';
//                     }
//                 },
//
//                 {
//                     text: 'Created By',
//                     align: 'center',
//                     datafield: 'created_by',
//                     cellsalign: 'center',
//                 },
//                 {
//                     text: 'Date',
//                     align: 'center',
//                     datafield: 'date',
//                     filtertype: 'date',
//                     cellsalign: 'center',
//                     cellsformat: 'd'
//                 }
//             ]
//         });
//
//
// }



