# rundeck-servicenow-plugin

This plugin can be used in a Rundeck workflow to create and close a Service Now change.

## Features
- Open a Service Now change;
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