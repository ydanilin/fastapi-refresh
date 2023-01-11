#!/bin/bash

poetry run uvicorn backend.app.main:app --reload
