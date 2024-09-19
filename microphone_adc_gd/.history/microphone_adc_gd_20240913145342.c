#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/uart.h"
#include "hardware/gpio.h"
#include "hardware/adc.h"


// UART defines
// By default the stdout UART is `uart0`, so we will use the second one
#define UART_ID uart0
#define BAUD_RATE 115200

// Use pins 4 and 5 for UART1
// Pins can be changed, see the GPIO function select table in the datasheet for information on GPIO assignments
#define UART_TX_PIN 0
#define UART_RX_PIN 1

#define ADC_D_NUM 0
#define ADC_G_NUM 1
#define ADC_D_PIN (26 + ADC_D_NUM)
#define ADC_G_PIN (26 + ADC_G_NUM)
#define ADC_VREF 3.3
#define ADC_RANGE (1 << 12)
#define ADC_CONVERT (ADC_VREF / (ADC_RANGE - 1))
#define N_SAMPLES 20



int main()
{
    stdio_init_all();

    // Set up our UART
    uart_init(UART_ID, BAUD_RATE);
    // Set the TX and RX pins by using the function select on the GPIO
    // Set datasheet for more information on function select
    gpio_set_function(UART_TX_PIN, GPIO_FUNC_UART);
    gpio_set_function(UART_RX_PIN, GPIO_FUNC_UART);
    
    // Use some the various UART functions to send out data
    // In a default system, printf will also output via the default UART
    
    // Send out a string, with CR/LF conversions
    uart_puts(UART_ID, " Hello, UART!\n");

    adc_init();
    adc_gpio_init( ADC_D_PIN);
    adc_gpio_init( ADC_G_PIN);
    
    // For more examples of UART use see https://github.com/raspberrypi/pico-examples/tree/master/uart
    uint adc_d_raw;
    uint adc_g_raw;
    float buffer_d[N_SAMPLES];
    float buffer_g[N_SAMPLES];
    while (true) {
        adc_select_input( ADC_D_NUM);
        adc_d_raw = adc_read(); 
        adc_select_input( ADC_G_NUM);
        adc_g_raw = adc_read(); 
        //printf("%.2f\t%.2f\n", adc_d_raw * ADC_CONVERT, adc_g_raw * ADC_CONVERT);
        sleep_us(10);
    }
}
