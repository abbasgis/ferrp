/**
 * Created by Dr. Ather Ashraf on 4/29/2018.
 */

var LayerStyleViewModel = function (olMapModel, layerInfo) {
    var me = this;
    me.olMapModel = olMapModel;
    me.panelIds = ["uploadSLD", "assignColor", "graducatedColor", "rasterSymbology"];
    me.expandedPanelId = "";
    me.layerInfo = layerInfo;
    me.columnName = "-1";
    me.columnValue = "-1";
    me.styleModel = null;
    // me.layerType = null;
    me.colorRamps = [{name: "red-yellow-green", color: ['#ff0000', '#ffff00', '#008000']},
        {name: "blue shades", color: ["#D7FCFF", "#0627FF"]},
        {name: "green shades", color: ["#EBFFD9", "#0B6D18"]},
        {name: "red shades", color: ['#FFF0F6', "#70001E"]},
        {name: "white-black", color: ['#ffffff', '#000000']},
        {name: "green-red", color: ["#009B00", "#9B0000"]}]

    me.setLayerInfo = function (info) {
        me.layerInfo = info;
    }
    me.initialize = function () {
        var layerType = me.layerInfo.layerType;
        var vector_style_div = $('#vector_style');
        var raster_style_div = $('#raster_style');
        var gradutae_color = $('#vector_style_gdc');
        if (layerType === 'Vector') {
            raster_style_div.css('display', 'none');
            vector_style_div.css('display', 'block');
            gradutae_color.css('display', 'block');

        } else {
            raster_style_div.css('display', 'block');
            vector_style_div.css('display', 'none');
            gradutae_color.css('display', 'none');
        }
        var styleType = me.layerInfo.geomType;
        if (styleType == "None") styleType = "Raster";
        me.styleModel = new StyleModel(styleType);
        $('#lblGeomType').text(styleType);
        for (var i = 0; i < me.panelIds.length; i++) {
            me.styleModel.removeAllRows(me.panelIds[i]);

        }
        me.setColorRamp();
        if (styleType != "Raster") {
            var url = "/get_attribute_list/?layername=" + me.layerInfo.layerName;

            callAJAX({url: url, dataType: "json"}, function (data) {
                // var columns = data.columns;
                var columnNameOptions = '<option value="-1">Select Column Name</option>';
                for (var i = 0; i < data.length; i++) {
                    columnNameOptions += "<option value='" + data[i]['column_name'] + "'>" + data[i]['column_name'] + "</option>";
                }
                $("select.selectColumnName").html(columnNameOptions).selectpicker('refresh');
            });
            me.selIndex = 0;
            me.setExpandedPanelId = function (id) {
                me.expandedPanelId = id;
                // alert(me.expandedPanelId);
            }
            for (var i = 0; i < me.panelIds.length; i++) {
                $('#' + me.panelIds[i]).on('show.bs.collapse', function () {
                    me.setExpandedPanelId($(this).attr("id"));
                });
            }
        } else {
            var rasClasses = [3, 5, 7]
            var classesOptions = ""
            for (var i = 0; i < rasClasses.length; i++) {
                classesOptions += "<option value='" + rasClasses[i] + "'>" + rasClasses[i] + "</option>";
            }
            $('#rasterClasses').html(classesOptions).selectpicker('refresh');
        }
    }

    me.setColorRamp = function () {

        for (var i = 0; i < me.colorRamps.length; i++) {
            var colorRamp = me.colorRamps[i];
            var option = $('<option value="' + i + '">' + colorRamp.name + '</option>');
            $("select.selectColorRamp").append(option)
        }
        $("select.selectColorRamp").selectpicker('refresh');
    }

    $("select.selectColumnName").on('change', function (sel) {
        me.styleModel.removeAllRows(me.expandedPanelId);
        selColNameItems = $("select.selectColumnName")
        for (var i = 0; i < selColNameItems.length; i++) {
            me.columnName = (selColNameItems[i].value == null ? -1 : selColNameItems[i].value);
            if (me.columnName != -1) {
                me.selIndex = i;
                break;
            }
        }
        // alert(columnName)
        if (me.expandedPanelId == "assignColor") {
            var url = "/get_attribute_distinct_value/?layer_name=" + me.layerInfo.layerName + "&column_name=" + me.columnName;
            callAJAX({url: url, dataType: "json"}, function (data) {
                // var columns = data.columns;
                var columnValueOptions = '<option value="-1">Select Column Value</option>';
                for (var i = 0; i < data.length; i++) {
                    columnValueOptions += "<option value='" + data[i][0] + "'>" + data[i][0] + "</option>";
                }
                $("select.selectColumnValue")[me.selIndex].innerHTML = columnValueOptions;
                $("select.selectColumnValue").selectpicker('refresh');
            });
        }
    })

    $("select.selectColumnValue").on('change', function (sel) {
        if (me.expandedPanelId == "assignColor") {
            selValueItems = $("select.selectColumnValue");
            // for (var i=0;i<selValueItems.length;i++)
            me.columnValue = (selValueItems[me.selIndex].value == null ? -1 : selValueItems[me.selIndex].value);
            // alert(columnValue);
        }
    })

    $("#btnAddStyle").on('click', function () {
        // alert(me.columnValue);
        if (me.columnValue != "-1") {
            var tbody = $("#styletbody");
            var style = me.styleModel.getStyle();
            me.styleModel.addStyleRow(me.columnValue, tbody, me.styleModel.rowIndex++, style);
        }
    })

    $('#btnUploadSLD').on('click', function () {
        // var url = "{% url "upload_sld" %}?layer_name=" + layerInfo.layerName
        // alert(url);
        formdata = new FormData();
        formdata.append('file', $('#file')[0].files[0]);
        params = {
            headers: {'X-CSRFToken': '{{ csrf_token }}'},
            type: "POST",
            url: url,
            data: formdata,
            dataType: "json",
            processData: false,
            contentType: false,
            async: false,
        }
        callAJAX(params, function (data) {
            me.olMapModel.refreshLayer(layerName);
            showAlertDialog("New style has been applied to the layer", dialogTypes.success)
        });
    })

    $("#btnSetLayerStyle").on('click', function () {
        if (me.layerInfo.layerType == "Vector") {
            var rules = me.styleModel.getStyleJSON(me.columnName, me.columnValue, me.expandedPanelId)
        } else {
            var rules = me.styleModel.getRasterStyleJSON($('#rasRamptbody'), me.expandedPanelId);
        }

        if (rules != null) {
            var scale = me.styleModel.getLayerScaleJSON();
            var data = {"rules": rules, 'scale': scale};
            if (me.layerInfo.isTempStyle == false) {
                data = JSON.stringify(data);
                var formdata = new FormData();
                formdata.append('data', data);
                formdata.append('layer_name', me.layerInfo.layerName)
                var params = {
                    headers: {'X-CSRFToken': me.layerInfo.csrfToken},
                    type: "POST",
                    url: '/web_services/set_layer_style/',
                    data: formdata,
                    dataType: "json",
                    processData: false,
                    contentType: false,
                    // async: true,
                };
                callAJAX(params, function (data) {
                    $('#LayerStylingModal').modal('hide');
                    me.olMapModel.refreshLayer(me.layerInfo.layerName)

                    // $('#LayerStylingModal').modal('hide');
                });
            } else {
                me.olMapModel.addTempStyleToWMSLayer(me.layerInfo.layerName, data);
                $('#LayerStylingModal').modal('hide');
            }
        } else {
            showAlert("Set styles before applying it.", dialogTypes.warning);
        }

    });

    $('#btnRemoveStyle').on('click', function () {
        if (me.styleModel.selectedRow != null) {
            $(me.styleModel.selectedRow).remove();
        } else {
            showAlertDialog("Please select a row to delete", dialogTypes.error);
        }
    });

    $("select.selectColorRamp").on('change', function () {
        me.styleModel.removeAllRows(me.expandedPanelId);
        var linearGradient = "linear-gradient(to right, {0} )"; //#33ccff 0%, #ff99cc 100%
        var rampIndex = ($("select.selectColorRamp").val() == null ? -1 : $("select.selectColorRamp").val());
        if (rampIndex != "-1") {
            var colorRamp = me.colorRamps[rampIndex];
            arrColor = colorRamp.color;
            var strColorGradient = "";
            for (var i = 0; i < arrColor.length; i++) {
                var colorVal = arrColor[i];
                var percentVal = (i / (arrColor.length - 1)) * 100
                strColorGradient += colorVal + " " + percentVal + "%,";
            }
            strColorGradient = strColorGradient.substring(0, strColorGradient.length - 1)
            linearGradient = linearGradient.replace("{0}", strColorGradient);
            $('#colorRamp').css({"background": linearGradient});


        }

    })

    $("#btnApplyColorRamp").on('click', function () {

        var rampIndex = ($("select.selectColorRamp").val() == null ? -1 : $("select.selectColorRamp").val());
        if (me.columnName != "-1" && rampIndex != "-1") {
            var url = "/get_attribute_distinct_value/?layer_name=" + me.layerInfo.layerName + "&column_name=" + me.columnName;
            var data = callSJAX({url: url});
            data = JSON.parse(data);
            var columnValues = [];
            var isNumber = true;
            for (var i = 0; i < data.length; i++) {
                if (isNumber) {
                    isNumber = validation.isNumber(data[i][0]);
                }
                columnValues.push(data[i][0]);
            }

            var colors = [];
            var colorRamp = me.colorRamps[rampIndex];
            for (var i = 0; i < colorRamp.color.length; i++) {
                colors.push(colorRamp.color[i]);
            }
            me.styleModel.applyColorRamp(me.columnName, isNumber, columnValues, colors);

        } else {
            showAlertDialog("Please select column name and/or color ramp for processing", dialogTypes.error);
        }
    });

    $('#btnApplyRasterColorRamp').on('click', function () {
        var rampIndex = ($("select.selectColorRamp").val() == null ? -1 : $("select.selectColorRamp").val());
        var noOfClass = $('#rasterClasses').val();
        if (rampIndex != "-1" && noOfClass) {
            var url = "/get_raster_summary/?layer_name=" + me.layerInfo.layerName;
            callAJAX({url: url, dataType: "json"}, function (data) {
                // alert(data)
                var colors = [];
                var colorRamp = me.colorRamps[rampIndex];
                for (var i = 0; i < colorRamp.color.length; i++) {
                    colors.push(colorRamp.color[i]);
                }
                me.styleModel.applyRasterColorRamp(colors, data[0], noOfClass);
            });

        } else {
            showAlertDialog("Select all parameters...", dialogTypes.error);
        }
    })
}

