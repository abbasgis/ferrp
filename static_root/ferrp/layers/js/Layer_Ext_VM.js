/**
 * Created by ather on 12/9/2017.
 */
var layerExtVM =null;
var olMapModel=new OLMapModel(extent, "map", null, layerExtVM,null);
Ext.application({
    name: 'FeatureGrids',
    launch: function () {
        var layerExtVM = new LayerExtVM( olMapModel);
        layerExtVM.initialize(layertype);
        olMapModel.setViewModel(layerExtVM);
        $('#settings').css('visibility', 'visible');
        Ext.on('resize', function () {
            var rem_height = layerExtVM.getViewportHeight();
            var panel = Ext.getCmp('extviewportPanel');
            // Ext.get("extviewport").setHeight(rem_height);
            panel.setHeight(rem_height);
            panel.updateLayout();
        });
    }
});

var LayerExtVM = function (olMapModel) {
    var me = this;
    me.olMapModel = olMapModel;//new OLMapModel(extent);
    // me.olMapModel = new OLMapModel(extent);
    me.toolbarModel = new ExtToolbarModel(me.olMapModel);
    me.statusbarModel = new ExtStatusbarModel();
    me.initialize = function (layer_type) {
        me.viewportItems = [];
        me.setMapPanel();
        me.setPanelEast();
        me.viewportItems.push(me.mapPanel);
        me.viewportItems.push(me.panelEast);
        if (layer_type == 'Vector') {
            // me.olMapModel.addVectorLayer(url_geojson, layername);
            // me.olMapModel.addTileVectorLayer(url_geojson,layername);
            // me.olMapModel.addTileWMSLayer(url_wms_map,layername);
            me.olMapModel.addImageWMSLayer(url_wms_map, layername);
            var vectorLayer = me.olMapModel.getVectorLayerByName(layername);
            var olMap = me.olMapModel.getMap();
            // me.setGridSouth(olMap, vectorLayer)
            // me.viewportItems.push(me.gridSouth);
        }
        else {
            // olMapModel.addImageWMSLayer(url_wms_map,layername);   //getVectorLayerByName(layername);
            me.olMapModel.addTileWMSLayer(url_wms_map, layername);
        }
        me.setViewPanel(me.viewportItems)
    }
    me.setMapPanel = function () {
        me.olMapModel.initialize();
        var olMap = me.olMapModel.getMap();
        me.mapComponent = Ext.create('GeoExt.component.Map', {
            map: olMap
        });
        me.mapPanel = Ext.create('Ext.panel.Panel', {
            id: 'map-panel',
            region: 'center',
            layout: 'fit',
            title: 'Map Panel',
            items: [me.mapComponent],
            tbar: me.toolbarModel.getToolbar(),
            bbar: me.statusbarModel.getStatusbar()
        });
    }
    me.setPanelEast = function () {
        me.panelEast = Ext.create('Ext.panel.Panel', {
            border: true,
            // region: 'east',
            width: '20%',
            // loadMask: true,
            resizable: true,
            collapsible: true,
            iconCls: 'settings',
            contentEl: 'settings',
            plugins: 'responsive',
            title: 'Setting Panel',
            responsiveConfig: {
                'width < 800': {
                    region: 'north',
                    collapsed: 'true'
                },
                'width >= 800': {
                    region: 'east',
                    // collapsed: 'false'
                },
                // 'height < 600': {
                //     collapsed: 'true'
                // },
                // 'height >=600': {
                //     collpased: 'false'
                // }
            },
            listeners: {
                beforecollapse: function (p, direction, animate, eOpts) {
                    // alert("in before Collapse")
                    $('#settings').css('visibility', 'hidden');
                },
                beforeexpand: function (p, animate, eOpts) {
                    // alert("in expand")
                    $('#settings').css('visibility', 'visible');
                }
            }
        })
    }
    me.setGridSouth = function (olMap, vectorLayer) {
        var featStore2 = Ext.create('GeoExt.data.store.Features', {
            layer: vectorLayer,
            map: olMap
        });
        me.gridSouth = Ext.create('Ext.grid.Panel', {
            title: 'Attribute Grid - ' + layername,
            border: true,
            region: 'south',
            // frame: true,
            store: featStore2,
            collapsible: true,
            columns: col_list,
            plugins: 'gridfilters',
            height: '25%',
            // collapsed: true,
            loadMask: true,
            resizable: true,
            features: [{
                id: 'group',
                ftype: 'groupingsummary',
                groupHeaderTpl: '{name}',
                hideGroupedHeader: true,
                enableGroupingMenu: true
            }],
            // plugins: 'responsive',
            // responsiveConfig: {
            //     'width < 800': {
            //         collapsed: 'true'
            //     },
            //     'width >= 800': {
            //         collapsed: 'false'
            //     }
            // },
            listeners: {
                'selectionchange': function (grid, selected) {
                    // reset all selections
                    featStore2.each(function (rec) {
                        var feature = rec.getFeature();
                        feature.setStyle(me.olMapModel.getStyle(feature));
                    });
                    // highlight grid selection in map
                    Ext.each(selected, function (rec) {
                        rec.getFeature().setStyle(me.olMapModel.getSelectStyle());
                    });
                }
            }
        });
    }

    // create feature store by passing a vector layer

    //// My View port
    me.getViewportHeight = function () {
        var width = Ext.getBody().getViewSize().width;
        var height = Ext.getBody().getViewSize().height;
        var navbar_height = Ext.get("base_nav").getViewSize().height;

        var header_height = (Ext.get("header") ? Ext.get("header").getViewSize().height : 0);
        var footer_heght = (Ext.get("footer") ? Ext.get("footer").getViewSize().height : 0);
        var rem_height = height - (navbar_height + header_height + footer_heght);
        return rem_height;
    }
    me.setViewPanel = function (viewportItems) {
        var renderTo = Ext.get('extviewport');
        var height = me.getViewportHeight();
        me.viewpanel = Ext.create('Ext.panel.Panel', {
            id: "extviewportPanel",
            layout: 'border',
            text: 'Map View',
            padding: 7,
            // margin: 10,
            items: viewportItems, //, gridWest, gridEast, description
            renderTo: renderTo,
            height: height,

        });
    }

}

