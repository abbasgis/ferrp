/**
 * Created by Dr. Ather Ashraf on 2/25/2018.
 */

/********************************************
 *
 * @constructor
 * usage:  var gridVM = new GridVM();
 gridVM.initializeLayerGridParames(me.layerInfo.layerName,viewModel);
 */
var GridVM = function (gridInfo) {
    var me = this;
    me.gridModel = null;
    me.gridInfo = gridInfo
    me.initializeLayerGridParames = function (layerName, viewModel, width, gridDivId) {
        if (!width) width = 300;

        me.gridDivId = gridDivId
        var url = me.gridInfo.attribute_url + "?layer_name=" + layerName + "&width=" + width
        var params = {
            url: url,
            type: "GET",
            // data: data,
            dataType: "json",
            processData: false,
            contentType: false,
            async: false
            // headers: {'X-CSRFToken': token},
        }
        // var data = callSJAX(params);
        callAJAX(params, function (data) {
            // data = JSON.parse(data)
            if (me.gridModel) {
                // me.gridModel = new GridModel(viewModel, me.gridDivId);
                // }else{
                try {
                    me.gridModel.clearGrid();
                } catch (e) {
                    console.log(e);
                }
            }
            me.gridModel = new GridModel(viewModel, me.gridDivId);
            me.gridModel.createGrid(layerName, data.data_fields, data.columns, data.data);
        })

    }

    me.getGridModel = function () {
        return me.gridModel;
    }
}


var GridModel = function (viewModel, gridDivId) {
    var me = this;
    me.viewModel = viewModel;
    me.outputTarget = $("#" + gridDivId + "");
    me.gridTarget = $('<div style="width:100%;height:100%;position:absolute"></div>');
    me.grid = null;
    me.gridColumns = [];
    me.dataAdapter = null;
    me.theme = me.viewModel.theme;
    me.layerName = null;
    me.createDataAdapter = function (dataFields, data) {
        var source = {
            datatype: 'json',
            datafields: dataFields,
            localdata: data
        }


        me.dataAdapter = new $.jqx.dataAdapter(source, {autoBind: true});
    }
    me.createGrid = function (layerName, fields, columns, data) {
        try {
            me.layerName = layerName
            me.gridColumns = columns;
            me.createDataAdapter(fields, data)

            me.outputTarget.append(me.gridTarget)
            me.gridTarget.jqxGrid({
                theme: me.theme,
                showfilterrow: true,
                filterable: true,
                width: '99%',
                height: '100%',
                source: me.dataAdapter,
                sortable: true,
                // altrows: true,
                enabletooltips: true,
                selectionmode: 'singlerow',
                columns: columns, //me.gridColumns,

                // scrollmode: 'logical',
                // filtermode: 'excel',
                columnsresize: true,
                autoshowfiltericon: true,

            });


        }
        catch (e) {
            console.log(e)
            // me.clearGrid();
        }
    }
    me.toggleGroupable = function () {
        var groupable = me.gridTarget.jqxGrid('groupable');
        me.gridTarget.jqxGrid({groupable: !groupable})
    }
    me.toggleShowFilterRow = function () {
        var showfilterrow = me.gridTarget.jqxGrid('showfilterrow');
        me.gridTarget.jqxGrid({showfilterrow: !showfilterrow});
    }
    me.clearGrid = function () {
        try {
            // me.gridTarget.jqxGrid({_cachedcolumns: null});
            me.gridTarget.jqxGrid('destroy');
            // me.gridTarget.empty();
            // me.grid = null;
        } catch (e) {
            console.log(e)
        }
    }

    // me.queryGrid = function () {
    //     // var fm = new FilterModel(me);
    //     // fm.initialize();
    //     var qm = new QueryModel(me.layerName);
    //     qm.initialize();
    // }

    me.selectGeometryOnMap = function (oid) {
        var url = "/web_services/wfs/get_feature/geom/"
        url = url + "?layer_name=" + me.layerName + "&oid=" + oid
        var params = {
            url: url,
            type: "GET",
            dataType: "json",
            processData: false,
            contentType: false,
            async: true
        }
        callAJAX(params, function (data) {
            me.viewModel.olMapModel.clearSelection()
            for (var i = 0; i < data.length; i++) {
                var geom = data[i];
                me.viewModel.olMapModel.showSelectedFeatureGeometry(geom[0], false)
            }
        });
    }
    me.gridTarget.on('rowselect', function (event) {
        // event arguments.
        var args = event.args;
        // row's bound index.
        var rowBoundIndex = args.rowindex;
        // row's data. The row's data object or null(when all rows are being selected or unselected with a single action). If you have a datafield called "firstName", to access the row's firstName, use var firstName = rowData.firstName;
        var rowData = args.row;
        var oid = rowData.oid;
        me.selectGeometryOnMap(oid)
    });

    me.gridTarget.on("filter", function (event) {
        var filterinfo = me.gridTarget.jqxGrid('getfilterinformation');
        // console.log(filterinfo)
        if (filterinfo.length > 0) {
            filterRows = me.gridTarget.jqxGrid('getrows');
            var oids = ""
            for (var i = 0; i < filterRows.length; i++) {
                // oids.push(filterRows[i].oid);
                oids += filterRows[i].oid + ","
            }
            oids = oids.substring(0, oids.length - 1)
            me.selectGeometryOnMap(oids)
        } else {
            me.viewModel.olMapModel.clearSelection()
        }
    });
}

