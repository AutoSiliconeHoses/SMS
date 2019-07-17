# Stock Management System
## What this includes
* Use a server/client model so processes are not hosted on office machines
* Create stock files in a basic format to later be converted to dropship/amazon/ebay formats
* Be configurable, so that we can use a .YML file to change settings instead of having them lost in code
* Multi-threading/multi-processing, this takes advantage of the server hardware by allocating different suppliers to different logical processors.

## How to run it
To run the server, simple install the necessary packages and run `python __servinit__.py`
Make sure that the IP address matches the one of the computer being used to run the server and change it in __clieinit__.py. From there, you can then run `python __clieinit__.py <args>`.

The currently supported arguments are:
* `RUN ` - This allows you to run the supplier scripts, the list of suppliers should be " "(space) delimited
* `UPDATE` - This restarts the server but keeps the queue, this is so that we don't have to walk up to the server to restart the script
* `CNFED` - This allows us to edit the config file from the client. This will become more prominent as we create the GUI.
* `QUEUE` - This allows the client to see the commands that are queued on the server.
