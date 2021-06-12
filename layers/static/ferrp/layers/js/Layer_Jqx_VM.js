/**
 * Created by Dr. Ather Ashraf on 3/1/2018.
 */
var theme = 'fresh';


var LayerJqxVM = function (viewportId, layerInfo) {
    var me = this;
    me.layerInfo = layerInfo
    me.olMapModel = null;
    me.toolbarModel = null;
    me.theme = theme;
    me.viewPort = $('#' + viewportId);
    me.jqxLayoutTarget = $('#jqxLayout');
    me.layoutDist = {"centergroup": "80%", "westgroup": "20%"};
    // me.outputDivId = 'output';
    me.layout = [{
        type: 'layoutGroup',
        orientation: 'horizontal',
        items: [
            {
                type: 'layoutGroup',
                orientation: 'vertical',
                width: me.layoutDist.centergroup,
                items: [
                    {
                        type: 'documentGroup',
                        height: '94%',
                        // minHeight: 200,
                        items: [{
                            type: 'documentPanel',
                            title: 'Map View',
                            contentContainer: 'MapPanel'
                        }]
                    }, {
                        type: 'autoHideGroup', //'autoHideGroup', //'tabbedGroup',
                        alignment: 'bottom',
                        height: '6%',
                        // pinnedHeight: '30%',
                        // allowPin: false,

                        unpinnedHeight: '50%',
                        items: [{
                            type: 'layoutPanel',
                            title: 'Output',
                            contentContainer: 'OutputPanel',
                            // selected: false
                        }]
                    }]
            },
            {
                // type: 'autoHideGroup',
                type: 'tabbedGroup',
                // orientation: "vertical",
                alignment: 'right',
                width: me.layoutDist.westgroup,
                // unpinnedWidth: '20%',
                items: [
                    // {
                    // type: 'layoutPanel',
                    // title: 'Solution Explorer',
                    // contentContainer: 'SolutionExplorerPanel',
                    // initContent: function () {
                    //
                    // }
                    //   },
                    {
                        type: 'layoutPanel',
                        title: 'Settings',
                        contentContainer: 'SettingPanel',
                        initContent: function () {
                            var settingPanelModel = new SettingPanelModel(me.layerInfo, me);
                            // var addLayerModel = new AddLayerModel(me.olMapModel)
                            // addLayerModel.initialize();
                        }
                    },
                    {
                        type: 'layoutPanel',
                        title: 'Orientation',
                        contentContainer: 'OrientationPanel',
                        initContent: function () {
                            cameraSettingVM.initCameraSettingPanel(me.olMapModel, me.olMapModel.olCesiumModel);
                        }
                    }
                ]
            }
        ]
    }]

    me.setLayout = function (olMapModel) {
        me.olMapModel = olMapModel
        me.jqxLayoutTarget.jqxLayout({theme: theme, width: '100%', height: me.getViewportHeight(), layout: me.layout});
        me.toolbarModel = new JQXToolbarModel("10%", layerInfo, me);
        var navbar = me.toolbarModel.navbar;
        navbarSeq = [navbar.fullExtent, me.toolbarModel.navbar.pan, navbar.zoom2Rect, navbar.zoomIn, navbar.zoomOut, me.toolbarModel.navbar.zoom2Prev, navbar.zoom2Next,
            navbar.spacebar, navbar.zoom2Selection, navbar.clearSelection, navbar.identifier, navbar.query, navbar.spatialQuery,
            navbar.spacebar, navbar.profileExtractor, navbar.shortestPath, navbar.spacebar, navbar.ThreeD]

        me.toolbarModel.initialize(me, navbarSeq);
        me.olMapModel.initialize();
        me.toolbarModel.monitorViewChange()
        // alert("image");
        // me.olMapModel.addImageWMSLayer(layerInfo.url, layerInfo.layerName)
        var olLayer = me.olMapModel.addTileWMSLayer(layerInfo.url, layerInfo.layerName);
        me.olMapModel.wait4LayerLoad(olLayer);
    }

    me.resizeMapArea = function () {
        me.olMapModel.resizeMapArea();
    }

    me.setViewportHeight = function () {
        var rem_height = me.getViewportHeight();
        me.viewPort.height(rem_height);
    }

    me.setViewportLayoutHeight = function () {
        var rem_height = me.getViewportHeight();

        // me.viewPort.height(rem_height);
        me.jqxLayoutTarget.jqxLayout({height: rem_height});
        me.resizeMapArea();
    }

    me.getViewportHeight = function () {
        var width = $(document).width();
        var height = $(document).height();
        var navbar_height = $("#base_nav").height();
        var header_height = $("#header").height();
        var footer_heght = $("#footer").height();
        var rem_height = height - (navbar_height + header_height + footer_heght);
        var minHeight = 425
        rem_height = (rem_height > minHeight ? rem_height : minHeight);
        return rem_height;
    }

    me.getOutputPanel = function () {
        var layout = me.jqxLayoutTarget.jqxLayout('layout');
        var outputPanel = layout[0].items[0].items[1];
        return outputPanel;
    }
    me.getOutputPanelSize = function () {
        var outputPanel = me.getOutputPanel();
        // alert(outputPanel.title)
        var width = $(outputPanel.widget[0]).width();
        var height = $(outputPanel.widget[0]).height();
        return {width: width, height: height};
    }
    me.showOutputPanel = function (index) {
        var outputPanel = me.getOutputPanel();
        // var mapPanel = me.getMapPanel();
        $('#output').empty();
        // $('#output').removeAttr( "role" );
        // $('#output').removeAttr( "class" );
        // $('#output').removeClass()
        // me.selectedIndex = index;
        // outputPanel.widget.jqxRibbon('selectAt', me.selectedIndex)
        if (outputPanel.type != 'tabbedGroup') {
            me.jqxLayoutTarget.jqxLayout('_unPin', outputPanel);
        }

    }
}


