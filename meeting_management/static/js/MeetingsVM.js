/**
 * Created by idrees on 11/23/2018.
 */

var GridModel = function (gridDivId) {
    var me = this;
    me.gridTarget = $("#" + gridDivId + "");
    me.grid = null;
    me.gridColumns = [];
    me.gridData = null;
    me.gridColumns = null;
    me.dataFields = null;
    me.dataAdapter = null;
    me.theme = 'Bootstrap';
    me.shortenUrlApi = 'https://www.googleapis.com/urlshortener/v1/url?key=AIzaSyDgYyiV-5-HR9UFuyiLMZ9KCNp5J_0i4BY';
    me.contentType = 'application/json; charset=utf-8';

    me.createDataAdapter = function (dataFields, data) {
        var source = {
            datatype: 'json',
            datafields: dataFields,
            localdata: data
        }
        me.dataAdapter = new $.jqx.dataAdapter(source, {autoBind: true});
    }

    me.createGrid = function (columns, fields, data) {

        fields = me.addSerialToFields(fields);
        columns = me.addSerialToColumns(columns);
        data = me.addSerialToData(data);
        columns = me.updateColumnWidths(columns);
        me.dataFields = fields;
        me.gridColumns = columns;
        me.gridData = data;
        gridData = data;
        me.populateColumnsListInCombo(columns);
        me.populateMeetingsListInCombo();

        if (type == 'all' || type == 'important' || type == 'short' || type == 'long' || type == 'completed' || type == 'meeting_initiatives_search') {
            me.createGridToAccordionPanel(data);
            me.recordFormModalOnLoad();
        }
        var groupsRenderer = function (text, group, expanded, data) {
            if (data.groupcolumn.datafield == "Donor Agency" && type == 'foreign') {
                //alert(data);
                var sumTotalCost = 0;
                var groupItems = data.subItems;
                for (var i = 0; i < groupItems.length; i++) {
                    var totalCost = groupItems[i]["Total Cost"];
                    sumTotalCost = sumTotalCost + totalCost;
                }
                return '<div class="jqx-grid-groups-row jqx-grid-groups-row-Bootstrap" style="position: absolute;"><span>' + group + "    ( Total Cost:" + sumTotalCost.toFixed(3) + " )" + '</span>';
            } else if (data.groupcolumn.datafield == 'Meeting Date' && type == 'meetings') {
                return '<div class="jqx-grid-groups-row jqx-grid-groups-row-Bootstrap" style="position: absolute;"><span>' + me.removeGMTFromDate(group) + '</span>';
            }
        }
        var groupFields = [];
        if (type == 'foreign') {
            groupFields = ["Donor Agency"];
        }
        else if (type == 'meetings') {
            groupFields = ['Meeting Date'];
        }
        try {
            me.gridColumns = columns;
            me.createDataAdapter(fields, data);
            me.gridTarget.jqxGrid({
                theme: me.theme,
                source: me.dataAdapter,
                columns: columns,
                altRows: true,
                filterable: true,
                showfilterrow: true,
                width: '100%',
                height: 450,
                pageable: true,
                pagesize: 100,
                pagesizeoptions: ['10', '100', '500', '1000', '5000'],
                groupable: true,
                groups: groupFields,
                groupsrenderer: groupsRenderer,
                // showgroupaggregates: true,
                sortable: true,
                enabletooltips: true,
                selectionmode: 'singlerow',
                columnsresize: true,
                showtoolbar: true,
                autoshowfiltericon: true,
                rendertoolbar: function (toolbar) {
                    if (type == 'quick') {
                        me.quickTasksToolbar(toolbar);
                    }
                    if (type == 'meetings') {
                        me.createMeetingsToolbar(toolbar);
                    }
                    if (type == 'foreign') {
                        me.createForeignBriefsToolbar(toolbar);
                    }
                    if (type == 'local') {
                        me.createLocalBriefsToolbar(toolbar);
                    }
                    if (type == 'contacts' || type == 'non_pnd' || type == 'foreigners') {
                        me.createSocialCallListToolbar(toolbar);
                    } else {
                        me.createGridToolbar(toolbar)
                    }
                }
            });

            $("#btnPrintReport").click(function () {
                me.getPrintPage();
            });

            $("#btnSearchGrid").click(function () {
                me.searchText();
            });
            me.applyOnLoadFilter();
        }
        catch (e) {
            console.log(e)
        }
    };

    me.cellclass = function (row, columnfield, value) {
        var currentDate = Date.now();
        var dueDate = Date.parse(value);
        if (dueDate < currentDate) {
            return 'red';
        }
        else if (dueDate == currentDate) {
            return 'yellow';
        }
        else return 'green';
    };

    me.createSocialCallListToolbar = function (toolbar) {
        try {
            var buttons = [
                {
                    id: "btnViewForm",
                    btnclass: "btn btn-success",
                    info: "Used for view form",
                    spanclass: 'fa fa-check-square-o',
                    onClickFn: "callListToolbarButtonClick",
                    args: '{"type":"form"}'
                }, {
                    id: "btnAddRecord",
                    btnclass: "btn btn-success",
                    info: "Used for adding new record",
                    spanclass: 'fa fa-plus-square-o',
                    onClickFn: "callListToolbarButtonClick",
                    args: '{"type":"add"}'
                }, {
                    id: "btnEditRecord",
                    btnclass: "btn btn-success",
                    info: "Used for editing selected Record",
                    spanclass: 'fa fa-pencil-square-o',
                    onClickFn: "callListToolbarButtonClick",
                    args: '{"type":"edit"}'
                }, {
                    id: "btnDeleteRecord",
                    btnclass: "btn btn-success",
                    info: "Used for deleting selected Record",
                    spanclass: 'fa fa-trash-o',
                    onClickFn: "callListToolbarButtonClick",
                    args: '{"type":"delete"}'
                }, {
                    id: "btnEmail",
                    btnclass: "btn btn-success",
                    info: "Used for email selected record(s)",
                    spanclass: 'fa fa-share',
                    onClickFn: "callListToolbarButtonClick",
                    args: '{"type":"email"}'
                }, {
                    id: "btnSMS",
                    btnclass: "btn btn-success",
                    info: "Used for sms selected record(s)",
                    spanclass: 'fa fa fa-envelope-o',
                    onClickFn: "callListToolbarButtonClick",
                    args: '{"type":"sms"}'
                },
            ];
            var container = $("<div style='margin: 5px;'></div>");
            for (var i = 0; i < buttons.length; i++) {
                var btn = $("<button class='" + buttons[i].btnclass + "' id='" + buttons[i].id + "'info='" + buttons[i].info + "' onClickFn='" + buttons[i].onClickFn + "' args='" + buttons[i].args + "'>" +
                    "<span id='span" + buttons[i].id + "' class='" + buttons[i].spanclass + "' info='" + buttons[i].info + "'></span></button>");

                container.append(btn);
                // btn.on('mouseover', function (event) {
                //     var el = event.target;
                //     var info = $('#' + el.id).attr("info");
                //     var spanId = el.id;
                //     if (spanId.indexOf("span") == -1) {
                //         spanId = "span" + spanId;
                //     }
                //     var spanclass = $('#' + spanId).attr("class");
                //     info = "Button <span class='" + spanclass + "'></span> " + info;
                //
                //     me.invokeAlert('success', info);
                //     // $(buttons[i].onClickFn)[0](buttons[i].info);
                // });
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

    me.createMeetingsToolbar = function (toolbar) {
        try {
            var buttons = [
                // {
                //     id: "btnViewForm",
                //     btnclass: "btn btn-success",
                //     info: "View participants list",
                //     spanclass: 'fa fa-users',
                //     onClickFn: "meetingsToolbarButtonClick",
                //     args: '{"type":"users"}'
                // },
                {
                    id: "btnAddRecord",
                    btnclass: "btn btn-success",
                    info: "Used for adding new record",
                    spanclass: 'fa fa-plus-square-o',
                    onClickFn: "meetingsToolbarButtonClick",
                    args: '{"type":"add"}'
                }, {
                    id: "btnEditRecord",
                    btnclass: "btn btn-success",
                    info: "Used for editing selected Record",
                    spanclass: 'fa fa-pencil-square-o',
                    onClickFn: "meetingsToolbarButtonClick",
                    args: '{"type":"edit"}'
                }, {
                    id: "btnDeleteRecord",
                    btnclass: "btn btn-success",
                    info: "Used for deleting selected Record",
                    spanclass: 'fa fa-trash-o',
                    onClickFn: "meetingsToolbarButtonClick",
                    args: '{"type":"delete"}'
                }, {
                    id: "btnEmail",
                    btnclass: "btn btn-success",
                    info: "Used for email selected record(s)",
                    spanclass: 'fa fa-share',
                    onClickFn: "meetingsToolbarButtonClick",
                    args: '{"type":"email"}'
                }, {
                    id: "btnSMS",
                    btnclass: "btn btn-success",
                    info: "Used for sms selected record(s)",
                    spanclass: 'fa fa fa-envelope-o',
                    onClickFn: "meetingsToolbarButtonClick",
                    args: '{"type":"sms"}'
                }, {
                    id: "btnPrint",
                    btnclass: "btn btn-success",
                    info: "Used for printing",
                    spanclass: 'fa fa-print',
                    onClickFn: "meetingsToolbarButtonClick",
                    args: '{"type":"print"}'
                }, {
                    id: "btnInitiative",
                    btnclass: "btn btn-success",
                    info: "Used for add initiative",
                    spanclass: 'fa fa-tasks',
                    onClickFn: "meetingsToolbarButtonClick",
                    args: '{"type":"initiative"}'
                },
                // {
                //     id: "btnPT",
                //     btnclass: "btn btn-warning",
                //     info: "Used for Pivot table",
                //     spanclass: 'fa fa-puzzle-piece',
                //     onClickFn: "meetingsToolbarButtonClick",
                //     args: '{"type":"pt"}'
                // },
            ];
            var container = $("<div style='margin: 5px;'></div>");
            for (var i = 0; i < buttons.length; i++) {
                var btn = $("<button class='" + buttons[i].btnclass + "' id='" + buttons[i].id + "'info='" + buttons[i].info + "'title='" + buttons[i].info + "' onClickFn='" + buttons[i].onClickFn + "' args='" + buttons[i].args + "'>" +
                    "<span id='span" + buttons[i].id + "' class='" + buttons[i].spanclass + "' info='" + buttons[i].info + "'></span></button>");

                container.append(btn);
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

    me.createForeignBriefsToolbar = function (toolbar) {
        try {
            var buttons = [
                // {
                //     id: "btnViewForm",
                //     btnclass: "btn btn-success",
                //     info: "Used for view form",
                //     spanclass: 'fa fa-check-square-o',
                //     onClickFn: "foreignBriefsToolbarButtonClick",
                //     args: '{"type":"form"}'
                // },
                {
                    id: "btnAddRecord",
                    btnclass: "btn btn-success",
                    info: "Used for adding new record",
                    spanclass: 'fa fa-plus-square-o',
                    onClickFn: "foreignBriefsToolbarButtonClick",
                    args: '{"type":"add"}'
                }, {
                    id: "btnEditRecord",
                    btnclass: "btn btn-success",
                    info: "Used for editing selected Record",
                    spanclass: 'fa fa-pencil-square-o',
                    onClickFn: "foreignBriefsToolbarButtonClick",
                    args: '{"type":"edit"}'
                }, {
                    id: "btnDeleteRecord",
                    btnclass: "btn btn-success",
                    info: "Used for deleting selected Record",
                    spanclass: 'fa fa-trash-o',
                    onClickFn: "foreignBriefsToolbarButtonClick",
                    args: '{"type":"delete"}'
                }, {
                    id: "btnEmail",
                    btnclass: "btn btn-success",
                    info: "Used for email selected record(s)",
                    spanclass: 'fa fa-share',
                    onClickFn: "foreignBriefsToolbarButtonClick",
                    args: '{"type":"email"}'
                }, {
                    id: "btnSMS",
                    btnclass: "btn btn-success",
                    info: "Used for sms selected record(s)",
                    spanclass: 'fa fa fa-envelope-o',
                    onClickFn: "foreignBriefsToolbarButtonClick",
                    args: '{"type":"sms"}'
                }, {
                    id: "btnPrint",
                    btnclass: "btn btn-success",
                    info: "Used for printing",
                    spanclass: 'fa fa-print',
                    onClickFn: "foreignBriefsToolbarButtonClick",
                    args: '{"type":"print"}'
                },
                // {
                //     id: "btnPT",
                //     btnclass: "btn btn-warning",
                //     info: "Used for Pivot table",
                //     spanclass: 'fa fa-puzzle-piece',
                //     onClickFn: "foreignBriefsToolbarButtonClick",
                //     args: '{"type":"pt"}'
                // },
            ];
            var container = $("<div style='margin: 5px;'></div>");
            for (var i = 0; i < buttons.length; i++) {
                var btn = $("<button class='" + buttons[i].btnclass + "'title='" + buttons[i].info + "' id='" + buttons[i].id + "'info='" + buttons[i].info + "' onClickFn='" + buttons[i].onClickFn + "' args='" + buttons[i].args + "'>" +
                    "<span id='span" + buttons[i].id + "' class='" + buttons[i].spanclass + "' info='" + buttons[i].info + "'></span></button>");

                container.append(btn);
                // btn.on('mouseover', function (event) {
                //     var el = event.target;
                //     var info = $('#' + el.id).attr("info");
                //     var spanId = el.id;
                //     if (spanId.indexOf("span") == -1) {
                //         spanId = "span" + spanId;
                //     }
                //     var spanclass = $('#' + spanId).attr("class");
                //     info = "Button <span class='" + spanclass + "'></span> " + info;
                //
                //     me.invokeAlert('success', info);
                //     // $(buttons[i].onClickFn)[0](buttons[i].info);
                // });
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

    me.createLocalBriefsToolbar = function (toolbar) {
        try {
            var buttons = [
                {
                    id: "btnViewForm",
                    btnclass: "btn btn-success",
                    info: "Used for view form",
                    spanclass: 'fa fa-check-square-o',
                    onClickFn: "localBriefsToolbarButtonClick",
                    args: '{"type":"form"}'
                },
                // {
                //     id: "btnAddRecord",
                //     btnclass: "btn btn-success",
                //     info: "Used for adding new record",
                //     spanclass: 'fa fa-plus-square-o',
                //     onClickFn: "localBriefsToolbarButtonClick",
                //     args: '{"type":"add"}'
                // },
                // {
                //     id: "btnEditRecord",
                //     btnclass: "btn btn-success",
                //     info: "Used for editing selected Record",
                //     spanclass: 'fa fa-pencil-square-o',
                //     onClickFn: "localBriefsToolbarButtonClick",
                //     args: '{"type":"edit"}'
                // },
                {
                    id: "btnEmail",
                    btnclass: "btn btn-success",
                    info: "Used for email selected record(s)",
                    spanclass: 'fa fa-share',
                    onClickFn: "localBriefsToolbarButtonClick",
                    args: '{"type":"email"}'
                }, {
                    id: "btnSMS",
                    btnclass: "btn btn-success",
                    info: "Used for sms selected record(s)",
                    spanclass: 'fa fa fa-envelope-o',
                    onClickFn: "localBriefsToolbarButtonClick",
                    args: '{"type":"sms"}'
                }, {
                    id: "btnPrint",
                    btnclass: "btn btn-success",
                    info: "Used for printing",
                    spanclass: 'fa fa-print',
                    onClickFn: "localBriefsToolbarButtonClick",
                    args: '{"type":"print"}'
                },
                // {
                //     id: "btnPT",
                //     btnclass: "btn btn-warning",
                //     info: "Used for Pivot table",
                //     spanclass: 'fa fa-puzzle-piece',
                //     onClickFn: "localBriefsToolbarButtonClick",
                //     args: '{"type":"pt"}'
                // },
            ];
            var container = $("<div style='margin: 5px;'></div>");
            for (var i = 0; i < buttons.length; i++) {
                var btn = $("<button class='" + buttons[i].btnclass + "'title='" + buttons[i].info + "' id='" + buttons[i].id + "'info='" + buttons[i].info + "' onClickFn='" + buttons[i].onClickFn + "' args='" + buttons[i].args + "'>" +
                    "<span id='span" + buttons[i].id + "' class='" + buttons[i].spanclass + "' info='" + buttons[i].info + "'></span></button>");

                container.append(btn);
                // btn.on('mouseover', function (event) {
                //     var el = event.target;
                //     var info = $('#' + el.id).attr("info");
                //     var spanId = el.id;
                //     if (spanId.indexOf("span") == -1) {
                //         spanId = "span" + spanId;
                //     }
                //     var spanclass = $('#' + spanId).attr("class");
                //     info = "Button <span class='" + spanclass + "'></span> " + info;
                //
                //     me.invokeAlert('success', info);
                //     // $(buttons[i].onClickFn)[0](buttons[i].info);
                // });
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

    me.createGridToolbar = function (toolbar) {
        try {
            var buttons = [
                {
                    id: "btnViewForm",
                    btnclass: "btn btn-success",
                    info: "Used for view form",
                    spanclass: 'fa fa-check-square-o',
                    onClickFn: "toolbarButtonClick",
                    args: '{"type":"form"}'
                }, {
                    id: "btnRemarksHistory",
                    btnclass: "btn btn-success",
                    info: "Used for viewing remarks history",
                    spanclass: 'fa fa-history',
                    onClickFn: "toolbarButtonClick",
                    args: '{"type":"history"}'
                }, {
                    id: "btnAddRecord",
                    btnclass: "btn btn-success",
                    info: "Used for adding new record",
                    spanclass: 'fa fa-plus-square-o',
                    onClickFn: "toolbarButtonClick",
                    args: '{"type":"add"}'
                }, {
                    id: "btnEditRecord",
                    btnclass: "btn btn-success",
                    info: "Used for editing selected Record",
                    spanclass: 'fa fa-pencil-square-o',
                    onClickFn: "toolbarButtonClick",
                    args: '{"type":"edit"}'
                }, {
                    id: "btnDeleteRecord",
                    btnclass: "btn btn-success",
                    info: "Used for deleting selected Record",
                    spanclass: 'fa fa-trash-o',
                    onClickFn: "toolbarButtonClick",
                    args: '{"type":"delete"}'
                }, {
                    id: "btnPictureGallery",
                    btnclass: "btn btn-success",
                    info: "Used for viewing picture gallery",
                    spanclass: 'fa fa-file-picture-o',
                    onClickFn: "toolbarButtonClick",
                    args: '{"type":"picture"}'
                }, {
                    id: "btnDocuments",
                    btnclass: "btn btn-success",
                    info: "Used for viewing documents",
                    spanclass: 'fa fa-file-pdf-o',
                    onClickFn: "toolbarButtonClick",
                    args: '{"type":"documents"}'
                }, {
                    id: "btnEmail",
                    btnclass: "btn btn-success",
                    info: "Used for email selected record(s)",
                    spanclass: 'fa fa-share',
                    onClickFn: "toolbarButtonClick",
                    args: '{"type":"email"}'
                }, {
                    id: "btnSMS",
                    btnclass: "btn btn-success",
                    info: "Used for sms selected record(s)",
                    spanclass: 'fa fa fa-envelope-o',
                    onClickFn: "toolbarButtonClick",
                    args: '{"type":"sms"}'
                },
                // {
                //     id: "btnAttachments",
                //     btnclass: "btn btn-warning",
                //     info: "Used for attachments",
                //     spanclass: 'fa fa-paperclip',
                //     onClickFn: "toolbarButtonClick",
                //     args: '{"type":"attachments"}'
                // },
                // {
                //     id: "btnPT",
                //     btnclass: "btn btn-warning",
                //     info: "Used for Pivot table",
                //     spanclass: 'fa fa-puzzle-piece',
                //     onClickFn: "toolbarButtonClick",
                //     args: '{"type":"pt"}'
                // },
            ];
            var container = $("<div style='margin: 5px;'></div>");
            for (var i = 0; i < buttons.length; i++) {
                var btn = $("<button class='" + buttons[i].btnclass + "'title='" + buttons[i].info + "' id='" + buttons[i].id + "'info='" + buttons[i].info + "' onClickFn='" + buttons[i].onClickFn + "' args='" + buttons[i].args + "'>" +
                    "<span id='span" + buttons[i].id + "' class='" + buttons[i].spanclass + "' info='" + buttons[i].info + "'></span></button>");
                container.append(btn);
                // btn.on('mouseover', function (event) {
                //     var el = event.target;
                //     var info = $('#' + el.id).attr("info");
                //     var spanId = el.id;
                //     if (spanId.indexOf("span") == -1) {
                //         spanId = "span" + spanId;
                //     }
                //     var spanclass = $('#' + spanId).attr("class");
                //     info = "Button <span class='" + spanclass + "'></span> " + info;
                //
                //     me.invokeAlert('success', info);
                //     // $(buttons[i].onClickFn)[0](buttons[i].info);
                // });
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

    me.getPrintPage = function () {
        if (type == 'quick' || type == 'important' || type == 'short' || type == 'long' || type == 'all') {
            me.printQuickTasks();
        }
        else if (type == 'foreign' || type == 'local') {
            me.printForeignBriefs();
        }
    }

    me.printForeignBriefs = function () {
        var titlePage = "";
        if (type == 'local') {
            titlePage = '<h3>' + me.rowData["scheme_name"] + '</h3>';
        }
        if (type == 'foreign') {
            titlePage = '<h3>' + me.rowData.project_name + '</h3>';
        }
        var documentBody = me.getForeignBriefsBodyHTML();
        var printWindow = window.open('', '', 'height=800,width=1000');
        printWindow.document.write('<html><head><title>' + me.rowData.project_name + '</title>');
        printWindow.document.write('<meta name="viewport" content="width=device-width, initial-scale=1">');
        printWindow.document.write('<style> @media print{@page{ size:A4;margin-top: 2.5cm; margin-bottom: 2.5cm; margin-right: 2cm; margin-left: 2cm;} h1 {page-break-before: always;} table, th, td {border: 1px solid black;border-collapse: collapse;}</style>');
        printWindow.document.write('</head><body >');
        printWindow.document.write(titlePage);
        printWindow.document.write(documentBody.get(0).outerHTML);

        printWindow.document.write('</body></html>');
        printWindow.document.close();
        printWindow.print();
    }

    me.printQuickTasks = function () {
        var titlePage = '<h3>' + title + '</h3>';
        var documentBody = me.getMeetingTable(me.rowData);
        var printWindow = window.open('', '', 'height=800,width=1000');
        printWindow.document.write('<html><head><title>' + title + '</title>');
        printWindow.document.write('<meta name="viewport" content="width=device-width, initial-scale=1">');
        printWindow.document.write('<style> @media print{@page{ size:A4;margin-top: 2.5cm; margin-bottom: 2.5cm; margin-right: 2cm; margin-left: 2cm;} h1 {page-break-before: always;} table, th, td {border: 1px solid black;border-collapse: collapse;}</style>');
        printWindow.document.write('</head><body >');
        printWindow.document.write(titlePage);
        printWindow.document.write(documentBody.get(0).outerHTML);

        printWindow.document.write('</body></html>');
        printWindow.document.close();
        printWindow.print();
    }

    me.getForeignBriefsBodyHTML = function () {
        var row = me.rowData;
        var tableElem = $("<table style='width: 100%'></table>");
        var tBodyElem = $('<tbody  style="width: 100%"></tbody>');
        for (var key in row) {
            if (key == 'id' || key == 'uid' || key == 'boundindex' || key == 'uniqueid' || key == 'visibleindex' || key == 'serial') {
            } else {
                var keyValue = row[key];
                if (key == 'due_date' || key == 'assignment_date' || key == 'task_date' || key == 'meeting_date'
                    || key == 'loan_effectiveness_date' || key == 'loan_closing_date' || key == 'loan_negotiation_date'
                    || key == 'loan_signing_date') {
                    keyValue = me.removeGMTFromDate(row[key])
                    // var testDate = new Date(keyValue);
                    // keyValue = testDate.toLocaleDateString("en-US") + ' - ' + testDate.toLocaleTimeString('ur-PK');
                }
                var bRow = $("<tr></tr>");
                var rName = $("<td style='width: 30%; color: darkgreen;'>" + me.getColumnTitle(key) + "</td>");
                var rValue = $("<td style='width: 70%;'>" + keyValue + "</td>");
                bRow.append(rName);
                bRow.append(rValue);
                tBodyElem.append(bRow);
            }
        }
        tableElem.append(tBodyElem);
        return tableElem;
    }

    me.quickTasksToolbar = function (toolbar) {
        try {
            var buttons = [
                {
                    id: "btnViewForm",
                    btnclass: "btn btn-success",
                    info: "Used for view form",
                    spanclass: 'fa fa-check-square-o',
                    onClickFn: "quickToolbarButtonClick",
                    args: '{"type":"form"}'
                },
                {
                    id: "btnAddRecord",
                    btnclass: "btn btn-success",
                    info: "Used for adding new record",
                    spanclass: 'fa fa-plus-square-o',
                    onClickFn: "quickToolbarButtonClick",
                    args: '{"type":"add"}'
                }, {
                    id: "btnEditRecord",
                    btnclass: "btn btn-success",
                    info: "Used for editing selected Record",
                    spanclass: 'fa fa-pencil-square-o',
                    onClickFn: "quickToolbarButtonClick",
                    args: '{"type":"edit"}'
                }, {
                    id: "btnDeleteRecord",
                    btnclass: "btn btn-success",
                    info: "Used for deleting selected Record",
                    spanclass: 'fa fa-trash-o',
                    onClickFn: "quickToolbarButtonClick",
                    args: '{"type":"delete"}'
                }, {
                    id: "btnEmail",
                    btnclass: "btn btn-success",
                    info: "Used for email selected record(s)",
                    spanclass: 'fa fa-share',
                    onClickFn: "quickToolbarButtonClick",
                    args: '{"type":"email"}'
                }, {
                    id: "btnSMS",
                    btnclass: "btn btn-success",
                    info: "Used for sms selected record(s)",
                    spanclass: 'fa fa fa-envelope-o',
                    onClickFn: "quickToolbarButtonClick",
                    args: '{"type":"sms"}'
                }
            ];
            var container = $("<div style='margin: 5px;'></div>");
            for (var i = 0; i < buttons.length; i++) {
                var btn = $("<button class='" + buttons[i].btnclass + "'title='" + buttons[i].info + "' id='" + buttons[i].id + "'info='" + buttons[i].info + "' onClickFn='" + buttons[i].onClickFn + "' args='" + buttons[i].args + "'>" +
                    "<span id='span" + buttons[i].id + "' class='" + buttons[i].spanclass + "' info='" + buttons[i].info + "'></span></button>");

                container.append(btn);
                // btn.on('mouseover', function (event) {
                //     var el = event.target;
                //     var info = $('#' + el.id).attr("info");
                //     var spanId = el.id;
                //     if (spanId.indexOf("span") == -1) {
                //         spanId = "span" + spanId;
                //     }
                //     var spanclass = $('#' + spanId).attr("class");
                //     info = "Button <span class='" + spanclass + "'></span> " + info;
                //
                //     me.invokeAlert('success', info);
                //     // $(buttons[i].onClickFn)[0](buttons[i].info);
                // });
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

    me.invokeAlert = function (type, text) {
        $('#alertText').html(text);
        var aClass = (type == '' ? '' : me.alertClasses[type]);
        $('#alertClass').removeClass().addClass(aClass);
    }

    me.callListToolbarButtonClick = function (args) {
        var type = args.type;
        if (type == 'add') {
            var url = '/admin_meetings/meeting_management/tblusers/add/?next=';
            me.redirectWithShortUrl(url);
        }
        if (type == 'edit') {
            if (me.rowData) {
                var recordId = me.rowData["id"];
                var url = '/admin_meetings/meeting_management/tblusers/' + recordId + '/change/?next=';
                me.redirectWithShortUrl(url);
            } else {
                alert('Please select a row first.');
            }
        }
        if (type == 'delete') {
            if (me.rowData) {
                var recordId = me.rowData["id"];
                var url = '/admin_meetings/meeting_management/tblusers/' + recordId + '/delete/?next=';
                me.redirectWithShortUrl(url);
            } else {
                alert('Please select a row first.');
            }
        }
        if (type == 'form') {
            if (me.rowData) {
                // document.getElementById('lblFormTitle').innerText = title;
                me.getMeetingForm(me.rowData);
                $("#recordFormModal").modal("show");
            } else {
                alert('Please select a row first.');
            }
        }
        if (type == 'sms') {
            if (me.rowData) {
                var contact = me.rowData["Name"] + '\n' + me.rowData["Designation"] + '\n' + me.rowData["Contact No"] + '\n' + me.rowData["Email Id"];
                $("#txtSMSBody").val(contact);
                $("#smsModal").modal("show");
            } else {
                alert('Please select a row first.');
            }
        }
        if (type == 'email') {
            if (me.rowData) {
                var contact = me.rowData["Name"] + '<br>' + me.rowData["Designation"] + '<br>' + me.rowData["Contact No"] + '<br>' + me.rowData["Email Id"];
                $("#txtEmailBody").jqxEditor().val(contact);
                $("#emailModal").modal("show");
            } else {
                alert('Please select a row first.');
            }
        }
    }

    me.foreignBriefsToolbarButtonClick = function (args) {
        var type = args.type;
        if (type == 'add') {
            $.ajax({
                url: me.shortenUrlApi,
                type: 'POST',
                contentType: me.contentType,
                data: '{ longUrl: "' + window.location.href + '"}',
                success: function (response) {
                    var shortenUrl = response.id;
                    window.location.href = '/admin_meetings/meeting_management/tblforeignbriefs/add/?next=' + shortenUrl;
                }
            });
        }
        if (type == 'edit') {
            if (me.rowData) {
                var recordId = me.rowData.id;
                $.ajax({
                    url: me.shortenUrlApi,
                    type: 'POST',
                    contentType: me.contentType,
                    data: '{ longUrl: "' + window.location.href + '"}',
                    success: function (response) {
                        var shortenUrl = response.id;
                        window.location.href = '/admin_meetings/meeting_management/tblforeignbriefs/' + recordId + '/change/?next=' + shortenUrl;
                    }
                });
            } else {
                alert('Please select a row first.');
            }
        }
        if (type == 'delete') {
            if (me.rowData) {
                var recordId = me.rowData.id;
                $.ajax({
                    url: me.shortenUrlApi,
                    type: 'POST',
                    contentType: me.contentType,
                    data: '{ longUrl: "' + window.location.href + '"}',
                    success: function (response) {
                        var shortenUrl = response.id;
                        window.location.href = '/admin_meetings/meeting_management/tblforeignbriefs/' + recordId + '/delete/?next=' + shortenUrl;
                    }
                });
            } else {
                alert('Please select a row first.');
            }
        }
        if (type == 'form') {
            if (me.rowData) {
                // document.getElementById('lblFormTitle').innerText = title;
                me.getMeetingForm(me.rowData);
                $("#recordFormModal").modal("show");
            } else {
                alert('Please select a row first.');
            }
        }
        if (type == 'print') {
            if (me.rowData) {
                me.printForeignBriefs();
            } else {
                alert('Please select a row first.');
            }
        }
        if (type == 'sms') {
            if (me.rowData) {
                var msgText = "Scheme: " + me.rowData["project_name"] + "\n";
                msgText = msgText + "Donor Agency: " + me.rowData["donor_agency"] + "\n";
                msgText = msgText + "Funding Mode: " + me.rowData["funding_mode"] + "\n";
                msgText = msgText + "Local Share: " + me.rowData["local_share"] + "\n";
                msgText = msgText + "Foreign Share: " + me.rowData["foreign_share"] + "\n";
                msgText = msgText + "Total Cost: " + me.rowData["total_cost"] + "\n";
                msgText = msgText + "Duration: " + me.rowData["duration"] + "\n";
                msgText = msgText + "Implementing Agency: " + me.rowData["implementing_agency"] + "\n";
                msgText = msgText + "Loan Effectiveness Date: " + me.removeGMTFromDate(me.rowData["loan_effectiveness_date"]) + "\n";
                msgText = msgText + "Loan Closing Date: " + me.rowData["loan_closing_date"] + "\n";
                msgText = msgText + "Loan Negotiation Date: " + me.rowData["loan_negotiation_date"] + "\n";
                msgText = msgText + "Loan Signing Date: " + me.rowData["loan_signing_date"] + "\n";
                $("#txtSMSBody").val(msgText);
                $("#smsModal").modal("show");
            } else {
                alert('Please select a row first.');
            }
        }
        if (type == 'email') {
            if (me.rowData) {
                // me.getMeetingForm(me.rowData);
                // var schemeTableHTML = document.getElementById('tblMeetingDetail').innerHTML;

                var msgText = "<b>Scheme: </b>" + me.rowData["project_name"].replace('&', ' and ') + "<br>";
                msgText = msgText + "<b>Donor Agency:</b> " + me.rowData["donor_agency"].replace('&', ' and ') + "<br>";
                msgText = msgText + "<b>Funding Mode:</b> " + me.rowData["funding_mode"].replace('&', ' and ') + "<br>";
                msgText = msgText + "<b>Local Share:</b> " + me.rowData["local_share"] + "<br>";
                msgText = msgText + "<b>Foreign Share:</b> " + me.rowData["foreign_share"] + "<br>";
                msgText = msgText + "<b>Total Cost:</b> " + me.rowData["total_cost"] + "<br>";
                msgText = msgText + "<b>Duration:</b> " + me.rowData["duration"] + "<br>";
                msgText = msgText + "<b>Implementing Agency:</b> " + me.rowData["implementing_agency"].replace('&', ' and ') + "<br>";
                msgText = msgText + "<b>Loan Effectiveness Date:</b> " + me.removeGMTFromDate(me.rowData["loan_effectiveness_date"]) + "<br>";
                msgText = msgText + "<b>Loan Closing Date:</b> " + me.removeGMTFromDate(me.rowData["loan_closing_date"]) + "<br>";
                msgText = msgText + "<b>Loan Negotiation Date:</b> " + me.removeGMTFromDate(me.rowData["loan_negotiation_date"]) + "<br>";
                msgText = msgText + "<b>Loan Signing Date:</b> " + me.removeGMTFromDate(me.rowData["loan_signing_date"]) + "<br>";

                $("#txtEmailBody").jqxEditor().val(msgText);
                $("#emailModal").modal("show");
            } else {
                alert('Please select a row first.');
            }
        }
    }

    me.localBriefsToolbarButtonClick = function (args) {
        var type = args.type;
        if (type == 'add') {
            $.ajax({
                url: me.shortenUrlApi,
                type: 'POST',
                contentType: me.contentType,
                data: '{ longUrl: "' + window.location.href + '"}',
                success: function (response) {
                    var shortenUrl = response.id;
                    window.location.href = '/admin_meetings/meeting_management/tbllocalbriefs/add/?next=' + shortenUrl;
                }
            });
        }
        if (type == 'edit') {
            if (me.rowData) {
                var recordId = me.rowData.id;
                $.ajax({
                    url: me.shortenUrlApi,
                    type: 'POST',
                    contentType: me.contentType,
                    data: '{ longUrl: "' + window.location.href + '"}',
                    success: function (response) {
                        var shortenUrl = response.id;
                        window.location.href = '/admin_meetings/meeting_management/tbllocalbriefs/' + recordId + '/change/?next=' + shortenUrl;
                    }
                });
            } else {
                alert('Please select a row first.');
            }
        }
        if (type == 'form') {
            if (me.rowData) {
                // document.getElementById('lblFormTitle').innerText = title;
                me.getMeetingForm(me.rowData);
                $("#recordFormModal").modal("show");
            } else {
                alert('Please select a row first.');
            }
        }
        if (type == 'print') {
            if (me.rowData) {
                me.printForeignBriefs();
            } else {
                alert('Please select a row first.');
            }
        }
        if (type == 'sms') {
            if (me.rowData) {
                var msgText = "Scheme: " + me.rowData["Scheme Name"] + "\n";
                msgText = msgText + "GS No: " + me.rowData["GS No"] + "\n";
                msgText = msgText + "Main Sector: " + me.rowData["Main Sector"] + "\n";
                msgText = msgText + "Sector: " + me.rowData["Sector"] + "\n";
                msgText = msgText + "Type: " + me.rowData["Type"] + "\n";
                msgText = msgText + "Approval: " + me.rowData["Approval"] + "\n";
                msgText = msgText + "Total Cost: " + me.rowData["Total Cost"] + "\n";
                msgText = msgText + "Allocation: " + me.rowData["Allocation"] + "\n";
                msgText = msgText + "Release: " + me.rowData["Release"] + "\n";
                msgText = msgText + "Utilization: " + me.rowData["Utilization"] + "\n";
                msgText = msgText + "Local Capital: " + me.rowData["Local Capital"] + "\n";
                msgText = msgText + "Local Revenue: " + me.rowData["Local Revenue"] + "\n";
                msgText = msgText + "Total Capital: " + me.rowData["Total Capital"] + "\n";
                msgText = msgText + "Total Revenue: " + me.rowData["Total Revenue"] + "\n";
                msgText = msgText + "Expense Upto June: " + me.rowData["Expense Upto June"] + "\n";
                msgText = msgText + "Projection One: " + me.rowData["Projection One"] + "\n";
                msgText = msgText + "Projection Two: " + me.rowData["Projection Two"] + "\n";
                msgText = msgText + "Throw Forward: " + me.rowData["Throw Forward"] + "\n";
                $("#txtSMSBody").val(msgText);
                $("#smsModal").modal("show");
            } else {
                alert('Please select a row first.');
            }
        }
        if (type == 'email') {
            if (me.rowData) {
                me.getMeetingForm(me.rowData);
                var schemeTableHTML = document.getElementById('tblMeetingDetail').innerHTML;
                $("#txtEmailBody").jqxEditor().val(schemeTableHTML);
                $("#emailModal").modal("show");
            } else {
                alert('Please select a row first.');
            }
        }
        if (type == 'pt') {
            // var pt = $("#divPTModal");
            // pt.empty();
            me.createFlexMonsterPivotTable(me.gridData, [{"uniqueName": "Sector"}], [{"uniqueName": "Type"}], [{
                "uniqueName": "Total Cost",
                "aggregation": "sum"
            }]);
            $("#ptModal").modal("show");
        }
    }

    me.quickToolbarButtonClick = function (args) {
        var type = args.type;
        if (type == 'add') {
            var url = '/admin_meetings/meeting_management/tblquicktasks/add/?next=';
            me.redirectWithShortUrl(url);
        }
        if (type == 'edit') {
            if (me.rowData) {
                var recordId = me.rowData.id;
                var url = '/admin_meetings/meeting_management/tblquicktasks/' + recordId + '/change/?next=';
                me.redirectWithShortUrl(url);
            } else {
                alert('Please select a row first.');
            }
        }
        if (type == 'delete') {
            if (me.rowData) {
                var recordId = me.rowData.id;
                var url = '/admin_meetings/meeting_management/tblquicktasks/' + recordId + '/delete/?next=';
                me.redirectWithShortUrl(url);
            } else {
                alert('Please select a row first.');
            }
        }
        if (type == 'form') {
            if (me.rowData) {
                var tblHistory = $('#dynamicTable');
                tblHistory.empty();
                me.getMeetingForm(me.rowData);
                $("#recordFormModal").modal("show");
            } else {
                alert('Please select a row first.');
            }
        }
        if (type == 'sms') {
            if (me.rowData) {
                var task = 'Task:' + me.rowData.task_name;
                $("#txtSMSBody").val(task);
                $("#smsModal").modal("show");
            } else {
                alert('Please select a row first.');
            }
        }
        if (type == 'email') {
            if (me.rowData) {
                var task = 'Task:' + me.rowData.task_name;
                $("#txtEmailBody").jqxEditor().val(task);
                $("#emailModal").modal("show");
            } else {
                alert('Please select a row first.');
            }
        }
    }

    me.meetingsToolbarButtonClick = function (args) {
        var type = args.type;
        if (type == 'users') {
            if (me.rowData) {
                var id = me.rowData.id;
                me.getParticipantsList(id)
            } else {
                alert('Please select a row first.');
            }
        }
        if (type == 'add') {
            var url = '/admin_meetings/meeting_management/tblmeetings/add/?next=';
            me.redirectWithShortUrl(url);
        }
        if (type == 'edit') {
            if (me.rowData) {
                var recordId = me.rowData.id;
                var url = '/admin_meetings/meeting_management/tblmeetings/' + recordId + '/change/?next=';
                me.redirectWithShortUrl(url);
            } else {
                alert('Please select a row first.');
            }
        }
        if (type == 'delete') {
            if (me.rowData) {
                var recordId = me.rowData.id;
                var url = '/admin_meetings/meeting_management/tblmeetings/' + recordId + '/delete/?next=';
                me.redirectWithShortUrl(url);
            } else {
                alert('Please select a row first.');
            }
        }
        if (type == 'initiative') {
            var url = '/admin_meetings/meeting_management/meetingsinitiatives/add/?next=';
            me.redirectWithShortUrl(url);
        }
        //initiative
        if (type == 'sms') {
            if (me.rowData) {
                var meeting = 'Meeting Agenda:' + me.rowData["Meeting Agenda"] + '\n';
                meeting = meeting + "Meeting Venue:" + me.rowData["Venue"] + '\n';
                meeting = meeting + "Meeting Date:" + me.removeGMTFromDate(me.rowData["Meeting Date"]) + '\n';
                $("#txtSMSBody").val(meeting);
                $("#smsModal").modal("show");
            } else {
                alert('Please select a row first.');
            }
        }
        if (type == 'email') {
            if (me.rowData) {
                var meeting = '<h3>Meeting Agenda:' + me.rowData["Meeting Agenda"] + '</h3><br>';
                meeting = meeting + "<b>Meeting Venue:</b>" + me.rowData["Venue"] + '<br>';
                meeting = meeting + "<b>Meeting Date:</b>" + me.removeGMTFromDate(me.rowData["Meeting Date"]) + '<br>';
                $("#txtEmailBody").jqxEditor().val(meeting);
                $("#emailModal").modal("show");
            } else {
                alert('Please select a row first.');
            }
        }
    }
    me.toolbarButtonClick = function (args) {
        var type = args.type;
        if (type == 'add') {
            var url = '/admin_meetings/meeting_management/meetingsinitiatives/add/?next=';
            me.redirectWithShortUrl(url);
        }
        if (type == 'edit') {
            if (me.rowData) {
                var recordId = me.rowData.id;
                var url = '/admin_meetings/meeting_management/meetingsinitiatives/' + recordId + '/change/?next=';
                me.redirectWithShortUrl(url);
            } else {
                alert('Please select a row first.');
            }
        }
        if (type == 'delete') {
            if (me.rowData) {
                var recordId = me.rowData.id;
                var url = '/admin_meetings/meeting_management/meetingsinitiatives/' + recordId + '/delete/?next=';
                me.redirectWithShortUrl(url);
            } else {
                alert('Please select a row first.');
            }
        }
        if (type == 'history') {
            if (me.rowData) {
                var recordId = me.rowData.id;
                me.getHistoryDetails(recordId);
            } else {
                alert('Please select a row first.');
            }
        }
        if (type == 'form') {
            if (me.rowData) {
                $("#recordFormModal").modal("show");
                me.collapseAllPanels();

            } else {
                alert('Please select a row first.');
            }
        }
        if (type == 'picture') {
            if (me.rowData) {
                me.getMeetingPictures();
            } else {
                alert('Please select a row first.');
            }
        }
        if (type == 'documents') {
            if (me.rowData) {
                me.getMeetingDocuments();
            } else {
                alert('Please select a row first.');
            }
        }
        if (type == 'sms') {
            if (me.rowData) {
                var meetingAgenda = 'Meeting Agenda:' + me.rowData["Meeting Agenda"] + '\n';
                meetingAgenda = meetingAgenda + "Assignment:" + me.rowData["Assignment"] + '\n';
                meetingAgenda = meetingAgenda + "Due Date:" + me.removeGMTFromDate(me.rowData["Due Date"]) + '\n';
                $("#txtSMSBody").val(meetingAgenda);
                $("#smsModal").modal("show");
            } else {
                alert('Please select a row first.');
            }
        }
        if (type == 'email') {
            if (me.rowData) {
                var meetingAgenda = '<h3>Meeting Agenda:' + me.rowData["Meeting Agenda"] + '</h3><br>';
                meetingAgenda = meetingAgenda + "<b>Assignment:</b>" + me.rowData["Assignment"] + '<br>';
                meetingAgenda = meetingAgenda + "<b>Due Date:</b>" + me.removeGMTFromDate(me.rowData["Due Date"]) + '<br>';
                $("#txtEmailBody").jqxEditor().val(meetingAgenda);
                $("#emailModal").modal("show");
            } else {
                alert('Please select a row first.');
            }
        }
    }

    me.getMeetingPictures = function () {
        try {
            var strPictures = me.rowData["Pictures"];
            var arrPictures = strPictures.split(';');
            var arrItems = [];
            for (var i = 0; i < arrPictures.length; i++) {
                var pic = arrPictures[i];
                if (pic) {
                    arrItems.push({src: meeting_pics_path + '/' + pic, w: 800, h: 600});
                }
            }
            if (arrItems.length > 0) {
                var pswpElement = document.querySelectorAll('.pswp')[0];
                var options = {
                    showAnimationDuration: 1,
                    hideAnimationDuration: 1
                };
                var gallery = new PhotoSwipe(pswpElement, PhotoSwipeUI_Default, arrItems, options);
                gallery.init();
            } else {
                alert('No pictures attached to this meeting.');
            }
        } catch (e) {
            alert('No picture(s) found.');
        }
    }

    me.getMeetingDocuments = function () {
        try {
            var table = $("#tblDocuments");
            table.empty();
            var strDocuments = me.rowData["Attachments"];
            var arrDocuments = strDocuments.split(';');
            if (arrDocuments.length > 1) {
                var tBodyElem = $('<tbody  style="width: 100%"></tbody>');
                for (var i = 0; i < arrDocuments.length; i++) {
                    var doc = arrDocuments[i];
                    if (doc) {
                        var tr = $('<tr style="width: 100%"></tr>');
                        var td = $('<td style="width: 100%"></td>');
                        var a = $("<a href='" + meeting_docs_path + '/' + doc + "' target='_blank'>" + doc + "</a>");
                        td.append(a);
                        tr.append(td)
                        tBodyElem.append(tr);
                    }
                }
                table.append(tBodyElem);
                $("#documentsModal").modal("show");
            } else {
                alert('No document attached.');
            }
        } catch (e) {
            alert('No Document(s) found.');
        }
    }

    me.recordFormModalOnLoad = function () {

        $("#recordFormModal").on('shown.bs.modal', function () {
            var selectedRowSerial = me.rowData["serial"];
            var sectionOffset = $('#content_' + selectedRowSerial).offset();
            var position = $(window).scrollTop();
            $('#recordFormModal').scrollTop(sectionOffset.top - 100);

        });
    }

    me.collapseAllPanels = function () {
        var selectedRowSerial = me.rowData["serial"];
        for (var i = 0; i < me.gridData.length; i++) {
            var serial = me.gridData[i].serial;
            if (selectedRowSerial == serial) {
                $('#content_' + serial).collapse('show');
            } else {
                $('#content_' + serial).collapse('hide');
            }
        }
    }

    me.getMeetingTable = function (row) {
        var tableElem = $("<table style='width: 100%'></table>");
        var tBodyElem = $('<tbody  style="width: 100%"></tbody>');
        var hRowElem = $("<tr></tr>");
        // var hRowNameElem = $("<th>Field Name</th>");
        // var hRowValueElem = $("<th>Field Value</th>");
        // hRowElem.append(hRowNameElem);
        // hRowElem.append(hRowValueElem);
        // tBodyElem.append(hRowElem);
        for (var key in row) {
            if (key == 'id' || key == 'uid' || key == 'boundindex' || key == 'uniqueid' || key == 'visibleindex' || key == 'serial') {
            } else {
                var keyValue = row[key];
                if (key == 'Meeting Date' || key == 'Due Date' || key == 'task_date' || key == 'meeting_date'
                    || key == 'loan_effectiveness_date' || key == 'loan_closing_date' || key == 'loan_negotiation_date'
                    || key == 'loan_signing_date') {
                    keyValue = me.removeGMTFromDate(row[key])
                }
                keyValue = (keyValue) ? keyValue : "";
                var bRow = $("<tr></tr>");
                var rName = $("<td style='width: 30%; color: darkgreen;'>" + me.getColumnTitle(key) + "</td>");
                if (key == 'Pictures') {
                    if (keyValue) {
                        var path = uploaded_path + '/' + keyValue
                        var rValue = $("<td style='width: 70%;'><img width='250' height='250' src=" + path + "></td>");
                    } else {
                        var rValue = $("<td style='width: 70%;'>" + keyValue + "</td>");
                    }
                } else {
                    var rValue = $("<td style='width: 70%;'>" + keyValue + "</td>");
                }
                bRow.append(rName);
                bRow.append(rValue);
                tBodyElem.append(bRow);
            }
        }
        tableElem.append(tBodyElem);
        return tableElem;
    }

    me.getMeetingInitiativesForm = function () {
        var row = me.rowData;
        if (type == 'meetings') {
            $("#myPleaseWait").modal("show");
            var url = 'initiatives_list?meeting_id=' + row['id'];
            $.ajax({
                type: 'GET',
                dataType: 'text',
                url: url,
                timeout: 9000000,
                success: function (data) {
                    $("#myPleaseWait").modal("hide");
                    $("#recordFormModal").modal("show");
                    var initiatives_data = eval('(' + JXG.decompress(data) + ')');

                    var tableDiv = $("#tblMeetingDetail");
                    tableDiv.empty();
                    var tableElem = $("<table style='width: 100%'></table>");
                    for (var key in row) {
                        if (key == 'id' || key == 'serial' || key == 'uid' || key == 'boundindex' || key == 'uniqueid' || key == 'visibleindex' || key == 'Proceedings') {
                        } else {
                            var keyValue = row[key];
                            if (key == 'Meeting Date') {
                                keyValue = me.removeGMTFromDate(row[key])
                            }
                            keyValue = (keyValue) ? keyValue : "";
                            var bRow = $("<tr></tr>");
                            var rName = $("<td style='width: 30%; color: darkgreen;'>" + me.getColumnTitle(key) + "</td>");
                            var rValue = null;
                            if (key == 'Decisions') {
                                rValue = $("<td style='width: 70%;'><div style='max-height: 350px;overflow: auto;'>" + keyValue + "</div></td>");
                            } else if (key == 'Attachments') {
                                var arrDocuments = keyValue.split(';');
                                if (arrDocuments.length > 1) {
                                    var rValue = $("<td style='width: 70%;'></td>");
                                    for (var i = 0; i < arrDocuments.length; i++) {
                                        var doc = arrDocuments[i];
                                        if (doc) {
                                            var a = $("<div><a href='" + meeting_docs_path + '/' + doc + "' target='_blank'>" + doc + "</a></div>");
                                            rValue.append(a);
                                        }
                                    }
                                } else {
                                    var rValue = $("<td style='width: 70%;'>" + keyValue + "</td>");
                                }
                            } else if (key == 'Pictures') {
                                var arrDocuments = keyValue.split(';');
                                if (arrDocuments.length > 1) {
                                    var rValue = $("<td style='width: 70%;'></td>");
                                    for (var i = 0; i < arrDocuments.length; i++) {
                                        var doc = arrDocuments[i];
                                        if (doc) {
                                            var a = $("<div><a href='" + meeting_pics_path + '/' + doc + "' target='_blank'>" + doc + "</a></div>");
                                            rValue.append(a);
                                        }
                                    }
                                } else {
                                    var rValue = $("<td style='width: 70%;'>" + keyValue + "</td>");
                                }
                            } else {
                                rValue = $("<td style='width: 70%;'>" + keyValue + "</td>");
                            }
                            bRow.append(rName);
                            bRow.append(rValue);
                            tableElem.append(bRow);
                        }
                    }
                    var phRow = $("<tr></tr>");
                    var ph = $("<td style='color: darkgreen;' >Proceedings</td>");
                    phRow.append(ph);
                    var proceedings = $("<td style='color: darkgreen;' ></td>");
                    for (var i = 0; i < initiatives_data.length; i++) {
                        var initiativeRow = initiatives_data[i];
                        var initiativeLink = $("<div ><a href=\"http://pnddch.info/mm/?type=all&id=" + initiativeRow['id'] + " \" target=\"_blank\">" + (i + 1) + " - " + initiativeRow['assignment'] + "</a></div>")
                        proceedings.append(initiativeLink);
                    }
                    phRow.append(proceedings);
                    tableElem.append(phRow);
                    tableDiv.append(tableElem);

                },
                error: function (xhr, ajaxOptions, thrownError) {
                    $("#myPleaseWait").modal("hide");
                },
            });
        }
    }

    me.getForeignBriefsTable = function () {
        var tableElem = $("<table style='width: 100%' ></table>");

        var trPName = $("<tr></tr>");
        var tdPName = $("<td width='40%'><b>Sceme</b></td>");
        var tdPNameVal = $("<td colspan='3' width='60%'>" + me.rowData["Scheme"] + "</td>");
        trPName.append(tdPName);
        trPName.append(tdPNameVal);
        tableElem.append(trPName);

        var trPName = $("<tr></tr>");
        var tdPName = $("<td width='40%'><b>Donor Agency</b></td>");
        var tdPNameVal = $("<td colspan='3' width='60%'>" + me.rowData["Donor Agency"] + "</td>");
        trPName.append(tdPName);
        trPName.append(tdPNameVal);
        tableElem.append(trPName);

        var trPName = $("<tr></tr>");
        var tdPName = $("<td width='40%'><b>Implementing Agency</b></td>");
        var tdPNameVal = $("<td colspan='3' width='60%'>" + me.parseNullString(me.rowData["Implementing Agency"]) + "</td>");
        trPName.append(tdPName);
        trPName.append(tdPNameVal);
        tableElem.append(trPName);

        var trProjectArea = $("<tr></tr>");
        var tdProjectArea = $("<td width='40%'><b>Total Cost</b> (MUSD)</td>");
        var tdProjectAreaVal = $("<td colspan='3' width='60%'>" + me.parseNullString(me.rowData["Total Cost"]) + "</td>");
        trProjectArea.append(tdProjectArea);
        trProjectArea.append(tdProjectAreaVal);
        tableElem.append(trProjectArea);

        var trPName = $("<tr></tr>");
        var tdPName = $("<td width='40%'><b>Foreign Share</b> (MUSD)</td>");
        var tdPNameVal = $("<td colspan='3' width='60%'>" + me.parseNullString(me.rowData["Foreign Cost"]) + "</td>");
        trPName.append(tdPName);
        trPName.append(tdPNameVal);
        tableElem.append(trPName);

        var trPName = $("<tr></tr>");
        var tdPName = $("<td width='40%'><b>Local Share</b> (MUSD)</td>");
        var tdPNameVal = $("<td colspan='3' width='60%'>" + me.parseNullString(me.rowData["Local Cost"]) + "</td>");
        trPName.append(tdPName);
        trPName.append(tdPNameVal);
        tableElem.append(trPName);

        var trProjectArea = $("<tr></tr>");
        var tdProjectArea = $("<td width='40%'><b>Project Area</b></td>");
        var tdProjectAreaVal = $("<td colspan='3' width='60%'>" + me.parseNullString(me.rowData["District"]) + "</td>");
        trProjectArea.append(tdProjectArea);
        trProjectArea.append(tdProjectAreaVal);
        tableElem.append(trProjectArea);

        var trProjectArea = $("<tr></tr>");
        var tdProjectArea = $("<td width='40%'><b>Funding Mode</b></td>");
        var tdProjectAreaVal = $("<td colspan='3' width='60%'>" + me.parseNullString(me.rowData["Funding Mode"]) + "</td>");
        trProjectArea.append(tdProjectArea);
        trProjectArea.append(tdProjectAreaVal);
        tableElem.append(trProjectArea);

        var trProjectArea = $("<tr></tr>");
        var tdProjectArea = $("<td width='40%'><b>Duration(Years)</b></td>");
        var tdProjectAreaVal = $("<td colspan='3' width='60%'>" + me.parseNullString(me.rowData["Duration(Years)"]) + "</td>");
        trProjectArea.append(tdProjectArea);
        trProjectArea.append(tdProjectAreaVal);
        tableElem.append(trProjectArea);

        var trProjectArea = $("<tr></tr>");
        var tdProjectArea = $("<td width='40%'><b>Loan Negot. Date</b></td>");
        var tdProjectAreaVal = $("<td colspan='3' width='60%'>" + me.removeGMTFromDate(me.rowData["Loan Negot. Date"]) + "</td>");
        trProjectArea.append(tdProjectArea);
        trProjectArea.append(tdProjectAreaVal);
        tableElem.append(trProjectArea);

        var trProjectArea = $("<tr></tr>");
        var tdProjectArea = $("<td width='40%'><b>Loan Signing Date</b></td>");
        var tdProjectAreaVal = $("<td colspan='3' width='60%'>" + me.removeGMTFromDate(me.rowData["Loan Signing Date"]) + "</td>");
        trProjectArea.append(tdProjectArea);
        trProjectArea.append(tdProjectAreaVal);
        tableElem.append(trProjectArea);

        var trProjectArea = $("<tr></tr>");
        var tdProjectArea = $("<td width='40%'><b>Loan Effect. Date</b></td>");
        var tdProjectAreaVal = $("<td colspan='3' width='60%'>" + me.removeGMTFromDate(me.rowData["Loan Effect. Date"]) + "</td>");
        trProjectArea.append(tdProjectArea);
        trProjectArea.append(tdProjectAreaVal);
        tableElem.append(trProjectArea);

        var trProjectArea = $("<tr></tr>");
        var tdProjectArea = $("<td width='25%'><b>Loan Closing Date</b></td>");
        var tdProjectAreaVal = $("<td colspan='3' width='75%'>" + me.removeGMTFromDate(me.rowData["Loan Closing Date"]) + "</td>");
        trProjectArea.append(tdProjectArea);
        trProjectArea.append(tdProjectAreaVal);
        tableElem.append(trProjectArea);

        var trProjectArea = $("<tr></tr>");
        var tdProjectArea = $("<td width='40%'><b>Start Date</b></td>");
        var tdProjectAreaVal = $("<td colspan='3' width='60%'>" + me.removeGMTFromDate(me.rowData["Project Start Date"]) + "</td>");
        trProjectArea.append(tdProjectArea);
        trProjectArea.append(tdProjectAreaVal);
        tableElem.append(trProjectArea);

        var trProjectArea = $("<tr></tr>");
        var tdProjectArea = $("<td width='40%'><b>End Date</b></td>");
        var tdProjectAreaVal = $("<td colspan='3' width='60%'>" + me.removeGMTFromDate(me.rowData["Project End Date"]) + "</td>");
        trProjectArea.append(tdProjectArea);
        trProjectArea.append(tdProjectAreaVal);
        tableElem.append(trProjectArea);

        var trProjectArea = $("<tr></tr>");
        var tdProjectArea = $("<td colspan='4' width='100%'><b>Description</b></td>");
        trProjectArea.append(tdProjectArea);
        tableElem.append(trProjectArea);

        var trProjectArea = $("<tr></tr>");
        var tdProjectAreaVal = $("<td colspan='4' width='100%'>" + me.parseNullString(me.rowData["Description"]) + "</td>");
        trProjectArea.append(tdProjectAreaVal);
        tableElem.append(trProjectArea);

        return tableElem;
    }

    me.getComponentsDLI = function () {
        var tableElem = $("<table style='width: 100%' ></table>");
        var trPName = $("<tr></tr>");
        var tdPName = $("<td colspan='4' >" + me.parseNullString(me.rowData["Components/DLIs"]) + "</td>");
        trPName.append(tdPName);
        tableElem.append(trPName);
        return tableElem;
    }

    me.getGanttChart = function () {
        var tableElem = $("<table style='width: 100%' ></table>");
        var trPName = $("<tr></tr>");
        var tdPName = $("<td colspan='4' ><b><a href='http://pcupiupnd.info/ppms/' target='_blank'>Gantt Chart</a></b></td>");
        trPName.append(tdPName);
        tableElem.append(trPName);
        return tableElem;
    }

    me.getFinancialProgress = function () {
        var tableElem = $("<table style='width: 100%' ></table>");
        // var tRow = $("<tr></tr>");
        // var tdPName = $("<td colspan='4' >" + me.parseNullString(me.rowData["Financial Progress"]) + "</td>");
        // var tDiv = $("<td colspan='4' style='text-align: center' ><b>Financial Progress</b></td>");
        // tRow.append(tDiv);
        // tableElem.append(tRow);

        var tRow = $("<tr></tr>");
        var tDiv = $("<td style='text-align: center; width: 25%;'><b>#</b></td>");
        var tDivA = $("<td style='text-align: center; width: 25%;' ><b>Allocation</b></td>");
        var tDivD = $("<td style='text-align: center; width: 25%;' ><b>Disbursement</b></td>");
        var tDivU = $("<td style='text-align: center; width: 25%;' ><b>Utilization</b></td>");
        tRow.append(tDiv);
        tRow.append(tDivA);
        tRow.append(tDivD);
        tRow.append(tDivU);
        tableElem.append(tRow);

        var tRow = $("<tr></tr>");
        var tDiv = $("<td style='text-align: left; width: 25%;'><b>Current Year</b></td>");
        var tDivA = $("<td style='text-align: center; width: 25%;' >" + me.parseNullString(me.rowData["CY Allocation"]) + "</td>");
        var tDivD = $("<td style='text-align: center; width: 25%;' >" + me.parseNullString(me.rowData["CY Disbursement"]) + "</td>");
        var tDivU = $("<td style='text-align: center; width: 25%;' >" + me.parseNullString(me.rowData["CY Utilization"]) + "</td>");
        tRow.append(tDiv);
        tRow.append(tDivA);
        tRow.append(tDivD);
        tRow.append(tDivU);
        tableElem.append(tRow);

        var tRow = $("<tr></tr>");
        var tDiv = $("<td style='text-align: left; width: 25%;'><b>Cumulative</b></td>");
        var tDivA = $("<td style='text-align: center; width: 25%;' >" + me.parseNullString(me.rowData["Cumulative Allocation"]) + "</td>");
        var tDivD = $("<td style='text-align: center; width: 25%;' >" + me.parseNullString(me.rowData["Cumulative Disbursement"]) + "</td>");
        var tDivU = $("<td style='text-align: center; width: 25%;' >" + me.parseNullString(me.rowData["Cumulative Utilization"]) + "</td>");
        tRow.append(tDiv);
        tRow.append(tDivA);
        tRow.append(tDivD);
        tRow.append(tDivU);
        tableElem.append(tRow);



        return tableElem;
    }

    me.getPhysicalProgress = function () {
        var tableElem = $("<table style='width: 100%' ></table>");
        var trPName = $("<tr></tr>");
        var tdPName = $("<td colspan='4' >" + me.parseNullString(me.rowData["Physical Progress"]) + "</td>");
        trPName.append(tdPName);
        tableElem.append(trPName);
        return tableElem;
    }

    me.getIssues = function () {
        var tableElem = $("<table style='width: 100%' ></table>");
        var trPName = $("<tr></tr>");
        var tdPName = $("<td colspan='4' >" + me.parseNullString(me.rowData["Issues/Way Forward"]) + "</td>");
        trPName.append(tdPName);
        tableElem.append(trPName);
        return tableElem;
    }


    me.getForeignBriefsOnePager = function () {
        var table = $("#tblMeetingDetail");
        table.empty();

        var accordion = $("<div class='panel-group' id='foreignBriefAccordion'></div>");
        var card = $("<div class='panel panel-success'></div>");
        var cardHeader = $("<div class='panel-heading' id='accrod_intro'></div>");
        var accordionTitle = $("<h5 class='panel-title'></h5>");
        var btnTitleText = $('<a style="width:100%; white-space: normal; " data-toggle="collapse" data-target="#content_intro" >Introduction</a>');
        var contentDiv = $('<div id="content_intro" class="panel-collapse collapse in"></div>');
        var contentDivBody = $('<div class="panel-body" ></div>');

        var introTable = me.getForeignBriefsTable();
        contentDivBody.append(introTable);
        contentDiv.append(contentDivBody);
        accordionTitle.append(btnTitleText);
        cardHeader.append(accordionTitle);
        card.append(cardHeader);
        card.append(contentDiv);
        accordion.append(card);

        var card = $("<div class='panel panel-success'></div>");
        var cardHeader = $("<div class='panel-heading' id='accrod_dli'></div>");
        var accordionTitle = $("<h5 class='panel-title'></h5>");
        var btnTitleText = $('<a style="width:100%; white-space: normal; " data-toggle="collapse" data-target="#content_dli" >Components / DLIs</a>');
        var contentDiv = $('<div id="content_dli" class="panel-collapse collapse"></div>');
        var contentDivBody = $('<div class="panel-body" ></div>');
        var introTable = me.getComponentsDLI();
        contentDivBody.append(introTable);
        contentDiv.append(contentDivBody);
        accordionTitle.append(btnTitleText);
        cardHeader.append(accordionTitle);
        card.append(cardHeader);
        card.append(contentDiv);
        accordion.append(card);

        var card = $("<div class='panel panel-success'></div>");
        var cardHeader = $("<div class='panel-heading' id='accrod_gantt'></div>");
        var accordionTitle = $("<h5 class='panel-title'></h5>");
        var btnTitleText = $('<a style="width:100%; white-space: normal; " data-toggle="collapse" data-target="#content_gantt" >Gantt Chart</a>');
        var contentDiv = $('<div id="content_gantt" class="panel-collapse collapse"></div>');
        var contentDivBody = $('<div class="panel-body" ></div>');
        var introTable = me.getGanttChart();
        contentDivBody.append(introTable);
        contentDiv.append(contentDivBody);
        accordionTitle.append(btnTitleText);
        cardHeader.append(accordionTitle);
        card.append(cardHeader);
        card.append(contentDiv);
        accordion.append(card);

        var card = $("<div class='panel panel-success'></div>");
        var cardHeader = $("<div class='panel-heading' id='accrod_financial'></div>");
        var accordionTitle = $("<h5 class='panel-title'></h5>");
        var btnTitleText = $('<a style="width:100%; white-space: normal; " data-toggle="collapse" data-target="#content_financial" >Financial Progress</a>');
        var contentDiv = $('<div id="content_financial" class="panel-collapse collapse"></div>');
        var contentDivBody = $('<div class="panel-body" ></div>');
        var introTable = me.getFinancialProgress();
        contentDivBody.append(introTable);
        contentDiv.append(contentDivBody);
        accordionTitle.append(btnTitleText);
        cardHeader.append(accordionTitle);
        card.append(cardHeader);
        card.append(contentDiv);
        accordion.append(card);

        var card = $("<div class='panel panel-success'></div>");
        var cardHeader = $("<div class='panel-heading' id='accrod_physical'></div>");
        var accordionTitle = $("<h5 class='panel-title'></h5>");
        var btnTitleText = $('<a style="width:100%; white-space: normal; " data-toggle="collapse" data-target="#content_physical" >Physical Progress</a>');
        var contentDiv = $('<div id="content_physical" class="panel-collapse collapse"></div>');
        var contentDivBody = $('<div class="panel-body" ></div>');
        var introTable = me.getPhysicalProgress();
        contentDivBody.append(introTable);
        contentDiv.append(contentDivBody);
        accordionTitle.append(btnTitleText);
        cardHeader.append(accordionTitle);
        card.append(cardHeader);
        card.append(contentDiv);
        accordion.append(card);

        var card = $("<div class='panel panel-success'></div>");
        var cardHeader = $("<div class='panel-heading' id='accrod_issues'></div>");
        var accordionTitle = $("<h5 class='panel-title'></h5>");
        var btnTitleText = $('<a style="width:100%; white-space: normal; " data-toggle="collapse" data-target="#content_issues" >Issues/Way Forward</a>');
        var contentDiv = $('<div id="content_issues" class="panel-collapse collapse"></div>');
        var contentDivBody = $('<div class="panel-body" ></div>');
        var introTable = me.getIssues();
        contentDivBody.append(introTable);
        contentDiv.append(contentDivBody);
        accordionTitle.append(btnTitleText);
        cardHeader.append(accordionTitle);
        card.append(cardHeader);
        card.append(contentDiv);
        accordion.append(card);

        table.append(accordion);
    }

    me.getForeignBriefsOnePagerTable = function () {
        var row = me.rowData;
        var tableElem = $("<table style='width: 100%' ></table>");

        var trPName = $("<tr></tr>");
        var tdPName = $("<td width='25%'><b>Project Name</b></td>");
        var tdPNameVal = $("<td colspan='3' width='75%'>" + me.rowData["project_name"] + "</td>");
        trPName.append(tdPName);
        trPName.append(tdPNameVal);
        tableElem.append(trPName);

        var trforeign_cost = $("<tr></tr>");
        var tdforeign_cost = $("<td width='25%'><b>Loan Amount US $</b></td>");
        var tdforeign_costVal = $("<td colspan='3' width='75%'>" + me.rowData["foreign_cost"] + "</td>");
        trforeign_cost.append(tdforeign_cost);
        trforeign_cost.append(tdforeign_costVal);
        tableElem.append(trforeign_cost);

        var trImplementingDepartments = $("<tr></tr>");
        var tdImplementingDepartments = $("<td width='25%'><b>Implementing Departments</b></td>");
        var tdImplementingDepartmentsVal = $("<td colspan='3' width='75%'>" + me.rowData["implementing_agency"] + "</td>");
        trImplementingDepartments.append(tdImplementingDepartments);
        trImplementingDepartments.append(tdImplementingDepartmentsVal);
        tableElem.append(trImplementingDepartments);

        var trProjectArea = $("<tr></tr>");
        var tdProjectArea = $("<td width='25%'><b>Project Area</b></td>");
        var tdProjectAreaVal = $("<td colspan='3' width='75%'>" + me.rowData["District"] + "</td>");
        trProjectArea.append(tdProjectArea);
        trProjectArea.append(tdProjectAreaVal);
        tableElem.append(trProjectArea);

        var trIP = $("<tr></tr>");
        var tdIP = $("<td colspan='4'><b>IMPLEMENTATION PERIOD</b></td>");
        trIP.append(tdIP);
        tableElem.append(trIP);

        var trLSD = $("<tr></tr>");
        var tdLSD = $("<td width='25%'>Loan Signing Date</td>");
        var tdLSDValue = $("<td width='25%'>" + me.removeGMTFromDate(me.rowData["loan_signing_date"]) + "</td>");
        var tdTL = $("<td width='25%'>Time-lapsed (%age)</td>");
        var tdTLVal = $("<td width='25%'>" + me.rowData["Time Lapsed prcnt"] + "</td>");
        trLSD.append(tdLSD);
        trLSD.append(tdLSDValue);
        trLSD.append(tdTL);
        trLSD.append(tdTLVal);
        tableElem.append(trLSD);


        var trLSD = $("<tr></tr>");
        var tdLSD = $("<td width='25%'>Loan Effectiveness Date</td>");
        var tdLSDValue = $("<td width='25%'>" + me.removeGMTFromDate(me.rowData["loan_effectiveness_date"]) + "</td>");
        var tdTL = $("<td width='25%'>Loan Closing Date</td>");
        var tdTLVal = $("<td width='25%'>" + me.rowData["loan_closing_date"] + "</td>");
        trLSD.append(tdLSD);
        trLSD.append(tdLSDValue);
        trLSD.append(tdTL);
        trLSD.append(tdTLVal);
        tableElem.append(trLSD);

        var trLSD = $("<tr></tr>");
        var tdLSD = $("<td width='25%'>Project Start Date</td>");
        var tdLSDValue = $("<td width='25%'>" + me.removeGMTFromDate(me.rowData["Project Start Date"]) + "</td>");
        var tdTL = $("<td width='25%'>Project Closing Date</td>");
        var tdTLVal = $("<td width='25%'>" + me.rowData["Project End Date"] + "</td>");
        trLSD.append(tdLSD);
        trLSD.append(tdLSDValue);
        trLSD.append(tdTL);
        trLSD.append(tdTLVal);
        tableElem.append(trLSD);

        var trIP = $("<tr></tr>");
        var tdIP = $("<td colspan='4'><b>CUMULATIVE DISBURSEMENTS (US$ Million)</b></td>");
        trIP.append(tdIP);
        tableElem.append(trIP);

        var trLSD = $("<tr></tr>");
        var tdLSD = $("<td width='25%'>Project Cost</td>");
        var tdLSDValue = $("<td width='25%'>" + me.rowData["total_cost"] + "</td>");
        var tdTL = $("<td width='25%'>Donor Share</td>");
        var tdTLVal = $("<td width='25%'>" + me.rowData["foreign_cost"] + "</td>");
        trLSD.append(tdLSD);
        trLSD.append(tdLSDValue);
        trLSD.append(tdTL);
        trLSD.append(tdTLVal);
        tableElem.append(trLSD);

        var trLSD = $("<tr></tr>");
        var tdLSD = $("<td width='25%'>CY Disbursement</td>");
        var tdLSDValue = $("<td width='25%'>" + me.rowData["CY Disbursement"] + "</td>");
        var tdTL = $("<td width='25%'>Cumulative Disbursement</td>");
        var tdTLVal = $("<td width='25%'>" + me.rowData["Cumulative Disbursement"] + "</td>");
        trLSD.append(tdLSD);
        trLSD.append(tdLSDValue);
        trLSD.append(tdTL);
        trLSD.append(tdTLVal);
        tableElem.append(trLSD);

        var trProjectArea = $("<tr></tr>");
        var tdProjectArea = $("<td width='25%'>Disbursement (%age)</td>");
        var tdProjectAreaVal = $("<td colspan='3' width='75%'>" + parseFloat(me.rowData["Cumulative Disbursement"] * 100) / parseFloat(me.rowData["total_cost"]) + "</td>");
        trProjectArea.append(tdProjectArea);
        trProjectArea.append(tdProjectAreaVal);
        tableElem.append(trProjectArea);

        var trIP = $("<tr></tr>");
        var tdIP = $("<td colspan='4'><b>EXPENDITURE (PKR Million)</b></td>");
        trIP.append(tdIP);
        tableElem.append(trIP);

        var trLSD = $("<tr></tr>");
        var tdLSD = $("<td width='25%'>Project Cost</td>");
        var tdLSDValue = $("<td width='25%'>" + me.rowData["total_cost"] + "</td>");
        var tdTL = $("<td width='25%'>Donor Share</td>");
        var tdTLVal = $("<td width='25%'>" + me.rowData["foreign_cost"] + "</td>");
        trLSD.append(tdLSD);
        trLSD.append(tdLSDValue);
        trLSD.append(tdTL);
        trLSD.append(tdTLVal);
        tableElem.append(trLSD);

        var trLSD = $("<tr></tr>");
        var tdLSD = $("<td width='25%'>Local Share</td>");
        var tdLSDValue = $("<td width='25%'>" + me.rowData["local_cost"] + "</td>");
        var tdTL = $("<td width='25%'>CY Allocation</td>");
        var tdTLVal = $("<td width='25%'>" + me.rowData["CY Allocation"] + "</td>");
        trLSD.append(tdLSD);
        trLSD.append(tdLSDValue);
        trLSD.append(tdTL);
        trLSD.append(tdTLVal);
        tableElem.append(trLSD);

        var trLSD = $("<tr></tr>");
        var tdLSD = $("<td width='25%'>CY Expenditure</td>");
        var tdLSDValue = $("<td width='25%'>" + me.rowData["CY Expenditure"] + "</td>");
        var tdTL = $("<td width='25%'>Cumulative Expenditure</td>");
        var tdTLVal = $("<td width='25%'>" + me.rowData["Cumulative Expenditure"] + "</td>");
        trLSD.append(tdLSD);
        trLSD.append(tdLSDValue);
        trLSD.append(tdTL);
        trLSD.append(tdTLVal);
        tableElem.append(trLSD);

        var trLSD = $("<tr></tr>");
        var tdLSD = $("<td width='25%'>%age</td>");
        var tdLSDValue = $("<td colspan='3' width='75%'></td>");
        trLSD.append(tdLSD);
        trLSD.append(tdLSDValue);
        tableElem.append(trLSD);

        return tableElem;
    }

    me.getForeignBriefsOnePagerTableTwo = function () {
        var tableElem = $("<table style='width: 100%' ></table>");

        var trPName = $("<tr></tr>");
        var tdPName = $("<td width='25%'><b>Scope and Objectives</b></td>");
        var tdPNameVal = $("<td width='75%'>" + me.rowData["Scope"] + "</td>");
        trPName.append(tdPName);
        trPName.append(tdPNameVal);
        tableElem.append(trPName);


        var trPName = $("<tr></tr>");
        var tdPName = $("<td width='25%'><b>Disbursement Linked Indicators (DLIs) or Components</b></td>");
        var tdPNameVal = $("<td width='75%'>" + me.rowData["Components"] + "</td>");
        trPName.append(tdPName);
        trPName.append(tdPNameVal);
        tableElem.append(trPName);


        var trPName = $("<tr></tr>");
        var tdPName = $("<td width='25%'><b>Progress</b></td>");
        var tdPNameVal = $("<td width='75%'>" + me.rowData["Progress"] + "</td>");
        trPName.append(tdPName);
        trPName.append(tdPNameVal);
        tableElem.append(trPName);


        var trPName = $("<tr></tr>");
        var tdPName = $("<td width='25%'><b>Issues / Bottlenecks</b></td>");
        var tdPNameVal = $("<td width='75%'>" + me.rowData["Issues"] + "</td>");
        trPName.append(tdPName);
        trPName.append(tdPNameVal);
        tableElem.append(trPName);

        return tableElem;

    }

    me.getMeetingForm = function (row) {
        var table = $("#tblMeetingDetail");
        table.empty();
        var tableElem = me.getMeetingTable(row);
        table.append(tableElem);
    }

    me.getHTMLTableFromGridRow = function (row) {
        var tableElem = $("<table style='width: 100%; word-wrap:break-word; table-layout: fixed;'></table>");
        var tBodyElem = $('<tbody  style="width: 100%"></tbody>');
        // var hRowElem = $("<tr></tr>");
        // var hRowNameElem = $("<th>Field Name</th>");
        // var hRowValueElem = $("<th>Field Value</th>");
        // hRowElem.append(hRowNameElem);
        // hRowElem.append(hRowValueElem);
        // tBodyElem.append(hRowElem);
        for (var key in row) {
            if (key == 'id' || key == 'uid' || key == 'boundindex' || key == 'uniqueid' || key == 'visibleindex' || key == 'serial' || key == 'is_completed') {
            } else {
                var keyValue = row[key];
                if (key == 'Meeting Date' || key == 'Due Date' || key == 'task_date' || key == 'meeting_date'
                    || key == 'loan_effectiveness_date' || key == 'loan_closing_date' || key == 'loan_negotiation_date'
                    || key == 'loan_signing_date') {
                    keyValue = me.removeGMTFromDate(row[key])
                }
                keyValue = (keyValue) ? keyValue : "";
                var bRow = $("<tr></tr>");
                var rName = $("<td style='width: 30%; color: darkgreen;'>" + me.getColumnTitle(key) + "</td>");
                if (key == 'pic_path') {
                    if (keyValue) {
                        var path = uploaded_path + '/' + keyValue
                        var rValue = $("<td style='width: 70%;'><img width='250' height='250' src=" + path + "></td>");
                    } else {
                        var rValue = $("<td style='width: 70%;'>" + keyValue + "</td>");
                    }
                } else if (key == 'Attachments') {
                    var arrDocuments = keyValue.split(';');
                    if (arrDocuments.length > 1) {
                        var rValue = $("<td style='width: 70%;'></td>");
                        for (var i = 0; i < arrDocuments.length; i++) {
                            var doc = arrDocuments[i];
                            if (doc) {
                                var a = $("<div><a href='" + meeting_docs_path + '/' + doc + "' target='_blank'>" + doc + "</a></div>");
                                rValue.append(a);
                            }
                        }
                    } else {
                        var rValue = $("<td style='width: 70%;'>" + keyValue + "</td>");
                    }
                } else if (key == 'Pictures') {
                    var arrDocuments = keyValue.split(';');
                    if (arrDocuments.length > 1) {
                        var rValue = $("<td style='width: 70%;'></td>");
                        for (var i = 0; i < arrDocuments.length; i++) {
                            var doc = arrDocuments[i];
                            if (doc) {
                                var a = $("<div><a href='" + meeting_pics_path + '/' + doc + "' target='_blank'>" + doc + "</a></div>");
                                rValue.append(a);
                            }
                        }
                    } else {
                        var rValue = $("<td style='width: 70%;'>" + keyValue + "</td>");
                    }
                } else {
                    var rValue = $("<td style='width: 70%;'>" + keyValue + "</td>");
                }
                bRow.append(rName);
                bRow.append(rValue);
                tBodyElem.append(bRow);
            }
        }
        tableElem.append(tBodyElem);
        return tableElem;
    }

    me.createGridToAccordionPanel = function (data) {
        var table = $("#tblMeetingDetail");
        table.empty();
        var accordion = $("<div class='accordion' id='meetingsAccordion'></div>");
        var index = 1;
        for (var i = 0; i < data.length; i++) {
            var row = data[i];
            var headingDivId = 'accrod_' + index;
            var contentDivId = 'content_' + index;
            var titleText = index + ' - ' + row["Assignment"];
            var card = $("<div class='card'></div>");
            var cardHeader = $("<div class='card-header' id='" + headingDivId + "'></div>");
            var accordionTitle = $("<h5 class='mb_0'>");
            var btnTitleText = $('<button class="btn btn-link" type="button" style="width:100%; white-space: normal; " data-toggle="collapse" data-target="#' + contentDivId + '" ' +
                'aria-expanded="true" aria-controls="' + contentDivId + '">' + titleText + '</button>');
            var contentDiv = $('<div id="' + contentDivId + '" class="collapse" aria-labelledby="' + headingDivId + '" data-parent="#meetingsAccordion"></div>');
            var contentDivBody = $('<div class="card-body" ></div>');

            var rowTable = me.getHTMLTableFromGridRow(row);
            contentDivBody.append(rowTable);
            contentDiv.append(contentDivBody);
            accordionTitle.append(btnTitleText);
            cardHeader.append(accordionTitle);
            card.append(cardHeader);
            card.append(contentDiv);
            accordion.append(card);
            index++;
        }
        table.append(accordion);
    }

    me.removeGMTFromDate = function (date) {
        if (date) {
            var dateString = new Date(date).toUTCString();
            dateString = dateString.split(' ').slice(0, 4).join(' ');
            return dateString;
        } else {
            return '';
        }
    }

    me.createHistoryTable = function (data) {
        var table = $("#dynamicTable");
        table.empty();

        var tableElem = $("<table style='width: 100%'></table>");
        var tBodyElem = $('<tbody  style="width: 100%"></tbody>');
        var hRowElem = $("<tr></tr>");
        var hRowNameElem = $("<th>Date</th>");
        var hRowValueElem = $("<th>Remarks</th>");
        hRowElem.append(hRowNameElem);
        hRowElem.append(hRowValueElem);
        tBodyElem.append(hRowElem);

        for (var i = 0; i < data.length; i++) {
            var bRow = $("<tr></tr>");
            var rName = $("<td style='width: 30%; color: darkgreen;'>" + me.removeGMTFromDate(data[i].remarks_date) + "</td>");
            var rValue = $("<td style='width: 70%;'>" + data[i].remarks + "</td>");
            bRow.append(rName);
            bRow.append(rValue);
            tBodyElem.append(bRow);
        }
        tableElem.append(tBodyElem);
        table.append(tableElem);
    }

    me.addSerialToColumns = function (columns) {
        for (var i = 0; i < columns.length; i++) {
            var text = columns[i].text;
            if (text === 'id' || text == "meeting_id") {
                columns.splice(i, 1);
            }
            if (text == 'Due Date' || text == 'Task Date' || text == 'Meeting Date') {
                columns[i]['cellclassname'] = me.cellclass;
            }
        }
        var serialCol = {
            align: "left",
            cellsalign: "right",
            datafield: "serial",
            datatype: "number",
            filtertype: "number",
            resizable: true,
            text: "Sr",
            width: 50
        };
        if (type == 'foreign' || type == 'local') {
        } else {
            columns.splice(0, 0, serialCol);
        }
        return columns;
    }

    me.updateColumnWidths = function (columns) {
        for (var i = 0; i < columns.length; i++) {
            var text = columns[i].text;
            var textLength = parseFloat(text.length) * 8;
            var width = columns[i].width;
            if (text == "Assignment") {
                columns[i].width = 350;
            }
            if (text == 'Scheme') {
                columns[i]['width'] = 500;
            } else {
                if (textLength > width) {
                    columns[i].width = textLength;
                }
            }
        }
        return columns;
    }

    me.addSerialToFields = function (fields) {
        if (type == 'foreign') {
        } else {
            fields.push({name: 'serial', type: 'number'});
        }
        return fields;
    }

    me.addSerialToData = function (data) {
        if (type == 'foreign') {
        } else {
            for (var i = 0; i < data.length; i++) {
                data[i]['serial'] = (i + 1)
            }
        }
        return data;
    }

    me.getParticipantsList = function (meetingId) {
        $("#myPleaseWait").modal("show");
        var url = 'participants_list?id=' + meetingId;
        $.ajax({
            type: 'GET',
            dataType: 'text',
            url: url,
            timeout: 9000000,
            success: function (data) {
                $("#myPleaseWait").modal("hide");
                var participants_data = eval('(' + JXG.decompress(data) + ')');
                if (participants_data) {

                } else {
                    alert('No remarks found.');
                }
            },
            error: function (xhr, ajaxOptions, thrownError) {
                $("#myPleaseWait").modal("hide");
            },
        });
    }

    me.getHistoryDetails = function (meetingId) {
        $("#myPleaseWait").modal("show");
        var url = 'history_data?id=' + meetingId;
        $.ajax({
            type: 'GET',
            dataType: 'text',
            url: url,
            timeout: 9000000,
            success: function (data) {
                $("#myPleaseWait").modal("hide");
                var history_data = eval('(' + JXG.decompress(data) + ')');
                if (history_data) {
                    var tblHistory = $('#dynamicTable');
                    tblHistory.empty();
                    me.createHistoryTable(history_data);
                    $("#recordHistoryModal").modal("show");
                } else {
                    alert('No remarks found.');
                }
            },
            error: function (xhr, ajaxOptions, thrownError) {
                $("#myPleaseWait").modal("hide");
            },
        });
    }

    me.getColumnTitle = function (name) {
        var title = '';
        switch (name) {
            case 'task_name':
                title = 'Task Name';
                break;
            case 'is_completed':
                title = 'Completed?';
                break;
            case 'task_date':
                title = 'Task Date';
                break;
            case 'meeting_date':
                title = 'Meeting Date';
                break;
            case 'meeting_agenda':
                title = 'Meeting Agenda';
                break;
            case 'sector':
                title = 'Sector';
                break;
            case 'sub_sector':
                title = 'Sub-Sector';
                break;
            case 'department':
                title = 'Department';
                break;
            case 'nature':
                title = 'Nature';
                break;
            case 'referred_by':
                title = 'Referred By';
                break;
            case 'assigned_to':
                title = 'Assigned To';
                break;
            case 'assignment':
                title = 'Assignment';
                break;
            case 'due_date':
                title = 'Due Date';
                break;
            case 'assignment_date':
                title = 'Due Date';
                break;
            case 'status':
                title = 'Status';
                break;
            case 'priority':
                title = 'Priority';
                break;
            case 'remarks':
                title = 'Remarks';
                break;
            case 'term':
                title = 'Assignment Term';
                break;
            case 'donor_agency':
                title = 'Donor Agency';
                break;
            case 'project_name':
                title = 'Project Pame';
                break;
            case 'funding_mode':
                title = 'Funding Mode';
                break;
            case 'local_share':
                title = 'Local Share';
                break;
            case 'foreign_share':
                title = 'Foreign Share';
                break;
            case 'total_cost':
                title = 'Total Cost';
                break;
            case 'duration':
                title = 'Duration';
                break;
            case 'loan_effectiveness_date':
                title = 'Loan Effectiveness Date';
                break;
            case 'loan_closing_date':
                title = 'Loan Closing Date';
                break;
            case 'loan_negotiation_date':
                title = 'Loan Negotiation Date';
                break;
            case 'loan_signing_date':
                title = 'Loan Signing Date';
                break;
            case 'implementing_agency':
                title = 'Implementing Agency';
                break;
            case 'designation':
                title = 'Designation';
                break;
            case 'email_id':
                title = 'Email Id';
                break;
            case 'contact_no':
                title = 'Contact No';
                break;
            case 'name':
                title = 'Name';
                break;
            case 'attachments':
                title = 'Attachments';
                break;
            case 'pics':
                title = 'Pictures';
                break;
            default:
                title = name;
                break;
        }
        return title;
    }

    me.toggleGroupable = function () {
        var groupable = me.gridTarget.jqxGrid('groupable');
        me.gridTarget.jqxGrid({groupable: !groupable})
    }
    me.toggleShowFilterRow = function () {
        var showfilterrow = me.gridTarget.jqxGrid('showfilterrow');
        me.gridTarget.jqxGrid({showfilterrow: !showfilterrow});
    }
    me.clearGrid = function () {
        try {
            me.gridTarget.jqxGrid('destroy');
        } catch (e) {
            console.log(e)
        }
    }
    me.rowData = null;
    me.gridTarget.on('rowselect', function (event) {
        var args = event.args;
        me.rowData = args.row;
        selectedRow = args.row;
    });

    me.gridTarget.on('rowdoubleclick', function (event) {
        if (type == 'important' || type == 'short' || type == 'long' || type == 'all' || type == 'completed' || type == 'meeting_initiatives_search') {
            $("#recordFormModal").modal("show");
            me.collapseAllPanels();
        } else if (type == 'meetings') {
            me.getMeetingInitiativesForm();

        } else if (type == 'quick') {
            var tblHistory = $('#dynamicTable');
            tblHistory.empty();
            me.getMeetingForm(me.rowData);
            $("#recordFormModal").modal("show");
        } else if (type == 'foreign') {
            $("#recordFormModal").modal("show");
            me.getForeignBriefsOnePager();
        }
    });


    me.redirectWithShortUrl = function (url) {
        $("#myPleaseWait").modal("show");
        $.ajax({
            url: me.shortenUrlApi,
            type: 'POST',
            contentType: me.contentType,
            data: '{ longUrl: "' + window.location.href + '"}',
            success: function (response) {
                $("#myPleaseWait").modal("hide");
                window.location.href = url + response.id;
            }
        });
    }


    me.gridTarget.on("filter", function (event) {
        var filterinfo = me.gridTarget.jqxGrid('getfilterinformation');
        // console.log(filterinfo)
        if (filterinfo.length > 0) {
            filterRows = me.gridTarget.jqxGrid('getrows');
            var oids = ""
            for (var i = 0; i < filterRows.length; i++) {
                // oids.push(filterRows[i].oid);
                oids += filterRows[i].oid + ","
            }
            oids = oids.substring(0, oids.length - 1)
        } else {

        }
    });

    me.flexMonster = null;
    me.createFlexMonsterPivotTable = function (data, rows, columns, measures) {
        var flexMonster = new Flexmonster({
            container: "divPTModal",
            componentFolder: "https://cdn.flexmonster.com/",
            toolbar: true,
            height: 500,
            report: {
                dataSource: {
                    data: data
                },
                "slice": {
                    "rows": rows,
                    "columns": columns,
                    "measures": measures
                },
            },
            licenseKey: 'Z7HI-XG503S-5O4M4H-6F456Z-0A3E3Z-1X663C-5O4R35-4R'// for dch server
            // licenseKey: 'Z7CJ-XF9J50-5J4J6X-2H136N-2L036W-1A0O01-6S5S6R-0W0T20-3C' // for localhost
        })
    }

    me.populateColumnsListInCombo = function (data) {
        for (var key in data) {
            var record = data[key];
            // if (key == '0') {
            //     $('#cmbFieldName').append($('<option selected>', {value: record.datafield}).text(record.text));
            // } else {
            $('#cmbFieldName').append($('<option>', {value: record.datafield}).text(record.text));
            // }
        }
    }

    me.populateMeetingsListInCombo = function () {
        if (type == 'meeting_initiatives_search') {
            for (var key in meetings_list) {
                var record = meetings_list[key];
                var meeting_name = record["id"]
                if (meeting_name == meetingName) {
                    $('#cmbMeetings').append($('<option selected>', {value: record['id']}).text(record['name']));
                } else {
                    $('#cmbMeetings').append($('<option>', {value: record['id']}).text(record['name']));
                }
            }
        }
    }


    me.getFieldType = function (field) {
        for (var key in me.gridColumns) {
            var record = me.gridColumns[key];
            if (record.datafield == field) {
                return record.datatype;
            }
        }

    }

    me.getFilterType = function (field) {
        if (field == 'string') {
            return 'stringfilter'
        } else if (field == 'number') {
            return 'numericfilter'
        } else if (field == 'date') {
            return 'datefilter'
        } else if (field == 'boolean') {
            return 'booleanfilter'
        } else {
            return 'stringfilter'
        }
    }

    me.applyOnLoadFilter = function () {
        if (type == 'all') {

            var vars = {};
            var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function (m, key, value) {
                vars[key] = value;
            });

            var id = vars['id'];
            if (id) {
                var assignmentName = me.getAssignmentNameFromGridData(id);
                me.gridTarget.jqxGrid('clearfilters');
                var filtervalue = assignmentName;
                var filtercondition = 'EQUAL';
                var filtergroup = new $.jqx.filter();
                var filter_or_operator = 1;
                var filter = filtergroup.createfilter('stringfilter', filtervalue, filtercondition);
                filtergroup.addfilter(filter_or_operator, filter);
                me.gridTarget.jqxGrid('addfilter', 'Assignment', filtergroup);
                // apply the filters.
                me.gridTarget.jqxGrid('applyfilters');
            }
        }
    }

    me.getAssignmentNameFromGridData = function (id) {
        var assignmentName = '';
        for (var index in me.gridData) {
            var dataId = me.gridData[index]["id"];
            if (dataId == id) {
                assignmentName = me.gridData[index]["Assignment"];
            }
        }
        return assignmentName;
    }

    me.searchText = function () {
        me.gridTarget.jqxGrid('clearfilters');
        var datafield = $("#cmbFieldName").val();
        var searchText = $("#txtFieldValue").val();
        if (datafield == '---- Select column ----') {
            $("#cmbFieldName").focus();
        }
        var columnType = me.getFieldType(datafield);
        var filterType = me.getFilterType(columnType);

        if (searchText == '' || searchText == null) {
            me.gridTarget.jqxGrid('clearfilters');
        }
        else {
            var filtergroup = new $.jqx.filter();
            var filter_or_operator = 1;
            var filtervalue = searchText;
            var filtercondition = 'contains';
            var filter = filtergroup.createfilter(filterType, filtervalue, filtercondition);
            filtergroup.addfilter(filter_or_operator, filter);
            me.gridTarget.jqxGrid('addfilter', datafield, filtergroup);
            // apply the filters.
            me.gridTarget.jqxGrid('applyfilters');
        }


    }

    me.parseNullString = function (str) {
        if (str) {
            return str;
        } else {
            return '';
        }
    }


};

