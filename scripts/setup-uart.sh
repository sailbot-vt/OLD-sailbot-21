#! /bin/sh cd /sys/devices/platform/bone_capemgr File=slots if grep -q "Override Board Name,00A0,Override Manuf,univ-emmc" "$File";  then    
    cd
    ###Overide capes with eeprom
    uboot_overlay_addr0=/lib/firmware/BB-UART1-00A0.dtbo
    uboot_overlay_addr1=/lib/firmware/BB-UART2-00A0.dtbo
    uboot_overlay_addr2=/lib/firmware/BB-UART4-00A0.dtbo
    uboot_overlay_addr3=/lib/firmware/BB-UART5-00A0.dtbo
    
    echo "\n Pin configuration available"
    echo "\n UART 4 configuration p9.11 and p9.13"
    sudo config-pin P9.11 uart
    sudo config-pin -q P9.11
    sudo config-pin P9.13 uart
    sudo config-pin -q P9.13
    echo "\n UART 1 configuration p9.26 and p9.24"
    sudo config-pin P9.24 uart
    sudo config-pin -q P9.24
    sudo config-pin P9.26 uart
    sudo config-pin -q P9.26

### Manual setup: 

### You can change /boot/uEnv.txt First of all enable UARTS:

### cape_disable=bone_capemgr.disable_partno=BB-BONELT-HDMI,BB-BONELT-HDMIN
### cape_enable=bone_capemgr.enable_partno=BB-UART1,BB-UART2,BB-UART4,BB-UART5

### Then don't forget to configure pinmux with appropriate dtbo's:

###Overide capes with eeprom
### uboot_overlay_addr0=/lib/firmware/BB-UART1-00A0.dtbo
### uboot_overlay_addr1=/lib/firmware/BB-UART2-00A0.dtbo
### uboot_overlay_addr2=/lib/firmware/BB-UART4-00A0.dtbo
### uboot_overlay_addr3=/lib/firmware/BB-UART5-00A0.dtbo

###