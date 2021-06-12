/**
 * Created by idrees on 12/13/2017.
 */

Ext.Loader.setConfig({enabled: true});
Ext.Loader.setPath('Ext.ux', '/static/Extjs-6.2.0/packages/ux/classic/src');
Ext.Loader.setPath('Arz', 'irrigation/js/Arz');

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
        var renderDiv = Ext.get('statsDashboard');
        var widthWin = window.innerWidth;
        var heightWin = window.innerHeight;

        var statsModel = new ArzSurveyStatsModel();
        var arzAdminQuery = new ArzAdminQueryModel();

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
                        xtype: 'panel',
                        titleAlign:'center',
                        headerCls: 'extPanel',
                        title:'MHRVA Survey Map',
                        id: 'olMap',
                        layout: 'fit',
                        flex:1.5,
                        margin:'0 0 0 0',
                        tbar:[
                            {
                                tooltip:   'Filter by administrative boundary',
                                icon: imgPath + '04.png',
                                handler:function () {
                                    arzAdminQuery.createQueryWindow();
                                }
                            },
                            {
                                icon: imgPath + 'drawline.png',
                                tooltip:'Draw Polygon',
                                handler:function () {
                                    if(statsModel.vectorOverlay){
                                        var features = statsModel.vectorOverlay.getSource().getFeatures();
                                        features.forEach(function(feature) {
                                            statsModel.vectorOverlay.getSource().removeFeature(feature);
                                        });
                                    }
                                    var draw = new ol.interaction.Draw({
                                        source: statsModel.vectorOverlaySource,
                                        type: 'Polygon'
                                    });
                                    statsModel.olMap.addInteraction(draw);
                                    draw.on('drawend',function(evt) {
                                        statsModel.olMap.removeInteraction(draw);
                                    }, this);
                                }
                            },
                            {
                                icon: imgPath + '11.png',
                                tooltip:'Upload polygon/shapefile',
                                handler:function () {
                                    $('#uploadPolygonModal').modal('show');
                                }
                            },
                            {
                                icon: imgPath + 'Clear.png',
                                tooltip:'Clear selection/overlays',
                                handler:function () {
                                    if(statsModel.vectorOverlay){
                                        var features = statsModel.vectorOverlay.getSource().getFeatures();
                                        features.forEach(function(feature) {
                                            statsModel.vectorOverlay.getSource().removeFeature(feature);
                                        });
                                    }
                                }
                            }
                        ],
                        },
                        {
                            layout: 'border',
                            padding:'0 0 0 0',
                            flex:1,
                            items:[
                                {
                                    region:'center',
                                    layout:'fit',
                                    border: false,
                                    items:[
                                        {
                                            xtype: 'panel',
                                            titleAlign:'center',
                                            headerCls: 'extPanel',
                                            title:'Survey Statistics',
                                            id: 'pnlStatsData',
                                            border: false,
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
            align: 'stretch',
            listeners: {
                resize: function (pnl, width, height, oldWidth, oldHeight, eOpts) {
                    setTimeout( function() { statsModel.olMap.updateSize();}, 100);
                }
            }
        });

        statsModel.createOlMap(res_data_json);
        statsModel.createStatsGrid();

        Ext.EventManager.onWindowResize(function () {
            var widthWin = window.innerWidth - 15;
            var heightWin = window.innerHeight;
            panel.setHeight(heightWin - 105);
            panel.setWidth(widthWin - 20);
        });
    }
});
