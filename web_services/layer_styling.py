import os
import xml.etree.ElementTree as ET

from pyxml2dict import XML2Dict
from sld import StyledLayerDescriptor

# from ferrp.layers.models import Info
from ferrp.layers.models import Info
from ferrp.utils import DB_Query


class Layer_Styling():
    style = {}

    def __init__(self, layer_name):
        self.layer_name = layer_name
        pass

    def process_sld(self, file):
        sld = Process_SLD(file)

    def get_default_raster_style(self, stats):
        if stats is not None:
            rules = []
            color_map = []

            min_val = stats[0]['min']
            max_val = stats[0]['max']
            mean_val = stats[0]['mean']
            stddev_val = stats[0]['stddev']
            mid_val = (float(max_val) - float(min_val)) / 2
            Q1 = mean_val / 4
            # arr_color_map = []
            # arr_color_map.append("%s 255  0    0   255" % max_val)
            # arr_color_map.append("%s 255  255  0   255" % mean_val)
            # arr_color_map.append("%s 0    255  0   255" % Q1)
            # arr_color_map.append("0  0    0    0   0")
            # arr_color_map.append("nv 0    0    0   0")
            # color_map = "\n".join(arr_color_map)
            color_map.append({"color": "#ff0000", "label": max_val, "opacity": 1, "quantity": max_val})
            color_map.append({"color": "#ffff00", "label": mean_val, "opacity": 1, "quantity": mean_val})
            color_map.append({"color": "#00ff00", "label": Q1, "opacity": 1, "quantity": Q1})
            rules.append({"raster_symbolizer": {"color_map": color_map}})
            self.style = {"rules": rules}
            self.update_layer_style()
        return self.style;

    def get_default_linestring_style(self):
        rules = []
        filter = {}
        line_symbolizer = {"stroke": "#262241", "stroke-width": "2",
                           "stroke-linecap": "square", "stroke-linejoin": "bevel"}
        rule = {"filter": filter, "line_symbolizer": line_symbolizer}
        rules.append(rule)
        self.style = {"rules": rules}
        self.update_layer_style()
        return self.style;

    def get_default_polygon_style(self):
        rules = []
        filter = {}
        polygon_symbolizer = {"fill": "#34258a", "stroke": "#000000", "fill_opacity": "0.5", "stroke-width": "2"}
        rule = {"filter": filter, "polygon_symbolizer": polygon_symbolizer}
        rules.append(rule)
        self.style = {"rules": rules}
        self.update_layer_style()
        return self.style;

    def get_default_point_style(self):
        rules = []
        filter = {}
        point_symbolizer = {"fill": "#34258a", "size": "5", "stroke": "#000000", "stroke-width": "2"}
        rule = {"filter": filter, "point_symbolizer": point_symbolizer}
        rules.append(rule)
        self.style = {"rules": rules}
        self.update_layer_style()
        return self.style;

    def get_default_vector_layer_style(self, geom_type):
        if "point" in geom_type.lower():
            style = self.get_default_point_style()
        elif "line" in geom_type.lower():
            style = self.get_default_linestring_style()
        else:
            style = self.get_default_polygon_style()

        return style

    def update_layer_style(self):
        if self.style is not {} and len(self.style['rules']) > 0:
            layer_info_list = Info.objects.filter(layer_name=self.layer_name)
            if layer_info_list.count() > 0:
                layer_info = layer_info_list[0]
                layer_info.style = self.style
                # layer_info.save()
                # layer_info.update(style = self.style)
                layer_info.save()
        pass

    def add_layer_style(self, geom_type, style=None):
        layer_info = Info.objects.filter(layer_name=self.layer_name)[0]
        if style is None:
            # ls = Layer_Styling(self.layer_name)
            style = self.get_default_vector_layer_style(layer_info.geom_type)
        layer_info.style = style
        layer_info.save()

    @classmethod
    def get_functional_layer_style(cls, code):
        if code == 'ssa':
            return {"rules": [
                {'raster_symbolizer': {'color_map': [{'color': '#ff0000', 'label': "Highly Suitable", 'opacity': 1, 'quantity': 0.8},
                                                     {'color': '#ffff00', 'label': "Suitable", 'opacity': 1,
                                                      'quantity': 0.6},
                                                     {'color': '#00ff00', 'label': "Not Suitable", 'opacity': 1,
                                                      'quantity': 0.4}]}}]}


