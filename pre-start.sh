#!/bin/bash

# Tagging and running the image
nerdctl build -t getresources .
nerdctl run -d -p 8080:8080 getresources

# nerdctl tag gitskill:1.0 us.icr.io/bravehearts/gitskill:1.0
