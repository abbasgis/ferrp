multifactSumAggregator = function() {
    return function(facts) {

        return function() {
            var summedFacts = {};

            for (_i = 0, _len = facts.length; _i < _len; _i++) {
                summedFacts[facts[_i]] = 0
            }

            return {

                push: function(record) {
                    for ( _i = 0, _len = facts.length; _i < _len; _i++) {
                        summedFacts[facts[_i]] += parseFloat(record[facts[_i]]);
                    }
                },

                multivalue: function() {
                    return summedFacts;
                },

                // return the first element for unsupported renderers.
                value: function() { return summedFacts[facts[0]]; },
                format: function(x) { return x; },

                label: "Facts"
            };
        };
    };
};

multifactTableRenderer = function(){
    return function(pivotData) {
        var aggregator, c, colAttrs, colKey, colKeys, i, j, r, result, rowAttrs, rowKey, rowKeys, th, totalAggregator, tr, txt, val, x;
        colAttrs = pivotData.colAttrs;
        rowAttrs = pivotData.rowAttrs;
        rowKeys = pivotData.getRowKeys();
        colKeys = pivotData.getColKeys();

        result = $("<table class='table table-bordered pvtTable'>");

        for (j in colAttrs) {
            c = colAttrs[j];
            tr = $("<tr>");
            if (parseInt(j) === 0 && rowAttrs.length !== 0) {

                tr.append($("<th>").attr("colspan", rowAttrs.length).attr("rowspan", colAttrs.length));
            }

            tr.append($("<th class='pvtAxisLabel'>").text(c));


            tmpAggregator = pivotData.getAggregator([], []);
            if (tmpAggregator.multivalue) {
                col_colspan = Object.keys(tmpAggregator.multivalue()).length;
                col_rowspan = 1
            } else {
                col_colspan = 1
                col_rowspan = 2
            }

            for (i in colKeys) {
                colKey = colKeys[i];
                th = $("<th class='pvtColLabel'>").text(colKey[j]).attr("colspan", col_colspan);
                if (parseInt(j) === colAttrs.length - 1 && rowAttrs.length !== 0) {
                    th.attr("rowspan", col_rowspan);
                }
                tr.append(th);
            }
            if (parseInt(j) === 0) {
                tr.append($("<th class='pvtTotalLabel'>").text("Totals").attr("colspan", col_colspan).attr("rowspan", col_rowspan));
            }
            result.append(tr);
        }
        if (rowAttrs.length !== 0) {
            tr = $("<tr>");
            for (i in rowAttrs) {
                r = rowAttrs[i];
                tr.append($("<th class='pvtAxisLabel'>").text(r));
            }

            tmpAggregator = pivotData.getAggregator([], []);
            if (tmpAggregator.multivalue) {
                if (colAttrs.length > 0) {
                    th = $("<th>");
                    tr.append(th);
                }

                val = tmpAggregator.multivalue();
                for (i in colKeys) {
                    for (v in val) {
                        tr.append($("<th class='pvtColLabel'>").text(v).data("value", v));
                    }
                }

                for (v in val) {
                    tr.append($("<th class='pvtColLabel'>").text(v).data("value", v));
                }
            } else {
                th = $("<th>");
                if (colAttrs.length === 0) {
                    th.addClass("pvtTotalLabel").text("Totals");
                }
                tr.append(th);
            }

            result.append(tr);
        }
        for (i in rowKeys) {
            rowKey = rowKeys[i];
            tr = $("<tr>");
            for (j in rowKey) {
                txt = rowKey[j];
                th = $("<th class='pvtRowLabel'>").text(txt).attr("rowspan", x);
                if (parseInt(j) === rowAttrs.length - 1 && colAttrs.length !== 0) {
                    th.attr("colspan", 2);
                }
                tr.append(th);
            }
            for (j in colKeys) {
                colKey = colKeys[j];
                aggregator = pivotData.getAggregator(rowKey, colKey);

                if (aggregator.multivalue) {
                    val = aggregator.multivalue();
                    for (v in val) {
                        tr.append($("<td class='pvtVal row" + i + " col" + j + "'>").text(aggregator.format(val[v])).data("value", val[v]));
                    }
                } else {
                    val = aggregator.value();
                    tr.append($("<td class='pvtVal row" + i + " col" + j + "'>").text(aggregator.format(val)).data("value", val));
                }

            }
            totalAggregator = pivotData.getAggregator(rowKey, []);


            if (totalAggregator.multivalue) {
                val = totalAggregator.multivalue();
                for (v in val) {
                    tr.append($("<td class='pvtTotal rowTotal'>").text(totalAggregator.format(val[v])).data("value", val[v]).data("for", "row" + i));
                }
            } else {
                val = totalAggregator.value();
                tr.append($("<td class='pvtTotal rowTotal'>").text(totalAggregator.format(val)).data("value", val).data("for", "row" + i));
            }

            result.append(tr);
        }
        tr = $("<tr>");
        th = $("<th class='pvtTotalLabel'>").text("Totals");
        th.attr("colspan", rowAttrs.length + (colAttrs.length === 0 ? 0 : 1));
        tr.append(th);
        for (j in colKeys) {
            colKey = colKeys[j];
            totalAggregator = pivotData.getAggregator([], colKey);

            if (totalAggregator.multivalue) {
                val = totalAggregator.multivalue();
                for (v in val) {
                    tr.append($("<td class='pvtTotal colTotal'>").text(totalAggregator.format(val[v])).data("value", val[v]).data("for", "col" + j));
                }
            } else {
                val = totalAggregator.value();
                tr.append($("<td class='pvtTotal colTotal'>").text(totalAggregator.format(val)).data("value", val).data("for", "col" + j));
            }
        }

        totalAggregator = pivotData.getAggregator([], []);

        if (totalAggregator.multivalue) {
            val = totalAggregator.multivalue();
            for (v in val) {
                tr.append($("<td class='pvtGrandTotal'>").text(totalAggregator.format(val[v])).data("value", val[v]));
            }
        } else {
            val = totalAggregator.value();
            tr.append($("<td class='pvtGrandTotal'>").text(totalAggregator.format(val)).data("value", val));
        }

        result.append(tr);
        result.data("dimensions", [rowKeys.length, colKeys.length]);
        return result;
    };
};

////////Report.js

var custom_renderers = {
    "Multifact Table": multifactTableRenderer()
};

var custom_aggregators = {
    "Multifact aggregator": multifactSumAggregator()
};


$("#declarations_report #pivottable").pivotUI(data, {
    aggregators: $.extend(custom_aggregators, $.pivotUtilities.aggregators),
    renderers: $.extend(custom_renderers, $.pivotUtilities.renderers, $.pivotUtilities.gchart_renderers),
    rows: ["person"],
    cols: ["company"],
    vals: ["hours", "turnover", "profit_margin"],
    hiddenAttributes: ["id"]
});