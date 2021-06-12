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

        var url = "/adp/adpMPR/data";
        schemesList = JSON.parse(localStorage.getItem("adpSchemesDraft"));
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
                    $('#myPleaseWait').modal('hide');
                    var schemesList = eval('(' + JXG.decompress(data) + ')');
                    adpVM.initialize(schemesList);
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
        localStorage.setItem("adpSchemesDraft", JSON.stringify(schemesList));
        $('#myPleaseWait').modal('hide');
    } catch (e) {
        localStorage.clear();
        localStorage.setItem("adpSchemesDraft", JSON.stringify(schemesList));
        $('#myPleaseWait').modal('hide');
        console.error(e.stack);
    }
}

function resizeContent() {
    var navbarHeight = $('#base_nav').height();
    var footnoteHeight = $('#footnote').height();
    height = $('body').height() - (navbarHeight + footnoteHeight);
    $('div#mainpanel').height(height);
}

function getInfographicDetails() {
    // var isMPR = false;
    var info;
    var tooltiprenderer = function (element) {
        $(element).jqxTooltip({position: 'mouse', content: $(element).text()});
    }
    // if(isMPR){
    info = getMPRInfographicDetails(tooltiprenderer);
    // }else{
    //     info = getADPinfographicsDetails(tooltiprenderer,adpVM);
    // }
    return info;
}

function getMPRInfographicDetails(tooltiprenderer) {
    var info = {
        infoGraphics: [
            {
                Name: "All Schemes",
                id: "all",
                class: "col-lg-2-4 col-md-2-4 col-sm-6 col-xs-12",
                PanelClass: "panel-primary"
            },
            {
                Name: "On-Going Schemes",
                id: "ogs",
                class: "col-lg-2-4 col-md-2-4 col-sm-6 col-xs-12",
                PanelClass: "panel-yellow"
            },
            {
                Name: "New Schemes",
                id: "ns",
                class: "col-lg-2-4 col-md-2-4 col-sm-6 col-xs-12",
                "PanelClass": "panel-red"
            },
            {
                Name: "Other Development Schemes",
                id: "odp",
                class: "col-lg-2-4 col-md-2-4 col-sm-6 col-xs-12",
                PanelClass: "panel-green"
            },
            {
                Name: "New Inducted Schemes",
                id: "ni",
                class: "col-lg-2-4 col-md-2-4 col-sm-6 col-xs-12",
                PanelClass: "panel-brown"
            }]
        ,
        infoGraphicInfo: [
            {id: "count", name: "Schemes", init: 0.00},
            {id: "cost", name: "Total Cost", init: 0.00, recordKey: "Total_Cost"},
            {id: "foreign_aid", name: "Foreign Aid", init: 0.00, recordKey: "Foreign_Aid_Total"},
            {id: "allocation", name: "Allocation", init: 0.00, recordKey: "Allocation"},
            {id: "release", name: "Release", init: 0.00, recordKey: "Release"},
            {id: "utilization", name: "Utilization", init: 0.00, recordKey: "Utilization"},
            {id: "utilization_wrt_allocation", name: "Utilization w.r.t. Allocation", init: 0.00},
            {id: "utilization_wrt_release", name: "Utilization w.r.t. Release", init: 0.00},
        ],
        columns: [
            {text: 'GS No', datafield: 'GS_No', width: 100, rendered: tooltiprenderer},
            {text: 'Scheme Name', datafield: 'Scheme_Name', width: 250, rendered: tooltiprenderer, aggregates: ["count"] },
            {text: 'Year', datafield: 'Year', width: 120, rendered: tooltiprenderer},
            {text: 'Approval Status', datafield: 'Approval', width: 80, rendered: tooltiprenderer, aggregates: ["count"]},
            {text: 'Sector', datafield: 'Sector', width: 120, rendered: tooltiprenderer, aggregates: ["count"]},
            {text: 'Type', datafield: 'Type', width: 120, rendered: tooltiprenderer, aggregates: ["count"]},
            {text: 'District', datafield: 'District', width: 120, rendered: tooltiprenderer, aggregates: ["count"] },
            {text: 'Monitoring', datafield: 'Monitoring',width: 120, rendered: tooltiprenderer, aggregates: ["count"]},
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
            {text: 'Expense Upto June', datafield: 'Expense_Upto_June', width: 120,rendered: tooltiprenderer,aggregates: ["sum"]},
            {text: 'Local Capital', datafield: 'Local_Capital', width: 120, rendered: tooltiprenderer},
            {text: 'Local Revenue', datafield: 'Local_Revenue', width: 120, rendered: tooltiprenderer},
            {text: 'Total Capital', datafield: 'Total_Capital', width: 120, rendered: tooltiprenderer},
            {text: 'Total Revenue', datafield: 'Total_Revenue', width: 120, rendered: tooltiprenderer},
            {text: 'Foreign Aid Capital', datafield: 'Foreign_Aid_Capital', width: 120, rendered: tooltiprenderer},
            {text: 'Foreign Aid Revenue', datafield: 'Foreign_Aid_Revenue', width: 120, rendered: tooltiprenderer},
            {text: 'Foreign Aid Total', datafield: 'Foreign_Aid_Total', width: 120, rendered: tooltiprenderer, aggregates: ["sum"]},
            {text: 'Release', datafield: 'Release', width: 120, rendered: tooltiprenderer},
            {text: 'Utilization', datafield: 'Utilization', width: 120, rendered: tooltiprenderer},
            {text: 'Projection One', datafield: 'Projection_One', width: 120, rendered: tooltiprenderer},
            {text: 'Projection Two', datafield: 'Projection_Two', width: 120, rendered: tooltiprenderer},
            {text: 'Throw Forward', datafield: 'Throw_Forward', width: 120, rendered: tooltiprenderer}
            //{ text: 'Location', datafield: 'Location', width: 120, rendered: tooltiprenderer }
        ]
        ,
        prefixKey: {
            "ALL SCHEMES": "all",
            "NEW SCHEMES": "ns",
            "ON-GOING SCHEMES": "ogs",
            "OTHER DEVELOPMENT PROGRAMME": "odp",
            "NEW INDUCTED SCHEMES": "ni"
        }
    }
    return info;
}