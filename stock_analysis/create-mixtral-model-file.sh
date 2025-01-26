#!/bin/bash

model_name="mixtral"
custom_model_name="crewai-mixtral"

ollama pull $model_name

ollama create $custom_model_name -f ./MixtralModelFile