var SettingPanelModel = function (layerInfo, viewModel) {
    var me = this;
    me.layoutVM = viewModel;
    me.layerInfo = layerInfo;
    me.olMapModel = viewModel.olMapModel;
    $('#settings').show();
    me.layerStyleModel = null
    $('#btnLayerStyling').on('click', function () {
        $('#LayerStylingModal').modal('show');
        if (me.layerStyleModel == null) {
            me.layerStyleModel = new LayerStyleViewModel(me.olMapModel, me.layerInfo);
        }
        me.layerStyleModel.initialize();
    })

    $('#btnDeleteLayer').on('click', function () {
        var url = me.layerInfo.urlDeleteLayer + "?layer_name=" + me.layerInfo.layerName + "&layer_type=" + me.layerInfo.layerType;
        callAJAX({url: url}, function (data) {
            if (data == "true") {
                showAlertDialog("Layer successfully deleted", dialogTypes.success);
                window.location.href = me.layerInfo.urlLayerBrowser;
            } else {
                showAlertDialog("Failed to delete file", dialogTypes.error);
            }
        })
    })
    $('#btnDownloadLayer').on('click', function () {
        var url = me.layerInfo.urlDownloadLayer + "?layer_name=" + me.layerInfo.layerName;
        window.location.href = url

    });

    $('#btnSetIcon').on('click', function () {
        if (me.olMapModel) {
            var image = me.olMapModel.capturePicture();
            // var data = {"img_name": me.layerInfo.layerName, "image": image};
            var formData = new FormData();
            formData.append("img_name", me.layerInfo.layerName);
            formData.append("image",image);
            var ajaxParam = {
                url: me.layerInfo.urlSetLayerIcon + "?layer_name=" + me.layerInfo.layerName,
                headers: {'X-CSRFToken': me.layerInfo.csrfToken},
                type: "POST",
                datatype: "json",
                data: formData
            };

            callAJAX(ajaxParam, function (data) {
                showAlertDialog("Icon has set", dialogTypes.success);
            })
        }
    });
    $("#btnShowAttribTable").on('click', function (data) {
        me.layoutVM.showOutputPanel(0);
        var size = me.layoutVM.getOutputPanelSize();
        gridVM.initializeLayerGridParames(me.layerInfo.layerName, viewModel, size.width, 'output')
    });
    $('#btnShowLabel').on('click', function () {
        var url = "/get_attribute_list/?layername=" + me.layerInfo.layerName;

        callAJAX({url: url, dataType: "json"}, function (data) {
            // var columns = data.columns;
            var labelFieldset = $('<fieldset></fieldset>');
            var fieldsetLegend = $('<legend>Label</legend>');
            labelFieldset.append(fieldsetLegend);

            var columnNameOptions = ' <label class="control-label">Column Name</label><select id="selColumnName" class="form-control"><option value="-1">Select Column Name</option>';
            for (var i = 0; i < data.length; i++) {
                columnNameOptions += "<option value='" + data[i]['column_name'] + "'>" + data[i]['column_name'] + "</option>";
            }
            columnNameOptions += "</select>"
            var columnNameSelect = $(columnNameOptions);
            labelFieldset.append(columnNameSelect);
            var labelColorName = $('<label class="control-label">Color</label>');
            labelFieldset.append(labelColorName);
            var labelColor = $('<input id="labelColor" class="form-control" />');
            labelColor[0].classList.add("form-control");
            var picker = new jscolor(labelColor[0]);
            var strColor = "#ffff00"//me.color2hex(shape.attr("fill"));
            picker.fromString(strColor);

            labelFieldset.append(labelColor);

            var labelSize = $('<div class="form-group"> <label class="control-label">Size</label> ' +
                '<input id="labelSize" class="form-control numbercounter" type="number" value=18 min="0" ' +
                'max="100" step="1"/> </div>');
            labelFieldset.append(labelSize);

            // $("select.selectColumnName").html(columnNameOptions).selectpicker('refresh');
            BootstrapDialog.show({
                title: 'Add Label',
                size: BootstrapDialog.SIZE_SMALL,
                type: BootstrapDialog.TYPE_SUCCESS,
                message: labelFieldset, //'Select Column Name: ' + columnNameOptions,
                onhide: function (dialogRef) {

                },
                buttons: [
                    {
                        label: 'Apply Label',
                        action: function (dialogRef) {
                            var colName = $("#selColumnName").val(); //dialogRef.getModalBody().find('select').val();
                            if (colName != -1) {
                                // var labelColor = '#ffff00'
                                labelColor = "#" + $('#labelColor').val();
                                // var fontSize = '18'
                                fontSize = $("#labelSize").val();
                                var fontType = 'arial'
                                me.olMapModel.addLabel2WMSLayer(me.layerInfo.layerName, colName, fontSize, fontType, labelColor);
                                dialogRef.close();
                            }
                        }
                    }, {
                        label: 'Clear Label',
                        action: function (dialogRef) {
                            me.olMapModel.removeLabelFromWMSLayer(me.layerInfo.layerName);
                            dialogRef.close();
                        }
                    }
                    // ,{
                    //     label: 'Close',
                    //     action: function (dialogRef) {
                    //         dialogRef.close();
                    //     }
                    // }
                ]
            });
        });

    });

    $('#btnCreateSubLayer').on('click', function (data) {
        // var qm = new QueryModel(me.layerInfo, true, me.layoutVM, 'output');
        // qm.initialize();

        var qm = new QueryModel(me.layoutVM, 'output', true);
        qm.createQueryDialog(me.layerInfo);
    })
    $('#btnShowLegendGraphics').on('click', function (data) {
        // var layer_style = me.olMapModel.getLayerStyle()
        me.olMapModel.showLegendgraphics(me.layerInfo.layerName)
    })
    $('#btnCreateRoadNetwork').on('click', function (data) {
        var networkModel = new NetworkTopologicalModel(me.layoutVM);
        networkModel.createNetworkTopology(me.layerInfo.layerName);
    })
    $('#btnAddToCategory').on('click', function (data) {
        var modalbody = $('<div ></div>');
        var form = '<form class="form-horizontal" action="/layers/set_layer_category/"><div class="form-group">' +
            '<label class="control-label col-sm-2" for="item_name">Layer:</label> ' +
            '<div class="col-sm-10"> <input type="text" class="form-control" id="item_name"  name="item_name" value="' + me.layerInfo.layerName + '" readonly> </div> </div> ' +
            '<div class="form-group"> <label class="control-label col-sm-2" for="category">Category:</label> ' +
            '<div class="col-sm-10"> <select  class="form-control" id="category" name="category"> ' +
            '<option>Administrative Boundary</option><option>Demography</option><option>Geology</option><option>Infrastructure</option><option>Landuse</option>' +
            '<option>Terrain</option><option>Waterbodies</option></select> ' +
            '</div> </div> <div class="form-group"> <div class="col-sm-offset-2 col-sm-10"> ' +
            '<button id="btnSubmitCategory" type="click" class="btn btn-default">Submit</button> </div> </div> </form>';
        modalbody.append(form);
        me.olMapModel.showDialog("Add Category", modalbody, BootstrapDialog.SIZE_NORMAL);
    })

}