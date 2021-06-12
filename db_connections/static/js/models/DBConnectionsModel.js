/**
 * Created by idrees on 11/19/2018.
 */


var DatabaseConnectionsModel = function () {
    var me = this;
    me.saveAnnexureToDatabase = function (connection_data) {
        $("#myPleaseWait").modal("show");
        var formData = new FormData();
        formData.append('data', JSON.stringify(connection_data));
        $.ajax({
            type: "POST",
            contentType: false,
            processData: false,
            dataType: "json",
            url: 'insert_connection_in_db',
            data: formData,
            success: function (data) {
                $("#myPleaseWait").modal("hide");
                alert(data);
            },
            error: function (xhr, ajaxOptions, thrownError) {
                $("#myPleaseWait").modal("hide");
            },
        });
    };




}