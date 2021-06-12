/**
 * Created by Shakir on 7/5/2017.
 */
/**
 * Created by Shakir on 2/7/2017.
 */
var treeGridEl = $('#treeGrid');
$(document).ready(function () {
    $("#financial").show();
    populateProjectsCombo(projects);

    createActivityTreeGrid(treeGridEl);
    $('.selectpicker').selectpicker('refresh');

});
function populateProjectsCombo(data) {
    for (var key in data) {
        $('#cmb_projects').append('<option value=' + data[key].project_id + ' >'
            + data[key].project_name + '</option>');
    }
}
$('#cmb_projects').on('change', function (e) {
    var project_id = e.target.value;
    updateGridDataWithLocalData(project_id);
});
function createActivityTreeGrid(treeGridEl) {
    var source =
        {
            dataType: "json",
            dataFields: [
                {name: 'dir_name', type: 'string'},
                {name: 'dir_level', type: 'number'},
                {name: 'parent_dir_id_id', type: 'number'},
                {name: 'project_id', type: 'string'},
                {name: 'file_name', type: 'string'},
                {name: 'updated_at', type: 'date'},
                {name: 'file_type', type: 'string'},
                {name: 'file_size', type: 'float'},
                {name: 'children', type: 'array'},
                {name: 'expanded', type: 'bool'},
                {name: 'dir_id', type: 'number'},
                {name: 'created_by', type: 'number'}

            ],
            hierarchy: {
                keyDataField: {name: 'dir_id'},
                parentDataField: {name: 'parent_dir_id_id'},
                //root: 'children'
            },
            url: '/projects/proj_dir_data?project_id=' + project_id,
            //updateRow: function (rowID, rowData, commit) {
            //    commit(true);
            //},
            id: 'dir_id',
            // localData: data
        };
    var dataAdapter = new $.jqx.dataAdapter(source);
    var cellClass = function (row, dataField, cellText, rowData) {
        var cellValue = rowData['dir_level'];
        var level = parseInt(cellValue);
        if (level === 0) {
            return "level0";
        }
        if (level === 1) {
            return 'level1';
        }
        if (level === 2) {
            return 'level2';
        }
        else {
            return 'same';
        }

    };

    // create Tree Grid
    treeGridEl.jqxTreeGrid(
        {
            theme: theme,
            source: dataAdapter,
            sortable: true,
            scrollBarSize: 7,
            //    enableTooltips: true,
            height: 500,// '100%',
            width: '100%',
            //  showAggregates: true,
            columnsResize: true,
            //   rowHeight:50,
            autoRowHeight: false,
            columnsReorder: true,
            altRows: true,
            // hierarchicalCheckboxes: true,
            // checkboxes: true,
            filterable: true,
            filterMode: 'advanced',
            icons: function (rowKey, rowData) {

                if (rowData.file_name !== null) {
                    return '/static/assets/img/file.png';
                } else {
                    return '/static/assets/img/folder.png';
                }

            },
            ready: function () {
                treeGridEl.jqxTreeGrid('expandAll');
                treeGridEl.jqxTreeGrid('sortBy', 'dir_name', 'asc');
            },
            //editable: true,
            columns: [
                {
                    text: 'Task',
                    width: 450,
                    dataField: 'dir_name',
                    pinned: true,
                    // cellClassName: cellClass
                },
                {
                    text: 'View', width: 50,
                    cellClassName: cellClass,
                    cellsRenderer: function (rowKey, dataField, value, data) {
                        if (data.file_name !== null) {
                            return "<div style='margin: 0px 20px;'><img id=v-" + rowKey + " onclick='icon_action(event)' style='margin-top: 2px;' width='16' height='16' src='/static/assets/img/view.png'/></div>";
                        }
                    }
                },
                {
                    text: 'Download', width: 90,
                    cellClassName: cellClass,
                    cellsRenderer: function (rowKey, dataField, value, data) {
                        if (data.file_name !== null) {
                            return "<div style='margin: 0px 20px;'><img id=d-" + rowKey + " onclick='icon_action(event)' style='margin-top: 2px;' width='16' height='16' src='/static/assets/img/download.png'/></div>";
                        }
                    }
                },
                {
                    text: 'Edit', width: 50,
                    cellClassName: cellClass,
                    cellsRenderer: function (rowKey, dataField, value, data) {
                        if (data.file_name !== null) {
                            return "<div style='margin: 0px 20px;'><img id=e-" + rowKey + " onclick='icon_action(event)' style='margin-top: 2px;' width='16' height='16' src='/static/assets/img/pencil.png'/></div>";
                        }
                    }
                },
                {
                    text: 'Type',
                    // hidden: true,
                    width: 100,
                    dataField: 'file_type',
                    cellClassName: cellClass
                },
                {
                    text: 'Size',
                    // hidden: true,
                    width: 100,
                    dataField: 'file_size',
                    cellClassName: cellClass,
                    cellsrenderer: function (row, column, value, defaulthtml, columnproperties) {
                        value = (value / 1024).toFixed(2);
                        return value + ' KB';
                    }
                },
                {
                    text: 'Date Modified',
                    cellsformat: 'f',
                    // width: 450,
                    dataField: 'updated_at',
                    cellClassName: cellClass
                },
                {
                    text: 'File Name',
                    hidden: true,
                    // width: 450,
                    dataField: 'file_name',
                    cellClassName: cellClass
                },
                {
                    text: 'Level',
                    dataField: 'dir_level',
                    // width: 100,
                    hidden: true,
                    cellClassName: cellClass
                },
                {
                    text: 'Parent Level',
                    dataField: 'parent_dir_id_id',
                    width: 100,
                    hidden: true,
                    cellClassName: cellClass
                },
                {
                    text: 'project_id',
                    editable: false,
                    hidden: true,
                    width: 100,
                    dataField: 'project_id',
                    // hidden: true,
                    cellClassName: cellClass
                },
                {
                    text: 'dir_id',
                    dataField: 'act_id',
                    editable: false,
                    width: 100,
                    hidden: true,
                    cellClassName: cellClass
                },
                {
                    text: 'created_by',
                    dataField: 'created_by',
                    editable: false,
                    width: 100,
                    hidden: true,
                    cellClassName: cellClass
                }
            ]

        });
    treeGridEl.on('bindingComplete', function () {
        treeGridEl.jqxTreeGrid('expandAll');
    });

}

