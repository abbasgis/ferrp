/**
 * Created by idrees on 11/13/2018.
 */


var AnalysisModel = function () {
    var me = this;
    me.panelHeader = ko.observable();
    me.panelBody = ko.observable();
    me.schemeDivId = 'divSchemesList';
    me.cmbYearsList = 'lstYears';
    me.mainPnlBody = $('#mainpnlbody');
    me.source = null;

    me.alertClasses = {
        "info": 'alert alert-info', "danger": 'alert alert-danger',
        "warning": 'alert alert-warning', "success": 'alert alert-success'
    };

    me.initialize = function () {
        // me.populateYearsList(schemesList);
        me.createGridPanel();

        // $('#lstYears').change(function () {
        //     $('#myPleaseWait').modal('show');
        //     me.applyFilterToJQXGrid();
        // });
    }

    me.createGridPanel = function () {
        $('[name=lstYears]').val( '-1' );
        me.panelHeader('<span class="glyphicon glyphicon-book"></span>');
        var infoMainRow = me.createRowEl();

        var gridRow = me.createRowEl();
        var gridPnl = me.createSchemesGridPanel();

        gridRow.append(gridPnl);
        me.mainPnlBody.append(infoMainRow);
        me.mainPnlBody.append(gridRow);

        me.createSchemesListGrid(schemesList);
    }

    //
    // me.applyFilterToJQXGrid = function () {
    //     var schemesGrid = $("#" + me.schemeDivId);
    //     schemesGrid.jqxGrid('clearfilters');
    //     var yearName = $('#lstYears').val();
    //     var yearFilterGroup = new $.jqx.filter();
    //     var year_operator = null;
    //     if (yearName != '-1') {
    //         yearFilterGroup.operator = 'and';
    //         year_operator = 0;
    //         var filtervalue = yearName;
    //         var filtercondition = 'equal';
    //         var yearFilter1 = yearFilterGroup.createfilter('stringfilter', filtervalue, filtercondition);
    //         yearFilterGroup.addfilter(year_operator, yearFilter1);
    //         schemesGrid.jqxGrid('addfilter', 'Year', yearFilterGroup);
    //         me.filterInformation += "Year =  " + yearName + ";";
    //         schemesGrid.jqxGrid('applyfilters');
    //     } else {
    //         schemesGrid.jqxGrid('clearfilters');
    //     }
    //     $('#myPleaseWait').modal('hide');
    // }
    // me.getYearData = function (year) {
    //     if (year != '-1') {
    //         var groupByData = me.groupBy('Year');
    //         for (var key in groupByData) {
    //             if (key == year) {
    //                 return groupByData[key];
    //             }
    //         }
    //     } else {
    //         return adpVM.schemesList;
    //     }
    // }
    //
    // me.groupBy = function (key) {
    //     var sortedList = _(schemesList).sortBy(key);
    //     var result = _(sortedList).groupBy(function (scheme) {
    //         if (scheme[key] != null) {
    //             var res = scheme[key].split(",");
    //             var value = null;
    //             if (res.length > 1) {
    //                 value = "Multiple-" + key;
    //             } else {
    //                 value = scheme[key].trim();
    //             }
    //             return value;
    //         }
    //     });
    //     return result;
    // }

    me.setDimensionModelingContents = function () {
        $('#myPleaseWait').modal('show');
        // $('#lstYears').addClass('hidden');
        me.mainPnlBody.html('');
        me.dimensionModel = new DimensionModel(me);
        me.dimensionModel.initialize();
        $('#myPleaseWait').modal('hide');
    }

    me.setOverviewContents = function () {
        $('#myPleaseWait').modal('show');
        // $('#lstYears').removeClass('hidden');
        me.mainPnlBody.html('');
        me.createGridPanel();
        $('#myPleaseWait').modal('hide');
    }

    me.createSchemesGridPanel = function () {
        var pnl = ' <div class="col-lg-12"> ' +
            '<div class="panel panel-primary"> ' +
            '<div class="panel-body"> ' +
            '<div class="alert alert-info" id="alertClass"> ' +
            '<a href="#" data-bind="click: removeAlert" class="close"  aria-label="close">x</a>' +
            '<span id="alertText">Scheme List Table</span> </div>' +  //
            '<div style="height: 500px;" id="' + me.schemeDivId + '" class="col-lg-12"></div> ' +
            '</div> </div>';
        return $(pnl);
    }

    me.invokeAlert = function (type, text) {
        $('#alertText').html(text);
        var aClass = (type == '' ? '' : me.alertClasses[type]);
        $('#alertClass').removeClass().addClass(aClass);
    }

    me.removeAlert = function () {
        me.invokeAlert('info', 'Scheme List Table');
    }

    me.createRowEl = function () {
        var row = '<div class="row"></div>';
        return $(row);
    }

    // me.populateYearsList = function (data) {
    //
    //     var yearsList = me.getUniqueValues(data, 'Year');
    //     $.each(yearsList, function (key, value) {
    //         $('#' + me.cmbYearsList).append($('<option>', {value: value}).text(value));
    //     });
    // }

    me.getUniqueValues = function (data, column) {
        var lookup = {};
        var items = data;
        var arrUniqueValues = [];
        for (var item, i = 0; item = items[i++];) {
            var key = item[column];
            if (!(key in lookup)) {
                if (key) {
                    lookup[key] = 1;
                    arrUniqueValues.push(key);
                }
            }
        }
        return arrUniqueValues;
    }

    me.createSchemesListGrid = function (schemesList) {
        try {
            var dataFields = me.prepareDataFieldList(schemesList[0]);
            me.source = {
                localdata: schemesList,
                datatype: "array",
                datafields: dataFields,
            };
            var dataAdapter = new $.jqx.dataAdapter(me.source);
            $("#" + me.schemeDivId).jqxGrid(
                {
                    source: dataAdapter,
                    theme: 'Bootstrap',
                    sortable: true,
                    filterable: true,
                    pageable: true,
                    pagesize: 7100,
                    pagesizeoptions: ['10', '100', '500', '1000', '5000'],
                    width: '100%',
                    height: 500,
                    showtoolbar: true,
                    groupable: true,
                    // rowdetails: true,
                    // rowdetailstemplate: {
                    //     rowdetails: "<div style='width:100%; margin: 10px;'><ul style='margin-left: 30px;'><li>Costing</li><li>Projection</li></ul><div class='costing'></div><div class='projection'></div></div>",
                    //     rowdetailsheight: 300
                    // },
                    columnsresize: true,
                    showfilterrow: true,
                    showgroupaggregates: true,
                    showstatusbar: true,
                    showaggregates: true,
                    statusbarheight: 30,
                    autoshowfiltericon: true,
                    // initrowdetails: me.initGridRowDetails,
                    enabletooltips: true,
                    groups: [],
                    columns: me.getColumnsList(),
                    rendertoolbar: function (toolbar) {
                        me.createGridToolbar(toolbar);
                    }
                });
            $('#' + me.schemeDivId).on('rowselect', function (event) {
                // event arguments.
                var args = event.args;
                // row's bound index.
                var rowBoundIndex = args.rowindex;
                // row's data. The row's data object or null(when all rows are being selected or unselected with a single action). If you have a datafield called "firstName", to access the row's firstName, use var firstName = rowData.firstName;
                var rowData = args.row;
                var datafield = "Name_of_Scheme";
                var cellElement = $('#' + me.schemeDivId).jqxGrid('getcell', rowBoundIndex, datafield);//event.owner.columnsrow[0].cells[1]//
                var value = cellElement.value;
                me.invokeAlert('warning', "Scheme Name: <b>" + value + "</b>");
                // $(cellElement).jqxTooltip({position: 'bottom', content: "<b>"+value+"</b>", autoHide:false });
            })
            // var records = $("#divSchemesList").jqxGrid('getrows');//.adapter;
            // me.calculateRecordStats(records);
            $("#" + me.schemeDivId).on("filter", function (event) {
                var filters = event.args.filters;
                var filterInformation = '';
                for (var i = 0; i < filters.length; i++) {
                    if (i == 0) {
                        filterInformation = 'Data Filtered where '
                    } else if (i == filters.length - 1) {
                        filterInformation += ", and ";
                    } else if (i > 0 && i < filters.length - 1) {
                        filterInformation += ", ";
                    }
                    var filter = filters[i];
                    var fieldName = filter.datafield;
                    filterInformation += "<b>" + fieldName + "</b>";
                    var filterDetails = filter.filter.getfilters();
                    for (var j = 0; j < filterDetails.length; j++) {
                        if (filterDetails.length > 1) {
                            if (j == filterDetails.length - 1) {
                                filterInformation += ", and";
                            } else if (j > 0) {
                                filterInformation += ", ";
                            }
                        }
                        filterInformation += " " + filterDetails[j].condition + " " + filterDetails[j].value;

                    }

                }
                if (filterInformation.length > 0) me.invokeAlert("success", filterInformation);
            });
        } catch (err) {
            console.error(err.stack);
        }
    }

    me.prepareDataFieldList = function (scheme) {
        var dataFields = [];
        for (var key in scheme) {
            var dataField = {};
            dataField.name = key;
            if (parseFloat(scheme[key]) == NaN) {
                dataField.type = 'string';
            } else {
                dataField.type = 'float';
            }
        }
        return dataFields;
    }

    me.getColumnsList = function () {
        var tooltiprenderer = function (element) {
            $(element).jqxTooltip({position: 'mouse', content: $(element).text()});
        }
        var columns = [
            {text: 'GS No', datafield: 'GS_No', width: 100, rendered: tooltiprenderer},
            {
                text: 'Scheme Name',
                datafield: 'Scheme_Name',
                width: 250,
                rendered: tooltiprenderer,
                aggregates: ["count"]
            },
            {text: 'Year', datafield: 'Year', width: 120, rendered: tooltiprenderer},
            {text: 'Approval', datafield: 'Approval', width: 80, rendered: tooltiprenderer, aggregates: ["count"]},
            {
                text: 'Main Sector',
                datafield: 'Main_Sector',
                width: 120,
                rendered: tooltiprenderer,
                aggregates: ["count"]
            },
            {text: 'Sector', datafield: 'Sector', width: 120, rendered: tooltiprenderer, aggregates: ["count"]},
            {text: 'Type', datafield: 'Type', width: 120, rendered: tooltiprenderer, aggregates: ["count"]},
            {text: 'District', datafield: 'District', width: 120, rendered: tooltiprenderer, aggregates: ["count"]},
            // {text: 'Monitoring', datafield: 'Monitoring',width: 120, rendered: tooltiprenderer, aggregates: ["count"]},
            {
                text: 'Total Cost',
                datafield: 'Total_Cost',
                width: 120,
                rendered: tooltiprenderer,
                aggregates: ["sum"],
                cellsrenderer: function (row, column, value, defaultRender, column, rowData) {

                    if (value.toString().indexOf("Sum") >= 0) {
                        return defaultRender.replace("Sum", "Total");
                    }
                },
                aggregatesrenderer: function (aggregates, column, element) {
                    var renderstring = '<div style="position: relative; margin-top: 4px; margin-right:5px; text-align: right; overflow: hidden;">' + "Total" + ': ' + aggregates.sum + '</div>';
                    return renderstring;
                }
            },
            {
                text: 'Allocation',
                datafield: 'Allocation',
                width: 120,
                rendered: tooltiprenderer,
                aggregates: ["sum"],
                cellsrenderer: function (row, column, value, defaultRender, column, rowData) {
                    if (value.toString().indexOf("Sum") >= 0) {
                        return defaultRender.replace("Sum", "Total");
                    }
                },
                aggregatesrenderer: function (aggregates, column, element) {
                    var renderstring = '<div style="position: relative; margin-top: 4px; margin-right:5px; text-align: right; overflow: hidden;">' + "Total" + ': ' + aggregates.sum + '</div>';
                    return renderstring;
                }
            },
            {
                text: 'Expense Upto June',
                datafield: 'Expense_Upto_June',
                width: 120,
                rendered: tooltiprenderer,
                aggregates: ["sum"]
            },
            {text: 'Local Capital', datafield: 'Local_Capital', width: 120, rendered: tooltiprenderer},
            {text: 'Local Revenue', datafield: 'Local_Revenue', width: 120, rendered: tooltiprenderer},
            {text: 'Total Capital', datafield: 'Total_Capital', width: 120, rendered: tooltiprenderer},
            {text: 'Total Revenue', datafield: 'Total_Revenue', width: 120, rendered: tooltiprenderer},
            {text: 'Foreign Aid Capital', datafield: 'Foreign_Aid_Capital', width: 120, rendered: tooltiprenderer},
            {text: 'Foreign Aid Revenue', datafield: 'Foreign_Aid_Revenue', width: 120, rendered: tooltiprenderer},
            {
                text: 'Foreign Aid Total',
                datafield: 'Foreign_Aid_Total',
                width: 120,
                rendered: tooltiprenderer,
                aggregates: ["sum"]
            },
            {text: 'Release', datafield: 'Release', width: 120, rendered: tooltiprenderer},
            {text: 'Utilization', datafield: 'Utilization', width: 120, rendered: tooltiprenderer},
            {text: 'Projection One', datafield: 'Projection_One', width: 120, rendered: tooltiprenderer},
            {text: 'Projection Two', datafield: 'Projection_Two', width: 120, rendered: tooltiprenderer},
            {text: 'Throw Forward', datafield: 'Throw_Forward', width: 120, rendered: tooltiprenderer}
            //{ text: 'Location', datafield: 'Location', width: 120, rendered: tooltiprenderer }
        ];
        return columns;
    }

    me.clearFilterFromGrid = function () {
        $("#" + me.schemeDivId).jqxGrid('clearfilters');
    }

    me.createGridToolbar = function (toolbar) {
        try {
            var buttons = [{
                id: "exportExcel",
                btnclass: "btn btn-success",
                info: "Used for Exporting Table to Excel",
                spanclass: 'fa fa-file-excel-o',
                onClickFn: "exportTo",
                args: '{"type":"excel"}'
            },
                {
                    id: "btnExportPDF",
                    btnclass: "btn btn-success",
                    info: "Used for Exporting Table to PDF",
                    spanclass: 'fa fa-file-pdf-o',
                    onClickFn: "exportTo",
                    args: '{"type":"pdf"}'
                },
                {
                    id: "btnExportCSV",
                    btnclass: "btn btn-success",
                    info: "Used for Exporting Table to CSV",
                    spanclass: 'fa fa fa-file-o',
                    onClickFn: "exportTo",
                    args: '{"type":"csv"}'
                },
                // {
                //     id: "btnViewSchemeInfo",
                //     btnclass: "btn btn-success",
                //     info: "View Scheme Info",
                //     spanclass: 'glyphicon glyphicon-list-alt',
                //     onClickFn: "viewSchemeInfo",
                //     args: ''
                // },
                // {
                //     id: "btnSchemeLocation",
                //     btnclass: "btn btn-success",
                //     info: "Used for Viewing Scheme Location on Map",
                //     spanclass: 'glyphicon glyphicon-map-marker',
                //     onClickFn: "viewOnMap",
                //     args: ''
                // },
            ];
            var container = $("<div style='margin: 5px;'></div>");
            for (var i = 0; i < buttons.length; i++) {
                var btn = $("<button class='" + buttons[i].btnclass + "' id='" + buttons[i].id + "'info='" + buttons[i].info + "' onClickFn='" + buttons[i].onClickFn + "' args='" + buttons[i].args + "'>" +
                    "<span id='span" + buttons[i].id + "' class='" + buttons[i].spanclass + "' info='" + buttons[i].info + "'></span></button>");

                container.append(btn);
                btn.on('mouseover', function (event) {
                    var el = event.target;
                    var info = $('#' + el.id).attr("info");
                    var spanId = el.id;
                    if (spanId.indexOf("span") == -1) {
                        spanId = "span" + spanId;
                    }
                    var spanclass = $('#' + spanId).attr("class");
                    info = "Button <span class='" + spanclass + "'></span> " + info;

                    me.invokeAlert('success', info);
                    // $(buttons[i].onClickFn)[0](buttons[i].info);
                });
                btn.click(function () {
                    try {
                        var target = $(this).attr("onClickFn");
                        var args = $(this).attr("args");
                        if (args.length > 2) {
                            var args = JSON.parse(args);
                        }
                        me[target](args);
                    } catch (err) {
                        console.error(err.stack);
                    }
                });

            }
            toolbar.append(container);

        } catch (err) {
            console.error(err.stack);
        }
    }

    me.exportTo = function (args) {
        var format = args.type;
        if (format === "excel") {
            $("#" + me.schemeDivId).jqxGrid('exportdata', 'xls', 'jqxGrid');
        }
        if (format === "pdf") {
            $("#" + me.schemeDivId).jqxGrid('exportdata', 'pdf', 'jqxGrid');
        }
        if (format === "csv") {
            $("#" + me.schemeDivId).jqxGrid('exportdata', 'csv', 'jqxGrid');
        }
        if (format === "html") {
            $("#" + me.schemeDivId).jqxGrid('exportdata', 'html', 'jqxGrid');
        }
        if (format === "json") {
            $("#" + me.schemeDivId).jqxGrid('exportdata', 'json', 'jqxGrid');
        }
        if (format === "xml") {
            $("#" + me.schemeDivId).jqxGrid('exportdata', 'xml', 'jqxGrid');
        }
    }

    me.viewSchemeInfo = function () {

        var getselectedrowindexes = $('#' + me.schemeDivId).jqxGrid('getselectedrowindexes');
        if (getselectedrowindexes.length > 0) {
            // returns the selected row's data.
            var selectedRowData = $('#' + me.schemeDivId).jqxGrid('getrowdata', getselectedrowindexes[0]);
            var gsNo = selectedRowData["GS No"];
            var monitoring = selectedRowData["Monitoring"];
            if (monitoring == true) {
                var url = "http://176.58.124.95/ferrp/ppms/public/submit_main?scheme=" + gsNo;
                // var url = "http://ferrp.com/ppms/submit_main?scheme=" + gsNo;
                window.open(url, "_blank ");
            } else {
                me.invokeAlert("danger", "This scheme is not being monitored.");
            }

        } else {
            me.invokeAlert("danger", "Please select a scheme first.");
        }
    }

    me.viewOnMap = function () {
        me.invokeAlert('danger', 'Location of Scheme isn\'t Available');
    }

    me.initGridRowDetails = function (index, parentElement, gridElement, datarecord) {
        try {
            var tabsdiv = null;
            var costing = null;
            var projection = null;
            tabsdiv = $($(parentElement).children()[0]);
            if (tabsdiv != null) {
                //getting tabs
                costing = tabsdiv.find('.costing');
                projection = tabsdiv.find('.projection');
                //creating container for costing tab with two columns.
                var containerCosting = $('<div style="margin: 5px;"></div>')
                var containerProjection = $('<div style="margin: 5px;"></div>')
                containerCosting.appendTo($(costing));
                containerProjection.appendTo($(projection));
                var label = '<p class="wordbreak"><b>' + datarecord["Name"] + '</b></p> <br/>'
                var leftcolumnCosting = $('<div style="float: left; width: 50%;"></div>');
                var rightcolumnCosting = $('<div style="float: left; width: 50%;"></div>');

                containerCosting.append(label);
                containerCosting.append(leftcolumnCosting);
                containerCosting.append(rightcolumnCosting);

                //setting information in containers.
                var totalCost = "<div style='margin: 10px;'><b>Total Cost:</b> " + numberFormat((datarecord["Total_Cost"])) + "</div>";
                var foreignAid = "<div style='margin: 10px;'><b>Foreign Aid:</b> " + numberFormat(datarecord["Foreign_Aid"]) + "</div>";
                var allocation = "<div style='margin: 10px;'><b>Allocation:</b> " + numberFormat(datarecord["Allocation"]) + "</div>"
                //var pndProposedAllocation ="<div style='margin: 10px;'><b>P&D Proposed Allocation:</b> " + me.adpVM.numberFormat(datarecord["PND_Proposed_Allocation"]) + "</div>"
                $(leftcolumnCosting).append(totalCost);
                $(leftcolumnCosting).append(foreignAid);
                $(leftcolumnCosting).append(allocation);
                //$(leftcolumnCosting).append(pndProposedAllocation);

                var localCapital = "<div style='margin: 10px;'><b>Local Capital:</b> " + numberFormat((datarecord["LocalCapital"])) + "</div>";
                var localRevenue = "<div style='margin: 10px;'><b>Local Revenue:</b> " + numberFormat((datarecord["LocalRevenue"])) + "</div>";
                var foreignCapital = "<div style='margin: 10px;'><b>Foreign Capital:</b> " + numberFormat((datarecord["ForeignCapital"])) + "</div>";
                var foreignRevenue = "<div style='margin: 10px;'><b>Foreign Revenue:</b> " + numberFormat((parseFloat(datarecord["ForeignRevenue"]))) + "</div>";
                var totalCapital = "<div style='margin: 10px;'><b>Total Capital</b> " + menumberFormat((parseFloat(datarecord["TotalCapital"]))) + "</div>";
                var totalRevenue = "<div style='margin: 10px;'><b>Total Revenue:</b> " + numberFormat((parseFloat(datarecord["TotalRevenue"]))) + "</div>";

                $(rightcolumnCosting).append(localCapital);
                $(rightcolumnCosting).append(localRevenue);
                $(rightcolumnCosting).append(foreignCapital);
                $(rightcolumnCosting).append(foreignRevenue);
                $(rightcolumnCosting).append(totalCapital);
                $(rightcolumnCosting).append(totalRevenue);

                var leftcolumnProjection = $('<div style="float: left; width: 100%;"></div>');
                containerProjection.append(leftcolumnProjection);

                var projection1718 = "<div style='margin: 10px;'><b>Projection 17-18:</b> " + numberFormat((datarecord["Projection_2017-18"])) + "</div>";
                var projection1819 = "<div style='margin: 10px;'><b>Projection 18-19:</b> " + numberFormat((datarecord["Projection_2018-19"])) + "</div>";
                var throwFOrward19 = "<div style='margin: 10px;'><b>Throw Forward 19:</b> " + numberFormat((datarecord["Throw_Forward"])) + "</div>";
                var expenseUptoJune = "<div style='margin: 10px;'><b>Expense Upto June:</b> " + numberFormat((datarecord["Exp_upto_June"])) + "</div>";

                $(leftcolumnProjection).append(projection1718);
                $(leftcolumnProjection).append(projection1819);
                $(leftcolumnProjection).append(throwFOrward19);
                $(leftcolumnProjection).append(expenseUptoJune);

                $(tabsdiv).jqxTabs({width: 750, height: 250});
            }
        } catch (err) {
            console.error(err.stack);
        }
    };

}