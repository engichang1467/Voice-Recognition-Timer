# Voice Assistence Timer with Picovoice

Using Picovoice's Python SDK to create a simple timer that allows users to set the timer with voice commands.

## Set up Picovoice

1. Create an account on [Picovoice](https://picovoice.ai/) to access the Picovoice console.
2. On `AccessKey`, click on `Create AccessKey` to get a new access key.
3. Create our wake word with `Porcupine Wake Word Engine`.
    - [Click here for more instructions](https://picovoice.ai/docs/quick-start/console-porcupine/)
4. Create our intent from spoken command with `Rhino Speech-to-Intent Engine`.
    - This is where it will create a ML model based on the spoekn command.
    - [Click here for more instructions](https://picovoice.ai/docs/quick-start/console-rhino/)

## To Compile
- Install required packages
```bash
pip3 install -m requirements.txt
```

- To run the program
```bash
python3 testPico.py --access_key {your access key}
```

## Check out my demo
[Check it out](https://youtu.be/DU60Ar3n4_M)

## References

- [Picovoice Console Tutorial: Designing a Drive Thru with Edge Voice AI](https://www.youtube.com/watch?v=npBaOx30QUs)
- [Picovoice Platform - Python SDK - Alarm Clock Demo](https://www.youtube.com/watch?v=MCWij6lZyP4)
- [End-to-End Voice Recognition with Python](https://medium.com/picovoice/end-to-end-voice-recognition-with-python-41f01c2d4346)
- [Picovoice demo Github](https://github.com/Picovoice/picovoice/tree/master/demo/tkinter)
- [Rhino Syntax Cheat Sheet](https://picovoice.ai/docs/tips/syntax-cheat-sheet/)
- [Picovoice Platform - Python Quick Start](https://picovoice.ai/docs/quick-start/picovoice-python/)