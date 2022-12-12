#!/bin/bash

protoc -I=../otomo-protobuf --python_out=../src ../otomo-protobuf/otomo.proto