var FilterModel = function (gridModel) {
    var me = this;
    me.grilModel = gridModel;
    me.handleCheckChange = true;
    me.colChooser = $('<div id="columnchooser"></div>');
    me.filterBox = $('<div style="margin-top: 10px;" id="filterbox"></div>');
    me.createColChooser = function (cols) {
        var source = []
        for (var i = 0; i < cols.length; i++) {
            if (cols[i].text == "oid") continue;
            obj = {}
            obj['label'] = cols[i].text;
            obj['value'] = cols[i].datafield;
            source.push(obj);
        }
        me.colChooser.jqxDropDownList({
            autoDropDownHeight: true, selectedIndex: 0, width: '100%', height: 25,
            source: source

        });
    }
    me.createFilterBox = function (initCol) {
        me.filterBox.jqxListBox({checkboxes: true, width: '100%', height: 250});
        me.updateFilterBox(initCol.datafield)
    }
    me.createFilterDialog = function () {
        var filterDiv = $('<div style="margin-top: 20px;"></div>');
        filterDiv.append(me.colChooser);
        filterDiv.append(me.filterBox);
        me.styleLayerDialog = new BootstrapDialog({
            size: BootstrapDialog.SIZE_SMALL,
            message: filterDiv,
            draggable: true,
            buttons: [
                {
                    id: "applyfilter",
                    label: "Apply Filter",
                    cssClass: 'btn-primary',
                    action: function (dialogRef) {

                        var dataField = me.colChooser.jqxDropDownList('getSelectedItem').value;
                        me.applyFilter(dataField);
                    }
                },
                {
                    id: "clearfilter",
                    label: "Clear Filter",
                    cssClass: 'btn-primary',
                    action: function (dialogRef) {
                        me.clearFilter();
                    }
                },
                {
                    label: 'Close',
                    cssClass: 'btn-primary',
                    action: function (dialogRef) {
                        dialogRef.close();
                    }
                }
            ]
        });
        me.styleLayerDialog.realize();
        me.styleLayerDialog.setTitle('Apply Filter');
        me.styleLayerDialog.setType(BootstrapDialog.TYPE_SUCCESS);
        me.styleLayerDialog.getModalHeader().css('height', '45');
        me.styleLayerDialog.open();
    }
    me.initialize = function () {

        me.createColChooser(me.grilModel.gridColumns)
        me.createFilterBox(me.grilModel.gridColumns[0]);
        me.createFilterDialog();
    }
    me.updateFilterBox = function (datafield) {
        var filterBoxAdapter = new $.jqx.dataAdapter(me.grilModel.source, {
            uniqueDataFields: [datafield],
            autoBind: true
        });
        var uniqueRecords = filterBoxAdapter.records;
        uniqueRecords.splice(0, 0, '(Select All)');
        me.filterBox.jqxListBox({source: uniqueRecords, displayMember: datafield});
        me.filterBox.jqxListBox('checkAll');
    }

    me.filtergroup = new $.jqx.filter();
    me.clearFilter = function () {
        me.grilModel.gridTarget.jqxGrid('clearfilters');
    }
    me.applyFilter = function (datafield) {
        me.filtergroup = new $.jqx.filter();
        var filtertype = 'stringfilter';
        if (datafield == 'date') filtertype = 'datefilter';
        if (datafield == 'price' || datafield == 'quantity') filtertype = 'numericfilter';
        var checkedItems = me.filterBox.jqxListBox('getCheckedItems');
        if (checkedItems.length == 0) {
            var filter_or_operator = 1;
            var filtervalue = "Empty";
            var filtercondition = 'equal';
            var filter = me.filtergroup.createfilter(filtertype, filtervalue, filtercondition);
            me.filtergroup.addfilter(filter_or_operator, filter);
        }
        else {
            for (var i = 0; i < checkedItems.length; i++) {
                var filter_or_operator = 1;
                var filtervalue = checkedItems[i].label;
                var filtercondition = 'equal';
                var filter = me.filtergroup.createfilter(filtertype, filtervalue, filtercondition);
                me.filtergroup.addfilter(filter_or_operator, filter);
            }
        }
        me.grilModel.gridTarget.jqxGrid('clearfilters');
        // add the filters.
        me.grilModel.gridTarget.jqxGrid('addfilter', datafield, me.filtergroup);
        // apply the filters.
        me.grilModel.gridTarget.jqxGrid('applyfilters');
    }

    me.filterBox.on('checkChange', function (event) {
        if (!me.handleCheckChange)
            return;
        if (event.args.label != '(Select All)') {
            me.handleCheckChange = false;
            me.filterBox.jqxListBox('checkIndex', 0);
            var checkedItems = me.filterBox.jqxListBox('getCheckedItems');
            var items = me.filterBox.jqxListBox('getItems');
            if (checkedItems.length == 1) {
                me.filterBox.jqxListBox('uncheckIndex', 0);
            }
            else if (items.length != checkedItems.length) {
                me.filterBox.jqxListBox('indeterminateIndex', 0);
            }
            me.handleCheckChange = true;
        }
        else {
            me.handleCheckChange = false;
            if (event.args.checked) {
                me.filterBox.jqxListBox('checkAll');
            }
            else {
                me.filterBox.jqxListBox('uncheckAll');
            }
            me.handleCheckChange = true;
        }
    });
    // handle columns selection.
    me.colChooser.on('select', function (event) {
        me.updateFilterBox(event.args.item.value);
    });

}


