# Docker development setup

## Getting started
These instructions should get you to a minimal working development setup in just 5 simple steps:

1. Copy `<repo>/web/tutoring/settings_dev.py` to `web/tutoring/settings.py`.
2. Create a folder `<repo>/coverapi` and drop the [Cover API tester files](https://bitbucket.org/cover-webcie/coverapi-tester/) in it.
3. Run `docker compose up`. Wait until everything is up and running. This might take a few minutes.
4. Visit [localhost:8000](http://localhost:8000) in your browser of choice and everything should work as expected.
5. Login with the username and password defined in `<repo>/coverapi/data.json`.

As the entire codebase is mounted as a volume, any changes you make will be applied directly. The same holds for the Cover API tester: you can change the data in `<repo>/coverapi/data.json` to whatever you need to test your features.
If needed during development (after installing a new dependency, for example), you can rebuild your containers by running `docker compose build`.

If you want to test any management scripts, for example the maildigest, you can run these like so `docker exec -it tutoring-main python manage.py senddailydigest`

## Concerns/remarks
- The current setup is using a sqlite database. This may not be the best in some cases, as sqlite is rather limited and therefore not capable of reproducing issues you might run into on the production version.
- Static files are probably not served correctly with the current setup.
- On production, uWSGI is configured to serve static files directly. While this is probably not a good idea for large-scale applications, this should be perfectly fine for this use case as the main concern is scalability.

Have fun!
