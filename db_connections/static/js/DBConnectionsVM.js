/**
 * Created by idrees on 11/19/2018.
 */

$("#myPleaseWait").modal("show");
$(document).ready(function () {
    var dbConModel = new DatabaseConnectionsModel();
    $.ajax({
        type: 'GET',
        dataType: 'text',
        url: 'engines_list',
        timeout: 9000000,
        success: function (data) {
            $("#myPleaseWait").modal("hide");
            var jsonData = JSON.parse(data);
            $.each(jsonData, function (key, value) {
                $('#cmbDbProviders').append($('<option>', {value: value.id}).text(value.name));
            });
        },
        error: function (xhr, ajaxOptions, thrownError) {
            $("#myPleaseWait").modal("hide");
        },
    });

    $("#btnAddNewConnection").click(function () {
        $("#addConnectionModal").modal("show");
    });

    $("#btnTestConnection").click(function () {
        alert('Connection Successfull...');
    });

    // $("#btnAddConnection").click(function () {
    //     // alert('Connection Added...');
    //     var conn_data = {db_engine:null, server:null, port:null, database:null, username:null, password:null};
    //     conn_data.db_engine = $('#cmbDbProviders  option:selected').text();
    //     conn_data.server = $('#txtHost').val();
    //     conn_data.port = $('#txtPort').val();
    //     conn_data.database = $('#txtDBName').val();
    //     conn_data.username = $('#txtUserName').val();
    //     conn_data.password = $('#txtPassword').val();
    //     dbConModel.saveAnnexureToDatabase(conn_data);
    // });





});