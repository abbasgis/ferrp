/**
 * Created by idrees on 11/13/2018.
 */

var DimensionModel = function (analysisVM) {
    var me = this;
    me.initialize = function () {
        try {
            analysisVM.panelHeader('<span class="glyphicon glyphicon-book"></span> ADP Dimension Modeling');
            var output = $(' <div id="output" style="margin: 30px;"></div>')
            analysisVM.mainPnlBody.append(output);
            me.createFlexMonsterPivotTable(schemesList);
        }catch(err){
            console.error(err.stack);
        }
    }

    me.createFlexMonsterPivotTable = function (data) {
        var flexmonster = new Flexmonster({
            container: 'mainpnlbody',
            componentFolder: "https://cdn.flexmonster.com/",
            toolbar: true,
            height:600,
            report: {
                dataSource: {
                    data: data
                },
                "slice": {
                    "rows": [
                        {
                            "uniqueName": "Main_Sector",
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
                        }
                    ]
                },
            },
            licenseKey: 'Z7HI-XG503S-5O4M4H-6F456Z-0A3E3Z-1X663C-5O4R35-4R'
        })
    }

}

