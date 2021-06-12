/**
 * Created by ather on 5/6/2017.
 */
$(document).ready(function(){
    // localStorage.clear();
    var schemesStats = JSON.parse(localStorage.getItem("adpdstats"));
    var ptVM = new PivotTableVM();
    if (!schemesStats) {
        $.getJSON("adpanalysis/adpdstats", function (data) {
            schemesStats = data;
            try {
                localStorage.setItem("adpDraft","");
                localStorage.setItem("adpdstats", JSON.stringify(schemesStats));
                ptVM.initialize(schemesStats);
            }catch(err){
                console.error(err.stack);
            }
        });
    }else{
        ptVM.initialize(schemesStats);
    }
});