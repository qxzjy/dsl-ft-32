# From GA to PSQL 

* First deploy Airbyte

```shell
git clone https://github.com/airbytehq/airbyte.git
cd airbyte
docker-compose up
```

* Then deploy postgresql and nocodedb 

```shell 
cd deploy_psql_and_nocode
docker-compose up
```

* Set up source - Google Analytics

![crack](https://lead-program-assets.s3.eu-west-3.amazonaws.com/M03-Data_pipelines/set_up_GA_source.png)

:::important 

The values credentials "Service Account Key" is the context of the `.json` file - [Here](https://lead-program-assets.s3.eu-west-3.amazonaws.com/M03-Data_pipelines/GA-decent-envoy-252111-55a1218c02dc.json)

:::

* Set up Destination - PostgreSQL

![crack](https://lead-program-assets.s3.eu-west-3.amazonaws.com/M03-Data_pipelines/Setup_psql_destination.png)

:::important 

Credentials should be the ones you used in PostgreSQL docker-compose!
:::

* Set up connection 

![crack](https://lead-program-assets.s3.eu-west-3.amazonaws.com/M03-Data_pipelines/Setup_ga_psql_connection.png)

* Launch an ELT and wait for it to be finished 

* Then go to Nocode DB on `localhost:8080` (might be different depending on your Docker-compose file) and then create a new project by connecting to a postgresql database:

![crack](https://lead-program-assets.s3.eu-west-3.amazonaws.com/M03-Data_pipelines/Setup_nocode_db_connection.png)
