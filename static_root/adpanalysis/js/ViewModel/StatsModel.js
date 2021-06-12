/**
 * Created by idrees on 5/5/2017.
 */
var StatsModel = function(aaBCM){
    var me =this;
    me.barChartModel = aaBCM;
    me.findIndex = function(list,value){
        for(var i=0;i<list.length;i++){
            if(list[i].indexOf('value')!= -1){
                return i;
            }
        }
    }
    me.groupBy=function(data,key) {
        //var sortedList = _(adpVM.schemesList).sortBy(key);
        var result = _(data).groupBy(function (scheme) {
            return scheme[key].trim(); //alert(obj);
        });
        return result;
    }
    me.sum=function(data,mkey){
        var sum =0;
        for(var i=0;i<data.length;i++){
            sum += parseFloat(data[i][mkey]);
        }
        return sum;
    }
    me.max=function(data, key){
        var result = _(data).max(function(scheme){
            return parseFloat(scheme[key]);
        });
        return result[key];
    }
    me.min=function(data, key){
        var result = _.min(data,function(scheme){
            return parseFloat(scheme[key]);
        });
        return result[key];
    }
    me.fields=function(dataset){
        if(!dataset) dataset = me.barChartModel.schemesStats[0];
        var result = _.keys(dataset);
        return result;
    }

    me.getColumnsList = function(data){
        var columnsList = [];
        if (data.length > 0){
            var columnsIn = data[0];
            for(var key in columnsIn){
                columnsList.push(key);
            }
        }else{
            console.log("No columns");
        }
        return columnsList;
    }

    me.getUniqueValues = function(data, column){
        var lookup = {};
        var items = data;
        var arrUniqueValues = [];
        for (var item, i = 0; item = items[i++];) {
            var key = item[column];
            if (!(key in lookup)) {
                if(key){
                    lookup[key] = 1;
                    arrUniqueValues.push(key);
                }
            }
        }
        return arrUniqueValues;
    }

}
