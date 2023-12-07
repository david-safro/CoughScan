# CoughScan

Now available at [coughscan.net](https://coughscan.net)!

Android + web app that leverages a two neural network solution to diagnosing COVID-19 from almost any device, anywhere.

Clientside made by Ian Porell, API/Neural Networks made by David Safro

## Symptoms Test
User must answer several questions regarding their symptoms and general information about them, this test is good at diagnosing general sickness and sicknesses similar to COVID-19, however it is not perfect as sicknesses that exhibit similar symptoms to COVID-19 will be hard for the neural network to distinguish between. This is where the cough test comes in.

## Cough Test
User must cough into their microphone and answer 3 simple questions. This test works best when sickness is given, so thats why taking the symptoms test beforehand is advised.

##Open Source Usage:
This app was created using only open-source material so it can be cloned directly and run. PM2 was used to run the sveltekit application and gunicorn with flask running in a tmux sessions was used for the flask api. To run the app clone the repo and run ```chmod +x run/sh``` and then "./run.sh```. To terminate, do the same but with terminate.sh

Docker image is currently being created. Coming soon.
