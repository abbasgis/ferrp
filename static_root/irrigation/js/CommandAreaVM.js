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
        var renderDiv = Ext.get('commandedAreaDashboard');
        var widthWin = window.innerWidth;
        var heightWin = window.innerHeight;
        var arzMapModel = new ArzMapModel();
        var panel = Ext.create('Ext.panel.Panel', {
            height: heightWin - 255,
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
                            // title: 'Administrative Map',
                            xtype: 'panel',
                            titleAlign:'center',
                            headerCls: 'extPanel',
                            id: 'HMapCA',
                            layout: 'fit',
                            flex:1,
                            padding:'0 10 0 0',
                            dockedItems:arzMapModel.mapPanelHeaderToolbar()
                        },
                        {
                            // title: 'Administrative Data',
                            xtype: 'panel',
                            titleAlign:'center',
                            headerCls: 'extPanel',
                            id: 'pnlCAData',
                            layout: 'fit',
                            flex:1.7,
                            items:[
                                {
                                    xtype: 'panel',
                                    flex: 2,
                                    bodyStyle: {
                                        backgroundColor: 'transparent'
                                    },
                                    border: false,
                                    width:widthWin - 15,
                                    layout: {
                                        type: 'vbox',
                                        align: 'stretch'
                                    },
                                    items: [
                                        {
                                            xtype: 'panel',
                                            headerCls: 'extPanel',
                                            padding: '0 0 0 0',
                                            layout: 'fit',
                                            border: true,
                                            titleAlign:'center',
                                            bodyStyle: {
                                                backgroundColor: 'transparent'
                                            },
                                            id: 'dataTableCA',
                                            flex: 2
                                        },
                                        Ext.create('Ext.tab.Panel', {
                                            tabPosition: 'bottom',
                                            id: 'tabChartsPanel',
                                            flex: 2,
                                            activeTab: 0,
                                            items: [
                                            {
                                                title: 'Commanded Area',
                                                layout: 'fit',
                                                items:[
                                                {
                                                    xtype: 'panel',
                                                    id: 'dataChartPanel',
                                                    bodyStyle: {
                                                        backgroundColor: 'transparent'
                                                    },
                                                    layout: 'fit'
                                                }]
                                            },
                                            {
                                                title: 'Canals',
                                                layout: 'fit',
                                                items:[
                                                    {
                                                        xtype: 'panel',
                                                        id: 'canalsChartPanel',
                                                        bodyStyle: {
                                                            backgroundColor: 'transparent'
                                                        },
                                                        layout: 'fit'
                                                    }
                                                ]
                                            },{
                                                title: 'Outlets',
                                                layout: 'fit',
                                                items:[
                                                    {
                                                        xtype: 'panel',
                                                        id: 'outletsChartPanel',
                                                        bodyStyle: {
                                                            backgroundColor: 'transparent'
                                                        },
                                                        layout: 'fit'
                                                    }
                                                ]
                                            },{
                                                title: 'Districts',
                                                layout: 'fit',
                                                tabConfig: {
                                                    listeners: {
                                                        click: function() {
                                                            var districtDataPanel = Ext.getCmp('distDataPanel');
                                                            if(!districtDataPanel){
                                                                Ext.MessageBox.show({
                                                                    title: 'Information',
                                                                    msg: 'Please select a row from above grid and press districts button.',
                                                                    buttons: Ext.MessageBox.OK,
                                                                    icon: 'ext-alert-custom-ico'
                                                                });
                                                            }
                                                        }
                                                    }
                                                },
                                                items:[
                                                    {
                                                        xtype: 'panel',
                                                        id: 'pnlDistrictsInformation',
                                                        bodyStyle: {
                                                            backgroundColor: 'transparent'
                                                        },
                                                        layout: 'fit'
                                                    }
                                                ]
                                            }],
                                            listeners:{

                                            }
                                        })
                                    ]
                                }
                            ]
                        },
                    ]
                },
                // {
                //     region: 'south',
                //     height: 30,
                //     border:true,
                //     margin:'5 10 2 0',
                //     layout:'fit',
                //     // items:arzMapModel.getStatusBarItems()
                // }
            ],
            renderTo: renderDiv,
            listeners: {
                resize: function (pnl, width, height, oldWidth, oldHeight, eOpts) {

                }
            }
        });

        arzMapModel.getMap();
        
        var chartsTab = Ext.getCmp("tabChartsPanel");
        chartsTab.setActiveTab(3);
        chartsTab.setActiveTab(2);
        chartsTab.setActiveTab(1);
        chartsTab.setActiveTab(0);
        
        Ext.EventManager.onWindowResize(function () {
            var widthWin = window.innerWidth - 15;
            var heightWin = window.innerHeight;
            panel.setHeight(heightWin - 255);
            panel.setWidth(widthWin - 20);
        });
    }
});



function validateEmail(email) {
  var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(email);
}
$( "#btnSendEMail" ).click(function() {
    var dataType = $('#dataType').val();
    var whereClause = $('#whereClause').val();
    var filterArray = $('#filtersArray').val();
    var emailId = $('#txtEmailId').val();
    if(validateEmail(emailId)){
        var url = 'onlineemailservice';
        var params = {data_type:dataType, where_clause:whereClause, emailid:emailId, filters:filterArray};
        var box = Ext.MessageBox.wait('Please wait...', 'Loading Data');
        Ext.Ajax.timeout = 900000;
        Ext.Ajax.request({
            url: url,
            params:params,//Ext.JSON.encode(params),
            headers:{'X-CSRFToken':csrf_token},
            method: "POST",
            success: function (response) {
                box.hide();
                alert(response.responseText);
                $('#eMailModal').modal('hide');
            },
            failure: function (res) {
                box.hide();
                alert(res.responseText);
            }
        });
    }else{
        alert('Invalid E-Mail address');
    }
});

function isNumberKey(evt) {
    var charCode = (evt.which) ? evt.which : evt.keyCode;
    if (charCode != 46 && charCode > 31
    && (charCode < 48 || charCode > 57))
    return false;
    return true;
}
function validateContactNo(contactNo) {
    var n = contactNo.length;
    if(n == 12){
        return true;
    }else {
        return false;
    }
}
function countContactNo(contactNo) {
    return contactNo.length;
}
$( "#btnSendSMS" ).click(function() {
    var dataType = $('#dataType').val();
    var whereClause = $('#whereClause').val();
    var filterArray = $('#filtersArray').val();
    var contactNo = $('#txtContactNo').val();
    if(validateContactNo(contactNo)){
        var url = 'onlinesmsservice';
        var params = {data_type:dataType, where_clause:whereClause, contact_no:contactNo, filters:filterArray};
        var box = Ext.MessageBox.wait('Please wait...', 'Loading Data');
        Ext.Ajax.timeout = 900000;
        Ext.Ajax.request({
            url: url,
            params:params,//Ext.JSON.encode(params),
            headers:{'X-CSRFToken':csrf_token},
            method: "POST",
            success: function (response) {
                box.hide();
                alert(response.responseText);
                $('#smsModal').modal('hide');
            },
            failure: function (res) {
                box.hide();
                alert(res.responseText);
            }
        });
    }else{
        alert('Invalid contact no. 12 required ' + countContactNo(contactNo) + ' entered.' );
    }
});
