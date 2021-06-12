/**
 * Created by idrees on 11/20/2018.
 */

$(document).ready(function () {

    $('#btnSubmit').on('click', function (e) {
        e.preventDefault();
        var selected = [];
        $('input[name="Select_Tables"]').each(function () {
            if(this.checked == true){
                selected.push($(this).val());
            }
        });
        uploadTablesList(selected);
    });

    function uploadTablesList(table_list) {
        $("#myPleaseWait").modal("show");
        var formData = new FormData();
        formData.append('data', JSON.stringify(table_list));
        $.ajax({
            type: "POST",
            contentType: false,
            processData: false,
            dataType: "json",
            url: 'insert_tables_in_db',
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


});

