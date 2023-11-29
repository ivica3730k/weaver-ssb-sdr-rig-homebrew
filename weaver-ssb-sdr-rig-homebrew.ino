#define PI 3.141592

#if defined(__AVR_ATmega2560__) || defined(ARDUINO_AVR_MEGA)
#define USE_TIMER_1 false
#define USE_TIMER_2 false
#define USE_TIMER_3 false
#define USE_TIMER_4 false
#define USE_TIMER_5 true
#define TMR ITimer5
#define PLATFORM "MEGA"
#elif defined(__AVR_ATmega328P__) || defined(ARDUINO_AVR_UNO)
#define USE_TIMER_1 false
#define USE_TIMER_2 true
#define USE_TIMER_3 false
#define USE_TIMER_4 false
#define USE_TIMER_5 false
#define TMR ITimer2
#define PLATFORM "UNO"
#endif

#include "./libs/TimerInterrupt/src/TimerInterrupt.h"

#define SAMPLE_RATE 22050
// long filter_bandwidth = 2400;

long current_sample_rx = 0;
long current_sample_tx = 0;

void sampling_loop_rx()
{
    digitalWrite(12, !digitalRead(12));
    // float cos_wave = cos(2*PI*2400*current_sample_rx/SAMPLE_RATE);
    // float sin_wave = sin(2*PI*2400*current_sample_rx/SAMPLE_RATE);

    if (current_sample_rx >= SAMPLE_RATE)
    {
        digitalWrite(13, !digitalRead(13));
        current_sample_rx = 0;
    }
    else if (current_sample_rx == 0)
    {
        current_sample_rx++;
    }
    else
    {
        current_sample_rx++;
    }
}

void sampling_loop_tx()
{
    digitalWrite(12, !digitalRead(12));
    // float cos_wave = cos(2*PI*2400*current_sample_rx/SAMPLE_RATE);
    // float sin_wave = sin(2*PI*2400*current_sample_rx/SAMPLE_RATE);

    if (current_sample_rx >= SAMPLE_RATE)
    {
        digitalWrite(13, !digitalRead(13));
        current_sample_rx = 0;
    }
    else if (current_sample_rx == 0)
    {
        current_sample_rx++;
    }
    else
    {
        current_sample_rx++;
    }
}
void setup()
{
    Serial.begin(115200);
    pinMode(13, OUTPUT);
    pinMode(12, OUTPUT);
    digitalWrite(13, LOW);
    digitalWrite(12, LOW);
    TMR.init();
    if (TMR.setFrequency(SAMPLE_RATE, sampling_loop_rx))
    {
        Serial.println("Timer set up");
    }
    else
    {
        Serial.println("Timer failed");
        while (1)
        {
        };
    }
};

void loop()
{
    // do something to occupy the CPU here
    while (1) {
        Serial.println("loop");
    }
};
