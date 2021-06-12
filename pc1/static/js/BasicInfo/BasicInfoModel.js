/**
 * Created by idrees on 9/4/2018.
 */

var BasicInfoModel = function () {
    try {

        var me = this;

        me.buttonStatus = {
            authorities_responsible: false,
            plan_provision: false,
            project_objectives: false,
            capital_cost_estimates: false,
            physical_plan: false,
            financial_plan: false,
            financial_plan_text: false,
            annual_operating_cost: false,
            demand_and_supply_analysis: false,
            benefits_of_the_projects_analysis: false,
            implementation_schedule: false,
            ms_and_mp: false,
            additional_projects_decisions_required: false,
            certified: false
        }

        me.setButtonStatus = function (buttonName) {
            for (var key in me.buttonStatus) {
                if (key === buttonName) {
                    me.buttonStatus[key] = true;
                } else {
                    me.buttonStatus[key] = false;
                }
            }
        }

        me.getButtonStatus = function () {
            for (var key in me.buttonStatus) {
                var status = me.buttonStatus[key];
                if (status == true) {
                    return key;
                    break;
                }
            }
        }

        me.getButtonName = function (info) {
            if (info == 'authorities_responsible') {
                return 'btnAuthResp';
            }
            if (info == 'plan_provision') {
                return 'btnPlanProvision';
            }
            if (info == 'project_objectives') {
                return 'btnProjectObjectives';
            }
            if (info == 'capital_cost_estimates') {
                return 'btnCapitalCostEstimates';
            }
            if (info == 'physical_plan') {
                return 'btnCCE_PhysicalPlan';
            }
            if (info == 'financial_plan') {
                return 'btnCCE_FinancialPlan';
            }
            if (info == 'annual_operating_cost') {
                return 'btnAnnualOperatingCost';
            }
            if (info == 'demand_and_supply_analysis') {
                return 'btnDemandAndSupplyAnalysis';
            }
            if (info == 'benefits_of_the_projects_analysis') {
                return 'btnBenefitsOfTheProjectAnalysis';
            }
            if (info == 'financial_plan') {
                return 'btnFinancialPlan';
            }
            if (info == 'financial_plan_text') {
                return 'btnFinancialPlanText';
            }
            if (info == 'implementation_schedule') {
                return 'btnImplementationSchedule';
            }
            if (info == 'ms_and_mp') {
                return 'btnMSandMR';
            }
            if (info == 'additional_projects_decisions_required') {
                return 'btnAPDR';
            }
            if (info == 'certified') {
                return 'btnCertified';
            }
        }

        me.addRemoveCSSClasses = function (btn) {
            $("#" + btn).removeClass("btn-primary glyphicon-upload").addClass("btn-success glyphicon-ok");
        }
        me.resetDefaultClasses = function (btn) {
            $("#" + btn).removeClass("btn-success glyphicon-ok").addClass("btn-primary glyphicon-upload");
        }

        me.exportToTable = function () {
            var regex = /^([a-zA-Z0-9\s_\\.\-:])+(.xlsx|.xls)$/;
            /*Checks whether the file is a valid excel file*/
            if (regex.test($("#excelfile").val().toLowerCase())) {
                var xlsxflag = false;
                /*Flag for checking whether excel is .xls format or .xlsx format*/
                if ($("#excelfile").val().toLowerCase().indexOf(".xlsx") > 0) {
                    xlsxflag = true;
                }
                /*Checks whether the browser supports HTML5*/
                if (typeof (FileReader) != "undefined") {
                    var reader = new FileReader();
                    reader.onload = function (e) {
                        var data = e.target.result;
                        /*Converts the excel data in to object*/
                        if (xlsxflag) {
                            var workbook = XLSX.read(data, {type: 'binary'});
                        }
                        else {
                            var workbook = XLS.read(data, {type: 'binary'});
                        }
                        /*Gets all the sheetnames of excel in to a variable*/
                        var sheet_name_list = workbook.SheetNames;

                        var cnt = 0;
                        /*This is used for restricting the script to consider only first sheet of excel*/
                        sheet_name_list.forEach(function (y) { /*Iterate through all sheets*/
                            /*Convert the cell value to Json*/
                            if (xlsxflag) {
                                var exceljson = XLSX.utils.sheet_to_json(workbook.Sheets[y]);
                                // var excelCSV = XLSX.utils.sheet_to_csv(workbook.Sheets[y]);
                                // alert(excelCSV);
                            }
                            else {
                                var exceljson = XLS.utils.sheet_to_row_object_array(workbook.Sheets[y]);
                                // var excelCSV = XLS.utils.sheet_to_csv(workbook.Sheets[y]);
                                // alert(excelCSV);
                            }
                            if (exceljson.length > 0 && cnt == 0) {
                                me.bindTable(exceljson, '#exceltable');
                                cnt++;
                            }
                        });
                        $('#exceltable').show();
                        var tableData = document.getElementById("divExcel").innerHTML;// $('#exceltable').html();
                        var editorText = $("#editor").jqxEditor().val();
                        var text = editorText + '<br/>' + tableData;
                        // alert(text);
                        $("#editor").jqxEditor().val(text);
                        $('#exceltable').hide();

                    }
                    if (xlsxflag) {/*If excel file is .xlsx extension than creates a Array Buffer from excel*/
                        reader.readAsArrayBuffer($("#excelfile")[0].files[0]);
                    }
                    else {
                        reader.readAsBinaryString($("#excelfile")[0].files[0]);
                    }
                }
                else {
                    alert("Sorry! Your browser does not support HTML5!");
                }
            }
            else {
                alert("Please upload a valid Excel file!");
            }
        }

        me.exportExcelToHTML = function () {
            var input = document.getElementById("excelfile");
            var reader = new FileReader();
            reader.readAsArrayBuffer(input.files[0]);
            reader.onload = function () {
                var data = new Uint8Array(reader.result);
                var wb = XLSX.read(data, {type: 'array'});
                var html = XLSX.write(wb, {type: 'binary', bookType: 'html'});
                var editorText = $("#editor").jqxEditor().val();
                var text = editorText + '<br/>' + html;
                $("#editor").jqxEditor().val(text);
            }
        }

        me.readExcelFile = function (file) {
            $('#myPleaseWait').modal('show');
            try {
                var reader = new FileReader();
                reader.readAsArrayBuffer(file.files[0]);
                reader.onload = function () {
                    var data = new Uint8Array(reader.result);
                    var wb = XLSX.read(data, {type: 'array'});
                    var htmlstr = XLSX.write(wb, {type: 'binary', bookType: 'html'});
                    return htmlstr;
                    $('#myPleaseWait').modal('hide');
                }
            } catch (err) {
                $('#myPleaseWait').modal('hide');
                alert(err);
            }
        }

        me.bindTable = function (jsondata, tableid) {/*Function used to convert the JSON array to Html Table*/
            var columns = me.bindTableHeader(jsondata, tableid);
            /*Gets all the column headings of Excel*/
            for (var i = 0; i < jsondata.length; i++) {
                var row$ = $('<tr/>');
                for (var colIndex = 0; colIndex < columns.length; colIndex++) {
                    var cellValue = jsondata[i][columns[colIndex]];
                    if (cellValue == null)
                        cellValue = "";
                    row$.append($('<td/>').html(cellValue));
                }
                $(tableid).append(row$);
            }
        }

        me.bindTableHeader = function (jsondata, tableid) {/*Function used to get all column names from JSON and bind the html table header*/
            var columnSet = [];
            var headerTr$ = $('<tr/>');
            var row = jsondata[0];
            for (var key in row) {
                if (row.hasOwnProperty(key)) {
                    if ($.inArray(key, columnSet) == -1) {/*Adding each unique column names to a variable array*/
                        columnSet.push(key);
                        headerTr$.append($('<th/>').html(key));
                    }
                }
            }
            $(tableid).append(headerTr$);
            return columnSet;
        }

        me.saveDataToDatabase = function () {
            $.ajax({
                type: "POST",
                contentType: "application/text",
                dataType: "text",
                url: '../insert_basic_info_data_in_db',
                data: JSON.stringify(localData),
                success: function (data) {
                    alert(data);
                }
            });
        }

        me.saveAnnexureToDatabase = function (annexure) {
            $.ajax({
                type: "POST",
                contentType: "application/text",
                dataType: "text",
                url: '../insert_annexure_in_db',
                data: JSON.stringify(annexure),
                success: function (data) {
                    alert(data);
                }
            });
        }

        //side_basic_info
    } catch (err) {
        console.log(err.message);
    }
}
