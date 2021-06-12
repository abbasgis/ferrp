/**
 * Created by Dr. Ather Ashraf on 8/22/2018.
 */

var JQXToolbarModel_3d = function (viewModel) {
    var me = this;
    me.toolbarHeight = '35px';
    me.toolbarTarget = $("#jqxToolBar_3d");
    me.toolbarItems = [];
    // me.viewInfo = viewInfo;
    me.viewModel = viewModel;
    me.cesiumModel = me.viewModel.getCesiumModel();
    me.navbar = {
        spacebar: {
            type: "space",
            name: "space",
            create: function (tool) {
            }
        },
        initialExtent: {
            name: "initialExtent",
            type: "button",
            tool: null,
            create: function (tool) {
                this.tool = tool;
                var button = $("<div style='width:100%;height: '100%' '>" + icons["initExtent"] + "</div>");
                tool.append(button);
                tool.jqxTooltip({content: 'Set Initial Extent'});
                tool.on("click", function () {
                    me.cesiumModel.setInitExtent();
                });
            }
        },
        camera: {
            name: "camera",
            type: "button",
            tool: null,
            create: function (tool) {
                this.tool = tool;
                var button = $("<div style='width:100%;height: '100%' '>" + icons["camera"] + "</div>");
                tool.append(button);
                tool.jqxTooltip({content: 'Camera Setting'});
                tool.on("click", function () {
                    me.viewModel.openCameraSettingPanel();
                });
            }
        },
    }

    me.init = function (navbarSeq) {
        me.toolbarTarget.height(me.toolbarHeight);
        // me.setNavbar(olMapModel)
        me.navbarSeq = navbarSeq;

        var tools = "";
        for (var i = 0; i < me.navbarSeq.length; i++) {
            if (me.navbarSeq[i].type == "space") {
                tools += "| "
            } else {
                tools += me.navbarSeq[i].type + " "
                me.toolbarItems.push(me.navbarSeq[i].name);
            }
        }

        me.toolbarTarget.jqxToolBar({
            theme: theme,
            width: "100%", height: me.toolbarHeight, tools: tools,
            initTools: function (type, index, tool, menuToolIninitialization) {
                me.navbar[me.toolbarItems[index]].create(tool);
            }
        });
        // me.monitorViewChange();
    }
    me.setCesiumModel = function(cModel){
        me.cesiumModel = cModel;
    }
}