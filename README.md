# HackYeah2022 Backend - Wesołe gradienty

Backend module for HackYeah 2022.

## Build

To build the project, execute the following from project directory.
```sh
docker build -i hackyeah-backend:1.0.0 .
```

## Run

Following environment variables need to be set:
* `TWITTER_API_BEARER_TOKEN` - Bearer API token for Twitter API

After setting this up, and building docker image, run the following:

```sh
docker run --publish 5000:5000 --env "TWITTER_API_BEARER_TOKEN=<token>" hackyeah-backend:1.0.0
```

After that API will be exposed at port localhost:5000
