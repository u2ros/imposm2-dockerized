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
    prefix='',
    proj='epsg:3857',
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

wind_turbine = Points(
    name = 'powerline_wind_turbine',
    mapping = {
        'power': {'generator'},
        'generator:source': ('wind',),
        'generator:method': ('wind_turbine',)
    }
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