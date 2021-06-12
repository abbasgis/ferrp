/**
 * Created by Dr. Ather Ashraf on 2/3/2018.
 */

/**
 * Created by ather on 12/9/2017.
 */
var olMapModel = new OLMapModel("map", extent);

Ext.application({
    name: 'FeatureGrids',
    launch: function () {
        var layerExtVM = new MapExtVM(olMapModel);
        layerExtVM.initialize();
        Ext.on('resize', function () {
            var rem_height = layerExtVM.getViewportHeight();

            var panel = Ext.getCmp('extviewportPanel');
            // Ext.get("extviewport").setHeight(rem_height);
            panel.setHeight(rem_height);
            panel.updateLayout();
        });
    }
});

var MapExtVM = function (olMapModel) {
    var me = this;
    me.olMapModel = olMapModel;//new OLMapModel(extent);
    // me.olMapModel = new OLMapModel(extent);
    me.toolbarModel = new ExtToolbarModel(me.olMapModel);
    me.statusbarModel = new ExtStatusbarModel();
    me.initialize = function () {
        me.viewportItems = [];
        me.viewportItems.push(me.setMapPanel());
        me.viewportItems.push(me.setPanelWest());
        me.setViewPanel(me.viewportItems)
    }
    me.setMapPanel = function () {
        me.olMapModel.initialize("layerSwitcher");
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
        return me.mapPanel;
    }
    me.setPanelWest = function () {
        me.panelWest = Ext.create('Ext.panel.Panel', {
            border: true,
            region: 'west',
            width: '20%',
            loadMask: true,
            contentEl: 'layerSwitcher',
            resizable: true,
            collapsible: true,
            iconCls: 'settings',
            title: 'Legend Panel',
            plugins: 'responsive',
            responsiveConfig: {
                'width < 800': {
                    region: 'north',
                    collapsed: 'true'
                },
                'width >= 800': {
                    region: 'west',
                    // collapsed: 'false'
                }
            },
            listeners: {
                beforecollapse: function (p, direction, animate, eOpts) {
                    // alert("in before Collapse")
                    $('#layerSwitcher').css('visibility', 'hidden');
                },
                beforeexpand: function (p, animate, eOpts) {
                    // alert("in expand")
                    $('#layerSwitcher').css('visibility', 'visible');
                }
            }
        })
        $('#layerSwitcher').css('visibility', 'visible');
        return me.panelWest;
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
        var rem_height = height - (navbar_height + header_height + footer_heght) + 10;
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
        //Add New Layer button
        var addNewLayerModel = new ExtAddNewLayerModel(me.olMapModel);
        me.toolbar.push(addNewLayerModel.initialize())

        //Add Full Extent Button
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


    var ExtAddNewLayerModel = function (olMapModel) {
        var me = this;
        me.olMapModel = olMapModel;
        me.selectedSource = "dch";

        me.initialize = function () {
            return me.createorgetAddLayerButton();
        }

        me.createorgetAddLayerButton = function () {
            if (!me.btnAddLayer) {
                me.btnAddLayer = Ext.create('Ext.Button', {
                    // text: 'Full Extent',
                    iconCls: 'fa fa-lg fa-plus',
                    toggleGroup: 'navigation',
                    handler: function () {
                        // alert('You clicked the button!');
                        me.showNewLayerWindow()
                    }
                });
            }
            return me.btnAddLayer;
        }

        me.createorgetAddLayerCmbStore = function () {
            me.layerSources = [
                {"abbr": "dch", "name": "P&D Data clearinghouse"},
                {"abbr": "base", "name": "Base Layers"}
            ]
            me.sourceStore = Ext.create('Ext.data.Store', {
                fields: ['abbr', 'name'],
                data: me.layerSources,

            });
            return me.sourceStore;
        }

        me.createorgetSourcesComboBox = function () {
            if (!me.cmbSources) {
                me.cmbSources = Ext.create('Ext.form.ComboBox', {
                    // fieldLabel: 'Choose Source',
                    region: 'north',
                    store: me.createorgetAddLayerCmbStore(),
                    queryMode: 'local',
                    displayField: 'name',
                    valueField: 'abbr',
                    forceSelection: true,
                    value: 'dch',
                    selectOnFocus: true,
                    listeners: {
                        select: function (combo, record, eOpts) {
                            me.selectedSource = record.data.abbr;
                            var store = me.createorgetAddLayerTreeStore(me.selectedSource);
                            // store.load();
                            // me.layerTreePanel.bindStore(store)

                        }
                    }
                    // renderTo: Ext.getBody()
                });
            }
            return me.cmbSources;
        }

        me.createorgetLayerTreePanel = function () {
            if (!me.layerTreePanel) {
                me.layerTreePanel = Ext.create('Ext.tree.Panel', {  // Let's put an empty grid in just to illustrate fit layout
                    xtype: 'treepanel',
                    region: 'center',
                    store: me.createorgetAddLayerTreeStore(me.selectedSource),
                    rootVisible: false,
                    frame: true,
                    autoScroll: true,
                });
            }
            return me.layerTreePanel
        }

        me.createorgetAddLayerTreeStore = function (type) {
            var url = url_add_layer_data + "?type=" + type
            var proxy = {
                type: 'ajax',
                url: url,
                reader: {
                    type: 'json',
                    rootProperty: 'children'
                }
            }
            if (!me.treePanelStore) {
                me.treePanelStore = Ext.create('Ext.data.TreeStore', {
                    root: {expanded: true},
                    proxy: proxy,
                    autoLoad: true
                });
            } else {
                me.treePanelStore.setProxy(proxy)
                me.treePanelStore.load()
            }

            return me.treePanelStore;
        }

        me.createorgetTreeButtonPanel = function () {
            if (!me.btnPanel) {
                me.btnPanel = Ext.create('Ext.panel.Panel', {
                    region: 'south',
                    html: '<button class="btn btn-primary btn-block"' +
                    ' id="btnTreeAddLayer">Add Layer</button>'
                })
                $(document).on("click", "#btnTreeAddLayer", function () {
                    var selectedItem = me.layerTreePanel.getSelection();
                    if (selectedItem.length > 0) {
                        var add_layer_name = selectedItem[0].data.text;
                        if (me.selectedSource == "base") {
                            me.olMapModel.addBaseLayer(add_layer_name);
                        } else {
                            me.olMapModel.addTileWMSLayer(url_wms_map, add_layer_name)
                        }

                    }

                });
            }
            return me.btnPanel;
        }
        me.showNewLayerWindow = function () {
            if (!me.layerWindow) {
                me.layerWindow = Ext.create('Ext.window.Window', {
                    title: 'Layer Sources',
                    height: 400,
                    width: 200,
                    layout: 'border',
                    closeAction: 'hide',
                    items: [
                        me.createorgetSourcesComboBox(),
                        me.createorgetLayerTreePanel(),
                        me.createorgetTreeButtonPanel()
                    ]
                });
                me.layerWindow.show();
            } else {
                me.layerWindow.show();
            }
        }
    }


}







