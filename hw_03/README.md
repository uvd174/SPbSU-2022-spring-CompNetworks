# Setup Guide
## System requirements
* Python 3 (3.9.7 will definitely work).

## Run the app
`python one-threaded_server.py`

The server will start at localhost:5000.

`python multi-threaded_server.py <concurrency_level>`

The server will start at localhost:5000 and will process incoming requests

using no more than `concurrency_level` threads.

`python client.py <server_host> <server_port> <file_name>`

The script will send a simple HTTP GET request at `server_host:server_port`

requesting a file in text format at the relative path `file_name`.