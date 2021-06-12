ol.control.LayerSwitcher = function(opt_options)
{	var options = opt_options || {};
	var self = this;
	this.dcount = 0;
	this.show_progress = options.show_progress;
	this.oninfo = (typeof (options.oninfo) == "function" ? options.oninfo: null);
	this.onextent = (typeof (options.onextent) == "function" ? options.onextent: null);
	this.hasextent = options.extent || options.onextent;
	this.hastrash = options.trash;
	this.reordering = (options.reordering!==false);
	var element;
	if (options.target) 
	{	element = $("<div>").addClass(options.switcherClass || "ol-layerswitcher");
	}
	else
	{	element = $("<div>").addClass((options.switcherClass || 'ol-layerswitcher') +' ol-unselectable ol-control ol-collapsed');
		this.button = $("<button>")
					.attr('type','button')
					.on("touchstart", function(e)
					{	element.toggleClass("ol-collapsed"); 
						e.preventDefault(); 
						self.overflow();
					})
					.click (function()
					{	element.toggleClass("ol-forceopen").addClass("ol-collapsed"); 
						self.overflow();
					})
					.appendTo(element);
		if (options.mouseover)
		{	$(element).mouseleave (function(){ element.addClass("ol-collapsed"); })
				.mouseover(function(){ element.removeClass("ol-collapsed"); });
		}
		this.topv = $("<div>").addClass("ol-switchertopdiv")
			.click(function(){ self.overflow("+50%"); })
			.appendTo(element);
		this.botv = $("<div>").addClass("ol-switcherbottomdiv")
			.click(function(){ self.overflow("-50%"); })
			.appendTo(element);
	}
	this.panel_ = $("<ul>").addClass("panel")
				.appendTo(element);
	this.panel_.on ('mousewheel DOMMouseScroll onmousewheel', function(e)
		{	if (self.overflow(Math.max(-1, Math.min(1, (e.originalEvent.wheelDelta || -e.originalEvent.detail)))))
			{	e.stopPropagation();
				e.preventDefault();
			}
		});
	this.header_ = $("<li>").addClass("ol-header").appendTo(this.panel_);
	ol.control.Control.call(this,
	{	element: element.get(0),
		target: options.target
	});
	// Enable jQuery dataTransfert
	// $.event.props.push('dataTransfer');
	this.target = options.target;
};
ol.inherits(ol.control.LayerSwitcher, ol.control.Control);