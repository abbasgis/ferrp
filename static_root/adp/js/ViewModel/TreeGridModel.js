/**
 * Created by ather on 5/1/2017.
 */
var TreeGridModel = function(model){
    var me = this;
    me.schemeDivId = model.overviewModel.schemeDivId;
    me.adpVM = model;
    me.source = null;

    me.createSchemesListGrid = function (schemesList) {
        try {
            var dataFields = me.prepareDataFieldList(schemesList[0]);
            me.source = {
                localdata: schemesList,
                datatype: "array",
                datafields : dataFields,
                // datafields: [{name: 'LONo', type: 'string'}],
            };



            var dataAdapter = new $.jqx.dataAdapter(me.source);

            $("#"+me.schemeDivId).jqxGrid(
                {
                    source: dataAdapter,
                    theme: 'Bootstrap',
                    sortable: true,
                    filterable: true,
                    pageable: true,
                    pagesize: 7100,
                    pagesizeoptions: ['10', '100', '500', '1000', '5000'],
                    width: '100%',
                    // rowsheight:'10',
                    // autorowheight: true,
                    // autoheight:true,
                    height: 570,
                    showtoolbar: true,
                    groupable: true,
                    rowdetails: true,
                    rowdetailstemplate: {
                        rowdetails: "<div style='width:100%; margin: 10px;'><ul style='margin-left: 30px;'><li>Costing</li><li>Projection</li></ul><div class='costing'></div><div class='projection'></div></div>",
                        rowdetailsheight: 300
                    },
                    columnsresize: true,
                    showfilterrow: true,
                    showgroupaggregates: true,
                    showstatusbar: true,
                    showaggregates: true,
                    statusbarheight: 30,
                    autoshowfiltericon: true,
                    initrowdetails: me.initGridRowDetails,
                    enabletooltips:true,
                    groups: [],
                    // autoheight: true,
                    // cellhover: function (element, pageX, pageY) {
                    //     // alert("cell hover");
                    //     $(element).jqxTooltip({position: 'bottom', content: "<b>"+$(element).text()+"</b>", autoHide:false });
                    // },

                    columns: me.getColumnsList(),
                    rendertoolbar: function (toolbar) {
                        me.createGridToolbar(toolbar);
                    }
                });
            $('#'+me.schemeDivId).on('rowselect', function (event)  {
                // event arguments.
                var args = event.args;
                // row's bound index.
                var rowBoundIndex = args.rowindex;
                // row's data. The row's data object or null(when all rows are being selected or unselected with a single action). If you have a datafield called "firstName", to access the row's firstName, use var firstName = rowData.firstName;
                var rowData = args.row;
                var datafield = "Name_of_Scheme";
                var cellElement = $('#'+me.schemeDivId).jqxGrid('getcell', rowBoundIndex, datafield);//event.owner.columnsrow[0].cells[1]//
                var value = cellElement.value;
                me.adpVM.invokeAlert('warning',"Scheme Name: <b>"+value+"</b>");
                // $(cellElement).jqxTooltip({position: 'bottom', content: "<b>"+value+"</b>", autoHide:false });
            })
            // var records = $("#divSchemesList").jqxGrid('getrows');//.adapter;
            // me.calculateRecordStats(records);
            $("#"+me.schemeDivId).on("filter", function (event) {
                var filters = event.args.filters;
                var filterInformation = '';
                for(var i=0;i<filters.length;i++){
                    if(i==0){
                        filterInformation = 'Data Filtered where '
                    } else if(i==filters.length-1){
                        filterInformation +=", and ";
                    }else if(i > 0 && i < filters.length - 1){
                        filterInformation +=", ";
                    }
                    var filter = filters[i];
                    var fieldName = filter.datafield;
                    filterInformation += "<b>"+fieldName+"</b>";
                    var filterDetails = filter.filter.getfilters();
                    for(var j=0;j<filterDetails.length;j++){
                        if(filterDetails.length > 1) {
                            if (j == filterDetails.length - 1) {
                                filterInformation += ", and";
                            } else if (j > 0) {
                                filterInformation += ", ";
                            }
                        }
                        filterInformation += " " + filterDetails[j].condition + " " + filterDetails[j].value;

                    }

                }
                me.adpVM.overviewModel.setRecordStatsInInfoGraphics();
                if(filterInformation.length > 0) me.adpVM.invokeAlert("success",filterInformation);
            });
        } catch (err) {
            console.error(err.stack);
        }
    }
    me.prepareDataFieldList = function(scheme){
        var dataFields = [];
        for(var key in scheme){
            var dataField = {};
            dataField.name = key;
            if(parseFloat(scheme[key]) == NaN){
                dataField.type = 'string';
            }else{
                dataField.type = 'float';
            }
        }
        return dataFields;
    }
    me.getColumnsList = function(){

        var columns = me.adpVM.info.columns;
        // alert(column)
        return columns;
    }
    me.clearFilterFromGrid = function(){
        $("#"+me.schemeDivId).jqxGrid('clearfilters');
        me.adpVM.overviewModel.setRecordStatsInInfoGraphics();
    }
    me.createGridToolbar = function(toolbar){
        try {
            var buttons=[{id:"exportExcel",btnclass:"btn btn-success",info:"Used for Exporting Table to Excel",spanclass:'fa fa-file-excel-o',onClickFn:"exportTo",args:'{"type":"excel"}'},
                {id:"btnExportPDF",btnclass:"btn btn-success",info:"Used for Exporting Table to PDF",spanclass:'fa fa-file-pdf-o',onClickFn:"exportTo",args:'{"type":"pdf"}'},
                {id:"btnExportCSV",btnclass:"btn btn-success",info:"Used for Exporting Table to CSV",spanclass:'fa fa fa-file-o',onClickFn:"exportTo",args:'{"type":"csv"}'},
                {id:"btnViewSchemeInfo",btnclass:"btn btn-success",info:"View Scheme Info",spanclass:'glyphicon glyphicon-list-alt',onClickFn:"viewSchemeInfo",args:''},
                {id:"btnSchemeLocation",btnclass:"btn btn-success",info:"Used for Viewing Scheme Location on Map",spanclass:'glyphicon glyphicon-map-marker',onClickFn:"viewOnMap",args:''},
            ];
            var container = $("<div style='margin: 5px;'></div>");
            for(var i=0;i<buttons.length;i++){
                var btn = $("<button class='"+buttons[i].btnclass+"' id='"+buttons[i].id+"'info='"+buttons[i].info+"' onClickFn='"+buttons[i].onClickFn+"' args='"+buttons[i].args+"'>" +
                    "<span id='span"+buttons[i].id+"' class='"+buttons[i].spanclass+"' info='"+buttons[i].info+"'></span></button>");

                container.append(btn);
                btn.on('mouseover',function(event){
                    var el = event.target;
                    var info=$('#'+el.id).attr("info");
                    var spanId =  el.id;
                    if(spanId.indexOf("span") == -1){
                        spanId = "span"+spanId;
                    }
                    var spanclass = $('#'+spanId).attr("class");
                    info = "Button <span class='"+spanclass+"'></span> "+info;

                    me.adpVM.invokeAlert('success',info);
                    // $(buttons[i].onClickFn)[0](buttons[i].info);
                });
                btn.click(function(){
                    try {
                        var target = $(this).attr("onClickFn");
                        var args = $(this).attr("args");
                        if(args.length>2) {
                            var args = JSON.parse(args);
                        }
                        me[target](args);
                    }catch(err){
                        console.error(err.stack);
                    }
                });

            }
            toolbar.append(container);

        }catch(err){
            console.error(err.stack);
        }
    }
    me.exportTo = function(args){
        var format = args.type;
        if(format === "excel"){
            $("#"+me.schemeDivId).jqxGrid('exportdata', 'xls', 'jqxGrid');
        }if(format === "pdf"){
            $("#"+me.schemeDivId).jqxGrid('exportdata', 'pdf', 'jqxGrid');
        }if(format === "csv"){
            $("#"+me.schemeDivId).jqxGrid('exportdata', 'csv', 'jqxGrid');
        }if(format === "html"){
            $("#"+me.schemeDivId).jqxGrid('exportdata', 'html', 'jqxGrid');
        }if(format === "json"){
            $("#"+me.schemeDivId).jqxGrid('exportdata', 'json', 'jqxGrid');
        }if(format === "xml"){
            $("#"+me.schemeDivId).jqxGrid('exportdata', 'xml', 'jqxGrid');
        }
    }

    me.viewSchemeInfo=function(){

        var getselectedrowindexes = $('#'+me.schemeDivId).jqxGrid('getselectedrowindexes');
        if (getselectedrowindexes.length > 0)
        {
            // returns the selected row's data.
            var selectedRowData = $('#'+me.schemeDivId).jqxGrid('getrowdata', getselectedrowindexes[0]);
            var gsNo = selectedRowData["GS No"];
            var monitoring = selectedRowData["Monitoring"];
            if(monitoring == true){
                var url = "http://176.58.124.95/ferrp/ppms/public/submit_main?scheme=" + gsNo;
                // var url = "http://ferrp.com/ppms/submit_main?scheme=" + gsNo;
                window.open(url, "_blank ");
            }else{
                me.adpVM.invokeAlert("danger","This scheme is not being monitored.");
            }

        }else{
            me.adpVM.invokeAlert("danger","Please select a scheme first.");
        }
    }

    me.viewOnMap=function(){
        me.adpVM.invokeAlert('danger','Location of Scheme isn\'t Available');
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
                var totalCost = "<div style='margin: 10px;'><b>Total Cost:</b> " + me.adpVM.numberFormat((datarecord["Total_Cost"])) + "</div>";
                var foreignAid = "<div style='margin: 10px;'><b>Foreign Aid:</b> " + me.adpVM.numberFormat(datarecord["Foreign_Aid"]) + "</div>";
                var allocation =  "<div style='margin: 10px;'><b>Allocation:</b> " + me.adpVM.numberFormat(datarecord["Allocation"]) + "</div>"
                //var pndProposedAllocation ="<div style='margin: 10px;'><b>P&D Proposed Allocation:</b> " + me.adpVM.numberFormat(datarecord["PND_Proposed_Allocation"]) + "</div>"
                $(leftcolumnCosting).append(totalCost);
                $(leftcolumnCosting).append(foreignAid);
                $(leftcolumnCosting).append(allocation);
                //$(leftcolumnCosting).append(pndProposedAllocation);

                var localCapital = "<div style='margin: 10px;'><b>Local Capital:</b> " + me.adpVM.numberFormat((datarecord["LocalCapital"])) + "</div>";
                var localRevenue = "<div style='margin: 10px;'><b>Local Revenue:</b> " + me.adpVM.numberFormat((datarecord["LocalRevenue"])) + "</div>";
                var foreignCapital = "<div style='margin: 10px;'><b>Foreign Capital:</b> " + me.adpVM.numberFormat((datarecord["ForeignCapital"])) + "</div>";
                var foreignRevenue = "<div style='margin: 10px;'><b>Foreign Revenue:</b> " + me.adpVM.numberFormat((parseFloat(datarecord["ForeignRevenue"]))) + "</div>";
                var totalCapital = "<div style='margin: 10px;'><b>Total Capital</b> " + me.adpVM.numberFormat((parseFloat(datarecord["TotalCapital"]))) + "</div>";
                var totalRevenue = "<div style='margin: 10px;'><b>Total Revenue:</b> " + me.adpVM.numberFormat((parseFloat(datarecord["TotalRevenue"]))) + "</div>";

                $(rightcolumnCosting).append(localCapital);
                $(rightcolumnCosting).append(localRevenue);
                $(rightcolumnCosting).append(foreignCapital);
                $(rightcolumnCosting).append(foreignRevenue);
                $(rightcolumnCosting).append(totalCapital);
                $(rightcolumnCosting).append(totalRevenue);

                var leftcolumnProjection = $('<div style="float: left; width: 100%;"></div>');
                containerProjection.append(leftcolumnProjection);

                var projection1718 = "<div style='margin: 10px;'><b>Projection 17-18:</b> " + me.adpVM.numberFormat((datarecord["Projection_2017-18"])) + "</div>";
                var projection1819 = "<div style='margin: 10px;'><b>Projection 18-19:</b> " + me.adpVM.numberFormat((datarecord["Projection_2018-19"])) + "</div>";
                var throwFOrward19 = "<div style='margin: 10px;'><b>Throw Forward 19:</b> " + me.adpVM.numberFormat((datarecord["Throw_Forward"])) + "</div>";
                var expenseUptoJune = "<div style='margin: 10px;'><b>Expense Upto June:</b> " + me.adpVM.numberFormat((datarecord["Exp_upto_June"])) + "</div>";

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