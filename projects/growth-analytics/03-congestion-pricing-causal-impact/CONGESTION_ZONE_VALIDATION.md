# Congestion Relief Zone validation

## Official definition

The MTA and NYC public guidance define the Congestion Relief Zone as local streets and avenues in Manhattan south of and including 60th Street. The FDR Drive, West Side Highway / Route 9A, and Hugh L. Carey Tunnel connections to West Street are excluded when used exclusively. TLC and public guidance state that the taxi/FHV per-trip charge can apply to journeys to, from, within, or through the zone.

Sources:

- [MTA Congestion Relief Zone](https://congestionreliefzone.mta.info/)
- [MTA FAQ](https://congestionreliefzone.mta.info/faqs)
- [NYC TLC trip-record data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
- [MTA CBD Geofence dataset](https://data.ny.gov/widgets/srxy-5nxn?mobile_redirect=true)

## Mapping method

1. Download the MTA polygon collection from State of New York Open Data.
2. Download the official TLC taxi-zone geometry ZIP.
3. Transform TLC zone geometry from EPSG:2263 to WGS84.
4. Transform the MTA polygons into the TLC geometry's projected CRS (EPSG:2263) before area calculations.
5. Union the transformed MTA polygons.
6. Calculate each zone's polygon-overlap ratio in projected square units.
7. Classify zones as inside at 95% or more overlap, partial above 5% overlap, and outside at 5% or less.

The script is `src/validate_zone_map.py`. It writes the full mapping to the ignored local file `analysis_data/growth_sources/cbd_taxi_zone_mapping.json`.

## Validation result

The downloaded TLC geometry contains 263 zone shapes. The mapping classified:

| Classification | Count |
|---|---:|
| Inside | 20 |
| Partial / boundary | 21 |
| Outside | 222 |

Inside zones include Clinton East, East Chelsea, East Village, Flatiron, Garment District, Gramercy, Greenwich Village North and South, Little Italy/NoLiTa, Lower East Side, Midtown Center/East/North/South, Murray Hill, Penn Station/Madison Sq West, SoHo, Times Sq/Theatre District, Union Sq, and West Village.

Partial zones include Alphabet City, Battery Park, Battery Park City, Chinatown, Clinton West, both Financial District zones, Hudson Sq, Kips Bay, both Lincoln Square zones, Meatpacking/West Village West, Seaport, Stuy Town/Peter Cooper Village, Sutton Place/Turtle Bay North, TriBeCa/Civic Center, Two Bridges/Seward Park, UN/Turtle Bay South, Upper East Side South, West Chelsea/Hudson Yards, and World Trade Center.

## What this does and does not solve

Polygon overlap creates a reproducible zone-boundary classification. It does not identify whether a trip stayed on an excluded roadway, crossed the zone without a local-street entry, or received a crossing credit. Origin and destination fields still cannot reconstruct the full route. Through-route exposure must therefore be flagged as ambiguous or validated with a route/fee field, not guessed from pickup zone.
