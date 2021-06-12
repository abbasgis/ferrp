/**
 * Created by Dr. Ather Ashraf on 3/2/2018.
 */

/****************************************************
 *
 * @param toolbarHeight in parcentage
 * @constructor
 * usage: me.toolbarModel = new JQXToolbarModel("10%");
 *      navbarSeq = [me.toolbarModel.navbar.addLayer, me.toolbarModel.navbar.fullExtent, me.toolbarModel.navbar.pan, me.toolbarModel.navbar.zoom2Rect, me.toolbarModel.navbar.zoomIn,
 me.toolbarModel.navbar.zoomOut, me.toolbarModel.navbar.zoom2Prev, me.toolbarModel.navbar.zoom2Next]
 *       me.toolbarModel.initialize(viewMode,navbarSeq);
 */
var JQXToolbarModel = function (toolbarHeight, viewInfo, viewModel) {
    var me = this;
    me.toolbarHeight = '35px';
    me.toolbarTarget = $("#jqxToolBar");
    me.toolbarItems = [];
    me.viewInfo = viewInfo;
    me.viewModel = viewModel;
    me.navbar = {
        spacebar: {
            type: "space",
            name: "space",
            create: function (tool) {

            }
        },
        saveMap: {
            name: "saveMap",
            type: "button",
            tool: null,
            create: function (tool) {
                this.tool = tool;
                var button = $("<div>" + icons["saveMap"] + "</div>");
                tool.append(button);
                tool.jqxTooltip({content: 'Save Map'})

                tool.on("click", function () {
                    if (mapInfo.mapName != '') {
                        me.saveMap(mapInfo.mapName);
                    } else {
                        BootstrapDialog.show({
                            message: 'Enter Map Name: <input type="text" class="form-control">',
                            onhide: function (dialogRef) {

                            },
                            buttons: [{
                                label: 'Save',
                                action: function (dialogRef) {
                                    var mapName = dialogRef.getModalBody().find('input').val();
                                    // if ($.trim(mapName.toLowerCase()) == 'banana') {
                                    if (!mapName) {
                                        showAlertDialog('Please enter the name before saving', dialogTypes.info);
                                        return false;
                                    } else {
                                        // var url = '/maps/save_map/?map_params=' + JSON.stringify(map_params);
                                        me.saveMap(mapName);
                                    }
                                }
                            },
                                {
                                    label: 'Close',
                                    action: function (dialogRef) {
                                        dialogRef.close()
                                    }

                                }]
                        });
                    }
                });

            }
        },
        setMapIcon: {},
        setMapPermission: {
            name: "setMapPermission",
            type: "button",
            tool: null,
            create: function (tool) {
                this.tool = tool;
                // me.btnZoom2NextExtent = tool;
                // var button = $("<div>" + "<i class='fa fa-lg fa-arrow-right'></i>" + "</div>");
                var button = $("<div style='width:100%;height: '100%' '>" + icons["setMapPermission"] + "</div>");
                tool.append(button);
                tool.on("click", function () {
                    // me.olMapModel.zoomToSelectedFeatures();
                    // alert(mapInfo.mapName);
                    if (me.viewInfo.mapName == '') {
                        showAlertDialog("Please save map before setting permission", dialogTypes, [])
                    } else {
                        $('#LayerPermissionModal').modal('show');
                    }
                });
                tool.jqxButton({disabled: false});
                tool.jqxTooltip({content: 'Set map permission'})
                // me.toolbarItems['ZoomToNextExtent'] = tool;
            }
        },

        addLayer: {
            name: "addLayer",
            type: "button",
            tool: null,
            create: function (tool) {
                this.tool = tool;

                var button = $("<div>" + icons["addLayer"] + "</div>");
                tool.append(button);
                tool.jqxTooltip({content: 'Add Layer'})

                tool.on("click", function () {
                    var layout = $("#jqxLayout").jqxLayout('layout');
                    var autohidegroup = layout[0].items[2]
                    autohidegroup.widget.jqxRibbon('selectAt', 0);
                });

                //  me.toolbarItems['AddLayer'] = tool;
            }
        },
        fullExtent: {
            name: "fullExtent",
            type: "button",
            tool: null,
            create: function (tool) {
                this.tool = tool;
                var button = $("<div style='width:100%;height: '100%' '>" + icons["fullExtent"] + "</div>");
                tool.append(button);
                tool.jqxTooltip({content: 'Full Extent'});
                tool.on("click", function () {
                    me.olMapModel.setFullExtent();
                });
            }
        },
        pan: {
            name: "pan",
            type: "button",
            tool: null,
            create: function (tool) {
                this.tool = tool;
                var button = $("<div style='width:100%;height: '100%' '>" + icons["pan"] + "</div>");
                tool.append(button);
                tool.on("click", function () {
                    me.olMapModel.removeAllInteraction();
                    me.olMapModel.pan();
                });
                tool.jqxTooltip({content: 'Pan'})
                // me.toolbarItems['Pan'] = tool;
            }
        },
        zoom2Rect: {
            name: "zoom2Rect",
            type: "button",
            tool: null,
            create: function (tool) {
                this.tool = tool;
                // var button = $("<div>" + "<i class='fa fa-lg fa-search'></i>" + "</div>");
                var button = $("<div style='width:100%;height: '100%' '>" + icons["zoom2Rect"] + "</div>");
                tool.append(button);
                tool.on("click", function () {
                    // me.olMapModel.removeAllInteraction();
                    me.olMapModel.zoomToRectangle();
                });
                tool.jqxTooltip({content: 'Zoom To Rectangle'})
                // me.toolbarItems['ZoomToRect'] = tool;
            }
        },
        zoomIn: {
            name: "zoomIn",
            type: "button",
            tool: null,
            create: function (tool) {
                this.tool = tool;
                // var button = $("<div>" + "<i class='fa fa-lg fa-search-plus'></i>" + "</div>");
                var button = $("<div style='width:100%;height: '100%' '>" + icons["zoomIn"] + "</div>");
                tool.append(button);
                tool.on("click", function () {
                    me.olMapModel.addBasicInteraction();
                    me.olMapModel.zoomIn();
                });
                tool.jqxTooltip({content: 'Zoom In'})
                // me.toolbarItems['ZoomIn'] = tool;

            }
        },
        zoomOut: {
            name: "zoomOut",
            type: "button",
            tool: null,
            create: function (tool) {
                this.tool = tool;
                // var button = $("<div>" + "<i class='fa fa-lg fa-search-minus'></i>" + "</div>");
                var button = $("<div style='width:100%;height: '100%' '>" + icons["zoomOut"] + "</div>");
                tool.append(button);
                tool.on("click", function () {
                    me.olMapModel.addBasicInteraction();
                    me.olMapModel.zoomOut();
                });
                tool.jqxTooltip({content: 'Zoom Out'})
                // me.toolbarItems['ZoomOut'] = tool;
            }
        },
        zoom2Prev: {
            name: "zoom2Prev",
            type: "button",
            tool: null,
            create: function (tool) {
                this.tool = tool;
                // var button = $("<div>" + "<i class='fa fa-lg fa-arrow-left'></i>" + "</div>");
                var button = $("<div style='width:100%;height: '100%' '>" + icons["zoom2Prev"] + "</div>");
                tool.append(button);
                tool.on("click", function () {
                    me.olMapModel.zoom2PreviousExtent();
                });
                tool.jqxButton({disabled: false});
                tool.jqxTooltip({content: 'Zoom To Previous Extent'})
                // me.toolbarItems['ZoomToPreviousExtent'] = tool;
            }
        },
        zoom2Next: {
            name: "zoom2Next",
            type: "button",
            tool: null,
            create: function (tool) {
                this.tool = tool;
                // me.btnZoom2NextExtent = tool;
                // var button = $("<div>" + "<i class='fa fa-lg fa-arrow-right'></i>" + "</div>");
                var button = $("<div style='width:100%;height: '100%' '>" + icons["zoom2Next"] + "</div>");
                tool.append(button);
                tool.on("click", function () {
                    me.olMapModel.zoom2NextExtent();
                });
                tool.jqxButton({disabled: false});
                tool.jqxTooltip({content: 'Zoom To Next Extent'})
                // me.toolbarItems['ZoomToNextExtent'] = tool;
            }
        },
        zoom2Selection: {
            name: "zoom2Selection",
            type: "button",
            tool: null,
            create: function (tool) {
                this.tool = tool;
                // me.btnZoom2NextExtent = tool;
                // var button = $("<div>" + "<i class='fa fa-lg fa-arrow-right'></i>" + "</div>");
                var button = $("<div style='width:100%;height: '100%' '>" + icons["zoom2Selection"] + "</div>");
                tool.append(button);
                tool.on("click", function () {
                    me.olMapModel.zoomToSelectedFeatures();
                });
                tool.jqxButton({disabled: false});
                tool.jqxTooltip({content: 'Zoom To selected features'})
                // me.toolbarItems['ZoomToNextExtent'] = tool;
            }
        },
        clearSelection: {
            name: "clearSelection",
            type: "button",
            tool: null,
            create: function (tool) {
                this.tool = tool;
                // var button = $("<div>" + "<i class='fa fa-lg fa-eraser'></i>" + "</div>");
                var button = $("<div style='width:100%;height: '100%' '>" + icons["clearSelection"] + "</div>");
                tool.append(button);
                tool.on("click", function () {
                    me.olMapModel.clearSelection()
                });
                tool.jqxTooltip({content: 'Clear Selection'})
                // me.toolbarItems['AddLayer'] = tool;
            }
        },
        identifier: {
            name: "identifier",
            type: "button",
            tool: null,
            create: function (tool) {
                this.tool = tool;
                // var button = $("<div>" + "<i class='fa fa-lg fa-info-circle'></i>" + "</div>");
                var button = $("<div style='width:100%;height: '100%' '>" + icons["identifier"] + "</div>");
                tool.append(button);
                tool.on("click", function () {
                    me.olMapModel.identifier();
                });
                tool.jqxTooltip({content: 'Identifier'})
                // me.toolbarItems['AddLayer'] = tool;
            }
        },
        query: {
            name: "query", //give name name
            type: "button",
            tool: null,
            create: function (tool) {
                this.tool = tool;
                var button = $("<div>" + icons["query"] + "</div>"); //write of name of icon written in step 2
                tool.append(button);
                tool.jqxTooltip({content: 'Attribute Query'})

                tool.on("click", function () {
                    // write your functionality here
                    var modalbody = $('<div id="divChangeStyleBody"></div>');
                    var layerSelect = me.olMapModel.createLayerNameSelect("layerName");

                    // layerSelect[0].classList.add("form-control");


                    modalbody.append(layerSelect);
                    BootstrapDialog.show({
                        title: "Select Layer For Query",
                        type: BootstrapDialog.TYPE_SUCCESS,
                        // size: BootstrapDialog.SIZE_SMALL,
                        message: modalbody,
                        buttons: [{
                            label: 'Open Query Dialog',
                            action: function (dialogItself) {
                                // dialogItself.close()
                                var layerInfo = {};
                                // layerInfo.csrfToken = me.olMapModel.csrfToken;
                                layerInfo.gridWidth = me.viewModel.getOutputPanelSize().width;
                                if (me.olMapModel.noOfLayers() > 1) {
                                    layerInfo.layerName = $("#layerName").find(":selected").val();
                                } else {
                                    layerInfo.layerName = $("#layerName").val();
                                }
                                if (layerInfo.layerName != "-1") {
                                    layerInfo.title = $("#layerName").find(":selected").text();
                                    var qm = new QueryModel(me.viewModel, 'output');
                                    qm.createQueryDialog(layerInfo, false);
                                } else {
                                    showAlertDialog("Select layer from drop down", dialogTypes.warning);
                                }
                                dialogItself.close()
                            }

                        }, {
                            label: 'Close',
                            action: function (dialogItself) {
                                dialogItself.close()
                            }
                        }]
                    });
                });
            },
        },

        spatialQuery: {
            name: "spatialQuery", //give name name
            type: "button",
            tool: null,
            create: function (tool) {
                this.tool = tool;
                var button = $("<div>" + icons["spatialQuery"] + "</div>"); //write of name of icon written in step 2
                tool.append(button);
                tool.jqxTooltip({content: 'Spatial Query'})

                tool.on("click", function () {
                    // write your functionality here
                    var qm = new QueryModel(me.viewModel, 'output');
                    qm.createSpatialQueryDialog();

                });

            }
        },
        profileExtractor: {
            name: "profileExtractor", //give name name
            type: "button",
            tool: null,
            create: function (tool) {
                this.tool = tool;
                var button = $("<div>" + icons["profileExtractor"] + "</div>"); //write of name of icon written in step 2
                tool.append(button);
                tool.jqxTooltip({content: 'Extract surface profile on drawing a line'})

                tool.on("click", function () {
                    // write your functionality here
                    // alert("working....")
                    // me.olMapModel.removeAllInteraction();
                    me.olMapModel.drawShape('LineString', me.olMapModel.profileExtractor);
                });

            }
        },
        shortestPath: {
            name: "shortestPath", //give name name
            type: "button",
            tool: null,
            create: function (tool) {
                this.tool = tool;
                //write of name of icon written in step 2
                var button = $("<div>" + icons["shortestPath"] + "</div>");
                tool.append(button);
                //write the tooltip contents
                tool.jqxTooltip({content: 'Optimul Route/Path Analysis'})

                tool.on("click", function () {
                    // write your functionality here
                    var networkModel = new NetworkTopologicalModel(me.viewModel);
                    networkModel.openPathInputDialog()
                });

            }
        },
        ThreeD: {
            name: "ThreeD",
            type: "button",
            tool: null,
            create: function (tool) {
                this.tool = tool;
                // var button = $("<div>" + "<i class='fa fa-lg fa-search'></i>" + "</div>");
                var button = $("<div style='width:100%;height: '100%' '>" + icons["ThreeD"] + "</div>");
                tool.append(button);
                tool.on("click", function () {
                    // me.olMapModel.removeAllInteraction();
                    me.olMapModel.set3DEnableDisable()
                });
                tool.jqxTooltip({content: 'Enable / Disable 3D View'})

            }
        },

        geoStatistics: {
            name: "geoStatistics", //give name name
            type: "button",
            tool: null,
            create: function (tool) {
                this.tool = tool;
                //write of name of icon written in step 2
                var button = $("<div>" + icons["geoStatistics"] + "</div>");
                tool.append(button);
                //write the tooltip contents
                tool.jqxTooltip({content: 'Statistics of marked location'})

                tool.on("click", function () {
                    me.viewModel.showStatsPanel();
                    // write your functionality here
                    // alert("working...")
                    me.olMapModel.drawShape("Point", function (feature) {
                        me.viewModel.siteSelModel.showBufferInputDialog(feature);

                    })
                });

            }
        },

        weather: {
            name: "weather", //give name name
            type: "dropdownlist",
            tool: null,
            create: function (tool) {
                this.tool = tool;
                this.tool.jqxDropDownList({
                    width: 100,
                    source: ["Clouds", "Precipitation", "Wind Speed", "Temperature", "Weather Data"],
                    placeHolder: "Weather"
                });
                tool.jqxTooltip({content: 'Add Weather Layer To Map'});
                tool.on("change", function (event) {
                    var args = event.args;
                    if (args) {
                        var label = args.item.label;
                        switch (label) {
                            case "Clouds":
                                me.olMapModel.addTileWeatherMap('Clouds', 'clouds_new');
                                break;
                            case "Precipitation":
                                me.olMapModel.addTileWeatherMap('Precipitation', 'precipitation_new');
                                break;
                            case "Wind Speed":
                                me.olMapModel.addTileWeatherMap('Wind Speed', 'wind_new');
                                break;
                            case "Temperature":
                                me.olMapModel.addTileWeatherMap('Temperature', 'temp_new');
                                break;
                            case "Weather Data":
                                me.olMapModel.getWeatherData(label);
                                break;

                        }

                    }
                });
                //write of name of icon written in step 2
                // var button = $("<div>" + icons["weather"] + "</div>");
                // tool.append(button);
                // //write the tooltip contents
                // tool.jqxTooltip({content: 'Add Weather Layer on Map'})
                // tool.on("click", function () {
                //     // write your functionality here
                //
                // });

            }
        },
        heatmap: {
            name: "heatmap",
            type: "button",
            tool: null,
            create: function (tool) {
                this.tool = tool;
                // var button = $("<div>" + "<i class='fa fa-lg fa-search'></i>" + "</div>");
                var button = $("<div style='width:100%;height: '100%' '>" + icons["heatmap"] + "</div>");
                tool.append(button);
                tool.on("click", function () {
                    me.viewModel.createHeatMapDialogue()
                    // me.viewModel.createHeatMapAnimationDialogue()
                });
                tool.jqxTooltip({content: 'Heat Map'})

            }
        },
        animation: {
            name: "animation",
            type: "button",
            tool: null,
            create: function (tool) {
                this.tool = tool;
                // var button = $("<div>" + "<i class='fa fa-lg fa-search'></i>" + "</div>");
                var button = $("<div style='width:100%;height: '100%' '>" + icons["animation"] + "</div>");
                tool.append(button);
                tool.on("click", function () {
                    // me.viewModel.createHeatMapDialogue()
                    me.viewModel.createHeatMapAnimationDialogue()
                });
                tool.jqxTooltip({content: 'Heat Map'})

            }
        },
        ssa: {
            name: "ssa", //give name name
            type: "button",
            tool: null,
            create: function (tool) {
                this.tool = tool;
                //write of name of icon written in step 2
                var button = $("<div>" + icons["ssa"] + "</div>");
                tool.append(button);
                //write the tooltip contents
                tool.jqxTooltip({content: 'Search New Site'});
                tool.on("click", function () {
                    me.viewModel.siteSelModel.createSearchNewSiteDialogue();
                });

            }
        },
        sms: {
            name: "sms", //give name name
            type: "button",
            tool: null,
            create: function (tool) {
                this.tool = tool;
                // tool.text("Enabled");
                // tool.attr('style', 'color: #fff !important;background: #f0ad4e !important;background-color: #f0ad4e !important;border-color: #eea236 !important;');
                //write of name of icon written in step 2
                var button = $("<div>" + icons["sms"] + "</div>");
                tool.append(button);
                //write the tooltip contents
                tool.jqxTooltip({content: 'Share location vis sms'});
                tool.on("click", function () {
                    me.olMapModel.drawShape('Point', function (feature) {
                        var extent = feature.getGeometry().getExtent();
                        var coord = ol.extent.getCenter(extent);
                        // var coord = feature.getGeometry().getCoordinates();
                        coord = ol.proj.transform(coord, 'EPSG:3857', 'EPSG:4326');
                        var lon = coord[0];
                        var lat = coord[1];
                        var locUrl = 'https://www.google.com/maps?q=' + lat + ',' + lon;
                        me.viewModel.siteSelModel.sendSMSDialogue(locUrl);
                    });
                });

            }
        },
        location: {
            name: "location", //give name name
            type: "button",
            tool: null,
            create: function (tool) {
                this.tool = tool;
                //write of name of icon written in step 2
                var button = $("<div>" + icons["location"] + "</div>");
                tool.append(button);
                //write the tooltip contents
                tool.jqxTooltip({content: 'Mark Site location on Map'});
                tool.on("click", function () {
                    me.olMapModel.drawShape('Point', function (feature) {
                        me.viewModel.siteSelModel.addFeaturesToSiteSelectionLayer([feature], false);
                        if (me.viewModel.project_id) {
                            me.viewModel.siteSelModel.addFeatureInDatabase(feature)
                        }

                    });

                });

            }
        },
        // project_location: {
        //     name: "project_location", //give name name
        //     type: "button",
        //     tool: null,
        //     create: function (tool) {
        //         this.tool = tool;
        //         tool.text("Add Location");
        //         tool.attr('style', 'color: #fff !important;background: #337ab7 !important;background-color: #337ab7 !important;border-color: #2e6da4 !important;');
        //         //write of name of icon written in step 2
        //         // var button = $("<div>" + icons["location"] + "</div>");
        //         // tool.append(button);
        //         //write the tooltip contents
        //         tool.jqxTooltip({content: 'Mark Site location on Map'});
        //         tool.on("click", function () {
        //             me.olMapModel.drawShape('Point', function (feature) {
        //                 me.viewModel.siteSelModel.addFeatureInDatabase(feature)
        //             });
        //
        //         });
        //
        //     }
        // },
        project_location: {
            name: "project_location", //give name name
            type: "dropdownlist",
            tool: null,
            create: function (tool) {
                this.tool = tool;
                this.tool.jqxDropDownList({
                    width: 170,
                    source: ["Mark on Map", "Load KML File", "Search Criteria"],
                    placeHolder: "Add Project Location"
                });
                tool.attr('style', 'color: #fff !important;background: #337ab7 !important;background-color: #337ab7 !important;border-color: #2e6da4 !important;');
                tool.jqxTooltip({content: 'Add Project Location'});
                tool.on("change", function (event) {
                    tool.jqxDropDownList('clearSelection', true);
                    var args = event.args;
                    if (args) {
                        var label = args.item.label;
                        switch (label) {
                            case "Mark on Map":
                                me.olMapModel.drawShape('Point', function (feature) {
                                    me.viewModel.siteSelModel.addFeatureInDatabase(feature)
                                });
                                break;
                            case "Load KML File":
                                me.viewModel.siteSelModel.createOpenFilePopup();
                                break;
                            case "Search Criteria":
                                me.viewModel.siteSelModel.createSearchNewSiteDialogue();
                                break;

                        }

                    }
                });
                //write of name of icon written in step 2
                // var button = $("<div>" + icons["weather"] + "</div>");
                // tool.append(button);
                // //write the tooltip contents
                // tool.jqxTooltip({content: 'Add Weather Layer on Map'})
                // tool.on("click", function () {
                //     // write your functionality here
                //
                // });

            }
        },
        submit_location: {
            name: "submit_location", //give name name
            type: "button",
            tool: null,
            create: function (tool) {
                this.tool = tool;
                this.tool.attr("id", "id_saveLocation_mtb");
                //write of name of icon written in step 2
                tool.text("Submit");
                tool.attr('style', 'color: #fff !important;background: #f0ad4e !important;background-color: #f0ad4e !important;border-color: #eea236 !important;');
                tool.jqxButton({disabled: false});
                //write the tooltip contents
                tool.jqxTooltip({content: 'Submit Project Location for Approval'});
                tool.on("click", function () {
                    var layer = me.olMapModel.specialLayers["siteSelectionFeatureLayer"];
                    var geoJsonStr = me.olMapModel.convertVectorLayerToGeoJSON(layer);
                    var data = {"geojson": geoJsonStr, "approved": 0, "submitted": 1};
                    me.viewModel.siteSelModel.saveLocationGeoJSONToDB(data);
                    me.viewModel.siteSelModel.setButtonsStatus();
                    // window.location.href = "http://pcupiupnd.info/pc1/basic_info/?scheme=" + me.viewModel.project_id
                });

            }
        },
        approve_location: {
            name: "approve_location", //give name name
            type: "button",
            tool: null,
            create: function (tool) {
                this.tool = tool;
                this.tool.attr("id", "id_approve_mtb");
                //write of name of icon written in step 2
                tool.text("Approve");
                tool.attr('style', 'color: #fff !important;background: #398439 !important;background-color: #398439 !important;border-color: #255625 !important;');

                //write the tooltip contents
                tool.jqxButton({disabled: true});
                tool.jqxTooltip({content: 'Approve Project Location'});
                tool.on("click", function () {
                    var layer = me.olMapModel.specialLayers["siteSelectionFeatureLayer"];
                    var geoJsonStr = me.olMapModel.convertVectorLayerToGeoJSON(layer);
                    var data = {"geojson": geoJsonStr, "approved": 1, "submitted": 1};
                    me.viewModel.siteSelModel.saveLocationGeoJSONToDB(data);
                    me.viewModel.siteSelModel.setButtonsStatus();
                    // window.location.href = "http://pcupiupnd.info/pc1/basic_info/?scheme=" + me.viewModel.project_id
                });

            }
        },
        disapprove_location: {
            name: "disapprove_location", //give name name
            type: "button",
            tool: null,
            create: function (tool) {
                this.tool = tool;
                this.tool.attr("id", "id_disApprove_mtb");
                //write of name of icon written in step 2
                tool.text("DisApprove");
                tool.attr('style', 'color: #fff !important;background: #ac2925 !important;background-color: #ac2925 !important;border-color: #761c19 !important;');

                //write the tooltip contents
                tool.jqxTooltip({content: 'Dis-Approve Location'});
                tool.jqxButton({disabled: true});
                tool.on("click", function () {
                    var layer = me.olMapModel.specialLayers["siteSelectionFeatureLayer"];
                    var geoJsonStr = me.olMapModel.convertVectorLayerToGeoJSON(layer);
                    var data = {"geojson": geoJsonStr, "approved": 0, "submitted": 0};
                    me.viewModel.siteSelModel.saveLocationGeoJSONToDB(data);
                    me.viewModel.siteSelModel.setButtonsStatus();
                    // window.location.href = "http://pcupiupnd.info/pc1/basic_info/?scheme=" + me.viewModel.project_id
                });

            }
        },

        land_cover: {
            name: "land_cover", //give name name
            type: "dropdownlist",
            tool: null,
            create: function (tool) {
                this.tool = tool;
                this.tool.jqxDropDownList({
                    width: 80,
                    source: ["AOI", "Navigation"],
                    placeHolder: "Land Cover"
                });
                tool.jqxTooltip({content: 'Extract landcover temporal information'});
                tool.on("change", function (event) {
                    var args = event.args;
                    if (args) {
                        var label = args.item.label;
                        switch (label) {
                            case "AOI":
                                me.olMapModel.drawShape("Polygon", me.getLandCoverStats);
                                break;
                            case "Navigation":
                                me.viewModel.btnLandCoverListener();
                                break;
                        }
                    }
                })
            }
        },
        mhvra_location: {
            name: "mhvra_location", //give name name
            type: "button",
            tool: null,
            create: function (tool) {
                this.tool = tool;
                //write of name of icon written in step 2
                var button = $("<div>" + icons["location"] + "</div>");
                tool.append(button);
                //write the tooltip contents
                tool.jqxTooltip({content: 'Mark location on Map for MHVRA'});
                tool.on("click", function () {
                    me.olMapModel.drawShape('Point', function (feature) {
                        var coord = feature.getGeometry().getCoordinates();
                        coord = ol.proj.transform(coord, 'EPSG:3857', 'EPSG:4326');
                        var lon = coord[0];
                        var lat = coord[1];
                        me.viewModel.showMHVRAStatsOfMarkedLocation(lon, lat)
                    });

                });

            }
        },
    };
    me.saveMap = function (mapName) {
        var url = me.viewInfo.url_save_map + '?item_name=' + me.viewInfo.mapName;
        // var groupLayers = [{'group_name': '', 'layers': me.olMapModel.getLayerNamesWithStyle()}];
        var groupLayers = [];
        var group_layers = me.olMapModel.groupLayers;
        for (var key in group_layers) {
            var group_name = me.olMapModel.groupLayers[key].get('title');
            var layers = me.olMapModel.groupLayers[key].getLayers();
            var obj = {'group_name': group_name, 'layers': me.olMapModel.getLayerNamesInGroupWithStyle(group_name)};
            groupLayers.push(obj);
        }
        groupLayers = JSON.stringify(groupLayers);
        // groupLayers = groupLayers.replace(/\\/g, "");
        var data = new FormData();
        data.append('map_title', mapName);
        data.append('group_layers', groupLayers);
        data.append('extent', me.olMapModel.getCurrentExtent());
        // alert(url);
        var params = {
            url: url, //'/maps/save_map/',
            type: "POST",
            data: data, // JSON.stringify(map_params),
            dataType: "json",
            processData: false,
            contentType: false,
            async: true,
            headers: {'X-CSRFToken': me.viewInfo.csrfToken},
        }
        callAJAX(params, function (res) {
            if (res.status == 200) {
                me.viewInfo.mapName = res.mapName;
                showAlertDialog("Map saved successfully", dialogTypes.success);
            } else {
                showAlertDialog("Failed to save map", dialogTypes.error);
            }
        })
    }
    me.referesh = true;
    me.initialize = function (viewModel, navbarSeq) {

        me.viewModel = viewModel;
        me.olMapModel = me.viewModel.olMapModel;
        me.toolbarTarget.height(me.toolbarHeight);
        // me.setNavbar(olMapModel)
        if (navbarSeq) {
            me.navbarSeq = navbarSeq;
        } else {
            me.navbarSeq = [me.navbar.fullExtent, me.navbar.pan, me.navbar.zoom2Rect, me.navbar.zoomIn, me.navbar.zoomOut,
                me.navbar.zoom2Prev, me.navbar.zoom2Next]
        }
        var tools = "";
        for (var i = 0; i < me.navbarSeq.length; i++) {
            if (me.navbarSeq[i].type == "space") {
                tools += "| "
            } else {
                tools += me.navbarSeq[i].type + " "
                me.toolbarItems.push(me.navbarSeq[i].name);
            }
        }

        me.toolbarTarget.jqxToolBar({
            theme: theme,
            minimizeWidth: 100,
            width: "100%",
            height: me.toolbarHeight,
            tools: tools,
            initTools: function (type, index, tool, menuToolIninitialization) {
                // alert(menuToolIninitialization);
                me.navbar[me.toolbarItems[index]].create(tool);
                // if (index == me.toolbarItems.length - 1 && me.referesh == true) {
                //     // alert(me.toolbarItems[index] + " refereshing toolbar");
                //     me.refereshToolbar();
                // }
                // return { minimizable: true }
            }

        });
        me.refereshToolbar();
        // me.monitorViewChange();
    }
    me.refereshToolbar = function () {
        me.toolbarTarget.jqxToolBar('render');
        // me.referesh = false;
    }
    me.enableDisableExtentButton = function () {
        if (me.olMapModel.getSizeOfNextExtent() > 0) {
            me.toolbarItems['ZoomToNextExtent'].jqxButton({disabled: false});
        } else {
            me.toolbarItems['ZoomToNextExtent'].jqxButton({disabled: true});
        }
        if (me.olMapModel.getSizeOfPreviousExtent() > 0) {
            me.toolbarItems['ZoomToPreviousExtent'].jqxButton({disabled: false});
        } else {
            me.toolbarItems['ZoomToPreviousExtent'].jqxButton({disabled: true});
        }
    }
    me.monitorViewChange = function () {
        me.olMapModel.getView().on('change:resolution', function () {
            me.olMapModel.addToPerviousExtentList()
            // me.enableDisableExtentButton();
        });
        // me.olMapModel.getView().on('change:center', function () {
        //     me.olMapModel.addToPerviousExtentList()
        //     // me.enableDisableExtentButton();
        // });
    }

    me.getLandCoverStats = function (feature) {
        var wkt = me.olMapModel.getGeometryWKT(feature.getGeometry());
        var formData = new FormData();
        formData.append("wkt", wkt)
        var url = "/land_cover/get_land_cover_aoi"
        var params = {
            url: url,
            type: "POST",
            data: formData,
            dataType: "json",
            processData: false,
            contentType: false,
            async: true,
            headers: {'X-CSRFToken': me.viewInfo.csrfToken},
        }
        callAJAX(params, function (grid_data) {
            me.viewModel.appendDataToJqxGrid(grid_data);
        });

    }
}

