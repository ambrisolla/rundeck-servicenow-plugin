# rundeck-servicenow-plugin

This plugin can be used in a Rundeck workflow to create and close a Service Now change.

## Features
- Open a Service Now Change;
- Close a Service Now Change;

## Requirements

This plugins uses Python3 to interact with Service Now, to work this plugins requires the following python libraries:
- requests;
- PyYAML;


To instal this libraries executes the following command:
```bash
$ pip3 install PyYAML requests
```

Be sure that the following path exists:
```bash
$ ls -l /usr/bin/python3
```


## Build
```
make clean build
```

## Install

```
cp build/libs/servicenow-approval-plugin.zip $RDECK_BASE/libext
```

## Plugin configuration example

The following configuration is required by the plugin:
  - <b>```servicenow_username```:</b>
    - <b>description:</b> Username with permissions to create a Change on ServiceNow. 
    - <b>type:</b> String
  - <b>```servicenow_password```:</b>
    - <b>description:</b> Path to Rundeck Key Storage to access ServiceNow password.
    - <b>type:</b> String
  - <b>```servicenow_server```:</b>
    - <b>description:</b> URL to connect to ServiceNow.
    - <b>type:</b> String
  - <b>```servicenow_action```:</b>
    - <b>description:</b> Action to perform on ServiceNow. Needs to be <b>open_change</b> or <b>close_change</b>.
    - <b>type:</b> String 
  - <b>```rundeck_server```:</b> 
    - <b>description:</b> URL to connecto to Rundeck.
    - <b>type:</b> String
  - <b>```rundeck_token```:</b>
    - <b>description:</b> Path to Rundeck Key Storage to access Rundeck API token.
    - <b>type:</b> String


### Screenshot of Plugin configuration


<img src="resources/plugin-example.png">
