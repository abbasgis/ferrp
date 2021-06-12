/**
 * Created by Dr. Ather Ashraf on 8/26/2018.
 */
/************************************************
 *
 * @param olMapModel
 * @constructor
 * usage: var addLayerModel = new AddLayerModel(olMapModel)
 addLayerModel.initialize();
 */
var AddLayerModel = function (olMapModel, viewInfo) {
    var me = this;
    me.viewInfo = viewInfo;
    me.layerStyleModel = null;
    me.catalogPanelTarget = $('#Catalogue');
    me.selectedTreeItem = "-1";
    me.dropDownTarget = $("<div id='CatDropDown'></div>");
    me.catalogPanelTarget.append(me.dropDownTarget);
    me.treeTarget = $("<div id='CatTree'></div>");
    me.catalogPanelTarget.append(me.treeTarget);
    me.olMapModel = olMapModel;
    me.layerTypeSources = [{label: 'Base Layers', value: "base"}, {label: 'Overlay Layers', value: "dch"}];
    me.initialize = function () {
        // me.addLayerTyeCombobox();
        me.addToolbar();
        me.addLayerTree(me.layerTypeSources[0].value)
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
                        var button = $("<div>" + "<i class='fa fa-lg fa-plus'></i>" + "</div>");
                        tool.append(button);
                        tool.on("click", function () {
                            // me.olMapModel.zoom2PreviousExtent();
                            if (me.selectedTreeItem != "-1") {
                                me.addLayerToMap();

                            } else {
                                showAlertDialog("Please select layer from below tree..", dialogTypes.info);
                            }
                        });
                        break;
                    case 1:
                        tool.jqxDropDownList({
                            theme: theme,
                            width: '70%',
                            source: me.layerTypeSources,
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
                                me.addLayerTree(value);
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

    me.addLayerTree = function (layerType) {
        me.destroyTree();
        // me.treeTarget = $('#CatTree');
        me.layerType = layerType;
        var params = {
            url: me.viewInfo.url_add_layer_data + "?layer_type=" + layerType,
            type: "GET",
            // data: data,
            dataType: "json",
            processData: false,
            contentType: false,
            async: true
            // headers: {'X-CSRFToken': token},
        };
        callAJAX(params, function (data) {
            var source =
                {
                    dataType: "json",
                    dataFields: [
                        {name: 'id'},
                        {name: 'parentid'},
                        {name: 'label'},
                        {name: 'value'}
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

            me.treeTarget.jqxTreeGrid({
                source: dataAdapter,
                width: '100%',
                filterable: true,
                filterMode: 'simple',
                columns: [{text: 'Layers', dataField: 'label'}]
            });
            me.treeTarget.on('rowClick', function (event) {
                var args = event.args;
                // row data.
                var row = args.row;
                me.selectedTreeItem = row;
            });
            me.treeTarget.on('rowDoubleClick', function (event) {
                var args = event.args;
                me.selectedTreeItem = args.row;
                me.addLayerToMap();
            });
        });
    }
    me.addLayerToMap = function () {
        if (me.layerType == "base") {
            me.olMapModel.addBaseLayer(me.selectedTreeItem.value);
        } else if (me.layerType == "dch") {
            var parent = me.selectedTreeItem.parent;
            if (parent !== null) {
                me.olMapModel.addTileWMSLayer(me.viewInfo.url_wms_map, me.selectedTreeItem.value, null, parent.label)
            }
        }
    }

}


/****************************************************
 *
 * @param target
 * @param viewModel
 * @constructor
 * me.layerContextMenuModel = new LayerContextMenuModel(me.layerContextMenuTarget,me);
 */
$(document).mousemove(function (e) {
    cursorX = e.pageX;
    cursorY = e.pageY;
});

var LayerContextMenuModel = function (target, viewModel, outputpanelId) {
    var me = this;
    me.viewModel = viewModel;
    me.btnOpenAttributeTable = $('#cmenuOpenAttributeTable');
    me.btnZoom2Layer = $('#cmenuZoom2Layer');
    me.btnLayerLegend = $('#cmenuLayerLegend');
    me.btnCreateSubLayer = $('#cmenuCreateSubLayer');
    me.btnChangeLayerStyle = $('#cmenuChangeStyle');
    me.contextMenuTarget = target;
    me.ooutputpanelId = outputpanelId;
    me.layerStyleModel = null;
    me.contextMenuTarget.jqxMenu({
        theme: theme,
        width: '210px',
        // height: '120px',
        autoOpenPopup: false,
        mode: 'popup'
    });
    me.selectedLayerName = null;
    me.info = false;
    me.openLayerContextMenu = function (layerNode) {
        me.selectedLayerName = layerNode.get("title");
        me.info = layerNode.get("info");
        if (me.info === 'weather') {
            var img_name = me.selectedLayerName.replace(' ', '');
            var img_src = "/static/ferrp/icons/legends/" + img_name + ".JPG";
            var modalbody = $('<div ><img src=' + img_src + ' width="100%" height="100%"></div>');
            me.viewModel.olMapModel.showDialog("Legend", modalbody, BootstrapDialog.SIZE_NORMAL);
        } else {
            me.contextMenuTarget.jqxMenu('open', parseInt(cursorX) + 5, parseInt(cursorY) + 5);
        }
    };

    me.btnOpenAttributeTable.on('click', function () {
        me.viewModel.showOutputPanel(0);
        var size = me.viewModel.getOutputPanelSize();
        gridVM.initializeLayerGridParames(me.selectedLayerName, me.viewModel, size.width, 'output')
    });
    me.btnZoom2Layer.on('click', function () {
        // alert(me.selectedLayerName)
        var url = '/layers/get_layer_extent/?layer_name=' + me.selectedLayerName
        var params = {url: url, dataType: "json", processData: false}
        callAJAX(params, function (data) {
            var extent = data;
            me.viewModel.olMapModel.zoomToExtent(extent.minX, extent.minY, extent.maxX, extent.maxY)
        })
    });
    me.btnLayerLegend.on('click', function () {
        var layerName = me.selectedLayerName;
        me.viewModel.olMapModel.showLegendgraphics(layerName)
    });
    me.btnCreateSubLayer.on('click', function () {
        var layerInfo = {};
        layerInfo.layerName = me.selectedLayerName;
        layerInfo.title = me.selectedLayerName;
        layerInfo.gridWidth = 300;
        layerInfo.onMap = true;
        layerInfo.wmsURL = "web_services/wms/get_map/";
        isCreateNewLayer = true;
        var qm = new QueryModel(me.viewModel, 'output', isCreateNewLayer);
        qm.createQueryDialog(layerInfo);
    })
    // me.contextMenuTarget.on('itemclick', function (event) {
    //     // get the clicked LI element.
    //     var element = event.args;
    //     console.log(element)
    // });
    me.btnChangeLayerStyle.on('click', function () {
        var layerName = me.selectedLayerName;
        var url = '/get_layer_info?layer_name=' + layerName;
        var params = {
            url: url,
            type: "GET",
            // data: {},
            dataType: "json",
            processData: false,
            contentType: false,
            async: true

        };

        callAJAX(params, function (info) {
            $('#LayerStylingModal').modal('show');
            info.isTempStyle = true;
            if (me.layerStyleModel == null) {
                me.layerStyleModel = new LayerStyleViewModel(me.viewModel.olMapModel, info);
                me.layerStyleModel.initialize();
            }else{
                me.layerStyleModel.setLayerInfo(info);
            }
        })


        // me.viewModel.olMapModel.showLegendgraphics(layerName)
    });

};