var StyleModel = function (geomType) {
    var me = this;
    me.rowIndex = 1;
    me.selectedRow = null;
    me.op = "=";
    me.geomType = geomType.toLowerCase();
    me.getValueFilter = function () {
        var url = "/web_services/wfs/query_layer/get_filter/" + "?layer_name=" + me.layerName
        // alert("url:"+url);
        var params = {
            url: url,
            type: "GET",
            // data: data,
            dataType: "json",
            processData: false,
            contentType: false,
            async: false
            // headers: {'X-CSRFToken': token},
        }
        var data = callSJAX(params);
        data = JSON.parse(data)
    }

    me.removeAllRows = function (pnlId) {
        var tbody = null;
        if (pnlId == "assignColor") {
            tbody = $("#styletbody tr").remove();
            me.rowIndex = 1;
            // if (me.styleModel.rowIndex == 1)
            var style = me.getStyle();
            me.addStyleRow('default', $("#styletbody"), me.rowIndex++, style);

        } else if (pnlId == "graducatedColor") {
            $("#ramptbody tr").remove();
        } else if (pnlId == "rasterSymbology") {
            $("#rasRamptbody tr").remove();
        }

    }

    me.addStyleRow = function (value, tbody, rowIndex, style) {
        // style = me.setStyleMissingParams(style)

        var tr = $('<tr id="' + rowIndex + '" class="clickable-row"></tr>');
        // value = "default"; //$("select#viewAttributes").text()
        var svg = $('<svg width="150" height="40"></svg>');
        if (me.geomType.indexOf("polygon") != -1) {
            svg.html('<rect width="150" height="40"style="stroke-width:' + style.strokeWidth + ';stroke:' + style.stroke + ';fill:' +
                style.fillColor + ';fill-opacity:' + style.fillOpacity + '" />');
        } else if (me.geomType.indexOf("linestring") != -1) {
            svg.html('<line x1="0" y1="20" x2="150" y2="20" style="stroke-width:' + style.strokeWidth + ';stroke:' + style.stroke + '" />')
        }
        else if (me.geomType.indexOf("point") != "-1") {
            var shape = '<circle cx="75" cy="10" r="' + style.pointSize + '" stroke="' + style.stroke + '" stroke-width="' + style.strokeWidth + '" fill="' + style.fillColor + '" />'
            svg.html(shape);
        } else {
            svg.html('<rect width="150" height="40"style="stroke-width:' + style.strokeWidth + ';stroke:' + style.stroke + ';fill:' +
                style.fillColor + ';fill-opacity:' + style.fillOpacity + '" />');
        }
        svg.click(function () {
            // callingElem = this;
            // $('#setStyleModal').modal('show');
            me.changeStyle(this);
        })
        var tdValue = $("<td>" + value + "</td>");
        var tdStyle = $("<td></td>");
        tdStyle.append(svg);
        tr.append(tdValue);
        tr.append(tdStyle);
        tbody.append(tr)

        tr.click(function () {
            me.selectedRowIndex = $(this).attr('id');
            me.selectedRow = this;
            if ($(this).hasClass("highlight") || me.selectedRowIndex == 1) {
                $(this).removeClass('highlight');
                me.selectedRow = null;
            } else {
                $(this).addClass('highlight').siblings().removeClass('highlight');
            }
            // alert(me.selectedRowIndex);
        })


    }

    me.changeStyle = function (svg) {
        var modalbody = $('<div id="divChangeStyleBody"></div>');
        if (me.geomType.indexOf("linestring") != "-1") {
            var strokeFieldset = me.getStrokeFieldset(svg.children[0].style.stroke, svg.children[0].style.strokeWidth);
            modalbody.append(strokeFieldset);
        }
        else if (me.geomType.indexOf("point") != "-1") {
            var pointFieldset = me.getPointFieldset($(svg.children[0]));
            modalbody.append(pointFieldset);
            var strokeFieldset = me.getStrokeFieldset($(svg.children[0]).attr("stroke"), $(svg.children[0]).attr("stroke"));
            modalbody.append(strokeFieldset);
        } else { //if (me.geomType.indexOf("polygon") != "-1") {
            var fillFieldset = me.getFillFieldset(svg.children[0].style.fill);
            var strokeFieldset = me.getStrokeFieldset(svg.children[0].style.stroke, svg.children[0].style.strokeWidth);
            modalbody.append(fillFieldset);
            modalbody.append(strokeFieldset);
        }
        // fillFieldset.css('visibility', 'visible');


        BootstrapDialog.show({
            title: "Change Style",
            type: BootstrapDialog.TYPE_SUCCESS,
            size: BootstrapDialog.SIZE_SMALL,
            message: modalbody,
            buttons: [{
                label: 'Set Style',
                action: function (dialogItself) {
                    var shape = svg.children[0]
                    if ($('#fillcolor').length > 0) {
                        var fillcolor = $('#fillcolor').val();
                        fillcolor = (fillcolor[0] == "#" ? fillcolor : "#" + fillcolor);
                        if (shape.style.fill) {
                            shape.style.fill = fillcolor;
                        } else {
                            $(shape).attr("fill", fillcolor)
                        }
                    }
                    if ($('#strokecolor').length > 0) {
                        var strokecolor = $('#strokecolor').val();
                        strokecolor = (strokecolor[0] == "#" ? strokecolor : "#" + strokecolor);
                        if (shape.style.stroke) {
                            shape.style.stroke = strokecolor;
                        } else {
                            $(shape).attr("stroke", strokecolor);
                        }

                    }
                    if ($('#strokewidthcounter').length > 0) {
                        var strokewidthcounter = $('#strokewidthcounter').val();
                        if (shape.style.strokeWidth) {
                            shape.style.strokeWidth = strokewidthcounter;
                        } else {
                            $(shape).attr("stroke-width", strokewidthcounter);
                        }
                    }
                    if ($('#opacitycounter').length > 0) {
                        var fillopacity = $('#opacitycounter').val()
                        shape.style.fillOpacity = parseInt(fillopacity) / 100;
                    }
                    if ($('#sizecounter').length > 0) {
                        var pointsize = $('#sizecounter').val()
                        $(shape).attr("r", pointsize)
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


    }

    me.clasifyData = function (arrdata, noOfClasses) {
        var gs = new geostats();
        gs.setSerie(arrdata);
        var classes = gs.getClassJenks(noOfClasses);
        return classes;
    }
    me.setStyleMissingParams = function (style) {
        if (!style.fillOpacity) {
            style.fillOpacity = 0.5;
        }
        if (!style.fillColor) {
            style.fillColor = "rgb(0,0,255)";
        }
        if (!style.stroke) {
            style.stroke = "rgb(0, 0, 0)";
        }
        if (!style.strokeWidth) {
            style.strokeWidth = "2";
        }
        if (!style.pointSize) {
            style.pointSize = "5";
        }
        return style
    }
    me.getStyle = function (rgb) {
        var style = {}
        if (rgb) {
            if (me.geomType.indexOf("polygon") != "-1") {
                style.fillColor = "rgb(" + rgb[0] + "," + rgb[1] + "," + rgb[2] + ")";
            } else if (me.geomType.indexOf("linestring") != "-1") {
                style.stroke = "rgb(" + rgb[0] + "," + rgb[1] + "," + rgb[2] + ")";
            } else if (me.geomType.indexOf("point") != "-1") {
                style.fillColor = "rgb(" + rgb[0] + "," + rgb[1] + "," + rgb[2] + ")";
            } else {
                style.fillColor = "rgb(" + rgb[0] + "," + rgb[1] + "," + rgb[2] + ")";
            }
        }
        style = me.setStyleMissingParams(style);
        return style;
    }
    me.applyRasterColorRamp = function (colors, stats, noOfClasses) {
        var level = noOfClasses / 3 + 1;
        var labels = [];
        for (var i = 0; i < level; i++) {
            if (i == 0) {
                labels.push(Math.round(stats.mean));
            } else {
                var val1 = Math.round(stats.mean - (i) * stats.stddev);
                var val2 = Math.round(stats.mean + (i) * stats.stddev);
                labels.push(val1)
                labels.push(val2)
            }
        }
        labels.sort()
        for (var i = 0; i < noOfClasses; i++) {
            var weight = i / (noOfClasses - 1);
            var rgb = me.getColorFromRamp(colors, weight);
            var style = me.getStyle(rgb);
            me.addStyleRow(labels[i], $("#rasRamptbody"), i, style);
        }
    }
    me.applyColorRamp = function (columnName, isNumber, columnValues, colors) {
        var eqs = []
        if (!isNumber) {
            for (var j = 0; j < columnValues.length; j++) {
                var valWeight = -1
                valWeight = j / (columnValues.length - 1);
                var rgb = me.getColorFromRamp(colors, valWeight);
                var style = me.getStyle(rgb);
                me.addStyleRow(columnValues[j], $("#ramptbody"), j, style);
            }
        } else {
            me.op = "between";
            // valWeight = parseFloat()
            me.noOfClasses = 6;
            var classes = me.clasifyData(columnValues, me.noOfClasses);
            for (var i = 0; i < me.noOfClasses; i++) {
                var weight = i / (me.noOfClasses - 1);
                var rgb = me.getColorFromRamp(colors, weight);
                var style = me.getStyle(rgb);
                // var fillColor = "rgb(" + rgb[0] + "," + rgb[1] + "," + rgb[2] + ")"
                label = Math.round(classes[i]) + " - " + Math.round(classes[i + 1]);
                me.addStyleRow(label, $("#ramptbody"), j, style);
            }
        }
    }

    // me.getColorFromRamp = function (color1, color2, cWeight1, cWeight2, weight) {
    me.getColorFromRamp = function (colors, weight) {
        var rgb = [];
        for (var i = 1; i < colors.length; i++) {
            var color1 = me.hex2rgb(colors[i - 1]);
            var color2 = me.hex2rgb(colors[i]);
            var cWeight1 = (i - 1) / (colors.length - 1);
            var cWeight2 = i / (colors.length - 1);
            if (weight <= cWeight2) {

                for (var i = 0; i < 3; i++) {
                    if (color2[i] != color1[i]) {
                        m = (color2[i] - color1[i]) / (cWeight2 - cWeight1);
                        c = color1[i] - m * cWeight1;
                        var val = Math.ceil(m * weight + c);
                    } else {
                        val = color1[i];
                    }
                    rgb.push(val);
                }
                // break;
            }
        }


        return rgb;

    }

    me.getFillFieldset = function (strColor) {
        if (!strColor) {
            strColor = 'ab2567'
        }
        var fillFieldset = $('<fieldset></fieldset>');
        var fillLegend = $('<legend>Fill</legend>');
        var fillColor = $('<input id="fillcolor" class="form-control" />');
        // var fillColor = document.createElement('INPUT');
        fillColor[0].classList.add("form-control");

        var picker = new jscolor(fillColor[0]);
        picker.fromString(strColor);

        var fillOpacity = $('<div class="form-group"> <label class="control-label">Opacity</label> ' +
            '<input id="opacitycounter" class="form-control numbercounter" type="number" value="100" min="0" ' +
            'max="100" step="5"/> </div>')
        fillFieldset.append(fillLegend);
        fillFieldset.append(fillColor);
        fillFieldset.append(fillOpacity);

        return fillFieldset;
    }
    me.getPointFieldset = function (shape) {
        var pointFieldset = $('<fieldset></fieldset>');
        var pointLegend = $('<legend>Point</legend>');

        var fillColor = $('<input id="fillcolor" class="form-control" />');
        // var fillColor = document.createElement('INPUT');
        fillColor[0].classList.add("form-control");
        var picker = new jscolor(fillColor[0]);
        strColor = "#ff0000"//me.color2hex(shape.attr("fill"));
        picker.fromString(strColor);
        var strSize = shape.attr("r");
        var pointSize = $('<div class="form-group"> <label class="control-label">Size</label> ' +
            '<input id="sizecounter" class="form-control numbercounter" type="number" value="' + strSize + '" min="0" ' +
            'max="100" step="1"/> </div>')
        pointFieldset.append(pointLegend);
        pointFieldset.append(fillColor);
        pointFieldset.append(pointSize);
        return pointFieldset;
    }
    me.getStrokeFieldset = function (strColor, strokeWidth) {
        if (!strokeWidth) strokeWidth = 1;
        if (!strColor) strColor = '000000';
        var strokeFieldset = $('<fieldset></fieldset>');
        var strokeLegend = $('<legend>Stroke</legend>');
        var strokeColor = $('<input id="strokecolor" class="jscolor form-control" value="000000" />');
        // var strokeColor = document.createElement('INPUT');
        strokeColor[0].classList.add("form-control");

        var picker = new jscolor(strokeColor[0]);
        picker.fromString(strColor);

        var strokeStyle = $('<div class="form-group"> ' +
            '<label class="control-label">Width</label> ' +
            '<input id="strokewidthcounter" class="form-control numbercounter" type="number" value="' + strokeWidth + '"' +
            'min="1" max="10"/> </div>');
        strokeFieldset.append(strokeLegend);
        strokeFieldset.append(strokeColor);
        strokeFieldset.append(strokeStyle);

        return strokeFieldset;
    };

    me.getLayerScaleJSON = function () {
        var min_scale = $('#min_scale_id').val();
        var max_scale = $('#max_scale_id').val();
        return {'min_scale': min_scale, 'max_scale': max_scale};
    };
    me.getStyleJSON = function (columnName, columnValue, pnlId) {
        var tab = null;
        if (pnlId == "assignColor") {
            tab = $("#styleTable")
        } else if (pnlId == "graducatedColor") {
            tab = $("#rampStyleTable");
        }
        if (tab != null) {
            trs = tab.find("tbody>tr");
            // data = {layer_name: layername}
            rules = []
            for (var i = 0; i < trs.length; i++) {
                rule = {}
                filter = {}
                value = trs[i].cells[0].innerText.trim();
                if (value != 'default') {
                    // if (me.op == "between"){
                    //     value = value.replace(" - ", " AND ");
                    // }
                    filter["literal"] = value;
                    filter["property_name"] = columnName;
                    filter["op"] = me.op;
                }
                rule["filter"] = filter
                var shape = trs[i].cells[1].lastChild.lastChild;
                var symbolizer = ""
                if (me.geomType.indexOf("polygon") != "-1") {
                    symbolizer = me.getPolygonSymbolizer(shape);
                    rule["polygon_symbolizer"] = symbolizer;
                } else if (me.geomType.indexOf("linestring") != "-1") {
                    symbolizer = me.getLineStringSymbolizer(shape)
                    rule["line_symbolizer"] = symbolizer;
                } else if (me.geomType.indexOf("point") != "-1") {
                    symbolizer = me.getPointSymbolizer(shape);
                    rule["point_symbolizer"] = symbolizer;
                }

                rules.splice(0, 0, rule)
            }
            // data['styles'] = rule;
            return rules;
        }
        return null;
    }

    me.getRasterStyleJSON = function (tbodyTarget, pnlId) {
        var trs = tbodyTarget.find("tr");
        var rules = [];
        var rule = {};
        var raster_symbolizer = {}
        var color_maps = []
        for (var i = 0; i < trs.length; i++) {

            var value = trs[i].cells[0].innerText;
            var shape = trs[i].cells[1].lastChild.lastChild;
            var color_map = me.getRasterColorMap(shape, value);
            color_maps.push(color_map);
        }
        raster_symbolizer["color_map"] = color_maps;
        rule["raster_symbolizer"] = raster_symbolizer;
        rules.push(rule);
        return rules;
    }
    me.getRasterColorMap = function (rect, value) {
        var color_map = {};
        color_map["color"] = me.color2hex(rect.style.fill);
        color_map["label"] = value;
        color_map["opacity"] = 1; //rect.style.fillOpacity;
        color_map["quantity"] = value;
        return color_map;
    }
    me.getPolygonSymbolizer = function (rect) {
        var polygon_symbolizer = {}
        polygon_symbolizer["fill"] = me.color2hex(rect.style.fill)
        polygon_symbolizer["stroke-width"] = rect.style.strokeWidth;
        polygon_symbolizer["stroke"] = me.color2hex(rect.style.stroke);
        polygon_symbolizer['fill_opacity'] = rect.style.fillOpacity;
        return polygon_symbolizer;
    }

    me.getLineStringSymbolizer = function (shape) {
        var lineSymbolizer = {};
        lineSymbolizer["stroke"] = me.color2hex(shape.style.stroke);
        lineSymbolizer["stroke-width"] = shape.style.strokeWidth;
        lineSymbolizer["stroke-linejoin"] = "bevel";
        lineSymbolizer["stroke-linecap"] = "square";
        return lineSymbolizer
    }
    me.getPointSymbolizer = function (shape) {
        var pointSymbolizer = {};
        pointSymbolizer["stroke"] = me.color2hex($(shape).attr("stroke"));
        pointSymbolizer["stroke-width"] = $(shape).attr("stroke-width");
        pointSymbolizer["fill"] = me.color2hex($(shape).attr("fill"));
        pointSymbolizer["size"] = $(shape).attr("r");
        return pointSymbolizer;
    }

    me.color2hex = function (color) {
        if (color.substr(0, 1) === '#') {
            return color;
        }
        var digits = /(.*?)rgb\((\d+), (\d+), (\d+)\)/.exec(color);
        if (digits == null) {
            digits = /(.*?)rgb\((\d+),(\d+),(\d+)\)/.exec(color);
        }
        // var red = parseInt(digits[2]).toString(16);
        // var green = parseInt(digits[3]).toString(16);
        // var blue = parseInt(digits[4]).toString(16);
        //
        // var hexColor = "#" + (red.length < 2 ? "0" + red : red) + (green.length < 2 ? "0" + green : green) +
        //     (blue.length < 2 ? "0" + blue : blue);
        var hexColor = me.rgb2hex(digits[2], digits[3], digits[4]);
        return hexColor
        // var rgb = blue | (green << 8) | (red << 16);
        // return digits[1] + '#' + rgb.toString(16);
    }

    me.rgb2hex = function (r, g, b) {
        var red = parseInt(r).toString(16);
        var green = parseInt(g).toString(16);
        var blue = parseInt(b).toString(16);

        var hexColor = "#" + (red.length < 2 ? "0" + red : red) + (green.length < 2 ? "0" + green : green) +
            (blue.length < 2 ? "0" + blue : blue);
        return hexColor
    }

    me.hex2rgb = function (hex) {
        hex = hex.replace('#', '');
        var r = parseInt(hex.substring(0, 2), 16);
        var g = parseInt(hex.substring(2, 4), 16);
        var b = parseInt(hex.substring(4, 6), 16);
        return [r, g, b];
    }

}