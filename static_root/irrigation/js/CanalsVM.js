/**
 * Created by idrees on 12/13/2017.
 */
var legend = document.getElementById('legend');
Ext.Loader.setConfig({enabled: true});
Ext.Loader.setPath('Ext.ux', '/static/Extjs-6.2.0/packages/ux/classic/src');
Ext.Loader.setPath('ArzCanals', 'irrigation/js/Arz/CanalModels');

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
        var renderDiv = Ext.get('canalsDashboard');
        var widthWin = window.innerWidth;
        var heightWin = window.innerHeight;
        var arzCanalsMapModel = new ArzCanalsMapModel();

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
                                    height:'60%',
                                    layout:'fit',
                                    items:[
                                        {
                                            xtype: 'panel',
                                            headerCls: 'extPanel',
                                            id: 'canalsLLMapPanel',
                                            layout: 'fit',
                                        }
                                    ]

                                },
                                {
                                    region: 'south',
                                    height: '40%',
                                    collapsed:true,
                                    collapsible:true,
                                    // resizable:true,
                                    id:'southCanalXSProfilePanel',
                                    border:true,
                                    title:'Height profile',
                                    titleAlign:'center',
                                    layout: 'fit',

                                    items:[
                                        {

                                            xtype: 'panel',
                                            id: 'pnlXSProfile',
                                            layout: 'fit',
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            layout: 'border',
                            padding:'0 0 0 0',
                            flex:1.4,
                            items:[
                                {
                                    region:'center',
                                    height:'60%',
                                    layout:'fit',
                                    items:[
                                        {
                                            xtype: 'panel',
                                            titleAlign:'center',
                                            headerCls: 'extPanel',
                                            id: 'pnlCanalsData',
                                            layout: 'fit',
                                        }
                                    ]

                                },
                                {
                                    region: 'south',
                                    height: '40%',
                                    collapsed:true,
                                    collapsible:true,
                                    resizable:true,
                                    id:'southCanalDetailPanel',
                                    border:true,
                                    title:'Canal Properties Information',
                                    titleAlign:'center',
                                    layout: 'fit',
                                    items:[
                                        {
                                            xtype: 'panel',
                                            id: 'pnlLSectionData',
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
            listeners: {
                resize: function (pnl, width, height, oldWidth, oldHeight, eOpts) {

                }
            }
        });
        arzCanalsMapModel.getMapAndTable();
        
        Ext.EventManager.onWindowResize(function () {
            var widthWin = window.innerWidth - 15;
            var heightWin = window.innerHeight;
            panel.setHeight(heightWin - 105);
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
        var url = '../onlineemailservice';
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
        var url = '../onlinesmsservice';
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
