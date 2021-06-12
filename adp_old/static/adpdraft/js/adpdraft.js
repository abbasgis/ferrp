/**
 * Created by ather on 3/23/2017.
 */
var schemesList;
$(document).ready(function () {
    try {
        resizeContent();
        $('#myPleaseWait').modal('show');

        var info = getInfographicDetails();
        var adpVM = new AdpVM(info);
        ko.applyBindings(adpVM);
        adpVM.createPageElements();

        var url = "/adp/adpReport/data";
        schemesList = JSON.parse(localStorage.getItem("adpSchemesReport"));
        if (!schemesList) {
            $.ajax({
                type: 'GET',
                dataType: 'text',
                url: url,
                timeout: 9000000,
                cache: false,
                error: function (xhr, ajaxOptions, thrownError) {
                    $('#myPleaseWait').modal('hide');
                    alert(thrownError);
                },
                success: function (data) {
                    var schemesList = data;//JXG.decompress(data);
                    var decompressSchemesList = eval('(' + schemesList + ')');
                    adpVM.initialize(decompressSchemesList);
                    $('#myPleaseWait').modal('hide');
                }
            });
        }
        else {
            $('#myPleaseWait').modal('hide');
            // var decompressSchemesList =  eval('(' + JXG.decompress(schemesList) + ')');
            var decompressSchemesList = eval('(' + schemesList + ')');
            adpVM.initialize(decompressSchemesList);
        }
        // decompressSchemesList ={};
        // adpVM.initialize(decompressSchemesList,info);
        $(window).resize(function () {
            resizeContent();
        });
    } catch (err) {
        console.error(err.stack);
    }
});

function cacheData() {
    $('#myPleaseWait').modal('show');
    try {
        localStorage.setItem("adpSchemesReport", JSON.stringify(schemesList));
        $('#myPleaseWait').modal('hide');
    } catch (e) {
        localStorage.clear();
        localStorage.setItem("adpSchemesReport", JSON.stringify(schemesList));
        $('#myPleaseWait').modal('hide');
        console.error(e.stack);
    }
}

function getFieldsDataFromModel(data) {
    var dataArray = [];
    for(var i = 0; i<data.length; i++){
        var fields = data[i].fields;
        dataArray.push(fields);
    }
    return dataArray;
}

function resizeContent() {
    var navbarHeight = $('#base_nav').height();
    var footnoteHeight = $('#footnote').height();
    height = $('body').height() - (navbarHeight + footnoteHeight);
    $('div#mainpanel').height(height);
}

function getInfographicDetails() {
    var info;
    var tooltiprenderer = function (element) {
        $(element).jqxTooltip({position: 'mouse', content: $(element).text()});
    }
    info = getADPinfographicsDetails(tooltiprenderer);
    return info;
}

