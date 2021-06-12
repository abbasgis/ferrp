/**
 * Created by Dr. Ather Ashraf on 5/19/2018.
 */
var FilterItemViewModel = function (itemList, headingKey, iconKey, itemNameKey, itemUrl) {
    var me = this;
    me.itemList = itemList;
    me.headingKey = headingKey;
    me.iconKey = iconKey;
    me.itemNameKey = itemNameKey;
    me.url = itemUrl;
    me.itemType = "Item";
    me.gbList = null;

    $(".btn-clear-filter").on('click', function () {
        me.clearFilter();
    })
    $("#itemKey").on('change', function (sel) {
        var value = this.value;
        // alert(value);
        $('#itemValue').find('option').remove().end();
        if (value != "-1") {
            me.gbList = _.groupBy(itemList, value)
            // $('#itemValue').selectpicker("refresh");
            $('#itemValue').append($('<option>', {value: "-1", text: ""}));
            for (var key in me.gbList) {
                $('#itemValue').append($('<option>', {
                    value: key,
                    text: key
                }));
            }
        }
        $('#itemValue').selectpicker("refresh");
    })
    $('#itemValue').on('change', function (sel) {
            var value = this.value;
            if (value != "-1") {
                var list = me.gbList[value];
                me.applyFilter(list);
            } else {
                me.clearFilter();
            }
        }
    )
    me.clearFilter = function () {
        var list = me.itemList;
        me.applyFilter(list)
    }
    me.applyFilter = function (list) {
        $('#itemListBody').empty();
        for (var i = 0; i < list.length; i++) {

            var heading = list[i][me.headingKey];
            var img_url = list[i][me.iconKey];
            var item_name = list[i][me.itemNameKey];
            var item_url = me.url + item_name;

            var row = $('<div class="row"></div>');
            $('#itemListBody').append(row);
            var col = $('<div class="col-md-10 col-md-offset-1"></div>');
            row.append(col);
            var panel = $('<div class="panel panel-default"></div>');
            col.append(panel);

            var panel_header = $('<div class="panel-heading"></div>');
            var header_info = $('<h2>' + heading + '</h2>');
            panel_header.append(header_info);
            panel.append(panel_header);

            var panel_body = $('<div class="panel-body"></div>');
            var body_row = $('<div class="row"></div>');
            panel_body.append(body_row);
            var body_col_icon = $('<div class="col-md-4"></div>');
            body_row.append(body_col_icon);
            if (img_url != null) {
                var img_div = $('<div class="imgdiv center-block" align="center" style="height:120px; padding:5px"> ' +
                    '<img class="img-responsive center-block" width="200" height="120" src="' + img_url + '"> ' +
                    '</div>');
            } else {
                var img_div = $('<div class="imgdiv center-block" align="center" style="height:120px; padding:5px"> ' +
                    '<i id="alternateIcon" class="glyphicon glyphicon-file"></i> </div>');
            }
            body_col_icon.append(img_div);
            var body_col_detail = $('<div class="col-md-8"></div>');
            body_row.append(body_col_detail);
            var detail_table = $('<table class="table table-striped table-condensed"></table>');
            body_col_detail.append(detail_table)
            var tbody = $('<tbody></tbody>');
            detail_table.append(tbody);
            for (var key in list[i]) {
                if (key != "icon" && key != "layer_name") {
                    var tr = $('<tr></tr>');

                    var th = $('<th>' + key + '</th>');
                    var td = $('<td>' + list[i][key] + '</td>');
                    tr.append(th);
                    tr.append(td);
                    tbody.append(tr);

                }
            }
            panel.append(panel_body);

            var panel_footer = $('<div class="panel-footer"></div>');
            var view_layer_btn = $('<a href="' + item_url + '" id="btnViewLayer" class="btn btn-primary btn-block">View ' + me.itemType + '</a>');
            panel_footer.append(view_layer_btn);
            panel.append(panel_footer);

        }
    }
}