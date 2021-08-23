-- moves tables from default public schema tu custom schema
-- find and replace all occurences of NEW_SCHEMA with your schema name

DO
$$
DECLARE
    row record;
    schema text = 'NEW_SCHEMA';
BEGIN
    FOR row IN SELECT tablename FROM pg_tables WHERE schemaname = 'public' AND tablename LIKE 'osm_%'
    LOOP
        EXECUTE 'ALTER TABLE public.' || quote_ident(row.tablename) || ' SET SCHEMA ' || schema || ';';
    END LOOP;
END;
$$;

DO
$$
DECLARE
    row record;
    schema text = 'NEW_SCHEMA';
BEGIN
    FOR row IN SELECT tablename FROM pg_tables WHERE schemaname = 'NEW_SCHEMA' AND tablename LIKE 'osm_%'
    LOOP
        EXECUTE 'ALTER TABLE ' || schema || '.' || quote_ident(row.tablename) || ' RENAME TO ' || regexp_replace(quote_ident(row.tablename), '_new', '') || ';';
    END LOOP;
END;
$$;

-- add some custom columns

ALTER TABLE NEW_SCHEMA.osm_places ADD COLUMN max_scale integer;
ALTER TABLE NEW_SCHEMA.osm_places ADD COLUMN min_scale integer;
ALTER TABLE NEW_SCHEMA.osm_places ADD COLUMN fontsize integer;

UPDATE NEW_SCHEMA.osm_places SET max_scale = 100000000, min_scale = 0, fontsize = 32 WHERE z_order = 4; -- city
UPDATE NEW_SCHEMA.osm_places SET max_scale = 250000, min_scale = 0, fontsize = 26 WHERE z_order = 3; --town
UPDATE NEW_SCHEMA.osm_places SET max_scale = 25000, min_scale = 0, fontsize = 20 WHERE z_order = 2; --village
UPDATE NEW_SCHEMA.osm_places SET max_scale = 10000, min_scale = 0, fontsize = 16 WHERE z_order = 1; --hamlet
UPDATE NEW_SCHEMA.osm_places SET max_scale = 10000, min_scale = 0, fontsize = 16 WHERE z_order = 0; --suburb
