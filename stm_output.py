###############################################################
# Code for OpenMV M7 camera
# Prints the attributes for the stm object
# Author: Adam A. Koch (aakoch)
# Date: 2017-12-20
# Copyright (c) 2017 Adam A. Koch
# This work is licensed under the MIT license.
###############################################################

import stm

for var in dir(stm):
    val = getattr(stm, var)
    if type(val).__name__ == "str":
        print(str(var) + "=" + val)
    elif type(val).__name__ == "int" and val > stm.TIM2:
        print(str(var) + "=" + str(hex(val)))
    else:
        print(str(var) + "=" + str(val))

#__name__=stm
#mem8=<8-bit memory>
#mem16=<16-bit memory>
#mem32=<32-bit memory>
#TIM2=1073741824
#TIM3=0x40000400
#TIM4=0x40000800
#TIM5=0x40000c00
#TIM6=0x40001000
#TIM7=0x40001400
#TIM12=0x40001800
#TIM13=0x40001c00
#TIM14=0x40002000
#LPTIM1=0x40002400
#RTC=0x40002800
#WWDG=0x40002c00
#IWDG=0x40003000
#SPI2=0x40003800
#SPI3=0x40003c00
#SPDIFRX=0x40004000
#USART2=0x40004400
#USART3=0x40004800
#UART4=0x40004c00
#UART5=0x40005000
#I2C1=0x40005400
#I2C2=0x40005800
#I2C3=0x40005c00
#I2C4=0x40006000
#CAN1=0x40006400
#CAN2=0x40006800
#CEC=0x40006c00
#PWR=0x40007000
#DAC=0x40007400
#UART7=0x40007800
#UART8=0x40007c00
#TIM1=0x40010000
#TIM8=0x40010400
#USART1=0x40011000
#USART6=0x40011400
#ADC=0x40012300
#ADC1=0x40012000
#ADC2=0x40012100
#ADC3=0x40012200
#SDMMC1=0x40012c00
#SPI1=0x40013000
#SPI4=0x40013400
#SYSCFG=0x40013800
#EXTI=0x40013c00
#TIM9=0x40014000
#TIM10=0x40014400
#TIM11=0x40014800
#SPI5=0x40015000
#SPI6=0x40015400
#SAI1=0x40015800
#SAI2=0x40015c00
#GPIOA=0x40020000
#GPIOB=0x40020400
#GPIOC=0x40020800
#GPIOD=0x40020c00
#GPIOE=0x40021000
#GPIOF=0x40021400
#GPIOG=0x40021800
#GPIOH=0x40021c00
#GPIOI=0x40022000
#GPIOJ=0x40022400
#GPIOK=0x40022800
#CRC=0x40023000
#RCC=0x40023800
#FLASH=0x40023c00
#DMA1=0x40026000
#DMA2=0x40026400
#ETH=0x40028000
#DCMI=0x50050000
#RNG=0x50060800
#QUADSPI=0xa0001000
#DBGMCU=0xe0042000
#CAN3=0x40003400
#SDMMC2=0x40011c00
#MDIOS=0x40017800
#ADC_SR=0
#ADC_CR1=4
#ADC_CR2=8
#ADC_SMPR1=12
#ADC_SMPR2=16
#ADC_JOFR1=20
#ADC_JOFR2=24
#ADC_JOFR3=28
#ADC_JOFR4=32
#ADC_HTR=36
#ADC_LTR=40
#ADC_SQR1=44
#ADC_SQR2=48
#ADC_SQR3=52
#ADC_JSQR=56
#ADC_JDR1=60
#ADC_JDR2=64
#ADC_JDR3=68
#ADC_JDR4=72
#ADC_DR=76
#CRC_DR=0
#CRC_IDR=4
#CRC_CR=8
#CRC_INIT=16
#CRC_POL=20
#DAC_CR=0
#DAC_SWTRIGR=4
#DAC_DHR12R1=8
#DAC_DHR12L1=12
#DAC_DHR8R1=16
#DAC_DHR12R2=20
#DAC_DHR12L2=24
#DAC_DHR8R2=28
#DAC_DHR12RD=32
#DAC_DHR12LD=36
#DAC_DHR8RD=40
#DAC_DOR1=44
#DAC_DOR2=48
#DAC_SR=52
#DBGMCU_IDCODE=0
#DBGMCU_CR=4
#DBGMCU_APB1FZ=8
#DBGMCU_APB2FZ=12
#DMA_LISR=0
#DMA_HISR=4
#DMA_LIFCR=8
#DMA_HIFCR=12
#EXTI_IMR=0
#EXTI_EMR=4
#EXTI_RTSR=8
#EXTI_FTSR=12
#EXTI_SWIER=16
#EXTI_PR=20
#FLASH_ACR=0
#FLASH_KEYR=4
#FLASH_OPTKEYR=8
#FLASH_SR=12
#FLASH_CR=16
#FLASH_OPTCR=20
#FLASH_OPTCR1=24
#GPIO_MODER=0
#GPIO_OTYPER=4
#GPIO_OSPEEDR=8
#GPIO_PUPDR=12
#GPIO_IDR=16
#GPIO_ODR=20
#GPIO_BSRR=24
#GPIO_LCKR=28
#GPIO_AFR0=32
#GPIO_AFR1=36
#SYSCFG_MEMRMP=0
#SYSCFG_PMC=4
#SYSCFG_EXTICR0=8
#SYSCFG_EXTICR1=12
#SYSCFG_EXTICR2=16
#SYSCFG_EXTICR3=20
#SYSCFG_CBR=28
#SYSCFG_CMPCR=32
#I2C_CR1=0
#I2C_CR2=4
#I2C_OAR1=8
#I2C_OAR2=12
#I2C_TIMINGR=16
#I2C_TIMEOUTR=20
#I2C_ISR=24
#I2C_ICR=28
#I2C_PECR=32
#I2C_RXDR=36
#I2C_TXDR=40
#IWDG_KR=0
#IWDG_PR=4
#IWDG_RLR=8
#IWDG_SR=12
#IWDG_WINR=16
#PWR_CR1=0
#PWR_CSR1=4
#PWR_CR2=8
#PWR_CSR2=12
#RCC_CR=0
#RCC_PLLCFGR=4
#RCC_CFGR=8
#RCC_CIR=12
#RCC_AHB1RSTR=16
#RCC_AHB2RSTR=20
#RCC_AHB3RSTR=24
#RCC_APB1RSTR=32
#RCC_APB2RSTR=36
#RCC_AHB1ENR=48
#RCC_AHB2ENR=52
#RCC_AHB3ENR=56
#RCC_APB1ENR=64
#RCC_APB2ENR=68
#RCC_AHB1LPENR=80
#RCC_AHB2LPENR=84
#RCC_AHB3LPENR=88
#RCC_APB1LPENR=96
#RCC_APB2LPENR=100
#RCC_BDCR=112
#RCC_CSR=116
#RCC_SSCGR=128
#RCC_PLLI2SCFGR=132
#RCC_PLLSAICFGR=136
#RCC_DCKCFGR1=140
#RCC_DCKCFGR2=144
#RTC_TR=0
#RTC_DR=4
#RTC_CR=8
#RTC_ISR=12
#RTC_PRER=16
#RTC_WUTR=20
#RTC_ALRMAR=28
#RTC_ALRMBR=32
#RTC_WPR=36
#RTC_SSR=40
#RTC_SHIFTR=44
#RTC_TSTR=48
#RTC_TSDR=52
#RTC_TSSSR=56
#RTC_CALR=60
#RTC_TAMPCR=64
#RTC_ALRMASSR=68
#RTC_ALRMBSSR=72
#RTC_OR=76
#RTC_BKP0R=80
#RTC_BKP1R=84
#RTC_BKP2R=88
#RTC_BKP3R=92
#RTC_BKP4R=96
#RTC_BKP5R=100
#RTC_BKP6R=104
#RTC_BKP7R=108
#RTC_BKP8R=112
#RTC_BKP9R=116
#RTC_BKP10R=120
#RTC_BKP11R=124
#RTC_BKP12R=128
#RTC_BKP13R=132
#RTC_BKP14R=136
#RTC_BKP15R=140
#RTC_BKP16R=144
#RTC_BKP17R=148
#RTC_BKP18R=152
#RTC_BKP19R=156
#RTC_BKP20R=160
#RTC_BKP21R=164
#RTC_BKP22R=168
#RTC_BKP23R=172
#RTC_BKP24R=176
#RTC_BKP25R=180
#RTC_BKP26R=184
#RTC_BKP27R=188
#RTC_BKP28R=192
#RTC_BKP29R=196
#RTC_BKP30R=200
#RTC_BKP31R=204
#SPI_CR1=0
#SPI_CR2=4
#SPI_SR=8
#SPI_DR=12
#SPI_CRCPR=16
#SPI_RXCRCR=20
#SPI_TXCRCR=24
#SPI_I2SCFGR=28
#SPI_I2SPR=32
#TIM_CR1=0
#TIM_CR2=4
#TIM_SMCR=8
#TIM_DIER=12
#TIM_SR=16
#TIM_EGR=20
#TIM_CCMR1=24
#TIM_CCMR2=28
#TIM_CCER=32
#TIM_CNT=36
#TIM_PSC=40
#TIM_ARR=44
#TIM_RCR=48
#TIM_CCR1=52
#TIM_CCR2=56
#TIM_CCR3=60
#TIM_CCR4=64
#TIM_BDTR=68
#TIM_DCR=72
#TIM_DMAR=76
#TIM_OR=80
#TIM_CCMR3=84
#TIM_CCR5=88
#TIM_CCR6=92
#TIM_AF1=96
#TIM_AF2=100
#USART_CR1=0
#USART_CR2=4
#USART_CR3=8
#USART_BRR=12
#USART_GTPR=16
#USART_RTOR=20
#USART_RQR=24
#USART_ISR=28
#USART_ICR=32
#USART_RDR=36
#USART_TDR=40
#WWDG_CR=0
#WWDG_CFR=4
#WWDG_SR=8
#RNG_CR=0
#RNG_SR=4
#RNG_DR=8
