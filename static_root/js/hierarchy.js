$(document).ready(function () {
    create_drop_down_list()


});
function create_drop_down_list() {

    var data_tree = [
        {
            "code": "irb",
            "name": "Irrigation_Boundary"
        },
        {
            "code": "bor",
            "name": "Board_Of_Revenue"
        },
        {
            "code": "adb",
            "name": "Administration_Boundary"
        },
        {
            "code": "lg",
            "name": "Local_Government"
        }

    ];
    var resource =
        {
            datatype: "json",
            datafields: [
                {name: 'code'},
                {name: 'name'}
            ],
            localdata: data_tree,
            //async: true
        };
    var dataAdapter = new $.jqx.dataAdapter(resource);

    $("#toppane").jqxDropDownList({
        selectedIndex: 2,
        source: dataAdapter,
        displayMember: "name",
        valueMember: "code",
        width: 210,
        height: 50,
        theme: 'energyblue',


    });
    $("#toppane").on('select', function (event) {
        if (event.args) {
            var item = event.args.item;
            if (item) {
                var url = '/tree/get_admin_tree?code=' + item.value;
                $.ajax({
                    url: url, success: function (result) {
                        create_admin_tree(result)
                    }
                });


            }
        }
    });
}

function create_admin_tree(data) {
    var source =
        {
            datatype: "json",
            datafields: [
                {name: 'id'},
                {name: 'parentid'},
                {name: 'text'},
                {name: 'value'}
            ],
            id: 'id',
            localdata: data
        };
    // create data adapter.
    var dataAdapter = new $.jqx.dataAdapter(source);
    // perform Data Binding.
    dataAdapter.dataBind();
    // get the tree items. The first parameter is the item's id. The second parameter is the parent item's id. The 'items' parameter represents
    // the sub items collection name. Each jqxTree item has a 'label' property, but in the JSON data, we have a 'text' field. The last parameter
    // specifies the mapping between the 'text' and 'label' fields.
    var records = dataAdapter.getRecordsHierarchy('id', 'parentid', 'items', [{name: 'text', map: 'label'}]);
    $('#leftpane').jqxTree({
        source: records,
        theme: 'energyblue',
        height: 200,
        width: 350,

      });
    $('#leftpane').bind('select', function (source) {
        var extent = source.args.element;
        var item = $('#leftpane').jqxTree('getItem', extent);
        alert(item.value);
    })

}


