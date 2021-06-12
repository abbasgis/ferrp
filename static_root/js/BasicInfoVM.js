/**
 * Created by idrees on 9/4/2018.
 */

var localData = {
    gs_no: '',
    authorities_responsible: '',
    implementation_schedule_from_date: '',
    implementation_schedule_to_date: '',
    plan_provision: '',
    project_objectives: '',
    capital_cost_estimates: '',
    annual_operating_cost: '',
    demand_and_supply_analysis: '',
    benefits_of_the_projects_analysis: '',
    physical_plan: '',
    financial_plan: '',
    financial_plan_text: '',
    implementation_schedule: '',
    ms_and_mp: '',
    additional_projects_decisions_required: '',
    certified: '',
};

var annexures_list = [];

$('#myPleaseWait').modal('show');
$(document).ready(function () {
    var basicInfoModel = new BasicInfoModel();
    localData.gs_no = gs_no;
    $.ajax({
        type: "GET",
        url: '../get_scheme_pc1_detail?scheme=' + gs_no,
        success: function (data) {
            $('#myPleaseWait').modal('hide');
            localData = JSON.parse(data);
            for (var key in localData) {
                var data = localData[key];
                if (data) {
                    var buttonName = basicInfoModel.getButtonName(key);
                    basicInfoModel.addRemoveCSSClasses(buttonName);
                }
            }
        },
        error: function (xhr, ajaxOptions, thrownError) {
            $('#myPleaseWait').modal('hide');
            alert(thrownError);
        },
    });

    $("#createPDF").click(function () {
        var titlePage = getTitlePage();
        var basicInfo = getBasicInfoHTMLTable();
        var annexures = getAnnexuresHtml();
        var printWindow = window.open('', '', 'height=800,width=1000');
        printWindow.document.write('<html><head><title>' + detail.s_name + '</title>');
        printWindow.document.write('<meta name="viewport" content="width=device-width, initial-scale=1">');
        printWindow.document.write('<style> @media print{@page{ size:A4;margin-top: 2.5cm; margin-bottom: 2.5cm; margin-right: 2cm; margin-left: 2cm;} h1 {page-break-before: always;} table, th, td {border: 1px solid black;border-collapse: collapse;}</style>');
        printWindow.document.write('</head><body >');
        printWindow.document.write(titlePage);
        printWindow.document.write(basicInfo);
        printWindow.document.write(annexures);

        printWindow.document.write('</body></html>');
        printWindow.document.close();
        printWindow.print();
    });

    $('#window').jqxWindow({
        autoOpen: false,
        position: 'center',
        theme: 'bootstrap',
        width: 700,
        height: 400,
        resizable: true,
        isModal: false,
        okButton: $('#btnSaveContent'),
        cancelButton: $('#cancel'),
        showCollapseButton: true,
        animationType: 'fade',
        initContent: function () {
            $("#editor").jqxEditor({
                    width: '100%',
                    height: 325,
                    tools: ' file | annexure',
                    createCommand: function (name) {
                        switch (name) {
                            case "file":
                                return {
                                    type: 'button',
                                    tooltip: 'Upload excel file',
                                    init: function (widget) {
                                        widget.jqxButton({height: 25, width: 100});
                                        widget.html("<span style='line-height: 24px;'>Upload Excel</span>");
                                    },
                                    refresh: function (widget, style) {
                                    },
                                    action: function (widget, editor) {
                                        $('#uploadExcelModal').modal('show');
                                    }
                                }
                            case "annexure":
                                return {
                                    type: 'button',
                                    tooltip: 'Attach Annexure file',
                                    init: function (widget) {
                                        widget.jqxButton({height: 25, width: 125});
                                        widget.html("<span style='line-height: 24px;'>Attach Annexure</span>");
                                    },
                                    refresh: function (widget, style) {
                                    },
                                    action: function (widget, editor) {
                                        $('#uploadAnnexureModal').modal('show');
                                    }
                                }
                        }
                    }
                }
            );
        }
    });
    $("#btnAuthResp").click(function () {
        basicInfoModel.setButtonStatus('authorities_responsible');
        $('#window').jqxWindow('open');
        $("#editor").jqxEditor().val('');
        $("#editor").jqxEditor().val(localData['authorities_responsible']);

    });
    $("#btnPlanProvision").click(function () {
        basicInfoModel.setButtonStatus('plan_provision');
        $('#window').jqxWindow('open');
        $("#editor").jqxEditor().val('');
        $("#editor").jqxEditor().val(localData['plan_provision']);

    });
    $("#btnProjectObjectives").click(function () {
        basicInfoModel.setButtonStatus('project_objectives');
        $('#window').jqxWindow('open');
        $("#editor").jqxEditor().val('');
        $("#editor").jqxEditor().val(localData['project_objectives']);

    });
    $("#btnCapitalCostEstimates").click(function () {
        basicInfoModel.setButtonStatus('capital_cost_estimates');
        $('#window').jqxWindow('open');
        $("#editor").jqxEditor().val('');
        $("#editor").jqxEditor().val(localData['capital_cost_estimates']);

    });
    $("#btnCCE_PhysicalPlan").click(function () {
        basicInfoModel.setButtonStatus('physical_plan');
        $('#window').jqxWindow('open');
        $("#editor").jqxEditor().val('');
        $("#editor").jqxEditor().val(localData['physical_plan']);
    });
    $("#btnCCE_FinancialPlan").click(function () {
        basicInfoModel.setButtonStatus('financial_plan');
        $('#window').jqxWindow('open');
        $("#editor").jqxEditor().val('');
        $("#editor").jqxEditor().val(localData['financial_plan']);

    });
    $("#btnAnnualOperatingCost").click(function () {
        basicInfoModel.setButtonStatus('annual_operating_cost');
        $('#window').jqxWindow('open');
        $("#editor").jqxEditor().val('');
        $("#editor").jqxEditor().val(localData['annual_operating_cost']);

    });
    $("#btnDemandAndSupplyAnalysis").click(function () {
        basicInfoModel.setButtonStatus('demand_and_supply_analysis');
        $('#window').jqxWindow('open');
        $("#editor").jqxEditor().val('');
        $("#editor").jqxEditor().val(localData['demand_and_supply_analysis']);

    });
    $("#btnFinancialPlanText").click(function () {
        basicInfoModel.setButtonStatus('financial_plan_text');
        $('#window').jqxWindow('open');
        $("#editor").jqxEditor().val('');
        $("#editor").jqxEditor().val(localData['financial_plan_text']);

    });
    $("#btnBenefitsOfTheProjectAnalysis").click(function () {
        basicInfoModel.setButtonStatus('benefits_of_the_projects_analysis');
        $('#window').jqxWindow('open');
        $("#editor").jqxEditor().val('');
        $("#editor").jqxEditor().val(localData['benefits_of_the_projects_analysis']);

    });
    $("#btnImplementationSchedule").click(function () {
        basicInfoModel.setButtonStatus('implementation_schedule');
        $('#window').jqxWindow('open');
        $("#editor").jqxEditor().val('');
        $("#editor").jqxEditor().val(localData['implementation_schedule']);

    });
    $("#btnMSandMR").click(function () {
        basicInfoModel.setButtonStatus('ms_and_mp');
        $('#window').jqxWindow('open');
        $("#editor").jqxEditor().val('');
        $("#editor").jqxEditor().val(localData['ms_and_mp']);
    });
    $("#btnAPDR").click(function () {
        basicInfoModel.setButtonStatus('additional_projects_decisions_required');
        $('#window').jqxWindow('open');
        $("#editor").jqxEditor().val('');
        $("#editor").jqxEditor().val(localData['additional_projects_decisions_required']);

    });
    $("#btnCertified").click(function () {
        basicInfoModel.setButtonStatus('certified');
        $('#window').jqxWindow('open');
        $("#editor").jqxEditor().val('');
        $("#editor").jqxEditor().val(localData['certified']);
    });
    $("#side_basic_info").addClass("w3-red");
    $("#btnSaveContent").click(function () {
        var button = basicInfoModel.getButtonStatus();
        var buttonName = basicInfoModel.getButtonName(button);
        var editorText = $("#editor").jqxEditor().val();
        if (editorText == "") {
            basicInfoModel.resetDefaultClasses(buttonName);
        } else {
            localData[button] = editorText;
            $('#window').jqxWindow('close');
            basicInfoModel.saveDataToDatabase();
            basicInfoModel.addRemoveCSSClasses(buttonName);

            // localStorage.removeItem("basic_info" + "_" + gs_no);
            // localStorage.setItem("basic_info" + "_" + gs_no, JSON.stringify(localData));

        }
    });

    $("#btnSaveBasicInfo").click(function () {
        basicInfoModel.saveDataToDatabase();
    });
    $("#btnGotoSpecificInfo").click(function () {
        window.location.href = 'specific_info/?scheme=' + gs_no;
    });

    var imagePath = '';
    $("#btnSaveMap").click(function () {
        $('#myPleaseWait').modal({show: true});
        var element = $("#divProjectLocationMap");
        var getCanvas;
        html2canvas(element, {
            onrendered: function (canvas) {
                $('#myPleaseWait').modal('hide');
                $("#previewImage").append(canvas);
                getCanvas = canvas;
                var imageData = getCanvas.toDataURL("image/png");
                var newData = imageData.replace(/^data:image\/png/, "data:application/octet-stream");
                var element = document.createElement('a');
                element.setAttribute('href', newData);
                element.setAttribute("download", "image.png");
                element.setAttribute('id', 'aaa');
                imagePath = element.getAttribute("href");
                element.style.display = 'none';
                document.body.appendChild(element);
                element.click();
                document.body.removeChild(element);
            }
        });
    });

    if (detail) {
        $('input[name="txtGSNo"]').val(gs_no);
        $('input[name="txtProjectName"]').val(detail.s_name);

        var strStartDate = (detail.start_date).split('-');
        var strEndDate = (detail.end_date).split('-');

        $('#impStartDate').val(strStartDate[0] + '-' + strStartDate[1] + '-' + strStartDate[2]);
        $('#impEndDate').val(strEndDate[0] + '-' + strEndDate[1] + '-' + strEndDate[2]);

    }
    $("#viewfile").click(function () {
        basicInfoModel.exportExcelToHTML();
    });

    function getTitlePage() {
        var strTitlePage = "<h1 style=\"text-align: center;\">" + detail.s_name.toUpperCase() + "</h1><br/><br/><br/>";
        strTitlePage = strTitlePage + "<h1 style=\"text-align: center;\">PC-I</h1><br/><br/>";
        strTitlePage = strTitlePage + "<h1  style=\"text-align: center;\">Cost Rs. " + detail.cost_total + " Millions</h1><br/><br/><br/><br/>";
        strTitlePage = strTitlePage + '<img alt="GOP" style="width:25%; display: block; margin-left: auto; margin-right: auto;"  src="' + gopLogo + '"><br/><br/><br/><br/><br/><br/><br/>';
        strTitlePage = strTitlePage + "<h1  style=\"text-align: center;\">GOVERNMENT OF THE PUNJAB,<BR/> " + detail.sec_name.toUpperCase() + " DEPARTMENT, PUNJAB </h1><br/><br/><br/><div/>";
        return strTitlePage;
    }

    function getBasicInfoHTMLTable() {
        var basicInfoHTML = '<h2 style="text-align: center;">PART A</h2><br/>';
        basicInfoHTML = basicInfoHTML + '<h2 style="text-align: center;">PROJECT DIGEST</h2>';
        basicInfoHTML = basicInfoHTML + '<table style="width:100%;">';
        basicInfoHTML = basicInfoHTML + '<tr><td>1</td><td><b>Name of Project</b></td><td>' + detail.s_name.toUpperCase() + '</td></tr>';
        basicInfoHTML = basicInfoHTML + '<tr><td>2</td><td><b>Location of Project</b></td><td>' + detail.district + ', ' + detail.tehsil + '</td></tr>';
        basicInfoHTML = basicInfoHTML + '<tr><td>3</td><td><b>Authorities Responsible for:</b></td><td></td></tr>';
        basicInfoHTML = basicInfoHTML + '<tr><td></td><td colspan="2">' + localData.authorities_responsible + '</td></tr>';
        basicInfoHTML = basicInfoHTML + '<tr><td>4</td><td><b>Plan Provision:</b></td><td></td></tr>';
        basicInfoHTML = basicInfoHTML + '<tr><td></td><td colspan="2">' + localData.plan_provision + '</td></tr>';
        basicInfoHTML = basicInfoHTML + '<tr><td>5</td><td><b>Project Objectives & its Relationship with the Sector Objectives:</b></td><td></td></tr>';
        basicInfoHTML = basicInfoHTML + '<tr><td></td><td colspan="2">' + localData.project_objectives + '</td></tr>';
        basicInfoHTML = basicInfoHTML + '<tr><td>6</td><td><b>Specific Information</b></td><td></td></tr>';
        basicInfoHTML = basicInfoHTML + '<tr><td>7</td><td><b>Annual Operating and Maintenance Cost after Completion of the Project:</b></td><td></td></tr>';
        basicInfoHTML = basicInfoHTML + '<tr><td></td><td colspan="2">' + localData.annual_operating_cost + '</td></tr>';
        basicInfoHTML = basicInfoHTML + '<tr><td>8</td><td><b>Demand and Supply Analysis:</b></td><td></td></tr>';
        basicInfoHTML = basicInfoHTML + '<tr><td></td><td colspan="2">' + localData.demand_and_supply_analysis + '</td></tr>';
        basicInfoHTML = basicInfoHTML + '<tr><td>9</td><td><b>Financial and Mode of Financing:</b></td><td></td></tr>';
        basicInfoHTML = basicInfoHTML + '<tr><td></td><td colspan="2">' + localData.financial_plan_text + '</td></tr>';
        basicInfoHTML = basicInfoHTML + '<tr><td>10</td><td><b>Project Benefit and Analysis:</b></td><td></td></tr>';
        basicInfoHTML = basicInfoHTML + '<tr><td></td><td colspan="2">' + localData.benefits_of_the_projects_analysis + '</td></tr>';
        basicInfoHTML = basicInfoHTML + '<tr><td>11</td><td><b>Implementation Schedule:</b></td><td></td></tr>';
        basicInfoHTML = basicInfoHTML + '<tr><td></td><td colspan="2">' + localData.implementation_schedule + '</td></tr>';
        basicInfoHTML = basicInfoHTML + '<tr><td>12</td><td><b>Management Structure & Manpower Requirement:</b></td><td></td></tr>';
        basicInfoHTML = basicInfoHTML + '<tr><td></td><td colspan="2">' + localData.ms_and_mp + '</td></tr>';
        basicInfoHTML = basicInfoHTML + '<tr><td>13</td><td><b>Additional Projects/ Decisions Required Maximizing Socio-Economic Benefits from the Proposed Project:</b></td><td></td></tr>';
        basicInfoHTML = basicInfoHTML + '<tr><td></td><td colspan="2">' + localData.additional_projects_decisions_required + '</td></tr>';
        basicInfoHTML = basicInfoHTML + '<tr><td>14</td><td><b>Certified:</b></td><td></td></tr>';
        basicInfoHTML = basicInfoHTML + '<tr><td></td><td colspan="2">' + localData.certified + '</td></tr>';

        basicInfoHTML = basicInfoHTML + '</table>';
        return basicInfoHTML;
    }

    function getAnnexuresHtml() {
        var annexureHtml = '<div>';
        for (var key in annexures_list) {
            var annexureId = annexures_list[key].annexure_id;
            var annexureTitle = annexures_list[key].annexure_title;
            var annexureData = annexures_list[key].annexure_data;
            annexureHtml = annexureHtml + annexureData;//'<h3 id="' + annexureId + '">' + annexureTitle + ' Annexure[' + (parseInt(key) + 1) + ']</h3>' + annexureData + '';
        }
        annexureHtml = annexureHtml + '</div>';
        return annexureHtml;
    }

    $("#btnGotoSpecificInfo").click(function () {
        window.location.href = 'specific_info/?scheme=' + gs_no;
    });

    $("#btnDownAuthResp").click(function () {
        // window.open('../get_sample_file?type=authorities_responsible', '_blank');
        window.open('/static/asstes/doc/Authorities Responsible.docx', '_blank');
    });
    $("#btnDownPlanProvision").click(function () {
        // window.open('../get_sample_file?type=plan_provision', '_blank');
        window.open('/static/asstes/doc/Plan Provision.docx', '_blank');
    });
    $("#btnDownProjectObjectives").click(function () {
        // window.open('../get_sample_file?type=project_objectives', '_blank');
        window.open('/static/asstes/doc/ProjectObjective.docx', '_blank');
    });
    $("#btnDownAnnualOperatingCost").click(function () {
        // window.open('../get_sample_file?type=annual_operating_cost', '_blank');
        window.open('/static/asstes/doc/annual_operating_cost.docx', '_blank');
    });
    $("#btnDownDemandAndSupplyAnalysis").click(function () {
        // window.open('../get_sample_file?type=demand_and_supply_analysis', '_blank');
        window.open('/static/asstes/doc/demand_and_supply_analysis.docx', '_blank');
    });
    $("#btnDownFinancialPlanText").click(function () {
        // window.open('../get_sample_file?type=financial_plan_text', '_blank');
        window.open('/static/asstes/doc/financial_plan_text.docx', '_blank');
    });
    $("#btnDownBenefitsOfTheProjectAnalysis").click(function () {
        // window.open('../get_sample_file?type=benefits_of_the_projects_analysis', '_blank');
        window.open('/static/asstes/doc/benefits_of_the_projects_analysis.docx', '_blank');
    });
    $("#btnDownImplementationSchedule").click(function () {
        // window.open('../get_sample_file?type=implementation_schedule', '_blank');
        window.open('/static/asstes/doc/implementation_schedule.docx', '_blank');
    });
    $("#btnDownMSandMR").click(function () {
        // window.open('../get_sample_file?type=ms_and_mp', '_blank');
        window.open('/static/asstes/doc/Management Structure & Manpower Requirement.docx', '_blank');
    });
    $("#btnDownAPDR").click(function () {
        // window.open('../get_sample_file?type=additional_projects_decisions_required', '_blank');
        window.open('/static/asstes/doc/additional_projects_decisions_required.docx', '_blank');
    });
    $("#btnDownCertified").click(function () {
        // window.open('../get_sample_file?type=certified', '_blank');
        window.open('/static/asstes/doc/certified.docx', '_blank');
    });

    $("#btnImportAnnexure").click(function () {
        try {
            var input = document.getElementById("annexureExcelFile");
            var reader = new FileReader();
            reader.readAsArrayBuffer(input.files[0]);
            reader.onload = function () {
                var data = new Uint8Array(reader.result);
                var wb = XLSX.read(data, {type: 'array'});
                var htmlstr = XLSX.write(wb, {type: 'binary', bookType: 'html'});
                var annexure_id = getAnnexureId();
                var annexureTitle = $('#txtAnnexureTitle').val();
                var annexureData = '<h3 id="' + annexure_id + '">' + annexureTitle + ' Annexure[' + annexure_id + ']</h3>' + htmlstr + '';
                setAnnexureData(annexureData);
                var editorText = $("#editor").jqxEditor().val();
                var text = editorText + '<a href="#' + annexure_id + '">Annexure[' + annexure_id + ']</a>';
                $("#editor").jqxEditor().val(text);
            }
        } catch (err) {
            alert(err);
        }
    });

    function getAnnexureCount() {
        var count = 0;
        var button = basicInfoModel.getButtonStatus();
        for (var key in annexures_list) {
            var annexure_for = annexures_list[key].annexure_title;
            if (annexure_for == button) {
                count++;
            }
        }
        return count;
    }

    function getAnnexureId() {
        // var count = getAnnexureCount();
        // var button = basicInfoModel.getButtonStatus();
        // var annexure_for_id = button + '_' + (count + 1);
        // return annexure_for_id;
        return (annexures_list.length + 1);
    }

    function setAnnexureData(data) {
        var annexure_item = {gs_no: '', annexure_id: '', annexure_title: '', annexure_data: ''};
        var annexure_id = getAnnexureId();
        annexure_item.gs_no = gs_no;
        annexure_item.annexure_title = $('#txtAnnexureTitle').val();
        annexure_item.annexure_id = gs_no + '_' + annexure_id;
        annexure_item.annexure_data = data;
        basicInfoModel.saveAnnexureToDatabase(annexure_item);
        annexures_list.push(annexure_item);
    }

    function getWordHtml() {
        var input = document.getElementById("wordFile");
        var mammoth = require("mammoth");
        mammoth.convertToHtml({path: input.files[0]})
            .then(function (result) {
                var html = result.value; // The generated HTML
                alert(html);
                var messages = result.messages; // Any messages, such as warnings during conversion
                alert(messages);
            }).done();

        // $('#divWord').show();
        // var input = document.getElementById("wordFile");
        // require("docx2html")(input.files[0], {container:document.getElementById('divWord')}).then(function (converted) {
        //     converted.toString()
        //     $('#divWord').hide();
        // })
    }

    if (annexures) {
        annexures_list = annexures;
    }

});


