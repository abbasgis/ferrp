/**
 * Created by ather on 5/2/2017.
 */
var DimensionModelingModel = function (adpVM) {
    var me = this;
    me.initialize = function () {
        try {
            adpVM.panelHeader('<span class="glyphicon glyphicon-book"></span> ADP Dimension Modeling');
            // var button =$('<button id="js2pdf" class="btn btn-danger">JS2PDF</button>');
            var output = $(' <div id="output" style="margin: 30px;"></div>')
            // adpVM.mainPnlBody.append(button);
            adpVM.mainPnlBody.append(output);
            me.createFlexMonsterPivotTable(adpVM.schemesList);
            // me.createPivotTable();
            // $(document).on('click','#js2pdf',function(){
            //     me.exportTo('pdf');
            // });
        } catch (err) {
            console.error(err.stack);
        }

    }

    me.createFlexMonsterPivotTable = function (data) {
        var flexmonster = new Flexmonster({
            container: 'mainpnlbody',
            componentFolder: "https://cdn.flexmonster.com/",
            toolbar: true,
            height:'100%',
            report: {
                dataSource: {
                    data: data
                },
                "slice": {
                    "rows": [
                        {
                            "uniqueName": "Sector",
                        }, {
                            "uniqueName": "Type",
                        }
                    ],
                    "columns": [
                        {
                            "uniqueName": "[Measures]"
                        }
                    ],
                    "measures": [
                        {
                            "uniqueName": "Total_Cost",
                            "aggregation": "sum"
                        },
                        {
                            "uniqueName": "Allocation",
                            "aggregation": "sum"
                        },
                        {
                            "uniqueName": "GS_No",
                            "aggregation": "count"
                        }
                    ]
                },
            },
            licenseKey: 'Z7HI-XG503S-5O4M4H-6F456Z-0A3E3Z-1X663C-5O4R35-4R'
        })
    }

    me.createPivotTable = function () {
        var derivers = $.pivotUtilities.derivers;
        var renderers = $.extend($.pivotUtilities.renderers,
            $.pivotUtilities.c3_renderers,
            $.pivotUtilities.d3_renderers,
            $.pivotUtilities.export_renderers);
        $("#output").pivotUI(adpVM.schemesList, {
            renderers: renderers,
            rendererOptions: {sort: {direction: "desc", column_key: ['Allocation']}},
            rows: ['Sector'],
            cols: [],
            vals: ["Allocation"],
            rendererName: "Table",
            aggregatorName: "Sum",
            // rowOrder: "value_z_to_a", colOrder: "value_z_to_a",
            // rendererOptions: {
            //     c3: { data: {colors: {
            //         Liberal: '#dc3912', Conservative: '#3366cc', NDP: '#ff9900',
            //         Green:'#109618', 'Bloc Quebecois': '#990099'
            //     }}}
            // }
        });
    }
    me.exportTo = function (type) {
        var source = $('table.pvtTable')[0];//document.getElementsByClassName("pvtTable"); //$('td.pvtRendererArea'); //.find("div"); //table.pvtTable
        // var doc = new jsPDF('p', 'pt');
        // var elem =  source; //document.getElementById("basic-table");
        // var res = doc.autoTableHtmlToJson(elem);
        // doc.autoTable(res.columns, res.data);
        // doc.save("table.pdf");
        // var doc = new jsPDF();
        // doc.fromHTML(
        //     source,
        //     15,
        //     15,
        //     {
        //         'width': 800
        //     });
        //         doc.output("dataurlnewwindow");

        // var doc = new jsPDF();
        html2canvas(source, {
            onrendered: function (canvas) {
                // document.body.appendChild(canvas);
                // var ctx = canvas.getContext('2d');
                // var imgData = canvas.toDataURL("image/png", 1.0);
                // var width = canvas.width;
                // var height = canvas.clientHeight;
                // pdf.addImage(imgData, 'PNG', 20, 20, (width - 10), (height));
                var pdf = new jsPDF('landscape');
                pdf.addHTML(canvas, function () {
                    pdf.save('stacking-plan.pdf');
                });

            }
        });
        // setTimeout(function() {
        //
        //     //jsPDF code to save file
        //     pdf.save('sample.pdf');
        //
        //     //Generate BLOB object
        //     var blob = pdf.output("blob");
        //
        //     //Getting URL of blob object
        //     var blobURL = URL.createObjectURL(blob);
        //
        //     //Showing PDF generated in iFrame element
        //     var iframe = document.getElementById('sample-pdf');
        //     iframe.src = blobURL;
        //
        //     //Setting download link
        //     var downloadLink = document.getElementById('pdf-download-link');
        //     downloadLink.href = blobURL;
        // }, 0);


        // setTimeout(function() {
        //     //jsPDF code to save file
        //     pdf.save('sample.pdf');
        // }, 0);
    }

}