function getADPinfographicsDetails(tooltiprenderer){
    var info = {
        infoGraphics: [
            {
                Name: "All Schemes",
                id: "all",
                class: "col-lg-3  col-md-3 col-sm-6 col-xs-12",
                PanelClass: "panel-primary"
            }, //panel-info
            {
                Name: "On-Going Schemes",
                id: "ogs",
                class: "col-lg-3 col-md-3 col-sm-6 col-xs-12",
                PanelClass: "panel-brown"
            },  //panel-warning
            {
                Name: "New Schemes",
                id: "ns",
                class: "col-lg-3 col-md-3 col-sm-6 col-xs-12",
                PanelClass: "panel-green"
            }, //panel-danger
            {
                Name: "Other Development Schemes",
                id: "odp",
                class: "col-lg-3 col-md-3 col-sm-6 col-xs-12",
                PanelClass: "panel-yellow"
            },//panel-success
            // {Name: "New Inducted Schemes", id: "ni", class: "col-lg-2-4 col-md-2-4 col-sm-6 col-xs-12", PanelClass: "panel-brown"}
        ]
        ,infoGraphicInfo: [
            {id: "count", name: "Schemes", init: 0.00},
            {id: "cost", name: "Total Cost", init: 0.00, recordKey: "Total_Cost"},
            {id: "foreign_aid", name: "Foreign Aid", init: 0.00, recordKey: "Foreign_Aid"},
            {id: "local_capital", name: "Local Capital", init: 0.00, recordKey: "LocalCapital"},
            {id: "local_revenue", name: "Local Revenue", init: 0.00, recordKey: "LocalRevenue"},
            {id: "foreign_capital", name: "Foreign Capital", init: 0.00, recordKey: "ForeignCapital"},
            {id: "foreign_revenue", name: "Foreign Revenue", init: 0.00, recordKey: "ForeignRevenue"},
            {id: "total_capital", name: "Total Capital", init: 0.00, recordKey: "TotalCapital"},
            {id: "total_revenue", name: "Total Revenue", init: 0.00, recordKey: "TotalRevenue"},
            {id: "allocaton", name: "Allocation", init: 0.00, recordKey: "Allocation"},
            //{id: "proposedallocation", name: "Proposed Allocation", init: 0.00,recordKey:"PND_Proposed_Allocation"},
            // {id: "release", name: "Release", init: 0.00,recordKey:"Release"},
            // {id: "utilization", name: "Utilization", init: 0.00,recordKey:"Utilization"},
            // {id: "utilization_wrt_allocation",name: "Utilization w.r.t. Allocation", init: 0.00},
            // {id: "utilization_wrt_release", name: "Utilization w.r.t. Release", init: 0.00},
        ]
        ,columns : [
            // {text: 'LO No', datafield: 'LONo', width: 100, rendered: tooltiprenderer},
            {
                text: 'GS No',
                datafield: 'GS_No',
                width: 80
                // rendered: tooltiprenderer,
                //aggregates: ["count"],
            },
            {
                text: 'Scheme Name',
                datafield: 'Name_of_Scheme',
                width: 250,
               // rendered: tooltiprenderer,
                aggregates: ["count"],
            },
            {text: 'Type', datafield: 'Type', width: 120, rendered: tooltiprenderer, aggregates: ["count"]},
            {text: 'Sector', datafield: 'Sector', width: 120, rendered: tooltiprenderer, aggregates: ["count"]},
            {
                text: 'District',
                datafield: 'District',
                width: 80,
                rendered: tooltiprenderer,
                aggregates: ["count"]
            },
            {
                text: 'Total Cost',
                datafield: 'Total_Cost',
                width: 120,
                // rendered: tooltiprenderer,
                // columntype: "numberinput",
                // createeditor: function (row, column, editor) {
                //     editor.jqxNumberInput({decimalDigits: 2, decimalSeparator: ",", inputMode: "simple", spinButtons: false});
                // },
                cellvaluechanging: function (row, datafield, columntype, oldvalue, newvalue) {
                    return newvalue.replace(/,/g, '');
                },
                aggregates: ["sum"],
                cellsrenderer: function (row, column, value, defaultRender, column, rowData) {
                    value = numberFormat(value,true);
                    // value = value.replace(/,/g, '');
                    // if (value.toString().indexOf("Sum") >= 0) {
                    //     return defaultRender.replace("Sum", "Total");
                    // }
                    return value;
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
                datafield: 'Exp_upto_June',
                width: 120,
                rendered: tooltiprenderer,
                aggregates: ["sum"]
            },
            {
                text: 'Foreign Aid',
                datafield: 'Foreign_Aid',
                width: 120,
                rendered: tooltiprenderer,
                aggregates: ["sum"],
                cellsrenderer: function (row, column, value, defaultRender, column, rowData) {
                    //value = me.adpVM.NumberFormat(value);
                    if (value.toString().indexOf("Sum") >= 0) {
                        return defaultRender.replace("Sum", "Total");
                    }
                },
                aggregatesrenderer: function (aggregates, column, element) {
                    var renderstring = '<div style="position: relative; margin-top: 4px; margin-right:5px; text-align: right; overflow: hidden;">' + "Total" + ': ' + aggregates.sum + '</div>';
                    return renderstring;
                }
            },
            {text: 'Local Capital', datafield: 'LocalCapital', width: 120, rendered: tooltiprenderer},
            {text: 'Local Revenue', datafield: 'LocalRevenue', width: 120, rendered: tooltiprenderer},
            {text: 'Foreign Capital', datafield: 'ForeignCapital', width: 120, rendered: tooltiprenderer},
            {text: 'Foreign Revenue', datafield: 'ForeignRevenue', width: 120, rendered: tooltiprenderer},
            {text: 'Total Capital', datafield: 'TotalCapital', width: 120, rendered: tooltiprenderer},
            {text: 'Total Revenue', datafield: 'TotalRevenue', width: 120, rendered: tooltiprenderer},

            {
                text: 'Projection 17-18',
                datafield: 'Projection_2017-18',
                width: 120,
                rendered: tooltiprenderer
            },
            {
                text: 'Projection 18-19',
                datafield: 'Projection_2018-19',
                width: 120,
                rendered: tooltiprenderer
            },
            {
                text: 'Projection 19 Onward',
                datafield: 'Throw_Forward',
                width: 120,
                rendered: tooltiprenderer
            }
            //{ text: 'Location', datafield: 'Location', width: 120, rendered: tooltiprenderer }
        ]
        ,prefixKey:{"ALL SCHEMES":"all", "NEW SCHEMES":"ns", "ON-GOING SCHEMES":"ogs", "OTHER DEVELOPMENT PROGRAM":"odp", "NEW INDUCTED SCHEMES":"ni"}
    }
    return info;

}

numberFormat = function(val,isDecimal){
    var parts = val.toString().split(".");
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    if(isDecimal) {
        if (!parts[1]) {
            parts.push('00');
        } else {
            if (parts[1].length > 2) {
                parts[1] = parts[1].substring(0, 2);
            }
        }
    }
    return parts.join(".");
}