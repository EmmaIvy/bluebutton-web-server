# Local Docker Development

To begin developing locally, internal software engineers will need to obtain and copy the `bb2-local-client` certificate files in to the `docker-compose/certstore` location to support the connection to the BFD FHIR server.

To startup the Docker containerized BB2 server, run the following command: 

```
docker-compose up -d

```

Alternatively, to monitor BB2 server logging:

```
docker-compose up -d
docker-compose logs -f | grep web

```
press Ctrl C will stop monitor logging.

## Setting up Pre Commit
Precommit config has been setup inside the repo which will make sure that the code is properly formatted prior to commiting. To setup run as follows:

```
source venv/bin/activate (unless already done)
pip install pre-commit
pre-commit install
```

Once that is setup the pre commit tooling should be run prior to every commit to ensure everything is formatted correctly.

## Blue Button DB image migrations

DB image migrations is done in docker container before blue button server is started.
this is enabled by adding below line to .env:

```
DB_MIGRATIONS=true
```

the migration creates a super user with below attributes, can be customized in .env:

```
SUPER_USER_NAME=root
SUPER_USER_PASSWORD=blue123
SUPER_USER_EMAIL=bluebutton@example.com
```

if chose not to do db image migrations automatically, follow below steps:

set the flag to false before run docker-compose up:

```
DB_MIGRATIONS=false
```

If you're working with a fresh db image
the migrations have to be run.

```
docker-compose exec web docker-compose/migrate.sh

```

If any permissions errors are thrown try the following command,
then run the migrate script again:
```
docker-compose exec web chmod +x docker-compose/migrate.sh
```

## DB Migrations

To check and see if any migrations have been added that haven't been applied to your local DB you can run the following command:
```
python manage.py showmigrations
```
NOTE: Make sure to run within the venv

To then apply any missing migrations you can run the following command:
```
python manage.py migrate
```

You can also undo a single migration, or group of migrations.
To do so you run the following command:
```
python manage.py migrate <app-name> <previous-migration-number>
```

Here's an example:
Migrations are run and here is the output:
```
Running migrations:
  Applying accounts.0002_auto_20210624_1454... OK
  Applying bb2_tools.0001_initial... OK
  Applying bb2_tools.0002_v2user... OK
  Applying bluebutton.0002_remove_resourcerouter_fld_20210624_0826... OK
  Applying bluebutton.0003_archivedcrosswalk... OK
  Applying server.0002_deprecate_resourcerouter_20210624_1454... OK
```

In this example lets pretend that the migration `bb2_tools.0002_v2user` ended up being a bad one and you would like to roll back just that migration.

To do so you'd run the following command:
```
python manage.py migrate bb2_tools 0001
```
NOTE: The number corresponds to the value right before the migration that you want to remove. You can also use `zero` and that will remove all migrations for that app.

The output would look like the following:
```
Operations to perform:
  Target specific migration: 0001_initial, from bb2_tools
Running migrations:
  Rendering model states... DONE
  Unapplying bb2_tools.0002_v2user... OK
```

## Populate BB2 Django models with large number of records

Run migrate.sh will in turn execute a django command among other things:

python manage.py create_test_user_and_application

this will populate BB2 Django models User, UserProfile, Application, Crosswalk, AccessToken with:

one user 'fred', one app 'TestApp', one access token, and one corresponding crosswalk entry, which can be used for minimum test, for local tests that require large number of users, applications, etc. there
is a command to help with that:

python manage.py create_test_users_and_applications_batch

which generates 50 dev users, each has 1-5 apps, and 30k bene users which have following relations:

1. dev users and apps created date are spread over past 700 days randomly
2. each bene sign up (grant access) with 1-3 apps by aproximately: 70% 1 app, 25% 2 apps, 5% 3 apps and
3. among these sign up (access token grants): 80% with demographic scopes, 20% deny demo access
4. benes sign up dates are randomized and set to a date approximately 10 days after apps created date
5. apps' client type, grant type, opt in/out of demographic info access are also randomly generated per a percent distribution

the data generation command assumes that the 30k synthetic beneficiary records in rif files are present
under BB2 local repo base directory:

