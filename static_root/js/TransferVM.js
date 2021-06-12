/**
 * Created by idrees on 5/17/2018.
 */

var surveyIdList = []
$(document).ready(function () {
    $( "#btnTransfer" ).click(function() {
        var surveyType = $('#typeList').find('option:selected').val();
        var from_date = $( "#fromDate" ).val();
        var to_date = $( "#toDate" ).val();

        var url = '../survey_ids_list?from_date=' + from_date + '&to_date='+to_date + '&type_id='+surveyType
        $.ajax({
            type: 'GET',
            url: url,
            timeout: 9000000,
            error: function (xhr, ajaxOptions, thrownError) {
                alert(thrownError);
            },
            success: function (data) {
                alert(data);
                var jsonData = JSON.parse(data);
                populateSurveyIdList(jsonData);
                transferData();
            }
        });
    });
});

function transferData() {
    var surveyType = $('#typeList').find('option:selected').val();
    for (var i = 0; i<surveyIdList.length; i++){
        var surveyId = surveyIdList[i];
        var url = '../parse_survey_property?survey_id=' + surveyId + '&survey_type_id=' + surveyType;
        // if(i > 1335){
            jqueryGetRequest(url, i, surveyIdList.length);
        // }
    }
    alert("Done.");
}

function populateSurveyIdList(data) {
    for(var i = 0; i<data.length; i++){
        surveyIdList.push(data[i]['survey_id']);
    }
}
function jqueryGetRequest(url, i, length) {
    $.ajax({
        type: 'GET',
        url: url,
        timeout: 9000000,
        error: function (xhr, ajaxOptions, thrownError) {
            $("#txtResult").val('Processed ' + i + ' of ' + length + ' records. Error');
        },
        success: function (data) {
            $("#txtResult").val('Processed ' + i + ' of ' + length + ' records.');
        }
    });
}