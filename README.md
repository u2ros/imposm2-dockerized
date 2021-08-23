# Imposm2-dockerized

## Motivation

Imposm is a great tool for importing/transforming Openstreetmap data. Sadly, version 3 does not support reprojection of data to anything other than EPSG:3857 and EPSG:4326 projections. I created this tool as I need support for local projections (UTM zones and whatnot). Unfortunately, Imposm 2 only supports python 2.7 and is dependant on many deprecated libraries that were available on the Ubuntu Trusty. This project uses Docker and docker-compose to allow running Imposm 2 on a modern host without the need to install an old system just for this.

## How to use

1. put the target pbf file into the ./imposm/pbf subfolder

2. optional: edit imposm mapping file or use default

3. edit docker-compose.yml, change the command under imposm service: (rename YOUR_PBF):

    `command: imposm --connection postgis://postgres:mypass@postgis/postgres -m imposm-mapping.py --proj EPSG:32633 --read --write --optimize ./pbf/YOUR_PBF`

4. spin up the postgis portion of the services:

    `docker-compose up -d postgis`

5. execute Imposm

    `docker-compose up imposm`

Optional step:  After import run post_proc.sql on the database to change table and schema names as Imposm creates a lot of prefixes.

**IMPORTANT: To connect to the containerized instance of postgis, use the port 5444 (not the default 5432) as defined in the docker-compose.yml**

Links: 

Imposm 2.6 reference: https://imposm.org/docs/imposm/latest/

Imposm mapping reference: https://imposm.org/docs/imposm/latest/mapping.html
