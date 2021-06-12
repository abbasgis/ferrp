/**
 * Created by idrees on 7/3/2018.
 */


var ArzAdminHierarchyToolbar = function (factsVM, factsModel) {
    var me = this;
    me.levelValue = {level: 'punjab', value: ''};
    me.factsVM = factsVM;
    me.factsModel = factsModel;
    me.getAdminToolbar = function () {
        var adminHierarchy = Ext.create('Ext.Action', {
            text: "Administrative Unit",
            id: 'btnAdmin',
            tooltip: "Select Administrative Unit",
            handler: function () {
            },
        });
        return adminHierarchy;
    };
    me.onItemClick = function (item) {
        me.factsModel.removeHighLightedLayer();
        var factsAccordion = Ext.getCmp('acrdnFacts');
        factsAccordion.expand();
        factsAccordion.setTitle(item.text + ' Facts');
        var extent = item.extent;
        var level = me.getLevelId(item.code);
        var id = me.getIdValue(item.code);
        me.factsVM.levelValue.level = level;
        me.factsVM.levelValue.value = id;

        if (extent == '') {
            alert('Location not available.');
        } else {
            me.factsModel.zoomToExtent(extent, true);
            me.factsModel.olMap.getLayers().forEach(function (layer) {
                if (layer instanceof ol.layer.Vector){
                    var title = layer.get('title');
                    if (title == level.split('_')[0]){
                        layer.setVisible(true);
                        var layerSource = layer.getSource();
                        var features = layerSource.getFeatures();
                        for (var index in features){
                            var feature = features[index];
                            var value = feature.get(level);
                            if (id == value){
                                var geometry = feature.getGeometry();
                                var ext = feature.getGeometry().getExtent();
                                if(level == 'mauza_id'){
                                    me.factsModel.zoomToExtent(extent, true);
                                }else{
                                    me.factsModel.olMap.getView().fit(ext, me.factsModel.olMap.getSize());
                                }
                                me.factsModel.highlightLayer(geometry);
                            }
                        }
                    }
                }
            });
        }

        me.getLevelSurveyStats(level, id);
        if (level == 'mauza_id') {
            me.getMauzaSurveyLocationData(id);
        }
    };

    me.getLevelId = function (code) {
        var level = code.split('_')[0];
        var levelId = '';
        switch (level) {
            case 'punjab':
                levelId = 'punjab';
                break;
            case 'district':
                levelId = 'district_id';
                break;
            case 'tehsil':
                levelId = 'tehsil_id';
                break;
            case 'qanungoi':
                levelId = 'qanungoi_halqa_id';
                break;
            case 'patwar':
                levelId = 'patwar_circle_id';
                break;
            case 'mauza':
                levelId = 'mauza_id';
                break;
            default:
                levelId = 'punjab';
        }
        return levelId;
    };
    me.getIdValue = function (code) {
        if (code.split('_')[1]) {
            return code.split('_')[1];
        } else {
            return null;
        }
    };
    me.getLevelSurveyStats = function (level, value) {
        var box = Ext.MessageBox.wait('Please wait...', 'Loading Data');
        var url = 'level_survey_stats?level=' + level + '&value=' + value;
        Ext.Ajax.request({
            url: url,
            timeout: 9000000000,
            method: "GET",
            success: function (response) {
                box.hide();
                var respText = response.responseText;
                var respnseText = eval('(' + JXG.decompress(respText) + ')');
                if (respnseText != "false") {
                    me.factsVM.setSurveyStats(respnseText);
                }
            },
            failure: function (res) {
                box.hide();
            }
        });
    };
    me.getMauzaSurveyLocationData = function (mauza_id) {
        var box = Ext.MessageBox.wait('Please wait...', 'Loading Data');
        var url = 'mauza_survey_location_data?mauza_id=' + mauza_id;
        Ext.Ajax.request({
            url: url,
            timeout: 9000000000,
            method: "GET",
            success: function (response) {
                box.hide();
                var respText = response.responseText;
                var respnseText = eval('(' + JXG.decompress(respText) + ')');
                if (respnseText != "false") {
                    var jsonData = respnseText;
                    var surveyData = JSON.parse(jsonData.survey_data);
                    var locationGeojson = JSON.parse(jsonData.survey_location);
                    me.factsVM.setSurveyStats(surveyData);
                    me.factsModel.addLocationsToMauzaLayer(locationGeojson);
                }
            },
            failure: function (res) {
                box.hide();
            }
        });
    }

}