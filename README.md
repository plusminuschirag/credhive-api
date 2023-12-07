# CredHive Coding Challenge

- Discussed tasked has been implemented in this README, we will be walking through the setup, code structure and certain assumptions and choice we made and the reasoning behind them.

## This README has the following sections

### 1. Assumptions to run the code:

- Python 3.12 installed in your system.
- MongoDB and MongoDB Compass installed to use the db and see changes in real time on UI.

### 2. How to run this code?

- For sake of simplicity .env file is committed with the code, **however best practices involve keeping the .env seperate from the code and generally using key-vault services for better and enhanced protection.**

- .env file looks like the following

  ```SECRET_KEY = ""
  ALGORITHM = ""
  ACCESS_TOKEN_EXPIRE_MINUTES = ""
  JWT_USERNAME = ""
  JWT_PASSWORD = ""
  MONGO_DB_CONN_STRING = ""
  APP_PORT = ""
  ```

  - `SECRET_KEY` and `ALGORITHM`: are used by Authentication Methods.
  - `ACCESS_TOKEN_EXPIRE_MINUTES` mentions the time within which the JWT Token will expire.
  - `JWT_USERNAME` and `JWT_PASSWORD`: are needed to generate a JWT Token or to use endpoints in /docs swagger endpoint.
  - `MONGO_DB_CONN_STRING`: Your mongo db connection string. If you have done fresh installation of mongoDB in your system, you can use the mentioned string in .env directly otherwise you have to construct a string which is straight forward from MongoDB Docs.
  - `APP_PORT` : Contains the port number to run uvicorn server, default 8002.

### 3. Steps to run the code.

- Create a virtual env in your project directory.
- Activate the environment.
- Run `pip install -r requirements.txt`
- Run `python -m pytest` to run the unit tests, make sure all the tests pass before moving ahead.
- Once Complete, run `python main.py`
- This will start serving the code on port 8002, otherwise you can change the APP_PORT in .env and run the server again.

### 4. Access API Endpoints @ /docs

- You can directly use swagger docs @ localhost:8002/docs assuming 8002 is your port number.
- To use any credit request, you have to first enable Authorization by clicking Authorize button on right top corner and entering username and password in the pop up from the .env(`JWT_USERNAME` and `JWT_PASSWORD` respectively) and clicking authorize. This will add Bearer Token to all requests needing authorization. Make sure to authorize again after 60 minutes as the token will expire after an hour.

- Sample Payloads are already present in the endpoint body, once you click Try It Out button on each request, respective paylods will show.
- For PUT Request, all the params are optional, you can hit this endpoint with company name only if you want to update it specifically. No need to provide all the parameters.

### 5. Code Directory Structure

- `clients/` : Directory contains wrapper over the 3rd party integrations such as `MongoDB` and `slowapi(rate limiter)`, this directory can be extended to have other 3rd party integrations for `redis(caching)`, `postgresSQL(credentials)` etc etc.

  - `mongo_client.py` : File contains connection initialization for the `MongoDB`
  - `rate_limiting_client.py` : File contains logic for rate-limiting, currently we are rate-limting based on remote address, more complex or specific algorithms can be used to rate limit.

- `data/` : This directory contains code and files relating to data. Data Manipulation, Checks, Generators and Validators all will be stored here. Idea is to keep data interacting code layer in this directory.

  - `models/` : Contains `MongoDB Document Models`, these models server as extra validation check for data after pydantic, pydantic ensures data incoming to the server passes the check and these models ensures data before entering db should pass the same/different checks.
  - `validators/` : Contains `pydantic` models for our requests, in our setup only `POST` and `PUT` requests need validation checks.
  - `company_data.json` : This is a json file generated via `generate_data.py` file. This file contains the data that you can dump in your `MongoDB` to exactly mimic the working of endpoints.
  - `generate_data.py` : This is a python file implementing `faker` package to create fake data for populating in db.

- `routers/` : Best practices always support routing to break similar functional endpoints into groups. In our current setup we have two such groups `authorization` : represented in `auth.py` and `credits` : represented in `credits.py`. This router directory can contain future endpoints similar to how we are having the current ones, just create a new file and define router in it and link it to `main.py`

  - `authentication/` : This directory relates to `auth.py` router, encapsulating the functionalities behind the scenes. Having such dedicated directories keep the code debt free and easy to track, debug and understand.
  - `auth.py` : `router` file containing authentication endpoints, mainly endpoint to generate JWT Token for `credits` endpoints.
  - `credits.py` : `router` file containing credits endpoints, where we can do operations such as GET, POST, DELETE and PUT on credits.

- `tests/`

  - `test_credit_endpoints.py` : Unit Test file based on pytest to mimic the working of api endpoints. Tests are divide in success and failure scenerios, all the test should pass before

- `main.py` : Entry point for the app.

- `requirements.txt` : Requirements file for the python environment.

### 7. Code Considerations

- `Incoming, Outgoing Data Validation` : Data validation checks using pydantic and mongoengine for incoming request data and outgoing data to db.
- `Rate Limiter on Endpoint Level` : Rate Limiter added on each endpoint with different config to simulate real world behaviour.
- `Integration of Global Exception Handler` : Global Internal Server Error for Server to recover out of any error.

### 6. Future Extensions

- **Rate Limiter**: Rate Limiter in production are different than the one we just used, we are using in-memory storage rate limiter but for a production setup we should use more persistent storage like Redis or instead of doing rate limiting on endpoint level, we can use API Gateway's integrated limiting. This is a design choice.
- **Authentication and Authorization** : Multiple users can be created with different access to endpoints. For production setup we will more robust authentication and authorization setup.
- **Caching**: Currently we aren't caching any API Response, once we figure out eviction policy, caching strategy and hit-miss ratio, we can have a very high response system with less load over our dbs.
- **Logging**: Custom logging can be added on top of logging package to properly show and save logs of a run for error tracing and RCA.
