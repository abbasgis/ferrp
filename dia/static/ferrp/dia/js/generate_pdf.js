/**
 * Created by Mariam on 2/18/2019.
 */

function pdf_generation() {
    // alert("in pdf function");

    var date = new Date();
    var fileName = encodeURIComponent(date);
    var fileNameExt = fileName + '.pdf';
    // var div= $("#bs-sidebar-navbar-collapse-1");
    var modelText = '';



    $.ajax({
        type: "POST",
        url: '/dia/print_dia',
        data: {
            "sourceHtml": modelText,
            "outputFilename": fileNameExt,
            "csrfmiddlewaretoken": token,
            "state": "inactive"
        },
        success: function (data, textStatus, jqXHR) {
            // var pdfWin = window.open("data:application/pdf;base64, " + data, '', 'height=650,width=840');
            a = document.createElement('a');
            var blob = new Blob([data], {type: 'application/pdf'})
            a.href = window.URL.createObjectURL(blob);
            a.download = fileNameExt;
            a.style.display = 'none';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            // window.open(data, content_type='application/pdf');
            // window.open(escape(data), "Title", "");
            // HttpResponse(response.getvalue(), content_type='application/pdf')
            // some actions with this win, example print...
        },
        error: function (jqXHR) {
            showError("...");
        }
    });
}
