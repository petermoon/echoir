# echoir
Remote control skill for Alexa

The client-side job runner only supports IguanaWorks IR.
# On the machine (I use Raspberry PI) that has the IR transceiver set up, use the record_remote script to record some IR blasts you want to be able to initiate from the Echo.
# Set up your Alexa skill on the Alexa website. This can't be automated at the moment.
# Set up your AWS Lambda function.
# Complete config_sample.json, rename to config.json, zip it up with echo_remote_lambda.py, then upload to Lambda.
# Run echoremote.py on a machine with IguanaWorks IR blaster.
# That's it.