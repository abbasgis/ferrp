/**
 * Created by Dr. Ather Ashraf on 8/26/2018.
 */
/************************************************
 *
 * @param olMapModel
 * @constructor
 * usage: var AddNavigationModel = new AddNavigationModel(olMapModel)
 AddNavigationModel.initialize();
 */
var AddNavigationModel = function (olMapModel, viewInfo) {
    var me = this;
    me.viewInfo = viewInfo;
    me.layerStyleModel = null;
    me.catalogPanelTarget = $('#Navigation');
    me.selectedTreeItem = "-1";
    me.dropDownTarget = $("<div id='NavigationDropDown'></div>");
    me.catalogPanelTarget.append(me.dropDownTarget);
    me.treeTarget = $("<div id='NavigationTree'></div>");
    me.catalogPanelTarget.append(me.treeTarget);
    me.olMapModel = olMapModel;
    me.adminLevelSources = [{label: 'Administration Boundary', value: "adb"}, {label: 'Board Of Revenue', value: "bor"},
        {label: 'Irrigation Boundary', value: "irb"}, {label: 'Local Government', value: "lg"},
        {label: 'Indus Basin Catchments', value: "basin"}];
    me.initialize = function () {
        // me.addLayerTyeCombobox();
        me.addToolbar();
        me.addAdminTree(me.adminLevelSources[0].value)
    };
    me.addToolbar = function () {
        me.dropDownTarget.jqxToolBar({
            theme: theme,
            width: '100%',
            height: 35,
            tools: 'button | dropdownlist',
            initTools: function (type, index, tool, menuToolIninitialization) {
                switch (index) {
                    case 0:
                        var button = $("<div>" + "<i class='fa fa-lg fa-search'></i>" + "</div>");
                        tool.append(button);
                        tool.on("click", function () {
                            // me.olMapModel.zoom2PreviousExtent();
                            if (me.selectedTreeItem != "-1") {
                                // me.addLayerToMap();
                                me.olMapModel.zoomToSelectedFeatures();
                            } else {
                                showAlertDialog("Please select layer from below tree..", dialogTypes.info);
                            }
                        });
                        break;
                    case 1:
                        tool.jqxDropDownList({
                            theme: theme,
                            width: '70%',
                            source: me.adminLevelSources,
                            selectedIndex: 0,
                            displayMember: "label",
                            valueMember: "value",
                        });
                        me.dropDownTarget = tool;
                        tool.on('select', function (event) {
                            var args = event.args;
                            if (args) {
                                var item = args.item;
                                var value = item.value;
                                // me.selecteLayerTypeVal = item.value
                                // alert(value);
                                me.addAdminTree(value);
                            }
                        });
                        break;
                }
            }
        });

    }
    me.destroyTree = function () {
        me.treeTarget.jqxTreeGrid('destroy');
        // me.treeTarget = $("<div id='CatTree'></div>");
        me.catalogPanelTarget.append(me.treeTarget);
    }
    me.addAdminTree = function (admin_code) {
        me.destroyTree();
        var params = {
            url: me.viewInfo.url_get_admin_tree + "?code=" + admin_code,
            type: "GET",
            // data: data,
            dataType: 'html',
            processData: false,
            contentType: false,
            async: true
            // headers: {'X-CSRFToken': token},
        }
        callAJAX(params, function (response) {
            var data = eval('(' + JXG.decompress(response) + ')');
            var source =
                {
                    dataType: "json",
                    dataFields: [
                        {name: 'id'},
                        {name: 'parentid'},
                        {name: 'text'},
                        {name: 'admin_level_name'}

                    ],
                    hierarchy: {
                        keyDataField: {name: 'id'},
                        parentDataField: {name: 'parentid'}
                    },
                    id: 'id',
                    localData: data
                };
            // create data adapter.
            var dataAdapter = new $.jqx.dataAdapter(source);
            // perform Data Binding.
            // dataAdapter.dataBind();
            var records = dataAdapter.getRecordsHierarchy('id', 'parentid', 'items', [{name: 'text', map: 'label'}]);
            // me.treeTarget.jqxTreeGrid({source: records, width: '100%'});
            me.treeTarget.jqxTreeGrid({
                source: dataAdapter,
                width: '100%',
                filterable: true,
                filterMode: 'simple',
                columns: [{text: 'Level Name', dataField: 'text'}, {text: 'Level', dataField: 'admin_level_name'}],
                ready: function () {
                    var rows = me.treeTarget.jqxTreeGrid('getRows');
                    var key = me.treeTarget.jqxTreeGrid('getKey', rows[0]);
                    me.treeTarget.jqxTreeGrid('expandRow', key);
                },
            });
            me.treeTarget.on('rowSelect', function (event) {
                var args = event.args;
                // row data.
                var row = args.row;
                me.selectedTreeItem = row;
                me.selectAdminLevelGeometryOnMap(me.selectedTreeItem.id);
                // var type = args.type; // mouse, keyboard or null. If the user selects with the mouse, the type will be "mouse".
            });
            me.treeTarget.on('rowDoubleClick', function (event) {
                var args = event.args;
                // row data.
                var row = args.row;
                me.selectedTreeItem = row;
                me.selectAdminLevelGeometryOnMap(me.selectedTreeItem.id);
                me.olMapModel.zoomToSelectedFeatures();
                // var type = args.type; // mouse, keyboard or null. If the user selects with the mouse, the type will be "mouse".
            });
        });
    }
    me.addLayerToMap = function () {
        if (me.layerType == "base") {
            me.olMapModel.addBaseLayer(me.selectedTreeItem.value);
        } else if (me.layerType == "dch") {
            me.olMapModel.addTileWMSLayer(me.viewInfo.url_wms_map, me.selectedTreeItem.value)
        }
    }
    me.selectAdminLevelGeometryOnMap = function (oid) {
        var url = "/web_services/wfs/get_feature/geom/admin_level/"
        url = url + "?level_id=" + oid
        var params = {
            url: url,
            type: "GET",
            dataType: "json",
            processData: false,
            contentType: false,
            async: true
        }
        callAJAX(params, function (data) {
            me.olMapModel.clearSelection()
            for (var i = 0; i < data.length; i++) {
                var geom = data[i];
                me.olMapModel.showSelectedFeatureGeometry(geom[0], false)
            }
        });
    }

}

