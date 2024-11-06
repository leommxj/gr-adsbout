# gr-adsbout
GNU Radio OOT module for encoding ADS-B signal
用于编码ADS-B消息的GNU Radio模块

## Disclaimer
The source code is published for academic purpose only.
本开源代码仅供学习使用。

## Features
* generate ADS-B DF17 position message
* generate ADS-B DF17 identification message
* A concentrator to put messages together 
* generate ADS-B DF17 velocity message

## TODO

## HOW-TO
see *examples/out.grc*

![grc](https://raw.githubusercontent.com/leommxj/gr-adsbout/master/examples/how_grc.png)
After Starting the transmission，You will soon recvive the signal.
![radar](https://raw.githubusercontent.com/leommxj/gr-adsbout/master/examples/how_radar.png)
As a result, you should find the fake flight info on whatever you use to recvive and decode the signal(above pic using virtual radar and adsbspy)


## References
[The 1090MHz Riddle](https://mode-s.org/decode/adsb/introduction.html)

[lyusupov's ADSB-Out](https://github.com/lyusupov/ADSB-Out)
