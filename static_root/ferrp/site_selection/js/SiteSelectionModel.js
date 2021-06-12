/**
 * Created by Shakir on 11/8/2018.
 */
var SiteSelectionModel = function (mapInfo, viewModel) {
    var me = this;
    var user_ppms = mapInfo.user_ppms;
    me.viewModel = viewModel;
    me.olMapModel = viewModel.olMapModel;
    me.mapInfo = mapInfo;
    // me.layerName ='site_selection_siteselectionselectedsites_20181118102104751163'; //'site_selection_siteselectionselectedsites_20181116014526553693';
    me.layerName = 'site_selection_siteselectionselectedsites';
    me.frmSearchSite = null;
    me.selected_site = null;
    me.frmTemplate = [];
    me.gridModel = null;
    me.options_near_far = [{'label': 'None', 'value': -1}, {'label': 'Near', 'value': 0}, {'label': 'Far', 'value': 1}];
    me.options_min_max = [{'label': 'None', 'value': -1}, {'label': 'Min', 'value': 0}, {'label': 'Max', 'value': 1}];
    me.options_insie_outside = [{'label': 'None', 'value': -1}, {'label': 'Outside', 'value': 0},
        {'label': 'Inside', 'value': 1}];
    me.site_names = [{'label': 'School', 'value': 'school'}, {'label': 'Hospital', 'value': 'hospital'},
        {'label': 'Industry', 'value': 'industry'}];
    me.init = function () {
        me.addSiteSelectionFeatureLayer();
        me.olMapModel.map.addLayer(me.olMapModel.specialLayers["siteSelectionFeatureLayer"]);
        me.getSelectedSitesGeomFromDB();
        // me.gridModel.grid.ready=function () {
        //     me.setButtonsStatus();
        // }
        // me.setButtonsStatus();
        //me.sendSMSDialogue();
        // me.olMapModel.addResultImageWMSLayer('rs_wms_temp', me.mapInfo.url_wms_map, '1541771959_ssma', null)
    };
    me.addSiteSelectionFeatureLayer = function () {
        me.olMapModel.specialLayers["siteSelectionFeatureLayer"] = new ol.layer.Vector({
            title: me.layerName,
            info: true,
            // openInLayerSwitcher: false,
            displayInLayerSwitcher: true,
            source: new ol.source.Vector({
                features: []
            }),
            style: function (feature) {
                return me.olMapModel.getSelectStyle(feature)
            }
        });
        me.olMapModel.specialLayers["siteSelectionFeatureLayer"].setZIndex(995);

    }
    me.addFeaturesToSiteSelectionLayer = function (features, isClear) {
        var layer = me.olMapModel.specialLayers["siteSelectionFeatureLayer"];
        var vectorSource = layer.getSource();
        if (isClear) vectorSource.clear();
        vectorSource.addFeatures(features);
        // layer.setVisible(true);
        layer.changed();
        me.olMapModel.refreshMap();

    }
    me.removeFeatureFromSitesLayer = function (oid, gridTarget, selectedrowindex) {
        var params = {
            url: "/ssa/remove_feature/?oid=" + oid, //'/maps/save_map/',
            type: "GET",
            // data: data, // JSON.stringify(map_params),
            dataType: "json",
            processData: false,
            contentType: false,
            async: true,
            headers: {'X-CSRFToken': me.mapInfo.csrfToken},
        };
        callAJAX(params, function (data) {
            me.getSelectedSitesGeomFromDB();
            me.olMapModel.clearSelection();
            // me.removeSelectedFeature(oid);
            // gridTarget.jqxGrid('deleterow', selectedrowindex);

        })
    };
    me.getSelectedSiteFeature = function (oid) {
        var selectedFeature = null;
        var layer = me.olMapModel.specialLayers["siteSelectionFeatureLayer"];
        var source = layer.getSource();
        var features = source.getFeatures();
        if (features !== null && features.length > 0) {
            for (var x in features) {
                var properties = features[x].getProperties();
                var id = properties.oid;
                if (id === oid) {
                    selectedFeature = features[x];
                    return selectedFeature;
                    // break;
                }
            }
        }
        return selectedFeature;
    }
    me.removeSelectedFeature = function (selectedFeatureID) {
        var layer = me.olMapModel.specialLayers["siteSelectionFeatureLayer"];
        var source = layer.getSource();
        var features = source.getFeatures();
        if (features !== null && features.length > 0) {
            for (var x in features) {
                var properties = features[x].getProperties();
                var id = properties.oid;
                if (id === selectedFeatureID) {
                    source.removeFeature(features[x]);
                    break;
                }
            }
        }
        layer.changed();
        me.olMapModel.refreshMap();
        me.getSelectedSitesGeomFromDB();

    };
    me.createSearchNewSiteDialogue = function () {
        var params = {
            url: "/ssa/get_district_names", //'/maps/save_map/',
            type: "GET",
            // data: data, // JSON.stringify(map_params),
            dataType: "json",
            processData: false,
            contentType: false,
            async: true,
            headers: {'X-CSRFToken': me.mapInfo.csrfToken},
        };
        callAJAX(params, function (data) {
            var d = {'label': 'Please select any district'};
            data.unshift(d);
            var modalbody = $('<div ></div>');
            me.frmSearchSite = $('<div id="frmSearchSite"></div>')
            me.frmTemplate = [
                {
                    bind: 'cmb_district',
                    type: 'option',
                    name: 'cmb_district',
                    label: 'District',
                    required: true,
                    info: 'Enter district name',
                    infoPosition: 'right',
                    labelWidth: '150px',
                    width: '300px',
                    component: 'jqxDropDownList',
                    options: data
                },
                {
                    bind: 'cmb_tehsil',
                    name: 'cmb_tehsil',
                    type: 'option',
                    label: 'Tehsil',
                    required: true,
                    labelWidth: '150px',
                    width: '300px',
                    filterable: true,
                    component: 'jqxDropDownList',
                    options: []
                },
                {
                    bind: 'cmb_site',
                    name: 'cmb_site',
                    type: 'option',
                    label: 'Site',
                    required: true,
                    labelWidth: '150px',
                    width: '300px',
                    filterable: true,
                    component: 'jqxDropDownList',
                    options: me.site_names
                },
                {
                    type: 'label',
                    label: 'Please Select any one condition  from below criteria',
                    rowHeight: '40px',
                },
                {
                    bind: 'cmb_rs_schools_gsd_100',
                    name: 'rs_schools_gsd_100',
                    type: 'option',
                    label: 'School',
                    labelWidth: '150px',
                    width: '300px',
                    filterable: true,
                    component: 'jqxDropDownList',
                    options: me.options_near_far
                },
                {
                    bind: 'cmb_rs_hospital_gsd_100',
                    name: 'rs_hospital_gsd_100',
                    type: 'option',
                    label: 'Hospital',
                    labelWidth: '150px',
                    width: '300px',
                    filterable: true,
                    component: 'jqxDropDownList',
                    options: me.options_near_far
                },
                {
                    bind: 'cmb_rs_population_gsd_100',
                    name: 'rs_population_gsd_100',
                    type: 'option',
                    label: 'Population',
                    labelWidth: '150px',
                    width: '300px',
                    filterable: true,
                    component: 'jqxDropDownList',
                    options: me.options_min_max
                },
                {
                    bind: 'cmb_rs_roads_gsd_100',
                    name: 'rs_roads_gsd_100',
                    type: 'option',
                    label: 'Roads',
                    labelWidth: '150px',
                    width: '300px',
                    filterable: true,
                    component: 'jqxDropDownList',
                    options: me.options_near_far
                },
                {
                    bind: 'cmb_rs_trunk_roads_gsd_100',
                    name: 'rs_trunk_roads_gsd_100',
                    type: 'option',
                    label: 'Trunk Roads',
                    labelWidth: '150px',
                    width: '300px',
                    filterable: true,
                    component: 'jqxDropDownList',
                    options: me.options_near_far
                },
                {
                    bind: 'cmb_rs_railways_gsd_100',
                    name: 'rs_railways_gsd_100',
                    type: 'option',
                    label: 'Railway',
                    labelWidth: '150px',
                    width: '300px',
                    filterable: true,
                    component: 'jqxDropDownList',
                    options: me.options_near_far
                },
                {
                    bind: 'cmb_rs_settlements_gsd_100',
                    name: 'rs_settlements_gsd_100',
                    type: 'option',
                    label: 'Settlements',
                    labelWidth: '150px',
                    width: '300px',
                    filterable: true,
                    component: 'jqxDropDownList',
                    options: me.options_near_far
                },
                {
                    bind: 'cmb_rs_glcf_gsd_100',
                    name: 'rs_glcf_gsd_100',
                    type: 'option',
                    label: 'Vegetation',
                    labelWidth: '150px',
                    width: '300px',
                    filterable: true,
                    component: 'jqxDropDownList',
                    options: me.options_near_far
                },
                {
                    bind: 'cmb_rs_industries_gsd_100',
                    name: 'rs_industries_gsd_100',
                    type: 'option',
                    label: 'Industries',
                    labelWidth: '150px',
                    width: '300px',
                    filterable: true,
                    component: 'jqxDropDownList',
                    options: me.options_near_far
                },
                {
                    bind: 'cmb_rs_minerals_gsd_100',
                    name: 'rs_minerals_gsd_100',
                    type: 'option',
                    label: 'Mines',
                    labelWidth: '150px',
                    width: '300px',
                    filterable: true,
                    component: 'jqxDropDownList',
                    options: me.options_near_far
                },
                {
                    bind: 'cmb_rs_fuels_gsd_100',
                    name: 'rs_fuels_gsd_100',
                    type: 'option',
                    label: 'Fuels',
                    required: true,
                    labelWidth: '150px',
                    width: '300px',
                    filterable: true,
                    component: 'jqxDropDownList',
                    options: me.options_near_far
                },
                {
                    bind: 'cmb_rs_flood_10_gsd_100',
                    name: 'rs_flood_10_gsd_100',
                    type: 'option',
                    label: 'Flood 2010',
                    labelWidth: '150px',
                    width: '300px',
                    filterable: true,
                    component: 'jqxDropDownList',
                    options: me.options_insie_outside
                },
                {
                    bind: 'cmb_rs_flood_14_gsd_100',
                    name: 'rs_flood_14_gsd_100',
                    type: 'option',
                    label: 'Flood 2014',
                    labelWidth: '150px',
                    width: '300px',
                    filterable: true,
                    component: 'jqxDropDownList',
                    options: me.options_insie_outside
                },
            ];
            me.showBootStrapDialog(modalbody);
            modalbody.jqxPanel({width: "100%", height: 350});
            me.frmSearchSite.jqxForm({
                template: me.frmTemplate,
                //    value: sampleValue,
                padding: {left: 30, top: 10, right: 30, bottom: 10}
            });
            modalbody.jqxPanel('append', me.frmSearchSite[0]);
            var cmb_district = me.frmSearchSite.jqxForm('getComponentByName', 'cmb_district');
            var cmb_tehsils = me.frmSearchSite.jqxForm('getComponentByName', 'cmb_tehsil');
            cmb_district.jqxDropDownList({filterable: true});
            cmb_district.on('change', function (event) {
                var args = event.args;
                var val = args.item.value;
                $.get('/ssa/get_tehsil_names?dist_id=' + val, function (response) {
                    var tehsil_names = JSON.parse(response);
                    cmb_tehsils.jqxDropDownList({filterable: true, source: tehsil_names});
                });

            });
        })
    };
    me.showBootStrapDialog = function (bodyContent) {
        var dialog = new BootstrapDialog({
            title: "Search New Site",
            type: BootstrapDialog.TYPE_SUCCESS,
            // size: BootstrapDialog.SIZE_SMALL,
            draggable: true,
            message: bodyContent,
            buttons: [
                {
                    label: 'Calculate',
                    action: function (dialogItself) {
                        var data = me.validateAndGetFormValues();
                        if (data.isValid) {
                            // me.frmSearchSite.jqxForm('submit', "/ssa/ssa_search_site/");
                            me.postSiteSearchForm(data.formData, dialogItself)
                        } else {
                            alert("Please choose any criteria for search");
                        }
                    }
                },

                {
                    label: 'Close',
                    action: function (dialogItself) {
                        dialogItself.close()
                    }
                },

            ]
            // closable: false
        });
        dialog.realize();
        // dialog.getModalHeader().hide();
        // dialog.getModalFooter().hide();
        // dialog.getModalBody().height(50);
        // dialog.getModalBody().css('scroll', 'auto');
        // dialog.getModalBody().css('color', '#fff');
        dialog.open();
    };
    me.validateAndGetFormValues = function () {
        var formData = new FormData();
        var isValid = false;
        for (var i = 0; i < me.frmTemplate.length; i++) {
            var field = me.frmSearchSite.jqxForm('getComponentByName', me.frmTemplate[i].name);
            if (field && me.frmTemplate[i].name) {
                formData.append(me.frmTemplate[i].name, field.val());
                if (me.frmTemplate[i].name.startsWith("rs_") && field.val() !== '-1') {
                    isValid = true;
                }
            }

        }
        return {'isValid': isValid, 'formData': formData};

    };
    me.postSiteSearchForm = function (data, dialogItself) {
        var params = {
            url: "/ssa/ssa_search_site/", //'/maps/save_map/',
            type: "POST",
            data: data,
            dataType: "json",
            processData: false,
            contentType: false,
            async: true,
            headers: {'X-CSRFToken': me.mapInfo.csrfToken},
        };
        callAJAX(params, function (response) {
            var bbox = response.bbox;
            var arrBbox = bbox.split(',');
            // me.olMapModel.zoomToExtent(parseFloat(arrBbox[0]), parseFloat(arrBbox[1]), parseFloat(arrBbox[3]), parseFloat(arrBbox[4]));
            me.olMapModel.addResultImageWMSLayer('rs_wms_temp', me.mapInfo.url_wms_map, response.layer_name, null);
            dialogItself.close()
        })

    };
    me.sendSMSDialogue = function (locUrl) {
        var modalbody = $('<div ></div>');
        var form = $('<form id="frmSendSMS"> <div class="form-group"> <label for="phone_no">Mobile:</label> ' +
            '<input type="number" placeholder="923334445566" class="form-control" id="phone_no" name="phone_no"> </div> <div class="form-group"> ' +
            '<label for="message">Message:</label> <textarea  class="form-control" rows="5" id="message" name="message">' +
            '</textarea> </div> </form>');
        modalbody.append(form);
        me.createMessageDialog(modalbody, locUrl);
    };
    me.createMessageDialog = function (bodyContent, locUrl) {
        var dialog = new BootstrapDialog({
            title: "Send SMS",
            type: BootstrapDialog.TYPE_SUCCESS,
            size: BootstrapDialog.SIZE_SMALL,
            draggable: true,
            message: bodyContent,
            buttons: [
                {
                    label: 'Send',
                    action: function (dialogItself) {
                        var phone_no = $('#phone_no').val();
                        var message = $('#message').val();
                        var formData = new FormData();
                        formData.append('phone_no', phone_no);
                        formData.append('message', message);
                        formData.append('url', locUrl);
                        me.postSendSMSForm(formData, dialogItself);
                    }
                },

                {
                    label: 'Close',
                    action: function (dialogItself) {
                        dialogItself.close()
                    }
                },

            ]
            // closable: false
        });
        dialog.realize();
        dialog.open();
    };
    me.postSendSMSForm = function (data, dialogItself) {
        var params = {
            url: "/ssa/ssa_send_sms/", //'/maps/save_map/',
            type: "POST",
            data: data,
            dataType: "json",
            processData: false,
            contentType: false,
            async: true,
            headers: {'X-CSRFToken': me.mapInfo.csrfToken},
        };
        callAJAX(params, function (response) {
            alert("Message Send Successfully");
            dialogItself.close();
        })

    };
    me.getSelectedSitesGeomFromDB = function () {
        var formData = new FormData();
        formData.append("project_id", me.mapInfo.project_id);
        var url = "/ssa/get_sites_geojson/";
        var params = {
            url: url,
            type: "POST",
            data: formData,
            dataType: "json",
            processData: false,
            contentType: false,
            async: true,
            headers: {'X-CSRFToken': me.mapInfo.csrfToken},
        }
        callAJAX(params, function (data) {
            if (data && data.features && data.features.length > 0) {
                var features = (new ol.format.GeoJSON()).readFeatures(data, {
                    dataProjection: 'EPSG:3857',
                    featureProjection: 'EPSG:3857'
                });
                me.addFeaturesToSiteSelectionLayer(features, true);
                var properties = [];
                for (var i = 0; i < data.features.length; i++) {
                    properties.push(data.features[i].properties)
                }
                me.createGridFromData(properties)
            } else {
                me.olMapModel.clearSelection();
                var layer = me.olMapModel.specialLayers["siteSelectionFeatureLayer"];
                var vectorSource = layer.getSource();
                vectorSource.clear();
                if (me.gridModel) {
                    me.gridModel.gridTarget.jqxGrid('clear');
                }
            }
        });

    };
    me.createGridFromData = function (data) {
        me.viewModel.showOutputPanel(0);
        me.gridModel = new GridModel(viewModel, 'output');
        me.gridModel.clearGrid();
        var fields = me.createFields(data[0]);
        var columns = me.sitesGridColumns();
        var navbarSeq = [];
        if (me.mapInfo.project_id && me.mapInfo.project_id !== '-1') {
            navbarSeq = ['spacebar', 'location', 'deleteLocation', 'sms', 'geoStatistics', 'geoStatsSummary', 'spacebar', 'saveLocation', 'approve', 'disApprove'];

        }
        me.gridModel.createGrid(me.layerName, fields, columns, data, navbarSeq, false);
    };
    me.sitesGridColumns = function () {
        var cols = [];
        cols.push({
            text: 'oid',
            // width: 300,
            dataField: 'oid',
            editable: false,
        });
        cols.push({
            text: 'project_id',
            // width: 300,
            dataField: 'project_id',
            editable: false,
        });
        // cols.push({
        //     text: 'site_name',
        //     // width: 300,
        //     dataField: 'site_name',
        //     editable: false,
        // })
        return cols;
    }
    me.createFields = function (obj) {
        var arrFields = [];
        for (var key in obj) {
            arrFields.push({name: key, type: 'string'});
        }
        return arrFields;
    };
    me.addFeatureInDatabase = function (feature) {
        var wkt = me.olMapModel.convertGeom2WKT(feature.getGeometry());
        // var coord = feature.getGeometry().getCoordinates();
        // coord = ol.proj.transform(coord, 'EPSG:3857', 'EPSG:4326');
        // var lon = coord[0];
        // var lat = coord[1];
        var formData = new FormData();
        // formData.append("long", lon);
        // formData.append("lat", lat);
        formData.append("wkt", wkt);
        formData.append("project_id", me.mapInfo.project_id);
        formData.append("site_name", me.selected_site);
        var url = "/web_services/wfs/add_feature/";
        var params = {
            url: url,
            type: "POST",
            data: formData,
            dataType: "json",
            processData: false,
            contentType: false,
            async: true,
            headers: {'X-CSRFToken': me.mapInfo.csrfToken},
        }
        callAJAX(params, function (data) {
            me.addFeaturesToSiteSelectionLayer([feature], false);
            me.getSelectedSitesGeomFromDB()

        });

    };
    me.setButtonsStatus = function () {
        var formData = new FormData();
        formData.append("project_id", me.mapInfo.project_id);
        formData.append("user_ppms", me.mapInfo.user_ppms);
        var url = "http://pcupiupnd.info/pc1/get_button_permission/";
        var params = {
            url: url,
            type: "POST",
            data: formData,
            dataType: "json",
            processData: false,
            contentType: false,
            async: true,
            // headers: {'X-CSRFToken': me.mapInfo.csrfToken},
        }
        callAJAX(params, function (data) {
            me.enabledDisabledButtons(data.submitted, data.approved, data.can_approve_pc1);
            // var can_approve_pc1 = data.can_approve_pc1;
            // if (data.submitted === 1) {
            //     $("#id_approve").jqxButton({disabled: false});
            //     $("#id_disApprove").jqxButton({disabled: false});
            //     $("#id_saveLocation").jqxButton({disabled: true});
            // }

            // me.gridModel.arr_navbar['approve'].jqxButton({disabled: false});
            // alert(data.submitted);

        });
    }
    me.enabledDisabledButtons = function (submitted, approved, can_approve_pc1) {
        var imgApprove = $("#id_approve");
        var imgDisApprove = $("#id_disApprove");
        var imgSubmit = $("#id_saveLocation");
        var btnApprove = $("#id_approve_mtb");
        var btnDisApprove = $("#id_disApprove_mtb");
        var btnSubmit = $("#id_saveLocation_mtb");
        if (submitted === 0 || can_approve_pc1 === false) {
            imgSubmit.jqxButton({disabled: false});
            imgApprove.jqxButton({disabled: true});
            imgDisApprove.jqxButton({disabled: true});

            btnSubmit.jqxButton({disabled: false});
            btnApprove.jqxButton({disabled: true});
            btnDisApprove.jqxButton({disabled: true});

            imgSubmit.show();
            imgApprove.hide();
            imgDisApprove.hide();

            btnSubmit.show();
            btnApprove.hide();
            btnDisApprove.hide();

        }
        else if (submitted === 1 && can_approve_pc1 === true) {
            imgSubmit.jqxButton({disabled: true});
            imgApprove.jqxButton({disabled: false});
            imgDisApprove.jqxButton({disabled: false});

            btnSubmit.jqxButton({disabled: true});
            btnApprove.jqxButton({disabled: false});
            btnDisApprove.jqxButton({disabled: false});

            imgSubmit.hide();
            imgApprove.show();
            imgDisApprove.show();

            btnSubmit.hide();
            btnApprove.show();
            btnDisApprove.show();

        }

    };
    me.saveLocationGeoJSONToDB = function (location) {
        var formData = new FormData();
        formData.append("project_id", me.mapInfo.project_id);
        formData.append("project_location", JSON.stringify(location))
        var url = "http://pcupiupnd.info/pc1/save_location/";
        var params = {
            url: url,
            type: "POST",
            data: formData,
            dataType: "json",
            processData: false,
            contentType: false,
            async: true,
            // headers: {'X-CSRFToken': me.mapInfo.csrfToken},
        }
        callAJAX(params, function (data) {
            alert(data.message);

        });
    }
    me.createOpenFilePopup = function () {
        var pWindow = document.getElementById("fileWin");
        if (pWindow) {
            $(pWindow).jqxWindow("close");
        }
        var winProp = {
            winId: "fileWin",
            winName: "Load File",
            accordionId: "file_div",
            winWidth: 400,
            winHeight: 250,
            accordions: []
        };
        me.createPopupWindow(winProp, null);
        me.createOpenFileForm('file_div');
    };
    me.createPopupWindow = function (winProp, arrFinalData) {
        var pWindow = document.getElementById(winProp.winId); //$('#'+winProp.winId);
        if (!pWindow) {
            var accordions = winProp.accordions;
            pWindow = $('<div id="' + winProp.winId + '"></div>');
            var header = $(' <div></div>').text(winProp.winName);
            var footer = $(' <footer></footer>');
            var button = '<button id="btnSubmit" class="btn btn-primary">Submit</button>&nbsp;';
            $(button).css("align", "center");
            if (arrFinalData) {
                $(footer).append(button);
            }
            var content = $(' <div > </div>');
            $(content).css("overflow", "hidden");
            var accordionsDiv = $('<div id="' + winProp.accordionId + '" ></div>');
            $(accordionsDiv).attr('class', 'easyui-accordion');
            for (var i = 0; i < accordions.length; i++) {
                var accordDiv = $('<div id="' + accordions[i].accordId + '"></div>');
                $(accordDiv).attr('title', accordions[i].title);
                $(accordionsDiv).append(accordDiv);
            }
            $(content).append(accordionsDiv);
            $(content).append(footer);
            $(pWindow).append(header, content);
        }
        //$("#jqxwindow").jqxWindow({
        $(pWindow).jqxWindow({
            position: {x: 100, y: 100},
            showCollapseButton: true, minHeight: 200, minWidth: 200, height: winProp.winHeight, width: winProp.winWidth,
        });
        $(pWindow).on('close', function (event) {
            $(pWindow).jqxWindow('destroy');
        });
        $(pWindow).jqxWindow('open');
    };
    me.createOpenFileForm = function (divID) {
        var contentDiv = $("#" + divID);
        var panel = $('<div class="easyui-panel" style="width:100%;max-width:400px;padding:30px 60px;">');
        var form = $('<form id="jsonFile" name="jsonFile" enctype="multipart/form-data" method="post" ></form>');
        var browseFile = $('<div class="form-group row"> <label  class="col-2 col-form-label">Load KML File From Local Path. . </label> <div class="col-10"> <input class="form-control" type="file" name="fileinput" id="fileinput"></div> </div>');
        var submitButton = $('<button type="submit" id="btnLoad" class="btn btn-primary">Load KML</button>');
        form.append(browseFile);
        form.append(submitButton);
        panel.append(form);
        $(contentDiv).append(panel);
        $("#btnLoad").click(function (event) {
            event.preventDefault();
            var input, file, fr;

            if (typeof window.FileReader !== 'function') {
                alert("The file API isn't supported on this browser yet.");
                return;
            }
            input = document.getElementById('fileinput');
            if (!input) {
                alert("Um, couldn't find the fileinput element.");
            }
            else if (!input.files) {
                alert("This browser doesn't seem to support the `files` property of file inputs.");
            }
            else if (!input.files[0]) {
                alert("Please select a file before clicking 'Load'");
            }
            else {
                file = input.files[0];
                var file_name = file.name;
                var file_ext = file_name.split(".");
                file_ext = file_ext.slice(-1)[0];
                if (file_ext.toLowerCase() === 'kml') {
                    fr = new FileReader();
                    fr.onload = me.receivedText;
                    fr.readAsText(file);
                } else {
                    alert("File format is not supported, Please upload any KML file not kmz or other format")
                }

            }
            //$("#jqxwindow").jqxWindow('destroy');
            return false;
        });
    };
    me.receivedText = function (e) {
        var lines = e.target.result;
        alert(lines);
        me.createKMLLayerFromKML(lines);
        var pWindow = document.getElementById("fileWin");
        if (pWindow) {
            $(pWindow).jqxWindow("close");
        }
        // var decryptText = window.atob(lines);
        // var jsonData = JSON.parse(decryptText);

    };
    me.createKMLLayerFromKML = function (kmlSourceDoc) {
        var kmlFormat = new ol.format.KML({
            showPointNames: true
        });

        //mapView is defined elsewhere and is the VIEW for my map
        var kmlFeatures = kmlFormat.readFeatures(kmlSourceDoc, {
            dataProjection: 'EPSG:4326',
            featureProjection: 'EPSG:3857'
        });
        for (var i = 0; i < kmlFeatures.length; i++) {
            var feature = kmlFeatures[i];
            me.addFeatureInDatabase(feature);
        }

        // var kmlSource = new ol.source.Vector({
        //     format: kmlFormat,
        //     features: kmlFeatures
        // });
        // var kmlLayer = new ol.layer.Vector({
        //     source: kmlSource
        // });
        // // me.addFeatureInDatabase(feature);
        // me.olMapModel.map.addLayer(kmlLayer);
    };
    me.showBufferInputDialog = function (feature) {
        var modalbody = $('<div ></div>');
        var form = $('<form id="frmBufferStats"> <div class="form-group"> <label for="id_buffer">Buffer (Meters):</label> ' +
            '<input type="number" step="any" value="5000" class="form-control" id="id_buffer" name="buffer"> </div></form>');
        modalbody.append(form);
        var dialog = new BootstrapDialog({
            title: "Stats Buffer",
            type: BootstrapDialog.TYPE_SUCCESS,
            size: BootstrapDialog.SIZE_SMALL,
            draggable: true,
            message: modalbody,
            buttons: [
                {
                    label: 'Calculate',
                    action: function (dialogItself) {
                        var buffer = $("#id_buffer").val();
                        var statsModel = me.olMapModel.getStatsModel();
                        if (feature) {
                            statsModel.getGeoStatistics(feature, buffer);
                        } else {
                            statsModel.getStatsSummaryFromDB(me.mapInfo.project_id, buffer);
                        }
                        dialogItself.close()

                    }
                },

                {
                    label: 'Close',
                    action: function (dialogItself) {
                        dialogItself.close()
                    }
                },

            ]
            // closable: false
        });
        dialog.realize();
        dialog.open();
    };
    me.getStatsSummaryFromDB = function (project_id, buffer) {
        var params = {
            url: "/ssa/remove_feature/?project_id=" + project_id + "&buffer=" + buffer, //'/maps/save_map/',
            type: "GET",
            // data: data, // JSON.stringify(map_params),
            dataType: "json",
            processData: false,
            contentType: false,
            async: true,
            headers: {'X-CSRFToken': me.mapInfo.csrfToken},
        };
        callAJAX(params, function (data) {
            me.getSelectedSitesGeomFromDB();
            me.olMapModel.clearSelection();
            // me.removeSelectedFeature(oid);
            // gridTarget.jqxGrid('deleterow', selectedrowindex);

        })
    };
};