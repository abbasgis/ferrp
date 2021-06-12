/**
 * Created by ather on 5/8/2017.
 */
var PivotTabularModel = function (aaVM) {
    var me = this;
    me.aaVM = aaVM
    me.initialize = function () {
        // var utils = $.pivotUtilities;
        // var heatmap = utils.renderers["Heatmap"];
        // var sumOverSum = utils.aggregators["Sum over Sum"];

        $("#"+me.containerDivId).pivotUI(
           me.aaVM.schemeStats, {
                rows: ["ADPYear"],
                cols: ["Sector"],
                als: ["Allocation"],
                aggregatorName: "Sum",
                // aggregator: sumOverSum(["tip", "total_bill"]),
                // renderer: heatmap
            });
    }
}