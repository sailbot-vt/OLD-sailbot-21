 #! /bin/sh cd /sys/devices/platform/bone_capemgr File=slots if grep -q "Override Board Name,00A0,Override Manuf,univ-emmc" "$File";  then    
    cd
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