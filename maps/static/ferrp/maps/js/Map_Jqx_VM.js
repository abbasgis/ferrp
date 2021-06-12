/**
 * Created by Dr. Ather Ashraf on 2/17/2018.
 */

var cursorX;
var cursorY;

// var theme = "";

$(document).ready(function () {
    // mapJqxVM.setViewportHeight();
    // $("#map").height("90%");
    // var cameraSettingVM = new CameraSettingVM();
    // var mapJqxVM = new MapJqxVM('viewport', cameraSettingVM);
    var olMapModel = new OLMapModel(mapInfo.extent, "map", "layerSwitcher", mapJqxVM, mapInfo.csrfToken, cameraSettingVM);
    mapJqxVM.setLayout(olMapModel);
    olMapModel.initialize();
    if (mapInfo.project_id !== '' && mapInfo.page === 'benefits') {
        mapJqxVM.showStatsPanel();
    }
    for (var j = 0; j < mapInfo.groupLayers.length; j++) {
        var layers = mapInfo.groupLayers[j].layers;
        var group_name = mapInfo.groupLayers[j].group_name;
        for (var i = 0; i < layers.length; i++) {
            olMapModel.addTileWMSLayer(mapInfo.url_wms_map, layers[i].layer_name, layers[i].layer_style, group_name);
        }
    }
    if (mapInfo.project_id !== '') {
        mapJqxVM.siteSelModel = new SiteSelectionModel(mapInfo, mapJqxVM);
        mapJqxVM.siteSelModel.init();
    }
    mapJqxVM.toolbarModel.monitorViewChange();

});

