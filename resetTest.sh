#!/bin/bash

influx -execute "drop database load_testing"
influx -execute "create database load_testing"