var ExtStatusbarModel = function () {
    var me = this;
    // me.setText = function (text){
    //     me.setStatusbar()
    // }
    me.getStatusbar = function () {
        if (!me.statusbar) me.setStatusbar();
        return me.statusbar
    }
    me.setStatusbar = function () {
        me.statusbar = Ext.create('Ext.ux.StatusBar', {
            id: 'map-status',

            // defaults to use when the status is cleared:
            // defaultText: 'Default status text',
            // defaultIconCls: 'default-icon',

            // values to set initially:
            text: 'Ready',
            iconCls: 'x-status-valid',

            // any standard Toolbar items:
            items: [
                // {
                //     id: 'mouse-position',
                //     text: 'A Button'
                // }, '-',
                '<div id="mouse-position" class="custom-mouse-position">Mouse Position</div>'
            ]
        })
    }
}

var ExtToolbarModel = function (olMapModel) {
    var me = this;
    me.olMapModel = olMapModel;
    me.toolbar = []
    me.getToolbar = function () {
        // if (me.toolbar.length)
        me.setNavigationToolbar();
        return me.toolbar;
    }

    me.setNavigationToolbar = function () {
        var btnFullExtent = Ext.create('Ext.Button', {
            // text: 'Full Extent',
            iconCls: 'fa fa-lg fa-globe',
            toggleGroup: 'navigation',
            handler: function () {
                // alert('You clicked the button!');
                me.olMapModel.setFullExtent();
            }
        });
        me.toolbar.push(btnFullExtent);

        var btnZoomToRectangle = Ext.create('Ext.Button', {
            iconCls: 'fa fa-lg fa-search',
            enableToggle: true,
            toggleGroup: 'navigation',
            toggleHandler: function (btn, state) {
                if (state == true) {
                    me.zoomRectInteraction = me.olMapModel.zoomToRectangle();
                } else {
                    me.olMapModel.removeInteraction(me.zoomRectInteraction)
                }
            }
        })
        me.toolbar.push(btnZoomToRectangle);

        var btnZoomIn = Ext.create('Ext.Button', {
            iconCls: 'fa fa-lg fa-search-plus',
            toggleGroup: 'navigation',
            handler: function () {
                // alert('You clicked the button!');
                me.olMapModel.zoomIn();
            }
        });
        me.toolbar.push(btnZoomIn);

        var btnZoomOut = Ext.create('Ext.Button', {
            iconCls: 'fa fa-lg fa-search-minus',
            toggleGroup: 'navigation',
            handler: function () {
                // alert('You clicked the button!');
                me.olMapModel.zoomOut();
            }
        });
        me.toolbar.push(btnZoomOut);

        var btnPan = Ext.create('Ext.Button', {
            iconCls: 'fa fa-lg fa-hand-paper-o',
            enableToggle: true,
            toggleGroup: 'navigation',
            toggleHandler: function (btn, state) {
                if (state == true) {
                    me.panInteraction = me.olMapModel.pan();
                } else {
                    me.olMapModel.removeInteraction(me.panInteraction);
                }
            }
        });
        me.toolbar.push(btnPan);

        var btnZoom2PerviousExtent = Ext.create('Ext.Button', {
            iconCls: 'fa fa-lg fa-arrow-left',
            tooltip: 'Zoom to pervious extent',
            toggleGroup: 'navigation',
            disabled: true,
            handler: function () {
                // alert('You clicked the button!');
                me.olMapModel.zoom2PreviousExtent();
            }
        });
        me.toolbar.push(btnZoom2PerviousExtent);

        var btnZoom2NextExtent = Ext.create('Ext.Button', {
            iconCls: 'fa fa-lg fa-arrow-right',
            tooltip: "Zoom to next extent",
            toggleGroup: 'navigation',
            disabled: true,
            handler: function () {
                // alert('You clicked the button!');
                me.olMapModel.zoom2NextExtent();
            }
        });
        me.toolbar.push(btnZoom2NextExtent);
        me.enableDisableExtentButton = function () {
            if (me.olMapModel.getSizeOfNextExtent() > 0) {
                btnZoom2NextExtent.setDisabled(false);
            } else {
                btnZoom2NextExtent.setDisabled(true);
            }
            if (me.olMapModel.getSizeOfPreviousExtent() > 0) {
                btnZoom2PerviousExtent.setDisabled(false);
            } else {
                btnZoom2PerviousExtent.setDisabled(true);
            }
        }
        me.olMapModel.getView().on('change:resolution', function () {
            me.enableDisableExtentButton();
        });
        me.olMapModel.getView().on('change:center', function () {
            me.enableDisableExtentButton();
        });

    }
}