<bb2_local_repo_base>/synthetic-data/

for detailed info about the synthetic data and how to fetch them, refer to: https://github.com/CMSgov/beneficiary-fhir-data/blob/master/apps/bfd-model/bfd-model-rif-samples/dev/design-sample-data-sets.md


## Running tests from your host

To run the Django unit tests, run the following command:

```
docker-compose exec web python runtests.py
```

You can run individual applications tests or tests with in a specific area as well.

The following are a few examples (drilling down to a single test):
```bash
docker-compose exec web python runtests.py apps.dot_ext.tests
```
```bash
docker-compose exec web python runtests.py apps.dot_ext.tests.test_templates
```
```bash
docker-compose exec web python runtests.py apps.dot_ext.tests.test_templates.TestDOTTemplates.test_application_list_template_override
```
Multiple arguments can be provided too:
```bash
docker-compose exec web python runtests.py apps.dot_ext.tests apps.accounts.tests.test_login
```


# Work on Windows

This requires the use of a linux sub system. This includes a choice of Cygwin, WSL, or VirtualBox + Linux.
Install the Docker Desktop on your Windows host, and set the DOCKER_HOST environment 
variable in linux sub system. Also enable the git configuration for proper EOL CRLF/LF 
convertion using the following command: 

```
git config --global core.autocrlf true

```
in case, with above git core.autocrlf setting, some steps e.g. migrate.sh still chokes (file not found etc.),
fix script manually, e.g. using dos2unix.

If needing to pass the docker compose environment variable, make a copy of the .env.example and
change it accordingly.

### In the .env file add the below hint to properly handle path:

```
COMPOSE_CONVERT_WINDOWS_PATHS=1
```

## Remote debugging BB2 server

Add the line below to the .env file to enable remote debugging
of BB2 server in a docker container:

```
BB20_ENABLE_REMOTE_DEBUG=true
```

After BB2 server is up, debugpy is listening on port 5678.
Afterward, attach to it from your IDE (e.g. VSCode) and put break 
points on the execution path. You can now start debugging.

Add the line below to the .env file to make debugpy wait on attaching, before execute
bluebutton server, this is needed when debugging logic during bluebutton server bootstrap.

```
BB2_REMOTE_DEBUG_WAIT_ATTACH=true
```

## Remote debugging Blue Button unit tests

Run the docker-compose command below to start the unittests with debugpy and for it to wait on port 6789 for the debugger to attach.
Attach to the unittests from an IDE (e.g. VSCode), then put break points in the test cases and debugging.

```
docker-compose up -d unittests

```

## Test and Verify Using Sample Clients

After the container is up, go to http://localhost:8000 (default) address location, and you will see the CMS Blue Button landing page,
Follow the documentation to create accounts, register applications, and other tasks in the local development environment. Note that some features, like email, work differently when running locally.  For example, a text version of an email is sent in to the main server log and is where you will find your signup confirmation activation link. 

You are also able to manually modify Django model objects when needed by using the Django ADMIN at: http://localhost:8000/admin.

To test if there is connectivity to the back end BFD FHIR server, go to the following URL at: http://localhost:8000/health/external.

###Test from clients:


