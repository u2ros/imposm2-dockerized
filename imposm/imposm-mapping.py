# Copyright 2011 Omniscale (http://omniscale.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from imposm.mapping import (
    Options,
    Points, LineStrings, Polygons,
    String, Bool, Integer, OneOfInt,
    set_default_name_type, LocalizedName,
    WayZOrder, ZOrder, Direction,
    GeneralizedTable, UnionView,
    FixInvalidPolygons,
    PseudoArea, meter_to_mapunit, sqr_meter_to_mapunit,
)

# # internal configuration options
# # uncomment to make changes to the default values
# import imposm.config
#
# # import relations with missing rings
# imposm.config.import_partial_relations = False
#
# # select relation builder: union or contains
# imposm.config.relation_builder = 'contains'
#
# # log relation that take longer than x seconds
# imposm.config.imposm_multipolygon_report = 60
#
# # skip relations with more rings (0 skip nothing)
# imposm.config.imposm_multipolygon_max_ring = 0
#
# # split ways that are longer than x nodes (0 to split nothing)
# imposm.config.imposm_linestring_max_length = 50
#
# # cache coords in a compact storage (with delta encoding)
# # use this when memory is limited (default)
# imposm.config.imposm_compact_coords_cache = True

# set_default_name_type(LocalizedName(['name:en', 'int_name', 'name']))

db_conf = Options(
    # db='osm',
    host='localhost',
    port=5432,
    user='osm',
    password='osm',
    sslmode='allow',
    prefix='osm_new_',
    proj='epsg:900913',
)

powerlines = LineStrings(
    name = 'powerline',
    mapping = {
        'power':  ('line',)
    },
    fields = (
        ('voltage', Integer()),
        ('operator', String()),
        ('wires', Integer()),
        ('name', String()),
    )
)

powerline_masts = Points(
    name = 'powerline_mast',
    mapping = {
        'power': ('tower', 'portal')
    },
    fields = (
        ('structure', String()),
        ('material', String()),
        ('height', Integer())
    )
)

powerline_area = Polygons(
    name = 'powerline_usw_kw',
    mapping = {
        'power': ('plant', 'substation')
    },
    fields = (
        ('name', String()),
        ('operator', String()),
    )
)

class Highway(LineStrings):
    fields = (
        ('tunnel', Bool()),
        ('bridge', Bool()),
        ('ref', String()),
        ('z_order', WayZOrder()),
    )
    field_filter = (
        ('area', Bool()),
    )

places = Points(
    name = 'places',
    mapping = {
        'place': (
            'city',
            'town',
            'village',
            'hamlet',
            'suburb',
        ),
    },
    fields = (
        ('z_order', ZOrder([
            'city',
            'town',
            'village',
            'hamlet',
            'suburb',
        ])),
    ),
)

admin = Polygons(
    name = 'admin',
    mapping = {
        'boundary': (
            'administrative',
        ),
    },
    fields = (
        ('admin_level', OneOfInt('1 2 3 4 5 6'.split())),
    ),
)

motorways = Highway(
    name = 'motorways',
    mapping = {
        'highway': (
            'motorway',
            'motorway_link',
            'trunk',
            'trunk_link',
        ),
    }
)

mainroads = Highway(
    name = 'mainroads',
    mapping = {
        'highway': (
            'primary',
            'primary_link',
            'secondary',
            'secondary_link',
            'tertiary',
    )}
)

buildings = Polygons(
    name = 'buildings',
    mapping = {
        'building': (
            '__any__',
    )}
)

minorroads = Highway(
    name = 'minorroads',
    mapping = {
        'highway': (
            'road',
            'track',
            'service',
            'bridleway',
            'living_street',
            'residential',
    )}
)

railways = LineStrings(
    name = 'railways',
    fields = (
        ('tunnel', Bool()),
        ('bridge', Bool()),
        # ('ref', String()),
        ('z_order', WayZOrder()),
    ),
    mapping = {
        'railway': (
            'rail',
            'tram',
            'light_rail',
            'subway',
            'narrow_gauge',
            'preserved',
            'funicular',
            'monorail',
    )}
)

waterways = LineStrings(
    name = 'waterways',
    mapping = {
        'waterway': (
            'stream',
            'river',
            'canal',
            'drain',
    )},
    field_filter = (
        ('tunnel', Bool()),
    ),
)

