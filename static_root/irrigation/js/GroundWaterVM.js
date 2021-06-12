/**
 * Created by idrees on 12/13/2017.
 */
var legend = document.getElementById('legend');
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
    name: 'IIMS',
    launch: function () {
        var me = this;
        var renderDiv = Ext.get('groundWaterDashboard');
        var widthWin = window.innerWidth;
        var heightWin = window.innerHeight;
        var arzWLMapModel = new ArzWLMapModel();
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
                            titleAlign: 'center',
                            headerCls: 'extPanel',
                            id: 'pnlWLllMap',
                            layout: 'fit',
                            flex: 1,
                            margin: '0 0 0 0',
                        },
                        {
                            layout: 'border',
                            padding: '0 0 0 0',
                            flex: 1.5,
                            items: [
                                {
                                    region: 'center',
                                    height: '60%',
                                    layout: 'fit',
                                    items: [
                                        {
                                            xtype: 'panel',
                                            titleAlign: 'center',
                                            headerCls: 'extPanel',
                                            id: 'pnlWLData',
                                            layout: 'fit',
                                        }
                                    ]
                                },
                                {
                                    region: 'south',
                                    height: '50%',
                                    collapsed: true,
                                    collapsible: true,
                                    resizable: true,
                                    border: true,
                                    title: 'Ground Water Detail',
                                    id: 'southWLPanel',
                                    titleAlign: 'center',
                                    layout: 'fit',
                                    items: [
                                        {
                                            xtype: 'panel',
                                            id: 'pnlWLHistoryData',
                                            layout: 'fit',
                                            items: [
                                                Ext.create('Ext.tab.Panel', {
                                                    tabPosition: 'bottom',
                                                    id: 'tabGroundWater',
                                                    flex: 2,
                                                    activeTab: 0,
                                                    items: [
                                                        {
                                                            title: 'Level Data',
                                                            id: 'tabLevelData',
                                                            name: 'tabLevelData',
                                                            layout: 'fit',
                                                            items: [
                                                                {
                                                                    xtype: 'panel',
                                                                    id: 'pnlLevelData',
                                                                    name: 'pnlLevelData',
                                                                    border: false,
                                                                    layout: 'fit',
                                                                    autoScroll: true,
                                                                }
                                                            ]
                                                        },
                                                        {
                                                            title: 'Quality Data',
                                                            id: 'tabQualityData',
                                                            name: 'tabQualityData',
                                                            layout: 'fit',
                                                            items: [
                                                                {
                                                                    xtype: 'panel',
                                                                    id: 'pnlQualityData',
                                                                    name: 'pnlQualityData',
                                                                    border: false,
                                                                    layout: 'fit',
                                                                    autoScroll: true,
                                                                }
                                                            ]
                                                        },
                                                        // {
                                                        //     title: 'Level Graph',
                                                        //     id: 'tabWaterLevel',
                                                        //     name: 'tabWaterLevel',
                                                        //     layout: 'fit',
                                                        //     // tbar:[
                                                        //     //     {
                                                        //     //         xtype:'button',
                                                        //     //         id:'btnPrevious',
                                                        //     //         icon: imgPath + 'arrow_left.png',
                                                        //     //         tooltip: 'Get previous record graph',
                                                        //     //         handler:function () {
                                                        //     //             arzLeafletWLMapModel.getPreviousRecordGraph();
                                                        //     //
                                                        //     //         }
                                                        //     //     },
                                                        //     //     {
                                                        //     //         xtype:'button',
                                                        //     //         id:'btnNext',
                                                        //     //         icon: imgPath + 'arrow_right.png',
                                                        //     //         tooltip: 'Get next record graph',
                                                        //     //         handler:function () {
                                                        //     //             arzLeafletWLMapModel.getNextRecordGraph();
                                                        //     //         }
                                                        //     //     }
                                                        //     // ],
                                                        //     items: [
                                                        //         {
                                                        //             xtype: 'panel',
                                                        //             id: 'pnlLevelGraph',
                                                        //             name: 'pnlLevelGraph',
                                                        //             border: false,
                                                        //             layout: 'fit',
                                                        //             autoScroll: true,
                                                        //         }
                                                        //     ]
                                                        // },
                                                        // {
                                                        //     title: 'Quality Graph',
                                                        //     layout: 'fit',
                                                        //     id: 'tabWaterQuality',
                                                        //     name: 'tabWaterQuality',
                                                        //     // tbar:[
                                                        //     //     {
                                                        //     //         xtype:'combo',
                                                        //     //         emptyText:'<--Location Id-->',
                                                        //     //         id:'cmbQualityId',
                                                        //     //     }
                                                        //     // ],
                                                        //     items: [
                                                        //         Ext.create('Ext.tab.Panel', {
                                                        //             tabPosition: 'bottom',
                                                        //             id: 'tabWaterQualityDetail',
                                                        //             name: 'tabWaterQualityDetail',
                                                        //             flex: 2,
                                                        //             activeTab: 0,
                                                        //             items: [
                                                        //                 {
                                                        //                     title: 'EC',
                                                        //                     layout: 'fit',
                                                        //                     id: 'tabWaterQualityEC',
                                                        //                     name: 'tabWaterQualityEC',
                                                        //                     items: [
                                                        //                         {
                                                        //                             xtype: 'panel',
                                                        //                             id: 'pnlQualityEC',
                                                        //                             name: 'pnlQualityEC',
                                                        //                             border: false,
                                                        //                             layout: 'fit',
                                                        //                             autoScroll: true,
                                                        //                         }
                                                        //                     ]
                                                        //                 },
                                                        //                 {
                                                        //                     title: 'SAR',
                                                        //                     layout: 'fit',
                                                        //                     id: 'tabWaterQualitySAR',
                                                        //                     name: 'tabWaterQualitySAR',
                                                        //                     items: [
                                                        //                         {
                                                        //                             xtype: 'panel',
                                                        //                             id: 'pnlQualitySAR',
                                                        //                             name: 'pnlQualitySAR',
                                                        //                             border: false,
                                                        //                             layout: 'fit',
                                                        //                             autoScroll: true,
                                                        //                         }
                                                        //                     ]
                                                        //                 }, {
                                                        //                     title: 'RSC',
                                                        //                     layout: 'fit',
                                                        //                     id: 'tabWaterQualityRSC',
                                                        //                     name: 'tabWaterQualityRSC',
                                                        //                     items: [
                                                        //                         {
                                                        //                             xtype: 'panel',
                                                        //                             id: 'pnlQualityRSC',
                                                        //                             name: 'pnlQualityRSC',
                                                        //                             border: false,
                                                        //                             layout: 'fit',
                                                        //                             autoScroll: true,
                                                        //                         }
                                                        //                     ]
                                                        //                 }],
                                                        //             listeners: {}
                                                        //         })
                                                        //     ]
                                                        // }
                                                        ],
                                                    listeners: {
                                                        resize:function (el) {
                                                            // llMap.invalidateSize();
                                                        }
                                                    }
                                                })
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

        arzWLMapModel.getMapAndTable();
        var southPanel = Ext.getCmp("southWLPanel");
        southPanel.expand();

        var groundWaterTab = Ext.getCmp("tabGroundWater");
        groundWaterTab.setActiveTab(3);
        groundWaterTab.setActiveTab(2);
        groundWaterTab.setActiveTab(1);
        groundWaterTab.setActiveTab(0);
        // var waterQualityTab = Ext.getCmp("tabWaterQualityDetail");
        // waterQualityTab.setActiveTab(2);
        // waterQualityTab.setActiveTab(1);
        // waterQualityTab.setActiveTab(0);

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
$("#btnSendEMail").click(function () {
    var dataType = $('#dataType').val();
    var whereClause = $('#whereClause').val();
    var filterArray = $('#filtersArray').val();
    var emailId = $('#txtEmailId').val();
    if (validateEmail(emailId)) {
        var url = '../onlineemailservice';
        var params = {data_type: dataType, where_clause: whereClause, emailid: emailId, filters: filterArray};
        var box = Ext.MessageBox.wait('Please wait...', 'Loading Data');
        Ext.Ajax.timeout = 900000;
        Ext.Ajax.request({
            url: url,
            params: params,//Ext.JSON.encode(params),
            headers: {'X-CSRFToken': csrf_token},
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
    } else {
        alert('Invalid E-Mail address');
    }
});


$("#createLevelSurface").click(function () {
    var levelYear = $('#cmbLevelYears').val();
    var levelType = $('#cmbLevelType').val();
    if (levelYear != '-1') {
        var url = '../level_year_type_data';
        var params = {year: levelYear, type: levelType};
        var box = Ext.MessageBox.wait('Please wait...', 'Loading Data');
        Ext.Ajax.timeout = 900000;
        Ext.Ajax.request({
            url: url,
            params: params,//Ext.JSON.encode(params),
            headers: {'X-CSRFToken': csrf_token},
            method: "POST",
            success: function (response) {
                box.hide();
                $('#levelSurfaceModal').modal('hide');
                var respText = response.responseText;
                var respnseText = eval('(' + JXG.decompress(respText) + ')');
                if (respnseText != "false") {
                    var dataArray = getLevelYearTypeArray(respnseText);
                    // heatLayer.clearLayers();
                    heatLayer.setLatLngs(dataArray);
                }
            },
            failure: function (res) {
                box.hide();
                $('#levelSurfaceModal').modal('hide');
                alert(res.responseText);
            }
        });
    } else {
        alert('Invalid E-Mail address');
    }
});
function getLevelYearTypeArray(data) {
    var dataArray = [];
    for (var i = 0; i < data.length; i++) {
        var record = data[i];
        var elevation = record['elevation'];
        var geomText = record['geom_text'];
        var heatRecord = [geomText.split(',')[1], geomText.split(',')[0], elevation]
        dataArray.push(heatRecord);
    }
    return dataArray;
}
function insertYears() {
    for (var i = 2003; i <= 2015; i++) {
        $("#cmbLevelYears").append($('<option>', {value: i}).text(i));
    }
}
insertYears();

function isNumberKey(evt) {
    var charCode = (evt.which) ? evt.which : evt.keyCode;
    if (charCode != 46 && charCode > 31
        && (charCode < 48 || charCode > 57))
        return false;
    return true;
}
function validateContactNo(contactNo) {
    var n = contactNo.length;
    if (n == 12) {
        return true;
    } else {
        return false;
    }
}
function countContactNo(contactNo) {
    return contactNo.length;
}
$("#btnSendSMS").click(function () {
    var dataType = $('#dataType').val();
    var whereClause = $('#whereClause').val();
    var filterArray = $('#filtersArray').val();
    var contactNo = $('#txtContactNo').val();
    if (validateContactNo(contactNo)) {
        var url = '../onlinesmsservice';
        var params = {data_type: dataType, where_clause: whereClause, contact_no: contactNo, filters: filterArray};
        var box = Ext.MessageBox.wait('Please wait...', 'Loading Data');
        Ext.Ajax.timeout = 900000;
        Ext.Ajax.request({
            url: url,
            params: params,//Ext.JSON.encode(params),
            headers: {'X-CSRFToken': csrf_token},
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
    } else {
        alert('Invalid contact no. 12 required ' + countContactNo(contactNo) + ' entered.');
    }
});