function updateGridDataWithLocalData(project_id) {
    var adapter = treeGridEl.jqxTreeGrid('source');
    var gridSource = adapter._source;
    var newSource = {
        dataType: "json",
        dataFields: gridSource.dataFields,
        hierarchy: {
            keyDataField: {name: 'dir_id'},
            parentDataField: {name: 'parent_dir_id_id'},
            //root: 'children'
        },
        id: 'act_id',
        url: '/projects/proj_dir_data?project_id=' + project_id,
        //localData: data
    };
    var newDataAdapter = new $.jqx.dataAdapter(newSource);
    treeGridEl.jqxTreeGrid({
        source: newDataAdapter
    });
    treeGridEl.jqxTreeGrid('updateBoundData');


}
function icon_action(e) {
    var img_id = e.currentTarget.id;
    var arr_id = img_id.split('-');
    var action = arr_id[0];
    var rowKey = arr_id[1];
    var row = treeGridEl.jqxTreeGrid('getRow', rowKey);
    var url = '/projects/proj_action_file/?action=' + action + '&file_name=' + row.file_name;
    window.location.href = url;
}
// showAlertDialog("Working . .",dialogTypes.error);
//
// function test() {
//     // var formData = new FormData();
//     // formData.append("username", "Groucho");
//     // formData.append("accountnum", 123456);
//     var url = '/projects/proj_dir_data?project_id=1';
//     var params = {
//         url: url,
//         type: "GET",
//         // data: formData,
//         dataType: "json",
//         processData: false,
//         contentType: false,
//         async: true,
//         // headers: {'X-CSRFToken': token},
//     };
//
//     callAJAX(params, function (data) {
//         alert(data);
//     });
// }
