/**
 * Created by idrees on 5/9/2017.
 */
var TabularDataModel = function (data) {
    var me = this;
    me.schemesData = data
    me.containerDiv = null;
    me.initialize = function (containerDiv) {
        me.containerDiv = containerDiv;
        try {
            var output = $(' <div id="output" style="margin: 30px;"></div>')
            me.containerDiv.append(output);
            me.createFlexMonsterPivotTable(me.schemesData);
            // me.createPivotTable();
        }catch(err){
            console.error(err.stack);
        }
    }

    me.createFlexMonsterPivotTable = function (data) {
        var flexmonster = new Flexmonster({
            container: 'containerDiv',
            componentFolder: "https://cdn.flexmonster.com/",
            toolbar: true,
            height:pwHeight - 70,
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

    me. createTypeofAttributeList = function(){
        var obj = me.schemesData[0];
        var hiddenAttibutes = [];
        var aggregators = [];
        //var regexp = /^[0-9]+([.]*[0-9]*)?$/g;
        //var result =
        for(var key in obj){
            //var res = parseFloat(obj[key]);
            if(typeof obj[key] != "string"){
                hiddenAttibutes.push(key);
                aggregators.push(key);
            }
        }
        return {ha:hiddenAttibutes,agg:aggregators};
    }
    me.createPivotTable = function(){
        var typeOfAttribute = me.createTypeofAttributeList();
        var derivers = $.pivotUtilities.derivers;
        var renderers = $.extend($.pivotUtilities.renderers,
            //$.pivotUtilities.c3_renderers,
            $.pivotUtilities.d3_renderers,
            $.pivotUtilities.export_renderers);
        $("#output").pivotUI(me.schemesData, {
            renderers: renderers,
            //hiddenAttributes: typeOfAttribute.ha,
            //dreviedAttibutes: derivers,
            rendererOptions: { sort: { direction : "desc", column_key : [ 'Allocation' ]} },
            rows: ['Main Sector'],
            cols:['Year'],
            vals: ['Allocation'],
            aggregators: $.pivotUtilities.aggregators,
            //renderers:   renderers,
            rendererName:"Table",
            aggregatorName : "Sum"
        });
    }
    me.exportTo = function(type){
        var source = $('table.pvtTable')[0];
        html2canvas(source, {
            onrendered: function(canvas) {
                var pdf = new jsPDF('landscape');
                pdf.addHTML(canvas, function() {
                    pdf.save('stacking-plan.pdf');
                });

            }
        });
    }

}