$(window).resize(function () {
    mapJqxVM.setViewportLayoutHeight();

});
// $('#map').resize(function(){
//     mapJqxVM.resizeMapArea();
// });
var MapJqxVM = function (viewportId, cameraSettingVM) {
    var me = this;
    me.project_id = mapInfo.project_id;
    // me.mapInfo = mapInfo;
    me.olMapModel = null;
    me.toolbarModel = null;
    me.layerContextMenuModel = null;
    me.theme = theme;
    me.viewPort = $('#' + viewportId);
    me.jqxLayoutTarget = $('#jqxLayout');
    me.layerContextMenuTarget = $('#jqxLayerConetextMenu');
    me.selectedIndex = null;
    me.cameraSettingVM = cameraSettingVM;
    me.statViewModel = null;
    me.siteSelModel = null;
    me.navigationPnlSel = false;
    if (mapInfo.page === 'project_location' || mapInfo.page === 'benefits') {
        me.navigationPnlSel = true;
    }
    // me.outputDivId = 'output';

    me.layoutDist = {"westgroup": "22%", "centergroup": "70%", "eastgroup": "8%"}
    me.layout = [{
        type: 'layoutGroup',
        orientation: 'horizontal',
        items: [
            {
                type: 'tabbedGroup',
                alignment: 'left',
                width: me.layoutDist.westgroup,
                minWidth: 300,
                items: [{
                    type: 'layoutPanel',
                    title: 'Table of Content',
                    contentContainer: 'TOCPanel'
                },
                    {
                        type: 'layoutPanel',
                        title: 'Navigation',
                        contentContainer: 'NavigationPanel',
                        selected: me.navigationPnlSel,
                        initContent: function (e) {
                            var addNavigationModel = new AddNavigationModel(me.olMapModel, mapInfo);
                            addNavigationModel.initialize();
                        }
                    }
                ]
            },
            {
                type: 'layoutGroup',
                orientation: 'vertical',
                width: me.layoutDist.centergroup,
                items: [{
                    type: 'documentGroup',
                    height: '94%',
                    minHeight: 200,
                    items: [{
                        type: 'documentPanel',
                        title: 'Map View',
                        contentContainer: 'MapPanel'
                    }]
                }, {
                    type: 'autoHideGroup', //'autoHideGroup', //'tabbedGroup',
                    alignment: 'bottom',
                    height: '6%',
                    // allowUnpin: 'false',
                    unpinnedHeight: '50%',
                    items: [{
                        // id:'OutputPanel',
                        type: 'layoutPanel',
                        title: 'Output',
                        contentContainer: 'outputPanel',
                        // selected: true
                    },
                        // {
                        //     // id:'OutputPanel',
                        //     type: 'layoutPanel',
                        //     title: 'Chart',
                        //     contentContainer: 'chartPanel',
                        //     // selected: true
                        // }
                    ]
                }]
            },
            {
                type: 'autoHideGroup',
                // type: 'tabbedGroup',
                alignment: 'right',
                width: me.layoutDist.eastgroup,
                // pinnedHeight: '50%',
                unpinnedWidth: '20%',
                items: [
                    {
                        type: 'layoutPanel',
                        title: 'Catalogue',
                        // height: '100%',
                        contentContainer: 'CataloguePanel',
                        initContent: function () {
                            var addLayerModel = new AddLayerModel(me.olMapModel, mapInfo)
                            addLayerModel.initialize();
                        }
                    },
                    {
                        type: 'layoutPanel',
                        title: 'Orientation Setting',
                        contentContainer: 'OrientationSettingPanel',
                        initContent: function () {
                            me.cameraSettingVM.initCameraSettingPanel(me.olMapModel, me.olMapModel.olCesiumModel);
                        }
                    }, {
                        type: 'layoutPanel',
                        title: 'Statistics',
                        // selected: true,
                        contentContainer: 'StatisticalPanel',
                        initContent: function () {
                            me.statViewModel = new StaticViewModel(me.olMapModel, mapInfo);
                            me.statViewModel.init();
                        }
                    }]
            }]
    }];
    me.setLayout = function (olMapModel) {
        me.olMapModel = olMapModel;
        me.jqxLayoutTarget.jqxLayout({
            theme: theme,
            width: '100%',
            height: me.getViewportHeight(),
            layout: me.layout
        });
        me.toolbarModel = new JQXToolbarModel("10%", mapInfo, me);
        var navbar = me.toolbarModel.navbar;
        var navbarSeq = [navbar.saveMap, navbar.setMapPermission, navbar.spacebar,
            navbar.addLayer, navbar.fullExtent, navbar.pan, navbar.zoom2Rect, navbar.zoomIn, navbar.zoomOut, navbar.zoom2Prev, navbar.zoom2Next,
            navbar.spacebar, navbar.zoom2Selection, navbar.clearSelection, navbar.identifier, navbar.query, navbar.spatialQuery,
            navbar.spacebar, navbar.profileExtractor, navbar.shortestPath, navbar.ThreeD, navbar.weather,

        ];
        if (mapInfo.page === 'project_location') {
            navbarSeq = [navbar.saveMap, navbar.setMapPermission, navbar.spacebar,
                navbar.addLayer, navbar.fullExtent, navbar.pan, navbar.zoom2Rect, navbar.zoomIn, navbar.zoomOut, navbar.zoom2Prev, navbar.zoom2Next,
                navbar.zoom2Selection, navbar.clearSelection, navbar.spacebar, navbar.ssa, navbar.spacebar, navbar.project_location, navbar.spacebar, navbar.submit_location,
                navbar.spacebar, navbar.approve_location, navbar.spacebar, navbar.disapprove_location]

            // me.jqxLayoutTarget.jqxLayout('selected', 1);
            // $('#NavigationPanel').jqxTabs('select', 1);

        }
        if (mapInfo.project_id !== '' && mapInfo.page !== 'project_location') {
             navbarSeq.push(navbar.geoStatistics);
            navbarSeq.push(navbar.ssa);
            navbarSeq.push(navbar.location);
            navbarSeq.push(navbar.sms);
        }
        me.toolbarModel.initialize(me, navbarSeq);
        me.layerContextMenuModel = new LayerContextMenuModel(me.layerContextMenuTarget, me, 'outputpanel');

    };
    me.resizeMapArea = function () {
        me.olMapModel.resizeMapArea();
    }
    me.setViewportHeight = function () {
        var rem_height = me.getViewportHeight();
        me.viewPort.height(rem_height);
    }
    me.setViewportLayoutHeight = function () {

        var rem_height = me.getViewportHeight();
        rem_height = (rem_height > 500 ? rem_height : 500);
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
        var minHeight = 450
        rem_height = (rem_height > minHeight ? rem_height : minHeight);
        return rem_height;
    }
    me.getOutputPanel = function () {
        var layout = me.jqxLayoutTarget.jqxLayout('layout');
        var outputPanel = layout[0].items[1].items[1];
        return outputPanel;
    }
    me.getNavigationPanel = function () {
        var layout = me.jqxLayoutTarget.jqxLayout('layout');
        return layout[0].items[0].items[1];

    }
    me.getOrientationPanel = function () {
        var layout = me.jqxLayoutTarget.jqxLayout('layout');
        return layout[0].items[2].items[1];

    }
    me.getStatsPanel = function () {
        var layout = me.jqxLayoutTarget.jqxLayout('layout');
        var statPanel = layout[0].items[2].items[2];
        return statPanel;
    }
    me.getMapPanel = function () {
        var layout = me.jqxLayoutTarget.jqxLayout('layout');
        var mapPanel = layout[0].items[1].items[0];
        return mapPanel;
    }
    me.getOutputPanelSize = function () {
        var outputPanel = me.getOutputPanel();
        // alert(outputPanel.title)
        var width = $(outputPanel.widget[0]).width();
        var height = $(outputPanel.widget[0]).height();
        return {width: width, height: height};
    }
    me.showOutputPanel = function (index) {
        $('#output').show();
        // var layout = me.jqxLayoutTarget.jqxLayout('layout');
        // layout.prototype._unPin(outputPanel);
        var outputPanel = me.getOutputPanel();
        var mapPanel = me.getMapPanel();
        $('#output').empty();
        // me.selectedIndex = index;
        // outputPanel.widget.jqxRibbon('selectAt', me.selectedIndex)
        if (outputPanel.type !== 'tabbedGroup') {
            me.jqxLayoutTarget.jqxLayout('_unPin', outputPanel);
        }
    }
    me.showHidePanel = function (panel, isShow) {
        panel.selected = isShow;
        me.jqxLayoutTarget.jqxLayout('render');
        if (panel.type !== 'tabbedGroup') {
            // me.selectedIndex = 2;
            me.jqxLayoutTarget.jqxLayout('_unPin', panel.parent);

        }
    };
    me.showStatsPanel = function () {
        // var layout = me.jqxLayoutTarget.jqxLayout('saveLayout');
        // var layout = me.jqxLayoutTarget.jqxLayout('layout');
        var statPanel = me.getStatsPanel();
        if (!statPanel.selected) {
            me.showHidePanel(statPanel, true);
        }

        // statPanel.selected = true;
        // // me.layout[0].items[2].items[2] = statPanel;
        // // me.jqxLayoutTarget.jqxLayout('loadLayout', me.layout);
        // // me.jqxLayoutTarget.jqxLayout('render');
        // me.jqxLayoutTarget.jqxLayout('refresh');
        //
        //
        // $('#statistics').show();
        // // var layout = me.jqxLayoutTarget.jqxLayout('layout');
        // // layout.prototype._unPin(outputPanel);
        // var statsPanel = me.getStatsPanel();
        // var mapPanel = me.getMapPanel();
        // // $('#statistics').empty();
        // // me.selectedIndex = index;
        // // outputPanel.widget.jqxRibbon('selectAt', me.selectedIndex)
        // if (statsPanel.type !== 'tabbedGroup') {
        //     // me.selectedIndex = 2;
        //     me.jqxLayoutTarget.jqxLayout('_unPin', statsPanel.parent);
        //
        // }
    }


    me.jqxLayoutTarget.on('pin', function (event) {
        var pinnedItem = event.args.item;
        if (me.selectedIndex) {
            pinnedItem.widget.jqxRibbon('selectAt', me.selectedIndex);
        }
        // alert(me.selectedIndex);
        // Some code here.
    });
    // me.jqxLayoutTarget.on('unpin', function (event) {
    //     var unpinnedItem = event.args.item;
    //     if (me.selectedIndex) {
    //         // unpinnedItem.items[me.selectedIndex].selected = true;
    //         // me.jqxLayoutTarget.jqxLayout('render');
    //         // me.jqxLayoutTarget.jqxLayout('refresh');
    //         // $('#statistics').show();
    //         var ribbonWidget = unpinnedItem.widget.find(".jqx-layout-ribbon-header");
    //         if (ribbonWidget) {
    //             ribbonWidget.jqxRibbon('selectAt', me.selectedIndex);
    //             ribbonWidget.jqxRibbon('showAt', me.selectedIndex);
    //         }
    //
    //     }
    //     me.selectedIndex = null;
    //     // alert(me.selectedIndex);
    //     // Some code here.
    // });

}