class Process_SLD():
    sld = '{http://www.opengis.net/sld}'
    ogc = "{http://www.opengis.net/ogc}"
    se = "{http://www.opengis.net/se}"
    style = {}
    operators = {
        ogc + "PropertyIsEqualTo": "=",
        ogc + "PropertyIsNotEqualTo": "<>",
        ogc + "PropertyIsLessThan": "<",
        ogc + "PropertyIsLessThanOrEqualTo": "<=",
        ogc + "PropertyIsGreaterThanOrEqualTo": ">=",
        ogc + "PropertyIsGreaterThan": ">",
        ogc + " PropertyIsLike": "like"
    }

    def __init__(self, layer_name, file):
        self.layer_name = layer_name
        layer_info = list(Info.objects.filter(layer_name=self.layer_name))[0]
        sld_data = file.read()
        sld_root = ET.fromstring(sld_data)
        if layer_info.layer_type == 'Raster':
            rule_tags = list(sld_root.iter(self.sld + 'Rule'))
            rules = []
            for rule_tag in rule_tags:
                rule = self.process_raster_style(rule_tag)
                rules.append(rule)
            self.style['rules'] = rules
        else:
            nl = sld_root.find(self.sld + 'NamedLayer')
            if nl is None:
                nl = sld_root.find(self.sld + 'UserLayer')
            us = nl.find(self.sld + 'UserStyle')
            ft = us.find(self.se + 'FeatureTypeStyle')
            if ft is None:
                ft = us.find(self.sld + 'FeatureTypeStyle')
            rule_tags = ft.findall(self.se + 'Rule')
            if len(rule_tags) == 0:
                rule_tags = ft.findall(self.sld + 'Rule')
            rules = []
            for rule_tag in rule_tags:
                if layer_info.geom_type in ['Polygon', 'MultiPolygon']:
                    rule = self.process_polygon_style(rule_tag)
                    rules.append(rule)
                elif layer_info.geom_type in ['LineString', 'MultiLineString']:
                    rule = self.process_polyline_style(rule_tag)
                    rules.append(rule)
            self.style['rules'] = rules
        pass

    def get_style(self):
        return self.style

    def process_raster_style(self, rule_tag):
        rule = {}
        # raster_symbolizer_list =  list(rule.iter(self.sld + 'RasterSymbolizer'))
        raster_symbolizer_tag = rule_tag.find(self.sld + "RasterSymbolizer")
        raster_symbolizer = {}
        color_map_list = []
        color_map = raster_symbolizer_tag.find(self.sld + 'ColorMap')
        for color_map_entry in color_map:
            color_map_list.append(color_map_entry.attrib)
        raster_symbolizer["color_map"] = color_map_list
        rule["raster_symbolizer"] = raster_symbolizer
        return rule

    def process_polygon_style(self, rule_tag):
        rule = {}
        filter_tag = rule_tag.find(self.ogc + "Filter")
        if filter_tag is None:
            filter_tag = rule_tag.find(self.sld + "Filter")
        filter = self.create_filter(filter_tag)
        rule['filter'] = filter
        polygon_symbolizer_tag = rule_tag.find(self.se + "PolygonSymbolizer")
        if polygon_symbolizer_tag is None:
            polygon_symbolizer_tag = rule_tag.find(self.sld + "PolygonSymbolizer")
        polygon_symbolizer = self.create_polygon_symbolizer(polygon_symbolizer_tag)
        rule['polygon_symbolizer'] = polygon_symbolizer
        return rule

    def process_polyline_style(self, rule_tag):
        rule = {}
        filter_tag = rule_tag.find(self.ogc + "Filter")
        filter = self.create_filter(filter_tag)
        rule['filter'] = filter
        line_symbolizer_tag = rule_tag.find(self.se + "LineSymbolizer")
        line_symbolizer = self.create_line_symbolizer(line_symbolizer_tag)
        rule['line_symbolizer'] = line_symbolizer
        return rule

    def create_polygon_symbolizer(self, polygon_symbolizer_tag):
        polygon_symbolizer = {}
        svg_params = list(polygon_symbolizer_tag.iter(self.se + 'SvgParameter'))
        if len(svg_params) == 0:
            svg_params = list(polygon_symbolizer_tag.iter(self.sld + 'CssParameter'))
        for svg_param in svg_params:
            polygon_symbolizer[svg_param.get('name')] = svg_param.text
        return polygon_symbolizer

    def create_line_symbolizer(self, line_symbolizer_tag):
        line_symbolizer = {}
        svg_params = list(line_symbolizer_tag.iter(self.se + 'SvgParameter'))
        for svg_param in svg_params:
            line_symbolizer[svg_param.get('name')] = svg_param.text
        return line_symbolizer

    def create_filter(self, filter_tag):
        filter = {}
        if filter_tag is not None:
            for child in filter_tag:
                op = self.operators[child.tag]
                property_name = child.find(self.ogc + "PropertyName").text
                literal = child.find(self.ogc + "Literal").text
                # filter = "%s %s '%s'" %(property_name,op,literal)
                filter['property_name'] = property_name
                filter['op'] = op
                filter['literal'] = literal
        return filter