waterareas = Polygons(
    name = 'waterareas',
    mapping = {
        'waterway': ('riverbank',),
        'natural': ('water',),
        'landuse': ('basin', 'reservoir'),
})

airports = Polygons(
    name = 'airport_area',
    mapping = {
        'aeroway': ('runway', 'taxiway', 'aerodrome', 'terminal', 'heliport', 'helipad', 'hangar', 'apron')},
    fields = (
        ('addr', String()),
        ('icao', String()),
        ('phone', String()),
        ('aerodrome:type', String()),
    )
)

landusages = Polygons(
    name = 'landusages',
    fields = (
        ('area', PseudoArea()),
    ),
    mapping = {
        'landuse': (
            'park',
            'forest',
            'residential',
            'commercial',
            'industrial',
            'railway',
            'grass',
            'farmyard',
            'farm',
            'farmland',
            'wood',
            'meadow',
            'quarry',
        ),
})

admin_gen0 = GeneralizedTable(
    name = 'admin_gen0',
    tolerance = meter_to_mapunit(250.0),
    origin = admin,
)

powerlines_gen0 = GeneralizedTable(
    name = 'powerline_gen0',
    tolerance = meter_to_mapunit(500.0),
    origin = powerlines,
)



motorways_gen2 = GeneralizedTable(
    name = 'motorways_gen2',
    tolerance = meter_to_mapunit(50.0),
    origin = motorways,
)

motorways_gen1 = GeneralizedTable(
    name = 'motorways_gen1',
    tolerance = meter_to_mapunit(200.0),
    origin = motorways_gen2,
)

motorways_gen0 = GeneralizedTable(
    name = 'motorways_gen0',
    tolerance = meter_to_mapunit(500.0),
    origin = motorways_gen1,
)




mainroads_gen2 = GeneralizedTable(
    name = 'mainroads_gen2',
    tolerance = meter_to_mapunit(50.0),
    origin = mainroads,
)

mainroads_gen1 = GeneralizedTable(
    name = 'mainroads_gen1',
    tolerance = meter_to_mapunit(100.0),
    origin = mainroads_gen2,
)

mainroads_gen0 = GeneralizedTable(
    name = 'mainroads_gen0',
    tolerance = meter_to_mapunit(250.0),
    origin = mainroads_gen1,
)



railways_gen2 = GeneralizedTable(
    name = 'railways_gen2',
    tolerance = meter_to_mapunit(50.0),
    origin = railways,
)

railways_gen1 = GeneralizedTable(
    name = 'railways_gen1',
    tolerance = meter_to_mapunit(100.0),
    origin = railways_gen2,
)

railways_gen0 = GeneralizedTable(
    name = 'railways_gen0',
    tolerance = meter_to_mapunit(250.0),
    origin = railways_gen1,
)




landusages_gen2 = GeneralizedTable(
    name = 'landusages_gen2',
    tolerance = meter_to_mapunit(50.0),
    origin = landusages,
    where = "ST_Area(geometry)>%f" % sqr_meter_to_mapunit(50000),
)

landusages_gen1 = GeneralizedTable(
    name = 'landusages_gen1',
    tolerance = meter_to_mapunit(100.0),
    origin = landusages_gen2,
    where = "ST_Area(geometry)>%f" % sqr_meter_to_mapunit(50000),
)

landusages_gen0 = GeneralizedTable(
    name = 'landusages_gen0',
    tolerance = meter_to_mapunit(250.0),
    origin = landusages_gen1,
    where = "ST_Area(geometry)>%f" % sqr_meter_to_mapunit(500000),
)



waterareas_gen0 = GeneralizedTable(
    name = 'waterareas_gen0',
    tolerance = meter_to_mapunit(50.0),
    origin = waterareas,
    where = "ST_Area(geometry)>%f" % sqr_meter_to_mapunit(50000),
)

waterareas_gen1 = GeneralizedTable(
    name = 'waterareas_gen1',
    tolerance = meter_to_mapunit(100.0),
    origin = waterareas,
    where = "ST_Area(geometry)>%f" % sqr_meter_to_mapunit(500000),
)


landuse_gen2_valid = FixInvalidPolygons(
    origin = landusages_gen2,
)

landuse_gen1_valid = FixInvalidPolygons(
    origin = landusages_gen1,
)

landuse_gen0_valid = FixInvalidPolygons(
    origin = landusages_gen0,
)