/************* usage
 *
 * @param viewModel
 * @param gridDivId
 * @param isCreateNewLayer
 * @constructor
 *
 * For simplae Query
 *  layerInfo={}
 * layerInfo.gridWidth = 300;
 * layerInfo.layerName = "test";
 * isCreateNewLayer = false;
 * var qm = new QueryModel(me.viewModel, 'output');
 * qm.createQueryDialog(layerInfo,isCreateNewLayer);
 *
 *  For spatial Query
 * var qm = new QueryModel(me.viewModel, 'output');
 * qm.createSpatialQueryDialog();
 *
 */

var QueryModel = function (viewModel, gridDivId, isCreateNewLayer) {
    var me = this;
    me.viewModel = viewModel;
    me.gridDivId = gridDivId;
    me.olMapModel = viewModel.olMapModel;
    me.spatial_ops = {
        "intersects": "st_intersects", "contains": "st_contains",
        "within": "st_within", "overlap": "st_overlap", "equal": "st_equal"
    };
    me.geomWKT = "";
    if (!isCreateNewLayer) {
        me.isCreateNewLayer = false;
    } else {
        me.isCreateNewLayer = isCreateNewLayer;
    }
    me.createFilters = function () {
        var url = "/web_services/wfs/query_layer/get_filter/" + "?layer_name=" + me.layerName
        // alert("url:"+url);
        var params = {
            url: url,
            type: "GET",
            // data: data,
            dataType: "json",
            processData: false,
            contentType: false,
            async: false
            // headers: {'X-CSRFToken': token},
        }
        var data = callSJAX(params);
        data = JSON.parse(data)
        // alert(data);
        me.filters = data.filters


    }
    me.createQueryBuilder = function () {
        me.createFilters();
        me.builderTarget.queryBuilder({
            plugins: [
                'bt-tooltip-errors',
                'not-group'
            ],

            filters: me.filters
        });
    }
    me.createQueryDialog = function (layerInfo) {

        me.layerInfo = layerInfo;
        me.token = me.olMapModel.csrfToken;
        me.layerName = layerInfo.layerName;
        me.layerTitle = layerInfo.title
        me.builderTarget = $('<div id="builder-import_export"></div>')
        var filterDiv = $('<div style="margin-top: 20px;"></div>');
        filterDiv.append(me.builderTarget);
        me.styleLayerDialog = new BootstrapDialog({
            size: BootstrapDialog.SIZE_WIDE,
            message: filterDiv,
            draggable: true,
            buttons: [
                {
                    id: "clearfilter",
                    label: "Query",
                    cssClass: 'btn-primary',
                    action: function (dialogRef) {
                        me.QueryLayer();
                        dialogRef.close()
                    }
                },
                {
                    id: "clearfilter",
                    label: "Clear Filter",
                    cssClass: 'btn-primary',
                    action: function (dialogRef) {
                        me.clearFilter();
                    }
                },
                {
                    label: 'Close',
                    cssClass: 'btn-primary',
                    action: function (dialogRef) {
                        dialogRef.close();
                    }
                }
            ]
        });
        me.styleLayerDialog.realize();
        me.styleLayerDialog.setTitle('Apply Filter');
        me.styleLayerDialog.setType(BootstrapDialog.TYPE_SUCCESS);
        me.styleLayerDialog.getModalHeader().css('height', '45');
        me.styleLayerDialog.open();
        me.createQueryBuilder();
    }
    me.clearFilter = function () {
        me.builderTarget.queryBuilder('reset');
    }
    me.QueryLayer = function () {
        // var result = me.builderTarget.queryBuilder('getSQL');
        var result = $('#builder-import_export').queryBuilder('getSQL', 'question_mark');
        // var where_caluse = result.sql
        // var literals =  result.params     //JSON.stringify(result.params, null, 2)

        if (me.isCreateNewLayer) {
            BootstrapDialog.show({
                draggable: true,
                message: 'Enter Layer Name: <input type="text" value ="' + me.layerTitle + '"class="form-control">',
                onhide: function (dialogRef) {
                    var reqlayerName = dialogRef.getModalBody().find('input').val();
                    me.sendQueryRequest(result, reqlayerName);
                },
                buttons: [{
                    label: 'Close',
                    action: function (dialogRef) {
                        dialogRef.close();
                    }
                }]
            });
        } else {
            me.sendQueryRequest(result, null, me.layerInfo.gridWidth)

        }

    }
    me.sendQueryRequest = function (result, newLayerName, gridWidth) {
        if (!newLayerName) newLayerName = me.layerName;
        if (!gridWidth) gridWidth = 400;
        var url = "/web_services/wfs/query_layer/query/"  //+ "?layer_name=" + me.layerName

        var formData = new FormData();

        formData.append("layer_name", me.layerName);
        formData.append("new_layer_name", newLayerName)
        formData.append("is_create_new_layer", me.isCreateNewLayer);
        formData.append("grid_width", gridWidth);
        formData.append("where_clause", result.sql)
        formData.append("literals", result.params)
        var params = {
            url: url,
            type: "POST",
            data: formData,
            dataType: "json",
            processData: false,
            contentType: false,
            async: true,
            headers: {'X-CSRFToken': me.token},
        }
        var data = callAJAX(params, function (data) {
            me.showResultantGrid(data)
        });
    }
    me.showResultantGrid = function (data) {
        if (data.status == "202") {
            if (me.isCreateNewLayer == true) {
                me.viewNewLayer(data.new_layer_name)
            } else {
                me.viewModel.showOutputPanel();
                var gridModel = new GridModel(me.viewModel, me.gridDivId);
                gridModel.createGrid(me.layerName, data.data_fields, data.data.columns, data.data.data);
            }
        } else {
            showAlertDialog("No result found...", dialogTypes.warning);
        }
    }

    me.viewNewLayer = function (layerName) {
        window.location.href = "/layers/viewlayer/?layer_name=" + layerName;
    }


    me.sendSpatialQueryRequest = function () {
        var spatialQueryInfo = {};
        spatialQueryInfo.gridWidth = me.viewModel.getOutputPanelSize().width
        // spatialQueryInfo.csrfToken = me.olMapModel.csrfToken;
        // layerInfo.gridWidth = me.viewModel.getOutputPanelSize().width
        spatialQueryInfo.layerName1 = $("#layerName1").find(":selected").val();
        spatialQueryInfo.layerName2 = $("#layerName2").find(":selected").val();
        spatialQueryInfo.spatialOp = $("#spatialOp").find(":selected").val();
        if(spatialQueryInfo.layerName2=="selectedFeatureLayer"){
            var geom = me.olMapModel.getSelectedFeatureGeometryCombined();
            me.geomWKT = me.olMapModel.convertGeom2WKT(geom);
        }
        // spatialQueryInfo.wkt = $("#wkt").val();
        me.layerName = spatialQueryInfo.layerName1;
        var formData = new FormData();
        formData.append("layerName1", spatialQueryInfo.layerName1);
        formData.append("layerName2", spatialQueryInfo.layerName2);
        formData.append("gridWidth", spatialQueryInfo.gridWidth);
        formData.append("spatialOp", spatialQueryInfo.spatialOp);
        formData.append("wkt", me.geomWKT);
        var url = "/web_services/wfs/query_layer/spatial_query/";
        var params = {
            url: url,
            type: "POST",
            data: formData,
            dataType: "json",
            processData: false,
            contentType: false,
            async: true,
            headers: {'X-CSRFToken': me.olMapModel.csrfToken},
        }
        callAJAX(params, function (data) {
            // alert(res);
            if (data.status == "202") {
                if (me.isCreateNewLayer == true) {
                    me.viewNewLayer(data.new_layer_name)
                } else {
                    me.showResultantGrid(data)
                }
            } else {
                showAlertDialog("No result found...", dialogTypes.warning);
            }
        })
    }
    me.createSpatialQueryDialog = function () {
        var modalbody = $('<div id="divChangeStyleBody"></div>');
        var layerSelect_1 = me.olMapModel.createLayerNameSelect("layerName1");

        layerSelect_1[0].classList.add("form-control");
        var layerSelect_2 = me.olMapModel.createLayerNameSelect("layerName2", true);
        layerSelect_2[0].classList.add("form-control");
        var select_ops = $('<select id="spatialOp" class="form-control layerNameCls" ></select>');
        // var hiddenWKT = $('<input id="wkt" type="hidden" class="form-control" value="">')
        // select_ops.append('<option value="-1">Select Spatial Operation</option>');
        for (var key in me.spatial_ops) {
            select_ops.append("<option value='" + me.spatial_ops[key] + "'>" + key + "</option>")
        }
        // select.selectpicker('refresh');
        modalbody.append("<span><b>Select 1st Layer:</b></span>");
        modalbody.append(layerSelect_1);
        // modalbody.append("<br></br>");
        modalbody.append("<span><b>Select Spatial Operators:</b></span>");
        modalbody.append(select_ops)
        // modalbody.append("<br></br>");
        modalbody.append("<span><b>Select 2nd Layer:</b></span>");
        modalbody.append(layerSelect_2);
        // modalbody.append(hiddenWKT);

        BootstrapDialog.show({
            title: "Spatial Query",
            type: BootstrapDialog.TYPE_SUCCESS,
            // size: BootstrapDialog.SIZE_S,MALL,
            message: modalbody,
            buttons: [{
                label: 'Draw',
                action: function (dialogItself) {
                    // dialogItself.getModal().hide()
                    dialogItself.close()
                    var draw = me.olMapModel.drawShape("Polygon", function (geometry) {
                        // alert(geomWKT);
                        me.geomWKT = me.olMapModel.convertGeom2WKT(geometry);
                        // alert(wkt);
                        me.olMapModel.zoomToRectangle();
                        $('#layerName2 option[value="drawFeatureLayer"]').prop('selected', true);
                        dialogItself.open();


                    })

                }
            }, {
                label: 'Query',
                action: function (dialogItself) {
                    // dialogItself.close()
                    me.sendSpatialQueryRequest();
                    dialogItself.close()
                }

            }, {
                label: 'Close',
                action: function (dialogItself) {
                    dialogItself.close()
                }
            }]
        });
    }


}

