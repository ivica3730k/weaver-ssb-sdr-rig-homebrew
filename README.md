# weaver-ssb-sdr-rig-homebrew
Arduino-ish based software defined radio transceiver attempt with direct sampling iq frontend 

## Idea 
The idea is to use Arduino or a similar microcontroller to send and receive LSB and USB signals in the radio-amateur allocated bands using Weaver SSB Modulation/Demodulation
as described by Derek Rowell, on Feb 18 2017.

The analogue front end consists of two pairs of ADE-1 Double balanced mixers, SI5351 clock IC for quadrature LO, and appropriate ADC and DAC devices. For the sake of performance and
cross-platform microcontroller capabilities, external DAC and ADC will be chosen later. 

The digital part will consist of audio pass filters in the IQ chain and the 2nd set of combiners as described in Derek's document.




