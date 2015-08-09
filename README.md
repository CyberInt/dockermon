# dockermon - Docker Monitor Utility

`dockermon` listens for events from docker daemon using the docker `/events`
[HTTP API][api].


[api]: https://docs.docker.com/reference/api/docker_remote_api_v1.19/

# Usage

## Library
You can use `dockermon` as a library and then call `watch(callback)`, you're
callback function will be called with new event (dict).

# Command Line
The other option is to use `dockermon` as a command line tool and specify a
program to call with every new event. The program will be launched and the event
encode in JSON will be send to the program standard input. For example:

    python -m dockermon "jq --unbuffered ."

If not program is specified, events will be printed to standard output as JSON
objects, one per line.

# Hacking
"one script no external dependencies" is a design goal, let's not break it :)

We use [tox](https://tox.readthedocs.org/en/latest/) to test. Please make sure
your code passes on all supported platforms (see `tox.ini`) before sending a
pull request.

# Bugs and Project

https://github.com/CyberInt/dockermon
