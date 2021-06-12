/**
 * Created by Shakir on 11/27/2018.
 */
var JQXGridToolbarModel = function (toolbarHeight, gridModel, grid_toolbar_el) {
    var me = this;
    me.toolbarHeight = '35px';
    me.toolbarTarget = grid_toolbar_el;//$("#jqxGridToolBar");
    me.toolbarItems = [];
    me.gridModel = gridModel;
    me.viewModel = null;
    me.olMapModel = null;
    me.initialize = function (viewModel, navbarSeq) {
        me.viewModel = viewModel;
        me.olMapModel = me.viewModel.olMapModel;
        me.toolbarTarget.height(me.toolbarHeight);
        // me.setNavbar(olMapModel)
        if (navbarSeq) {
            me.navbarSeq = navbarSeq;
        } else {
            me.navbarSeq = [me.navbar.analysis, me.navbar.zoom]
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
            width: "100%", height: me.toolbarHeight, tools: tools,
            initTools: function (type, index, tool, menuToolIninitialization) {
                me.navbar[me.toolbarItems[index]].create(tool);
            }
        });
        // me.monitorViewChange();
    }
    me.navbar = {
        spacebar: {
            type: "space",
            name: "space",
            create: function (tool) {

            }
        },
        analysis: {
            name: "analysis", //give name name
            type: "button",
            tool: null,
            create: function (tool) {
                this.tool = tool;
                //write of name of icon written in step 2
                var button = $("<div>" + grid_toolbar_icons["analysis"] + "</div>");
                tool.append(button);
                //write the tooltip contents
                tool.jqxTooltip({content: 'Pivot Grid Analysis'});
                tool.on("click", function () {
                    me.gridModel.createAnalysisGridDialog(me.gridModel.gridData);
                });

            }
        },
        zoom: {
            name: "zoom", //give name name
            type: "button",
            tool: null,
            create: function (tool) {
                this.tool = tool;
                //write of name of icon written in step 2
                var button = $("<div>" + grid_toolbar_icons["zoom"] + "</div>");
                tool.append(button);
                //write the tooltip contents
                tool.jqxTooltip({content: 'Zoom to Location'});
                tool.on("click", function () {
                    var selectedrowindex = me.gridModel.gridTarget.jqxGrid('getselectedrowindex');
                    if (selectedrowindex !== -1) {
                        me.viewModel.olMapModel.zoomToSelectedFeatures()
                    } else {
                        alert("Please, select row from table. . ");
                    }

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
                var button = $("<div>" + grid_toolbar_icons["location"] + "</div>");
                tool.append(button);
                //write the tooltip contents
                tool.jqxTooltip({content: 'Mark Site location on Map'});
                tool.on("click", function () {
                    me.olMapModel.drawShape('Point', function (feature) {
                        me.viewModel.siteSelModel.addFeatureInDatabase(feature)
                    });

                });

            }
        },
        deleteLocation: {
            name: "deleteLocation", //give name name
            type: "button",
            tool: null,
            create: function (tool) {
                this.tool = tool;
                //write of name of icon written in step 2
                var button = $("<div>" + grid_toolbar_icons["deleteLocation"] + "</div>");
                tool.append(button);
                //write the tooltip contents
                tool.jqxTooltip({content: 'Delete Selected Location'});
                tool.on("click", function () {
                    var selectedrowindex = me.gridModel.gridTarget.jqxGrid('getselectedrowindex');
                    if (selectedrowindex !== -1) {
                        var rowData = me.gridModel.gridTarget.jqxGrid('getrowdata', selectedrowindex);
                        me.viewModel.siteSelModel.removeFeatureFromSitesLayer(rowData.oid, me.gridModel.gridTarget, selectedrowindex)

                        // me.viewModel.olMapModel.zoomToSelectedFeatures()
                    } else {
                        alert("Please, select row from table. . ");
                    }

                });

            }
        },
        sms: {
            name: "sms", //give name name
            type: "button",
            tool: null,
            create: function (tool) {
                this.tool = tool;
                //write of name of icon written in step 2
                var button = $("<div>" + grid_toolbar_icons["sms"] + "</div>");
                tool.append(button);
                //write the tooltip contents
                tool.jqxTooltip({content: 'Share location vis sms'});
                tool.on("click", function () {
                    var selectedrowindex = me.gridModel.gridTarget.jqxGrid('getselectedrowindex');
                    if (selectedrowindex !== -1) {
                        var rowData = me.gridModel.gridTarget.jqxGrid('getrowdata', selectedrowindex);
                        var vectorSource = me.viewModel.olMapModel.specialLayers["selectedFeatureLayer"].getSource();
                        var feature = vectorSource.getFeatures()[0];
                        if (!feature) {
                            feature = me.viewModel.siteSelModel.getSelectedSiteFeature(rowData.oid)
                        }
                        // var coord = feature.getGeometry().getCoordinates();
                        var extent = feature.getGeometry().getExtent();
                        var coord = ol.extent.getCenter(extent);
                        coord = ol.proj.transform(coord, 'EPSG:3857', 'EPSG:4326');
                        var lon = coord[0];
                        var lat = coord[1];
                        var locUrl = 'https://www.google.com/maps?q=' + lat + ',' + lon;
                        me.viewModel.siteSelModel.sendSMSDialogue(locUrl);
                    } else {
                        alert("Please, select row from table. . ");
                    }
                });

            }
        },
        geoStatistics: {
            name: "geoStatistics", //give name name
            type: "button",
            tool: null,
            create: function (tool) {
                this.tool = tool;
                //write of name of icon written in step 2
                var button = $("<div>" + grid_toolbar_icons["geoStatistics"] + "</div>");
                tool.append(button);
                //write the tooltip contents
                tool.jqxTooltip({content: 'Statistics of marked location'});
                tool.on("click", function () {
                    var selectedrowindex = me.gridModel.gridTarget.jqxGrid('getselectedrowindex');
                    if (selectedrowindex !== -1) {
                        var rowData = me.gridModel.gridTarget.jqxGrid('getrowdata', selectedrowindex);
                        var vectorSource = me.viewModel.olMapModel.specialLayers["selectedFeatureLayer"].getSource();
                        var feature = vectorSource.getFeatures()[0];
                        if (!feature) {
                            feature = me.viewModel.siteSelModel.getSelectedSiteFeature(rowData.oid)
                        }
                        me.viewModel.siteSelModel.showBufferInputDialog(feature);
                    } else {
                        alert("Please, select row from table. . ");
                    }
                });

            }
        },
        geoStatsSummary: {
            name: "geoStatsSummary", //give name name
            type: "button",
            tool: null,
            create: function (tool) {
                this.tool = tool;
                //write of name of icon written in step 2
                var button = $("<div>" + grid_toolbar_icons["geoStatsSummary"] + "</div>");
                tool.append(button);
                //write the tooltip contents
                tool.jqxTooltip({content: 'Statistics summary of all locations'});
                tool.on("click", function () {
                    me.viewModel.siteSelModel.showBufferInputDialog(null);
                });

            }
        },
        saveLocation: {
            name: "saveLocation", //give name name
            type: "button",
            tool: null,
            create: function (tool) {
                this.tool = tool;
                this.tool.attr("id", "id_saveLocation");
                //write of name of icon written in step 2
                // var button = $('<button type="button" class="btn btn-primary">Primary</button>');
                var button = $("<div>" + grid_toolbar_icons["saveLocation"] + "</div>");
                tool.append(button);
                //write the tooltip contents
                tool.jqxTooltip({content: 'Save locations'});
                tool.on("click", function () {
                    var layer = me.olMapModel.specialLayers["siteSelectionFeatureLayer"];
                    var geoJsonStr = me.olMapModel.convertVectorLayerToGeoJSON(layer);
                    var data = {"geojson": geoJsonStr, "approved": 0, "submitted": 1};
                    me.viewModel.siteSelModel.saveLocationGeoJSONToDB(data);
                    // var data = me.gridModel.gridTarget.jqxGrid('getrows');
                    // alert(data.length);

                });

            }
        },
        approve: {
            name: "approve", //give name name
            type: "button",
            tool: null,
            create: function (tool) {
                this.tool = tool;
                this.tool.attr("id", "id_approve");
                //write of name of icon written in step 2
                var button = $("<div>" + grid_toolbar_icons["approve"] + "</div>");
                tool.append(button);
                //write the tooltip contents
                tool.jqxButton({disabled: true});
                tool.jqxTooltip({content: 'Approve location'});
                tool.on("click", function () {
                    var layer = me.olMapModel.specialLayers["siteSelectionFeatureLayer"];
                    var geoJsonStr = me.olMapModel.convertVectorLayerToGeoJSON(layer);
                    var data = {"geojson": geoJsonStr, "approved": 1, "submitted": 1};
                    me.viewModel.siteSelModel.saveLocationGeoJSONToDB(data);
                });

            }
        },
        disApprove: {
            name: "disApprove", //give name name
            type: "button",
            disabled: true,
            tool: null,
            create: function (tool) {
                this.tool = tool;
                this.tool.attr("id", "id_disApprove");
                //write of name of icon written in step 2
                var button = $("<div>" + grid_toolbar_icons["disApprove"] + "</div>");
                tool.append(button);
                tool.jqxButton({disabled: true});
                //write the tooltip contents
                tool.jqxTooltip({content: 'Dis Approve location'});
                tool.on("click", function () {
                    var layer = me.olMapModel.specialLayers["siteSelectionFeatureLayer"];
                    var geoJsonStr = me.olMapModel.convertVectorLayerToGeoJSON(layer);
                    var data = {"geojson": geoJsonStr, "approved": 0, "submitted": 0};
                    me.viewModel.siteSelModel.saveLocationGeoJSONToDB(data);
                });

            }
        },
    };

}