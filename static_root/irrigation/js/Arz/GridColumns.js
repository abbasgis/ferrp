/**
 * Created by idrees on 2/16/2018.
 */
var ArzGridColumns = function () {
    var me = this;
    me.strColumn = "string";
    me.numColumn = 'number';
    me.dateColumn = 'date';

    me.getCommandedAreaColumnsList = function (level) {
        var columnsList = [
            {xtype: 'rownumberer'},
            {dataIndex: 'name', text: me.getDataLabel(level), flex:1, filter: me.getStringFilterObj(me.strColumn),
                summaryType: 'count',
                summaryRenderer: function(value, summaryData, dataIndex) { return ((value === 0 || value > 1) ? '(' + value + ' ' + me.getDataLabel(level) + 's )' : '(1 ' + me.getDataLabel(level) + ' )'); },
                field: { xtype: 'textfield' }
            },
            {dataIndex: 'gca_geom_ma', text: 'GCA Shape', flex:1, filter: me.numColumn,
                summaryType: 'sum',
                renderer: function(value, metaData, record, rowIdx, colIdx, store, view){ return value; },
                summaryRenderer: function(value, summaryData, dataIndex) { return value.toFixed(2) + ' Million Acres'; },
                field: { xtype: 'numberfield' }
            },
            {dataIndex: 'cca_geom_ma', text: 'CCA Shape', flex:1, filter: me.numColumn,
                summaryType: 'sum',
                renderer: function(value, metaData, record, rowIdx, colIdx, store, view){ return value; },
                summaryRenderer: function(value, summaryData, dataIndex) { return value.toFixed(2) + ' Million Acres'; },
                field: { xtype: 'numberfield' }
            },
            {dataIndex: 'gca_ma', text: 'GCA (MA)', flex:1, filter: me.numColumn,
                summaryType: 'sum',
                renderer: function(value, metaData, record, rowIdx, colIdx, store, view){ return value; },
                summaryRenderer: function(value, summaryData, dataIndex) { return value.toFixed(2) + ' Million Acres'; },
                field: { xtype: 'numberfield' }
            },
            {dataIndex: 'cca_ma', text: 'CCA (MA)', flex:1, filter: me.numColumn,
                summaryType: 'sum',
                renderer: function(value, metaData, record, rowIdx, colIdx, store, view){ return value; },
                summaryRenderer: function(value, summaryData, dataIndex) { return value.toFixed(2) + ' Million Acres'; },
                field: { xtype: 'numberfield' }
            },
            {dataIndex: 'canal_length', text: 'Canals Length (KM)', flex:1, filter: me.numColumn,
                summaryType: 'sum',
                renderer: function(value, metaData, record, rowIdx, colIdx, store, view){ return value; },
                summaryRenderer: function(value, summaryData, dataIndex) { return value.toFixed(2) + ' KM'; },
                field: { xtype: 'numberfield' }
            },
            {dataIndex: 'shape_length', text: 'Canals Shape (KM)', flex:1, filter: me.numColumn,
                summaryType: 'sum',
                renderer: function(value, metaData, record, rowIdx, colIdx, store, view){ return value; },
                summaryRenderer: function(value, summaryData, dataIndex) { return value.toFixed(2) + ' KM'; },
                field: { xtype: 'numberfield' }
            },
            {dataIndex: 'outlets', text: 'Outlets', flex:1, filter: me.numColumn,
                summaryType: 'sum',
                renderer: function(value, metaData, record, rowIdx, colIdx, store, view){ return value; },
                summaryRenderer: function(value, summaryData, dataIndex) { return value.toFixed(2) + ' Sum'; },
                field: { xtype: 'numberfield' }
            },
        ];
        return columnsList;
    };

    me.getCCAColumnsList = function () {
        var columnsList = [
            {xtype: 'rownumberer'},
            {dataIndex: 'cca_name', text: 'Name', flex:1, filter: me.getStringFilterObj(me.strColumn),
                summaryType: 'count',
                summaryRenderer: function(value, summaryData, dataIndex) { return ((value === 0 || value > 1) ? '(' + value + ' CCAs )' : '(1  CCA)'); },
                field: { xtype: 'textfield' }
            },
            {dataIndex: 'acz_name', text: 'Agri. Zone', flex:1, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'doab', text: 'Doab', flex:1, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'basin', text: 'Basin', flex:1, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'area_acre', text: 'Area (Acres)', flex:1, filter: me.numColumn,
                summaryType: 'sum',
                renderer: function(value, metaData, record, rowIdx, colIdx, store, view){ return value; },
                summaryRenderer: function(value, summaryData, dataIndex) { return value.toFixed(2) + ' Acres'; },
                field: { xtype: 'numberfield' }
            },
            {dataIndex: 'cca_dam', text: 'Dam', flex:1, filter: me.numColumn},
            {dataIndex: 'zone_name', text: 'Zone', flex:1, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'circle_name', text: 'Circle', flex:1, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'division_name', text: 'Division', flex:1, filter: me.getStringFilterObj(me.strColumn)},
        ];
        return columnsList;
    };

    me.getCommandedAreaDistrictsColumnsList = function (level) {
        var columnsList = [
            {xtype: 'rownumberer'},
            {dataIndex: 'district_name', text: 'District', flex:1, filter: me.getStringFilterObj(me.strColumn),
                summaryType: 'count',
                summaryRenderer: function(value, summaryData, dataIndex) { return ((value === 0 || value > 1) ? '(' + value + ' Districts )' : '(1 District )'); },
                field: { xtype: 'textfield' }
            },
            {dataIndex: 'name', text: me.getDataLabel(level), flex:1, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'admin_boundary_area', text: me.getDataLabel(level) + ' Area', flex:1, filter: me.numColumn,
                summaryType: 'sum',
                renderer: function(value, metaData, record, rowIdx, colIdx, store, view){ return value; },
                summaryRenderer: function(value, summaryData, dataIndex) { return value.toFixed(2) + ' Sq.KM'; },
                field: { xtype: 'numberfield' }
            },
            {dataIndex: 'admin_boundary_part', text: me.getDataLabel(level) + ' Part Area', flex:1, filter: me.numColumn,
                summaryType: 'sum',
                renderer: function(value, metaData, record, rowIdx, colIdx, store, view){ return value; },
                summaryRenderer: function(value, summaryData, dataIndex) { return value.toFixed(2) + ' Sq.KM'; },
                field: { xtype: 'numberfield' }
            },
            {dataIndex: 'admin_boundary_percentage', text: me.getDataLabel(level) + ' Percent', flex:1, filter: me.numColumn,},
            {dataIndex: 'district_area', text: 'District Area', flex:1, filter: me.numColumn},
        ];


        return columnsList;
    };

    me.getCanalsColumnsList = function () {
        var columnsList = [
            {xtype: 'rownumberer', width:40},
            {dataIndex: 'zone_name', text: 'Zone', width:100, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'channel_name', text: 'Canal', width:120, filter: me.getStringFilterObj(me.strColumn),
                summaryType: 'count',
                summaryRenderer: function(value, summaryData, dataIndex) { return ((value === 0 || value > 1) ? '(' + value + ' Canals )' : '(1 Canal )'); },
                field: { xtype: 'textfield' },

            },
            {dataIndex: 'circle_name', text: 'Circle', width:100, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'division_name', text: 'Division', width:100, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'length_km', text: 'Length (KM)', width:120, filter: me.numColumn,
                summaryType: 'sum',
                renderer: function(value, metaData, record, rowIdx, colIdx, store, view){ return value; },
                summaryRenderer: function(value, summaryData, dataIndex) { return value.toFixed(2) + ' Km'; },
                field: { xtype: 'numberfield' }
            },
            {dataIndex: 'gca', text: 'GCA', width:70, filter: me.numColumn,
                summaryType:'sum',
                summaryRenderer: function(value, summaryData, dataIndex) { return value.toFixed(0)}
            },
            {dataIndex: 'cca', text: 'CCA', width:70, filter: me.numColumn,
                summaryType:'sum',
                summaryRenderer: function(value, summaryData, dataIndex) { return value.toFixed(0)}
            },
            {dataIndex: 'flowtype_e', text: 'Flow Type', width:70, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'tail_rd', text: 'Tail RD', width:70, filter: me.numColumn},
            {dataIndex: 'head_x', text: 'Head X', width:70, filter: me.numColumn},
            {dataIndex: 'head_y', text: 'Head Y', width:70, filter: me.numColumn},
            {dataIndex: 'tail_x', text: 'Tail X', width:70, filter: me.numColumn},
            {dataIndex: 'tail_y', text: 'Tail Y', width:70, filter: me.numColumn},
            {dataIndex: 'imis_code', text: 'IMIS Code', width:120, filter: me.numColumn},
            {dataIndex: 'is_l_section', text: 'L Section', width:70, filter: me.getBooleanFilterObj(),
                summaryType: function () {
                    // var store = Ext.getStore('canalsDataStore');
                    // var records = store.data.items;
                    // var field = ['is_l_section'];
                    // var totalCount = 0;
                    // if (this.isGrouped()) {
                    //     var trueCount = 0;
                    //     var groups = this.getGroups();
                    //     var len = groups.length, group;
                    //     for (var i = 0; i < len; i++) {
                    //         group = groups.items[i];
                    //         var lenn = group.length;
                    //         for (var j = 0; j < lenn; ++j) {
                    //             var record = group.items[j].data[field];
                    //             if(record == true){
                    //                 trueCount++;
                    //                 totalCount++;
                    //             }
                    //         }
                    //         return trueCount;
                    //     }
                    // } else {
                    //     return totalCount;
                    // }
                    // if (this.isGrouped()) {
                    //     var groups = this.getGroups();
                    //     var i = 0;
                    //     var len = groups.length;
                    //     var out = {},
                    //     group;
                    //     for (; i < len; i++) {
                    //         group = groups[i];
                    //         out[group.zone_name] = Suma.apply(store, [group.children].concat(field));
                    //     }
                    //     var groupSum = out[groups[w].zone_name];
                    //     w++;
                    //     return groupSum;
                    // } else {
                    //     return Suma.apply(store, [records].concat(field));
                    // }

                },
                summaryRenderer: function(value, summaryData, dataIndex) {
                    // return '<b>' + value + '</b>';
                },
            },
            {dataIndex: 'is_gate', text: 'Gate', width:70, filter: me.getBooleanFilterObj()},
            {dataIndex: 'is_gauge', text: 'Gauge', width:70, filter: me.getBooleanFilterObj()},
            {dataIndex: 'is_row', text: 'ROW', width:70, filter: me.getBooleanFilterObj()},
            {dataIndex: 'is_structure', text: 'Structure', width:70, filter: me.getBooleanFilterObj()},
            {dataIndex: 'is_outlet', text: 'Outlet', width:70, filter: me.getBooleanFilterObj()},
        ];
        return columnsList;
    };

    me.getLSectionColumnsList = function () {
        var columnsList = [
            {xtype: 'rownumberer'},
            {dataIndex: 's_name_rd', text: 'RD Name', width:80, filter: me.getStringFilterObj(me.strColumn),
                summaryType: 'count',
                summaryRenderer: function(value, summaryData, dataIndex) { return ((value === 0 || value > 1) ? '(' + value + ' L Sections )' : '(1 L Section )'); },
                field: { xtype: 'textfield' }
            },
            {dataIndex: 'name_of_canal', text: 'Canal', width:100, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'from_rd_m', text: 'From RD', width:80, filter: me.numColumn},
            {dataIndex: 'to_rd_m', text: 'To RD', width:80, filter: me.numColumn},
            {text:'Design Discharge', columns:[
                {dataIndex: 'dd_lined', text: 'Lined', width:80, filter: me.numColumn},
                {dataIndex: 'dd_full_supply_discharge_cusecs', text: 'Full Supply Discharge', width:me.getColumnWidth('Full Supply Discharge'), filter: me.numColumn},
                {dataIndex: 'dd_bank_width', text: 'Bank Width (Left)', width:me.getColumnWidth('Bank Width (Left)'), filter: me.numColumn},
                {dataIndex: 'dd_bank_width_right', text: 'Bank Width (Right)', width:me.getColumnWidth('Bank Width (Right)'), filter: me.numColumn},
                {dataIndex: 'dd_free_board', text: 'Free Board', width:me.getColumnWidth('Free Board'), filter: me.numColumn},
                {dataIndex: 'dd_water_surface_slope_prcnt', text: 'Water Surface Slope', width:me.getColumnWidth('Water Surface Slope'), filter: me.numColumn},
                {dataIndex: 'dd_laceys_f_n_cvr', text: 'Laceys of N CVR', width:me.getColumnWidth('Laceys of N CVR'), filter: me.numColumn},
                {dataIndex: 'dd_full_supply_dpeth', text: 'Full Supply Depth', width:me.getColumnWidth('Full Supply Depth'), filter: me.numColumn},
                {dataIndex: 'dd_bed_width', text: 'Bed Width', width:me.getColumnWidth('Bed Width'), filter: me.numColumn},
                {dataIndex: 'dd_full_supply_level', text: 'Full Supply Level', width:me.getColumnWidth('Full Supply Level'), filter: me.numColumn},
                {dataIndex: 'dd_bed_level', text: 'Bed Level', width:me.getColumnWidth('Bed Level'), filter: me.numColumn},
                {dataIndex: 'dd_nsl', text: 'Near Surface Level', width:me.getColumnWidth('Near Surface Level'), filter: me.numColumn}
            ]},
            {text:'Existing Discharge', columns:[
                {dataIndex: 'dd_lined', text: 'Lined', width:80, filter: me.numColumn},
                {dataIndex: 'ed_full_supply_discharge', text: 'Full Supply Discharge', width:me.getColumnWidth('Full Supply Discharge'), filter: me.numColumn},
                {dataIndex: 'ed_bank_width_left', text: 'Bank Width (Left)', width:me.getColumnWidth('Bank Width (Left)'), filter: me.numColumn},
                {dataIndex: 'ed_bank_width_right', text: 'Bank Width (Right)', width:me.getColumnWidth('Bank Width (Right)'), filter: me.numColumn},
                {dataIndex: 'ed_free_board', text: 'Free Board', width:me.getColumnWidth('Free Board'), filter: me.numColumn},
                {dataIndex: 'ed_water_surface_slope', text: 'Water Surface Slope', width:me.getColumnWidth('Water Surface Slope'), filter: me.numColumn},
                {dataIndex: 'ed_laceys_f_n_cvr', text: 'Laceys of N CVR', width:me.getColumnWidth('Laceys of N CVR'), filter: me.numColumn},
                {dataIndex: 'ed_full_supply_depth', text: 'Full Supply Depth', width:me.getColumnWidth('Full Supply Depth'), filter: me.numColumn},
                {dataIndex: 'ed_bed_width', text: 'Bed Width', width:me.getColumnWidth('Bed Width'), filter: me.numColumn},
                {dataIndex: 'ed_full_supply_level', text: 'Full Supply Level', width:me.getColumnWidth('Full Supply Level'), filter: me.numColumn},
                {dataIndex: 'ed_bed_level', text: 'Bed Level', width:me.getColumnWidth('Bed Level'), filter: me.numColumn},
                {dataIndex: 'ed_nsl', text: 'Near Surface Level', width:me.getColumnWidth('Near Surface Level'), filter: me.numColumn}
            ]},
            {dataIndex: 'imis_code', text: 'IMIS Code', width:100, filter: me.numColumn},
            {dataIndex: 'name_of_zone', text: 'Zone', width:100, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'name_of_circle', text: 'Circle', width:100, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'name_of_division', text: 'Division', width:100, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'sanction_date', text: 'Sanction Date', width:100, filter: me.getStringFilterObj(me.strColumn)},
        ];
        return columnsList;
    };

    me.getGatesColumnsList = function () {
        var columnsList = [
            {xtype: 'rownumberer'},
            {dataIndex: 'is_geom', text: 'Is Geom', width:100, filter: me.getBooleanFilterObj()},
            {dataIndex: 'name_of_canal', text: 'Canal', width:100, filter: me.getStringFilterObj(me.strColumn),
                summaryType: 'count',
                summaryRenderer: function(value, summaryData, dataIndex) { return ((value === 0 || value > 1) ? '(' + value + ' Gates )' : '(1 Gate )'); },
                field: { xtype: 'textfield' }
            },
            {dataIndex: 'name_of_structure', text: 'Structure', width:100, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'rd', text: 'RD', width:80, filter: me.numColumn},
            {dataIndex: 'north', text: 'North', width:80, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'east', text: 'East', width:80, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'year_of_construction', text: 'Construction Year', width:100, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'cost_of_construction', text: 'Construction Cost', width:100, filter: me.numColumn},
            {dataIndex: 'design_discharge', text: 'Design Discharge', width:100, filter: me.numColumn},
            {dataIndex: 'nsl', text: 'NSL', width:80, filter: me.numColumn},
            {dataIndex: 'bed', text: 'Bed', width:80, filter: me.numColumn},
            {dataIndex: 'crest_level', text: 'Crest Level', width:100, filter: me.numColumn},
            {dataIndex: 'full_supply', text: 'Full Supply', width:100, filter: me.numColumn},
            {dataIndex: 'free_board', text: 'Free Board', width:100, filter: me.numColumn},
            {dataIndex: 'bed_width', text: 'Bed Width', width:100, filter: me.numColumn},
            {dataIndex: 'no_of_bays', text: 'Bays', width:80, filter: me.numColumn},
            {dataIndex: 'length_of_gate', text: 'Gate Length', width:100, filter: me.numColumn},
            {dataIndex: 'height_of_gate', text: 'Gate Height', width:100, filter: me.numColumn},
            {dataIndex: 'no_of_gates', text: 'Gates', width:80, filter: me.numColumn},
            {dataIndex: 'type_of_gate', text: 'Gate Type', width:100, filter: me.numColumn},
            {dataIndex: 'groove_dimensions', text: 'Groove Dimensions', width:120, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'top_rl_of_slab', text: 'Slab Top', width:100, filter: me.numColumn},
            {dataIndex: 'pier_top_rl', text: 'Pier Top', width:100, filter: me.numColumn},
            {dataIndex: 'thickness_of_piers', text: 'Pier Thickness', width:100, filter: me.numColumn},
            {dataIndex: 'abutment_top_rl', text: 'Abutment Top', width:100, filter: me.numColumn},
            {dataIndex: 'top_rl_of_floor_of_hoisting_deck', text: 'Hoisting Deck Top FLoor', width:me.getColumnWidth('Hoisting Deck Top FLoor'), filter: me.numColumn},
            {dataIndex: 'capacity', text: 'Capacity', width:100, filter: me.numColumn},
            {dataIndex: 'rope_drum_type', text: 'Rope Drum Type', width:120, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'stem_rod_type', text: 'Stem Rod Type', width:120, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'name_of_manufacture', text: 'Manufacturer', width:100, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'year', text: 'Year', width:100, filter: me.numColumn},
            {dataIndex: 'amount', text: 'Amount', width:100, filter: me.numColumn},
            {dataIndex: 'imis_code', text: 'IMIS Code', width:100, filter: me.numColumn},
            {dataIndex: 'zone_name', text: 'Zone', width:100, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'circle_name', text: 'Circle', width:100, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'division_name', text: 'Division', width:100, filter: me.getStringFilterObj(me.strColumn)},
        ];
        return columnsList;
    };

    me.getGaugesColumnsList = function () {
        var columnsList = [
            {xtype: 'rownumberer'},
            // {dataIndex: 'is_geom', text: 'Is Geom', width:100, filter: me.getBooleanFilterObj()},
            {dataIndex: 'canal_name', text: 'Canal', width:100, filter: me.getStringFilterObj(me.strColumn),
                summaryType: 'count',
                summaryRenderer: function(value, summaryData, dataIndex) { return ((value === 0 || value > 1) ? '(' + value + ' Gauges )' : '(1 Gauge )'); },
                field: { xtype: 'textfield' }
            },
            {dataIndex: 'rd_m', text: 'RD', width:100, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'gauge_location_rd', text: 'Head RD', width:120, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'gauge_location_tail_rd', text: 'Tail RD', width:120, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'year_of_installation', text: 'Installation Year', width:100, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'type_guage_design', text: 'Gauge Design', width:100, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'category_guage_design', text: 'Design Category', width:100, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'discharge_cusecs_guage_design', text: 'Gauge Discharge', width:100, filter: me.numColumn},
            {dataIndex: 'rl_guage_design', text: 'Gauge RL', width:80, filter: me.numColumn},
            {dataIndex: 'depth_guage_design', text: 'Gauge Depth', width:80, filter: me.numColumn},
            {dataIndex: 'setting_guage_design', text: 'Gauge Setting', width:80, filter: me.numColumn},
            {dataIndex: 'type_existing_gauge_details', text: 'Gauge Type Existing', width:100, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'category_existing_gauge_details', text: 'Category Existing', width:100, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'discharge_cusecs_existing_gauge_details', text: 'Discharge Existing', width:100, filter: me.numColumn},
            {dataIndex: 'rl_existing_gauge_details', text: 'Gauge RL Existing', width:100, filter: me.numColumn},
            {dataIndex: 'depth_existing_gauge_details', text: 'Depth Existing', width:80, filter: me.numColumn},
            {dataIndex: 'setting_existing_gauge_details', text: 'Setting Existing', width:100, filter: me.numColumn},
            {dataIndex: 'closure_report', text: 'Closure Report', width:120, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'cost_history_rs', text: 'Cost History', width:100, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'year_history', text: 'Year History', width:80, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'name_of_guage_reader', text: 'Gauge Reader', width:100, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'cell_of_guage_reader', text: 'Cell No.', width:120, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'imis_code', text: 'IMIS Code', width:100, filter: me.numColumn},
            {dataIndex: 'sub_divison', text: 'Sub Division', width:100, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'section', text: 'Section', width:100, filter: me.getStringFilterObj(me.strColumn)},
        ];
        return columnsList;
    };

    me.getOutletsColumnsList = function () {
        var columnsList = [
            {xtype: 'rownumberer'},
            {dataIndex: 'is_geom', text: 'Is Geom', width:100, filter: me.getBooleanFilterObj()},
            {dataIndex: 'name_of_canal', text: 'Canal', width:100, filter: me.getStringFilterObj(me.strColumn),
                summaryType: 'count',
                summaryRenderer: function(value, summaryData, dataIndex) { return ((value === 0 || value > 1) ? '(' + value + ' Outlets )' : '(1 Outlet )'); },
                field: { xtype: 'textfield' }
            },
            {dataIndex: 'rd', text: 'RD', width:70, filter: me.numColumn},
            {dataIndex: 'l_r', text: 'L R', width:70, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'year_of_installation', text: 'Installation Year', width:100, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'design_discharge_cusecs', text: 'Design Discharge', width:100, filter: me.numColumn},
            {dataIndex: 'outlet_type', text: 'Outlet Type', width:80, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'gca_acres', text: 'GCA (Acres)', width:100, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'cca_acres', text: 'CCA (Acres)', width:80, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'height_of_outlet_ft', text: 'Height (Ft)', width:80, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'head_above_crest_outlet_ft', text: 'Head Above Crest (Ft)', width:100, filter: me.numColumn},
            {dataIndex: 'submergence_h_ft', text: 'Submergence Height (Ft)', width:100, filter: me.numColumn},
            {dataIndex: 'diameter_breadth_width_ft', text: 'Diameter', width:100, filter: me.numColumn},
            {dataIndex: 'crest_r_l_ft', text: 'Crest R L', width:100, filter: me.numColumn},
            {dataIndex: 'minimum_modular_head_ft', text: 'Minimum Modular', width:100, filter: me.numColumn},
            {dataIndex: 'working_head_ft', text: 'Working Head (Ft)', width:80, filter: me.numColumn},
            {dataIndex: 'closure_report', text: 'Closure Report', width:100, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'amount_rs', text: 'Amount (Rs.)', width:80, filter: me.numColumn},
            {dataIndex: 'imis', text: 'IMIS Code', width:100, filter: me.numColumn},
            {dataIndex: 'division', text: 'Division', width:100, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'sub_division', text: 'Sub Division', width:100, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'section', text: 'Section', width:100, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'district', text: 'District', width:100, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'tehsil', text: 'Tehsil', width:100, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'police_station', text: 'Police Station', width:100, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'village', text: 'Village', width:100, filter: me.getStringFilterObj(me.strColumn)},
        ];
        return columnsList;
    };

    me.getROWColumnsList = function () {
        var columnsList = [
            {xtype: 'rownumberer'},
            {dataIndex: 'name_of_canal', text: 'Canal', width:100, filter: me.getStringFilterObj(me.strColumn),
                summaryType: 'count',
                summaryRenderer: function(value, summaryData, dataIndex) { return ((value === 0 || value > 1) ? '(' + value + ' ROWs )' : '(1 ROW )'); },
                field: { xtype: 'textfield' }
            },
            {dataIndex: 'rd_length', text: 'RD', width:70, filter: me.numColumn},
            {dataIndex: 'l_ft', text: 'L (Ft)', width:70, filter: me.numColumn},
            {dataIndex: 'r_ft', text: 'R (Ft)', width:70, filter: me.numColumn},
            {dataIndex: 'federalgovt', text: 'Fed. Govt.', width:100, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'govtofpunjab', text: 'GOP', width:100, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'irrigation_deptt', text: 'Irrigation', width:80, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'total_l_r_ft', text: 'Total R L (Ft)', width:80, filter: me.numColumn},
            {dataIndex: 'anyotherdeptt', text: 'Other Deptt.', width:80, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'imis', text: 'IMIS Code', width:100, filter: me.numColumn},
            {dataIndex: 'zone', text: 'Zone', width:100, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'circle', text: 'Circle', width:100, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'division', text: 'Division', width:100, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'sub_division', text: 'Sub Division', width:100, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'section', text: 'Section', width:100, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'district', text: 'District', width:100, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'tehsil', text: 'Tehsil', width:100, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'police_station', text: 'Police Station', width:100, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'village', text: 'Village', width:100, filter: me.getStringFilterObj(me.strColumn)},
        ];
        return columnsList;
    };

    me.getStructureColumnsList = function () {
        var columnsList = [
            {xtype: 'rownumberer'},
            {dataIndex: 'is_geom', text: 'Is Geom', width:100, filter: me.getBooleanFilterObj()},
            {dataIndex: 'canal_name', text: 'Canal', width:100, filter: me.getStringFilterObj(me.strColumn),
                summaryType: 'count',
                summaryRenderer: function(value, summaryData, dataIndex) { return ((value === 0 || value > 1) ? '(' + value + ' Structures )' : '(1 Structure )'); },
                field: { xtype: 'textfield' }
            },
            {dataIndex: 'name_of_structure', text: 'Structure', width:70, filter: me.numColumn},
            {dataIndex: 'rd', text: 'RD', width:70, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'construction_year', text: 'Construction Year', width:100, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'construction_cost', text: 'Cost', width:100, filter: me.numColumn},
            {dataIndex: 'discharge_us_design_cusec', text: 'US Discharge', width:80, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'nsl_rl_us_design', text: 'NSL US', width:100, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'bed_rl_us_design', text: 'Bed RL US', width:80, filter: me.numColumn},
            {dataIndex: 'crest_level_us_design', text: 'Crest Level', width:80, filter: me.numColumn},
            {dataIndex: 'full_supply_rl_us_design', text: 'Full Supply RL US', width:100, filter: me.numColumn},
            {dataIndex: 'free_board_us_design', text: 'Free Board US', width:100, filter: me.numColumn},
            {dataIndex: 'bed_width_us_design', text: 'Bed Width US', width:100, filter: me.numColumn},
            {dataIndex: 'no_of_bays_us_design', text: 'No of Bayes US', width:100, filter: me.numColumn},
            {dataIndex: 'bay_width_us_design', text: 'Bay Width', width:100, filter: me.numColumn},
            {dataIndex: 'top_rl_of_slab_us_design', text: 'Slab Top RL', width:80, filter: me.numColumn},
            {dataIndex: 'total_x_sectional_width_us_design_ft', text: 'XS Width', width:100, filter: me.numColumn},
            {dataIndex: 'total_length_along_l_section_us_design_ft', text: 'LS Width', width:80, filter: me.numColumn},
            {dataIndex: 'diameter_of_piles_us_design_ft', text: 'Piles Diameter', width:80, filter: me.numColumn},
            {dataIndex: 'pier_top_rl_us_design_ft', text: 'Pier Top', width:80, filter: me.numColumn},
            {dataIndex: 'thickness_of_piers_us_design_ft', text: 'Pier Thickness', width:80, filter: me.numColumn},
            {dataIndex: 'abutment_top_rl_us_design_l', text: 'Abutment Top', width:80, filter: me.numColumn},
            {dataIndex: 'nsl_rl_ds_design', text: 'NSL RL DS', width:80, filter: me.numColumn},
            {dataIndex: 'closure_report', text: 'Closure Report', width:80, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'imis_code', text: 'IMIS Code', width:100, filter: me.numColumn},
        ];
        return columnsList;
    };

    me.getHeadWorkColumnsList = function () {
        var columnsList = [
            {xtype: 'rownumberer', width:40},
            {dataIndex: 'dam_name', text: 'Name', flex:1, filter: me.getStringFilterObj(me.strColumn),
                summaryType: 'count',
                summaryRenderer: function(value, summaryData, dataIndex) { return ((value === 0 || value > 1) ? '(' + value + ' Headworks )' : '(1 Headwork )'); },
                field: { xtype: 'textfield' }
            },
            {dataIndex: 'river', text: 'River', flex:1, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'main_basin', text: 'Main Basin', flex:1, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'near_city', text: 'Near City', flex:1, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'catch_skm', text: 'Catchment (SKM)', flex:1, filter: me.numColumn,
                summaryType: 'sum',
                renderer: function(value, metaData, record, rowIdx, colIdx, store, view){ return value; },
                summaryRenderer: function(value, summaryData, dataIndex) { return value.toFixed(2) + ' Sq.Km'; },
                field: { xtype: 'numberfield' }
            },
            {dataIndex: 'main_use', text: 'Main Use', flex:1, filter: me.getStringFilterObj(me.strColumn)}
        ];
        return columnsList;
    }



    me.getHeadWorkDischargeColumnsList = function () {
        var columnsList = [
            {xtype: 'rownumberer', width:30},
            {dataIndex: 'head_works', text: 'Head Work', width:90, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'river', text: 'River', width:90, filter: me.getStringFilterObj(me.strColumn),},
            {dataIndex: 'discharge_date', text: 'Discharge Date', flex:1, filter: me.getStringFilterObj(me.dateColumn),
                summaryType: 'count',
                summaryRenderer: function(value, summaryData, dataIndex) { return ((value === 0 || value > 1) ? '(' + value + ' Discharges )' : '(1 Discharge )'); },
                field: { xtype: 'textfield' }
            },
            {dataIndex: 'discharge_time', text: 'Discharge Time', flex:1, filter: me.getStringFilterObj(me.dateColumn)},
            {dataIndex: 'us', text: 'Up Stream', width:100, filter: me.numColumn,
                summaryType: 'max',
                renderer: function(value, metaData, record, rowIdx, colIdx, store, view){ return value; },
                summaryRenderer: function(value, summaryData, dataIndex) { return value.toFixed(0) + ' Max'; },
                field: { xtype: 'numberfield' }
            },
            {dataIndex: 'ds', text: 'Down Stream', width:90, filter: me.numColumn,
                summaryType: 'max',
                renderer: function(value, metaData, record, rowIdx, colIdx, store, view){ return value; },
                summaryRenderer: function(value, summaryData, dataIndex) { return value.toFixed(0) + ' Max'; },
                field: { xtype: 'numberfield' }
            },
            {dataIndex: 'reservior_level_ft', text: 'Depth(Ft)', width:me.getColumnWidth('Depth(Ft)'), filter: me.numColumn},
        ];
        return columnsList;
    }

    me.getGroundWaterColumnsList = function () {
        var columnsList = [
            {xtype: 'rownumberer', width:30},
            {dataIndex: 'id', text: 'Location Id', width:70, filter:me.numColumn,
                summaryType: 'count',
                summaryRenderer: function(value, summaryData, dataIndex) { return ((value === 0 || value > 1) ? '(' + value + ' Count )' : '(1 Count )'); },
                field: { xtype: 'textfield' }
            },
            {dataIndex: 'zone', text: 'Zone', width:120, filter: me.getStringFilterObj(me.strColumn),
                summaryType: 'count',
                summaryRenderer: function(value, summaryData, dataIndex) { return ((value === 0 || value > 1) ? '(' + value + ' Count )' : '(1 Count )'); },
                field: { xtype: 'textfield' }
            },
            {dataIndex: 'circle', text: 'Circle', width:120, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'division', text: 'Division', width:120, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'elevation', text: 'Elevation', width:120, filter: me.numColumn,
                summaryType: 'max',
                renderer: function(value, metaData, record, rowIdx, colIdx, store, view){ return value; },
                summaryRenderer: function(value, summaryData, dataIndex) { return value.toFixed(0) + ' Max'; },
                field: { xtype: 'numberfield' }
            },
            {dataIndex: 'type_wl_wq', text: 'Type', width:120, filter: me.getStringFilterObj(me.strColumn),
                summaryType: 'count',
                summaryRenderer: function(value, summaryData, dataIndex) { return ((value === 0 || value > 1) ? '(' + value + ' Count )' : '(1 Count )'); },
                field: { xtype: 'textfield' }
            },
            {dataIndex: 'major_canal', text: 'Canal', width:100, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'disty_minor', text: 'Minor', width:120, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'district', text: 'District', width:100, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'tehsil', text: 'Tehsil', width:100, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'qanongo_halka', text: 'Qanongo Halka', width:100, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'patwar_circle', text: 'Patwar Circle', width:100, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'mauza', text: 'Mauza', width:100, filter: me.getStringFilterObj(me.strColumn)},

        ];
        return columnsList;
    }
    me.getGroundWaterLevelColumnsList = function () {
        var columnsList = [
            {xtype: 'rownumberer', width:30},
            {dataIndex: 'ql_id', text: 'Location Id', width:70, filter:me.numColumn,
                summaryType: 'count',
                summaryRenderer: function(value, summaryData, dataIndex) { return ((value === 0 || value > 1) ? '(' + value + ' Count )' : '(1 Count )'); },
                field: { xtype: 'textfield' }
            },
            {dataIndex: 'year', text: 'Year', width:120, filter: me.getStringFilterObj(me.strColumn),
                summaryType: 'count',
                summaryRenderer: function(value, summaryData, dataIndex) { return ((value === 0 || value > 1) ? '(' + value + ' Count )' : '(1 Count )'); },
                field: { xtype: 'textfield' }
            },
            {dataIndex: 'season', text: 'Season', width:120, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'water_depth', text: 'Water Depth', width:120, filter: me.numColumn,
                summaryType: 'max',
                renderer: function(value, metaData, record, rowIdx, colIdx, store, view){ return value; },
                summaryRenderer: function(value, summaryData, dataIndex) { return value.toFixed(0) + ' Max'; },
                field: { xtype: 'numberfield' }
            },
            {dataIndex: 'elevation', text: 'Elevation', width:120, filter: me.numColumn,
                summaryType: 'max',
                renderer: function(value, metaData, record, rowIdx, colIdx, store, view){ return value; },
                summaryRenderer: function(value, summaryData, dataIndex) { return value.toFixed(0) + ' Max'; },
                field: { xtype: 'numberfield' }
            }
        ];
        return columnsList;
    }
    me.getGroundWaterQualityColumnsList = function () {
        var columnsList = [
            {xtype: 'rownumberer', width:30},
            {dataIndex: 'ql_id', text: 'Location Id', width:70, filter:me.numColumn,
                summaryType: 'count',
                summaryRenderer: function(value, summaryData, dataIndex) { return ((value === 0 || value > 1) ? '(' + value + ' Count )' : '(1 Count )'); },
                field: { xtype: 'textfield' }
            },
            {dataIndex: 'year', text: 'Year', width:120, filter: me.getStringFilterObj(me.strColumn),
                summaryType: 'count',
                summaryRenderer: function(value, summaryData, dataIndex) { return ((value === 0 || value > 1) ? '(' + value + ' Count )' : '(1 Count )'); },
                field: { xtype: 'textfield' }
            },
            {dataIndex: 'season', text: 'Season', width:120, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'water_quality', text: 'Water Quality', width:120, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'quality_type', text: 'Quality Type', width:120, filter: me.getStringFilterObj(me.strColumn)},
            {dataIndex: 'elevation', text: 'Elevation', width:120, filter: me.numColumn,
                summaryType: 'max',
                renderer: function(value, metaData, record, rowIdx, colIdx, store, view){ return value; },
                summaryRenderer: function(value, summaryData, dataIndex) { return value.toFixed(0) + ' Max'; },
                field: { xtype: 'numberfield' }
            }
        ];
        return columnsList;
    }


    me.getSummaryRenderer = function (unitDesc) {

    }
    me.getStringFilterObj = function (type) {
        return filter = {type:type, itemDefaults:{emptyText:'Search for...'}, caseSensitive: true, exactMatch: true, anyMatch: false,};
    }
    me.getBooleanFilterObj = function () {
        return filter = {
            type: 'boolean',
            yesText: 'True',
            noText: 'False'
        };
    }
    me.getColumnWidth = function (name) {
        var length = name.length * 6;
        if(length < 80){
            return 80
        }else {
            return length;
        }
    }
    me.getDataLabel = function(level) {
            if(level == 'zone_name'){
                return 'Zone';
            }if(level == 'circle_name'){
                return 'Circle';
            }if(level == 'division_name'){
                return 'Division';
            }else {
                return 'Name';
            }
        }
}