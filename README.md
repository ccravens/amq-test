## AMQP-Tester
A basic project for load testing AMQP messaging installs. 

#### Running the Test Framework
You can run the basic setup via docker-compose with:

`docker-compose up --build`

In the docker-compose.yml, you can see it will stand up an active-mq server, a publisher, and a consumer. The `src/loadtester.py`
file is the source for both the publisher and consumer. You control it's behavior via environment variables.

#### Configuring loadtester Image
Use the following environment variables:

- TEST_ROLE: Valid values are `publisher` or `consumer`. 
- AMQP_SERVER: The host an port to use for the AMQP server.
- AMQP_ADDRESS: The address of the messaging queue to communicate with.
- RECURRING_PUBLISHER_PERIOD: Float number determining how many seconds to wait between sending each message.
- RECURRING_PUBLISHER_MIN_MSG_LEN: Minimum length of random messages to be generated for transmission during the test.
- RECURRING_PUBLISHER_MAX_MSG_LEN: Maximum length of random messages to be generated for transmission during the test.

