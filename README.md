# echoir
Remote control skill for Alexa

The client-side job runner only supports IguanaWorks IR.

  1. On the machine (I use Raspberry PI) that has the IR transceiver set up, use the record_remote script to record some IR blasts you want to be able to initiate from the Echo.
  2. Set up your Alexa skill on the Alexa website. This can't be automated at the moment.
  3. Set up your AWS Lambda function.
  4. Complete config_sample.json, rename to config.json, zip it up with echo_remote_lambda.py, then upload to Lambda.
  5. Run echoremote.py on a machine with IguanaWorks IR blaster.
  6. That's it.