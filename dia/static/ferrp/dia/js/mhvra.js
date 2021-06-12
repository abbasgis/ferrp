/**
 * Created by Mariam on 1/31/2019.
 */
var updateMhvraGridDataWithLocalData = function (data) {
    console.log("in grid data function", data)

    var adapter = $("#grid").jqxGrid('source');
    var source =
        {
            datatype: "json",
            datafields: adapter._source.datafields,
            localdata: data
        };
    var dataAdapter = new $.jqx.dataAdapter(source);
    dataAdapter.dataBind();
    $("#grid").jqxGrid({source: dataAdapter});
    $("#grid").jqxGrid('updatebounddata');
};
function get_mhvra_list_data(projectId) {
    var me = this;
    var url = '/dia/get_hazard_flood_data/?project_id=' + projectId;
    var params = {
        url: url,
        type: "GET",
        // data: data,
        // dataType: "json",
        processData: false,
        contentType: false,
        async: true
        // headers: {'X-CSRFToken': token},
    };
    // var data = callSJAX(params);
    callAJAX(params, function (response) {
        console.log(response)
        me.updateMhvraGridDataWithLocalData(response)

    })
}

var create_jqx_grid = function (projectId) {
        var me = this;
        var projectId=projectId;
        console.log(projectId)
        me.get_mhvra_list_data(projectId);
        me.gridEL = $("#grid");
        var source = {
            datatype: "json",
            datafields: [
                {name: 'category', type: 'string'},
                {name: 'design_criteria', type: 'string'},
                {name: 'value_mhvra', type: 'number'},
                {name: 'value_unit', type: 'string'},
                {name: 'vulnerability', type: 'number'},
                {name: 'damage', type: 'number'},
                {name: 'order_address', type: 'string'},
                {name: 'risk', type: 'number'},
                {name: 'qualitative_measure', type: 'number'},
                {name: 'probability', type: 'number'},
                {name: 'cost_impact ', type: 'number'}

            ]

        };
        var dataAdapter = new $.jqx.dataAdapter(source, {
            loadComplete: function () {
            }
        });
        // create grid.
        me.gridEL.jqxGrid(
            {
                width: '100%',
                source: dataAdapter,
                // pageable: true,
                // autorowheight: true,
                altrows: true,
                groupable:true,
                groups:['category'],
                columnsresize: true,
                columns: [
                    {
                        text: 'Category',
                        columngroup: 'NATURAL',
                        cellsalign: 'center',
                        align: 'center',
                        datafield: 'category',
                        width: 100
                    },
                    {
                        text: 'Design Criteria (dc)',
                        columngroup: 'NATURAL',
                        datafield: 'design_criteria',
                        cellsalign: 'center',
                        align: 'center',
                        width: 140
                    },
                    {
                        text: 'Value MHVRA',
                        columngroup: 'NATURAL',
                        cellsalign: 'center',
                        align: 'center',
                        cellsformat: 'd',
                        datafield: 'value_mhvra',
                        width: 100
                    },
                    {
                        text: 'Value Unit',
                        columngroup: 'NATURAL',
                        datafield: 'value_unit',
                        cellsformat: 'd',
                        cellsalign: 'center',
                        align: 'center',
                        width: 100
                    },
                    {
                        text: 'Damage (D) Km2',
                        columngroup: 'RISK ASSESSMENT',
                        cellsalign: 'center',
                        align: 'center',
                        datafield: 'damage',
                        width: 170
                    },
                    {
                        text: 'Vulnerability',
                        columngroup: 'RISK ASSESSMENT',
                        datafield: 'vulnerability',
                        cellsformat: 'd',
                        cellsalign: 'center',
                        align: 'center',
                        width: 100
                    },
                    {
                        text: 'Risk R (class)',
                        columngroup: 'RISK ASSESSMENT',
                        cellsalign: 'center',
                        align: 'center',
                        datafield: 'risk',
                        width: 120
                    },
                    {
                        text: 'Qualitative Measure',
                        columngroup: 'RISK ASSESSMENT',
                        datafield: 'qualitative_measure',
                        cellsformat: 'd',
                        cellsalign: 'center',
                        align: 'center',
                        width: 140
                    },
                    {
                        text: 'Probability (p)',
                        columngroup: 'RISK ASSESSMENT',
                        datafield: 'probability',
                        cellsformat: 'd',
                        align: 'center',
                        cellsalign: 'center',
                        width: 130
                    },

                ],
                columngroups: [
                    {text: 'RISK ASSESSMENT', align: 'center', name: 'RISK ASSESSMENT'},
                    {text: 'NATURAL HAZARD IDENTIFICATION', align: 'center', name: 'NATURAL'}


                ]
            });
    }