* You can test from in the browser on the homepage using the testclient. This is located from the top of the page by clicking the link `testclient`
* You can test using one of our sample clients applications. See the related blog posts for more information: 
  * [Sample Client Applications](https://bluebutton.cms.gov/blog/Sample-Applications.html) 
  * [More Sample Client Applications](https://bluebutton.cms.gov/blog/More-Sample-Applications.html)
  * [Install a Django Client](https://bluebutton.cms.gov/blog/Installing-a-Django-client-application.html)

Make changes to configurations by following the sample clients instructions and test the end to end scenarios.

## Test with Sample Beneficiary

The following can be used to test FHIR resource calls using CURL commands. These use the sample beneficiary user `fred` that is setup when running the `migration.sh` script in the initial setup.

```
export ACCESS_TOKEN="sample-token-string"
export BENE_ID="-20140000008325"
export HOST="http://localhost:8000"

```

Get Pateint FHIR Resource json


```
curl --header "Authorization: Bearer ${ACCESS_TOKEN}"  "${HOST}/v1/fhir/Patient/${BENE_ID}"

```

Get ExplanationOfBenefit FHIR Resource json

```
curl -k -v --header "Authorization: Bearer ${ACCESS_TOKEN}"  "${HOST}/v1/fhir/ExplanationOfBenefit/?Patient=${BENE_ID}"

```


## Developing and Running Integration Tests in Local Development

The Python source code is located under the `apps/integration_tests` path.

The difference with these tests is the usage of the [LiveServerTestCase](https://docs.djangoproject.com/en/3.1/topics/testing/tools/#django.test.LiveServerTestCase) class from the Django contrib testing tools.  This launches a LIVE Django server in the background on setup. This allows the integration tests to use a live running server for testing BB2 FHIR endpoints, and can also be used to create real user type, simulated browser tests with a [Selenium](http://seleniumhq.org/) client. The live server can also be setup to use a BFD backend service for tests. This is done for the CBC PR checks.

Ultimately these tests are utilized by a CBC (Cloud Bees Core) project/job for Github PR checks. This instruction provides a few ways to test these out locally and to test using the same Docker container image as CBC.

The Python `runtests.py` program, which is also used for running the Django unit type tests, includes an "--integration" option for running integration type tests. This is called by the `docker-compose/run_integration_tests_local_keybase.sh` script that performs pre-setup and sources environment variables from Keybase needed to utilize a live BFD back end system.

There are ways to test locally using the `docker-compose/run_integration_tests_local_keybase.sh` script:

  To get usage help use the following command:

  ```
  docker-compose/run_integration_tests_local_keybase.sh
  ```

  1. Using the docker-compose local development setup and containers. This is the quickest!

     The currently checked out (or working branch) will be used.

     ```
     docker-compose/run_integration_tests_local_keybase.sh dc
     ```
     To debug integration tests:

     ```
     docker-compose/run_integration_tests_local_keybase.sh dc-debug
     ```

  2. Using a Doocker one-off run using the same image (bb2-cbc-build) as CBC. This takes longer, but provides a better test before using in CBC.

     The currently checked out (or working branch) will be used.

     ```
     docker-compose/run_integration_tests_local_keybase.sh cbc
     ```

  3. Using the docker-compose local development setup and containers with local bfd as backend.

     The currently checked out (or working branch) will be used.

     ```
     docker-compose/run_integration_tests_local_keybase.sh local
     ```
     To debug integration tests:

     ```
     docker-compose/run_integration_tests_local_keybase.sh local-debug
     ```

NOTES:
  * The settings variables in the `docker-compose/run_integration_tests_local_keybase.sh cbc` may need to be updated to match your local development platform.
  * For the CBC related setup see these files for more details:
    * `Jenkinsfiles/Jenkinsfile.cbc-run-integration-tests` - Jenkinsfile for running the tests in a CBC project/job. 
    * `Jenkinsfiles/cbc-run-integration-tests.yaml` - Kubernetes docker container specification.  These settings will also need to be updated when there are CBC image naming changes.

## Developing and Running Selenium tests in Local Development
You can run selenium tests by following below steps:

  1. Make sure there is no blue button server and its dependent services running
  2. Go to the base directory of the local repo and run:

     use MSLSX (default)   
     ```
     ./docker-compose/run_selenium_tests_local_keybase.sh
     ```

     ```
     ./docker-compose/run_selenium_tests_local_keybase.sh mslsx
     ```

     use SLSX
     ```
     ./docker-compose/run_selenium_tests_local_keybase.sh slsx
     ```

  3. To trouble shoot tests (visualize webUI interaction): point VNC client to localhost:6900
     1. requires installation of vnc viewer, password (secret)
     2. also need to comment out webdriver headless option, as shown below:
     ```
        ./apps/integration_tests/selenium_tests.py: setUp():
        ...
        opt = webdriver.ChromeOptions()
        opt.add_argument('--headless')
        opt.add_argument("--disable-dev-shm-usage")
        ...
     ```

