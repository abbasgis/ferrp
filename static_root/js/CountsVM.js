/**
 * Created by idrees on 4/24/2018.
 */

Ext.Loader.setConfig({enabled: true});

Ext.require([
    'Ext.Viewport',
    'Ext.grid.Panel',
    'Ext.panel.Panel',
    'Ext.container.Container',
]);
//Ext.Ajax.setTimeout(600000);
Ext.application({
    name:'MHVRA',
    launch:function () {
        var me = this;
        var tableName = null;
        var renderDiv = Ext.get('recordsCountDashboard');
        var widthWin = window.innerWidth;
        var heightWin = window.innerHeight;
        var countStore = new Ext.data.Store({
            proxy: {
                type: 'ajax',
                timeout: 2000000000,
                url: '../tables',
                reader: {
                    type:'json',
                }
            },
            fields: ['name', 'remote_count', 'local_count']
        });
        countStore.load();
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
                            layout: 'border',
                            flex:1,
                            margin:'0 0 0 0',
                            items:[
                                {
                                    region:'center',
                                    height:'100%',
                                    layout:'fit',
                                    items:[
                                        {
                                            xtype: 'panel',         
                                            title:'Tables with rows count',
                                            titleAlign:'center',
                                            headerCls: 'extPanel',
                                            id: 'rowsCountPanel',
                                            layout: 'fit',
                                            items:[
                                            {
                                                xtype:'grid',
                                                listeners: {
                                                    select: function(selModel, record, index, options){
                                                        tableName = record.data.name;
                                                    }
                                                },
                                                store:countStore,
                                                columnLines: true,
                                                columns:[
                                                    {xtype:'rownumberer', width:60, text:'Serial'},
                                                    {text: "Table Name",dataIndex: 'name', flex: 1, sortable: true},
                                                    {text: "Remote Count",dataIndex: 'remote_count', flex: 1, sortable: true},
                                                    {text: "Local Count",dataIndex: 'local_count', flex: 1, sortable: true}
                                                ],
                                                tbar: [{
                                                    text: 'Migrate',
                                                    tooltip: 'Migrate data',
                                                    handler:function () {
                                                        if(tableName != null){
                                                            var box = Ext.MessageBox.wait('Please wait...', 'Updating Records');
                                                            var url = '../service?table='+tableName;
                                                            Ext.Ajax.timeout = 900000;
                                                            Ext.Ajax.request({
                                                                url: url,
                                                                timeout:600000,
                                                                method: "GET",
                                                                success: function (response) {
                                                                    box.hide();
                                                                    var respText = response.responseText;
                                                                    alert(respText);
                                                                    // countStore.reload();
                                                                },
                                                                failure: function (res) {
                                                                    box.hide();
                                                                }
                                                            });
                                                        }else {
                                                            alert('Please select a record first.');
                                                        }
                                                    }
                                                }, '-', {
                                                    text: 'Refresh',
                                                    tooltip: 'Refresh Data',
                                                }],
                                            }
                                            ]
                                        }
                                    ]

                                }
                            ]
                        }
                    ]
                }
            ],
            renderTo: renderDiv,
            listeners: {
                resize: function (pnl, width, height, oldWidth, oldHeight, eOpts) {

                }
            }
        });
        Ext.EventManager.onWindowResize(function () {
            var widthWin = window.innerWidth - 15;
            var heightWin = window.innerHeight;
            panel.setHeight(heightWin - 105);
            panel.setWidth(widthWin - 20);
        });
    }
});

