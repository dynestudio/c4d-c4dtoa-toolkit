"""
Set Noice Driver - C4D script v0.1 wip 02
Thanks for download - for commercial and personal uses.
This script / tool granted shall not be copied, distributed, or-sold, offered for resale, transferred in whole or in part except that you may make one copy for archive purposes only.

http://dyne.studio/
Writen by: Carlos Dordelly
Special thanks: Pancho Contreras, Terry Williams & Roberto Gonzalez.

Organize your arnold drivers in one group
Date start: 15/apr/2018
Date version: 15/apr/2018
Date end: --
Written and tested in Cinema 4D R19 / R18 / R17 / R16.

Set Noice Driver belongs to C4DtoA Script Tools and Dyne Tools (group of digital tools from dyne).

"""

import c4d

def main():
    c4d.CallCommand(1040909, 100) # #$06Arnold Driver
    print "Arnold denoiser driver created."

if __name__=='__main__':
    main()