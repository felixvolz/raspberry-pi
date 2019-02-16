## Intro

I have a Raspberry Pi. This repo will contain scripts I have found handy

## Scripts
### push_button_pull_up.py

#### Usecase: Marketing want to display physical products and to track engagement with the product.

(e.g. Company have an interactive display of shoes, every time consumers pick up the product we count it)

- This implementation assumes a Raspberry Pi with button has been setup. 
- This implementation assumes the product is resting on the button and the button is depressed.
- This script will log every time the button is released (i.e. product is picked up)
- This script plays an eductional video when the product is picked up
- This script will re-set every time the button is pressed (i.e. the product is put back down on the button)

- Error Handling
- This script ignores/handles false positives (i.e. light switch triggers power surge, causes GPIO event)
- This script prevents video from playing if already playing

#### Specifics/Setup
Raspberry PI
Setup a circuit to connect a pushbutton to Raspberry Pi
	similar to http://www.toptechboy.com/tutorial/raspberry-pi-lesson-29-configuring-gpio-pins-as-inputs/

Script assumes pin 12 to be an input pin and set initial value to be pulled high and  pin 6 to ground

1. 