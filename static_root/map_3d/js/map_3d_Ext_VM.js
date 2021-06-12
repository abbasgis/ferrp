/**
 * Created by Dr. Ather Ashraf on 2/7/2018.
 */
// var cesiumCnt = 'extviewportPanel';

Ext.require(['Ext.panel.Panel', 'layout.border']);

Ext.application({
    name: 'FeatureGrids',
    launch: function () {
        var map3ExtVM = new Map3DExtVM();
        map3ExtVM.initialize();
        Ext.on('resize', function () {
            var rem_height = map3ExtVM.getViewportHeight();
            var panel = Ext.getCmp('extviewportPanel');
            // Ext.get("extviewport").setHeight(rem_height);
            panel.setHeight(rem_height);
            panel.updateLayout();
        });
    }
});

var Map3DExtVM = function () {
    var me = this;
    me.initialize = function () {
        me.viewportItems = [];
        me.viewportItems.push(me.setCesiumPanel());
        // me.viewportItems.push(me.setPanelWest());
        me.setViewPanel(me.viewportItems)
        var viewer = new Cesium.Viewer('cesiumContainer')
    }
    me.getViewportHeight = function () {
        var width = Ext.getBody().getViewSize().width;
        var height = Ext.getBody().getViewSize().height;
        var navbar_height = Ext.get("base_nav").getViewSize().height;
        var header_height = (Ext.get("header") ? Ext.get("header").getViewSize().height : 0);
        var footer_heght = (Ext.get("footer") ? Ext.get("footer").getViewSize().height : 0);
        var rem_height = height - (navbar_height + header_height + footer_heght) + 10;
        return rem_height;
    }
    me.setCesiumPanel = function () {
        extToolBar = new ExtToolbarModel();
        me.cesiumPanel = Ext.create('Ext.panel.Panel', {
            id: 'cesium-panel',
            region: 'center',
            // layout: 'fit',
            // title: '3D Map',
            tbar: extToolBar.getToolbar(),
            html: '<div id="cesiumContainer"></div>'
            // items: [me.mapComponent],
            // tbar: me.toolbarModel.getToolbar(),
            // bbar: me.statusbarModel.getStatusbar()
        });
        return me.cesiumPanel;
    }
    me.setViewPanel = function (viewportItems) {
        var renderTo = Ext.get('extviewport');
        var height = me.getViewportHeight();
        me.viewpanel = Ext.create('Ext.panel.Panel', {
            id: "extviewportPanel",
            layout: 'border',
            // text: '3D Map',
            padding: '7 0 0 0',
            // margin: 10,
            items: viewportItems, //, gridWest, gridEast, description
            renderTo: renderTo,
            height: height,

        });
    }
}

var ExtToolbarModel = function () {
    var me = this;
    me.toolbar = []

    me.getToolbar = function () {
        // if (me.toolbar.length)
        me.setNavigationToolbar();
        return me.toolbar;
    }
    me.setNavigationToolbar = function () {
        var addNewLYayerModel = new ExtAddNewLayerModel();
        me.toolbar.push(addNewLYayerModel.initialize());
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

