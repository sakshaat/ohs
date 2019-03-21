#!/usr/bin/env bash
psql -d ohs -U ohs-user -p 5432 -h localhost -w -a -f ./backend/core/table_setup.sql
