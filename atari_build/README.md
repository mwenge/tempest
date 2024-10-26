# Building Tempest Using the Original Atari Toolset

<!-- vim-markdown-toc GFM -->

* [Prerequisites](#prerequisites)
* [Starting the Build Environment](#starting-the-build-environment)
* [Let's Build](#lets-build)
  * [Building Tempest Version 2A(alt)](#building-tempest-version-2aalt)
* [Let's Link](#lets-link)
* [Getting Files off the PDP-11 and Onto Our Local Machine](#getting-files-off-the-pdp-11-and-onto-our-local-machine)
  * [The Dirty Way](#the-dirty-way)
  * [The Tedious Way](#the-tedious-way)
* [About Our Emulated Build Environment](#about-our-emulated-build-environment)
  * [The Files in this Directory](#the-files-in-this-directory)
  * [The Tempest Source Files: tempest_original.rk05](#the-tempest-source-files-tempest_originalrk05)
* [Sidenote: Viewing A Floppy Disk](#sidenote-viewing-a-floppy-disk)
* [Sidenote: Building with Listings](#sidenote-building-with-listings)
* [Acknowledgments](#acknowledgments)

<!-- vim-markdown-toc -->
## Prerequisites
We need the PDP-11 emulator provided by `simh`:
```
sudo apt install simh
```

## Starting the Build Environment
From within this folder issue the following command:
```
pdp11 tempest.ini
```

We're now inside an emulated RT-11 environment on an emulated PDP-11.

To make things easier we'll enable normal backspace operations:
```
SET TT SCOPE
```

To exit the environment at any time press Ctrl-E and type:
```
exit
```

Alternatively you can re-enter the environment with:
```
cont
```

## Let's Build

`OBJ` and `BIN` are used as nicknames in our build commands for the locations of the object files
and final linked binary. We're going to write them to the tempest disk which has the name `RK1`. So let's 
assign these nicknames accordingly:
```
ASS RK1 OBJ
ASS RK1 BIN
```

To actually view the sources on our tempest disk we have to do:

```
DIR DK1:
```

I'm not totally clear why we use `DK1` and `RK1` interchangeably this way. But here are the files on our
tempest disk (tempest_original.rk05) anyway.
```
.DIR DK1:

ALVGUT.MAC    19                 ALCOIN.MAC     1
STATE2.MAP     1                 MBUCOD.V05    32
002X2 .DAT     1                 MBOX  .SAV    19
ALEXEC.LDA    77                 HLL65 .MAC     4
ALHARD.MAC     7                 ALSOUN.MAC    17
ALWELG.MAC   129                 TEMPST.DOC    16
ALHAR2.MAC     7                 ALDISP.MAC   111
MBUDOC.DOC    34                 ALSCO2.MAC    50
ALDIS2.MAC   111                 ALSCOR.MAC    50
ALCOMN.MAC    52                 ALVROM.MAC    77
ALLANG.MAC    14                 STATE2.COM     1
ALEXEC.MAP    12                 ALTES2.MAC    34
ALEARO.MAC    12                 VGMC  .MAC     8
STATE2.MAC     2                 ANVGAN.MAC    12
ALEXEC.COM     2                 ALEXEC.MAC    24
TEMPST.LDA    77                 MABOX .DAT     1
002X1 .DAT     1                 MBUCOD.MAP     2
MBUCOD.COM     1                 STATE2.SAV     1
ALDIAG.MAC     6                 COIN65.MAC    47
ALTEST.MAC    32                 ASCVG .MAC     2
 40 Files, 1106 Blocks
  400 Free blocks
```

(See [The Tempest Source Files: tempest_original.rk05](#the-tempest-source-files-tempest_originalrk05) for how we created
this disk with the sources on it.)

### Building Tempest Version 2A(alt)

Now we can run the `MAC65` macro assembler to assemble each of the source files. Trying to assemble all the files in one
run does not seem to work in practice (some files get ignored), so we split the process in two below.

```
R MAC65
OBJ:ALWELG=ALWELG
OBJ:ALSCO2=ALSCO2
OBJ:ALDIS2=ALDIS2
OBJ:ALEXEC=ALEXEC
OBJ:ALSOUN=ALSOUN
OBJ:ALVROM=ALVROM

```

To run the second batch press `Ctrl-C` to 'close' the assembler first, then paste:

```
R MAC65
OBJ:ALCOIN=ALCOIN
OBJ:ALLANG=ALLANG
OBJ:ALHAR2=ALHAR2
OBJ:ALTES2=ALTES2
OBJ:ALEARO=ALEARO
OBJ:ALVGUT=ALVGUT

```

Below is the output of our build commands. The files are successfully assembled. Note that we have to press Ctrl-C
at the very end to 'close' the assembler.
```
.R MAC65
*OBJ:ALWELG=ALWELG
OBJ:ALSCO2=ALSCO2
OBJ:ALDIS2=ALDIS2
OBJ:ALEXEC=ALEXEC
OBJ:ALSOUN=ALSOUN
OBJ:ALVROM=ALVROM
ERRORS DETECTED: 0
FREE CORE: 11479. WORDS

*ERRORS DETECTED: 0
FREE CORE: 12479. WORDS

*ERRORS DETECTED: 0
FREE CORE: 11890. WORDS

*ERRORS DETECTED: 0
FREE CORE: 13003. WORDS

*ERRORS DETECTED: 0
FREE CORE: 12597. WORDS

*ERRORS DETECTED: 0
FREE CORE: 12599. WORDS

```
```
.R MAC65
*OBJ:ALCOIN=ALCOIN
OBJ:ALLANG=ALLANG
OBJ:ERRORS DETECTED: 0
FREE CORE: 11118. WORDS

*ALHAR2=ALHAR2
OBJ:ALTES2=ALTES2
OBJ:ALEARO=ALEARO
OBJ:ALVGUT=ALVGUT
ERRORS DETECTED: 0
FREE CORE: 11892. WORDS

*ERRORS DETECTED: 0
FREE CORE: 13186. WORDS

*ERRORS DETECTED: 0
FREE CORE: 12298. WORDS

*ERRORS DETECTED: 0
FREE CORE: 13010. WORDS

*ERRORS DETECTED: 0
FREE CORE: 13178. WORDS

```

We can view the assembled files with a `DIR` command:

```
DIR OBJ:
```

This shows us everything on the tempest disk but you'll notice our object files at the very end of
the listing:
```
.DIR OBJ:

ALVGUT.MAC    19                 ALCOIN.MAC     1
HLL65 .MAC     4                 ALHARD.MAC     7
ALSOUN.MAC    17                 ALWELG.MAC   129
ALHAR2.MAC     7                 ALDISP.MAC   111
ALSCO2.MAC    50                 ALDIS2.MAC   111
ALSCOR.MAC    50                 ALCOMN.MAC    52
ALVROM.MAC    77                 ALLANG.MAC    14
ALTES2.MAC    34                 ALEARO.MAC    12
VGMC  .MAC     8                 STATE2.MAC     2
ANVGAN.MAC    12                 ALEXEC.MAC    24
ALDIAG.MAC     6                 COIN65.MAC    47
ALTEST.MAC    32                 ASCVG .MAC     2
ALEXEC.LDA    77                 ALWELG.OBJ    40
ALSCO2.OBJ    18                 ALDIS2.OBJ    32
ALEXEC.OBJ     8                 ALSOUN.OBJ     4
ALVROM.OBJ    13                 ALCOIN.OBJ     2
ALLANG.OBJ    12                 ALHAR2.OBJ     3
ALTES2.OBJ    11                 ALEARO.OBJ     3
ALVGUT.OBJ     2                 ALEXEC.LST   108
ALEXEC.MAP    10
 47 Files, 3126 Blocks
  2902 Free blocks

```

## Let's Link
Now that we have our assembled object files we need to collate them into a single 'executable' binary. This process
is called linking and the Atari tool du-jour was `LINKM`.

The command to link our object files is:
```
R LINKM
BIN:ALEXEC/L,ALEXEC/A=OBJ:ALWELG,ALSCO2,ALDIS2,ALEXEC,ALSOUN,ALVROM/C
ALCOIN,ALLANG,ALHAR2,ALTES2,ALEARO,ALVGUT
```


Unfortunately this does not work:
```
.R LINKM
*BIN:ALEXEC/L,ALEXEC/A=OBJ:ALWELG,ALSCO2,ALDIS2,ALEXEC,ALSOUN,ALVROM/C
*ALCOIN,ALLANG,ALHAR2,ALTES2,ALEARO,ALVGUT
MULT DEF OF VGBRIT IN MODULE:  000C
MULT DEF OF VGLIST IN MODULE:  000C
MULT DEF OF XCOMP  IN MODULE:  000C
BYTE RELOCATION ERROR AT A8E5
BYTE RELOCATION ERROR AT AF10
BYTE RELOCATION ERROR AT AF15
BYTE RELOCATION ERROR AT B1BA
BYTE RELOCATION ERROR AT B1F7
BYTE RELOCATION ERROR AT B1FC
BYTE RELOCATION ERROR AT B32D
BYTE RELOCATION ERROR AT B89B
BYTE RELOCATION ERROR AT B89F
BYTE RELOCATION ERROR AT B964
BYTE RELOCATION ERROR AT B96C
BYTE RELOCATION ERROR AT C180
BYTE RELOCATION ERROR AT C185
BYTE RELOCATION ERROR AT C727
BYTE RELOCATION ERROR AT D827
BYTE RELOCATION ERROR AT DCB5
```

The problem is that the version of the MAC65 assembler we have (VM 03.09) has not correctly interpreted lines like the following:
```
    63   0034    85    02G                      STA SCLEVEL+2
```
What we actually want it to assemble is something like this:
```
    63   0034    8D  0002G                      STA SCLEVEL+2
```

That is, we need it to recognize that `SCLEVEL` is a global value that is two bytes long and so requires the `8D` opcode
for the `STA` operation rather than the `85` opcode, which is `STA' for a single-byte value.

It recognises it correctly in the previous line:
```
    62   0031    8D  0000G                      STA SCLEVEL
```
What has thrown it off in our case is the offset of `+2`.

The `LINKM` version on our disk is 'V04-06'. According to the map file that came with our sources the
version actually used to build Tempest was 'V05.00':
```
ATARI LINKM V05.00 LOAD MAP   27-AUG-81   16:46:53 
BIN:ALEXEC.SAV 
```
So we likely have the 'wrong' version of both assembler and linker.

Now, we could try patching the assembler and linker but that would take ages. Instead what we can do is fix up all instances of this issue in the
original source. For example to fix `SCLEVEL+2` we can do the following:

```diff
diff --git a/ALVROM.MAC b/ALVROM.MAC
index a122b96..d64e7b0 100644
--- a/ALVROM.MAC
+++ b/ALVROM.MAC
 SCLEVEL	=SCLEVL-SCORES+SCOBUF
+SCLVL2	=SCLEVEL+2
--- a/ALSCO2.MAC
+++ b/ALSCO2.MAC
@@ -31,7 +31,8 @@
 	.GLOBL MBOLIFE,MSPIKE,MAPROA,MSUPZA
 	.GLOBL VGSTAT,EABAD
 	.GLOBL HISLOC,SCALOC,LIVLOC,SCOLOC
-	.GLOBL SCECOU,SCORES,HIILOC,LSYMB0,SCOBUF,SCLEVEL,VORBOX
+	.GLOBL SCECOU,SCORES,HIILOC,LSYMB0,SCOBUF,SCLEVEL,VORBOX,SCLVL2
@@ -70,7 +71,7 @@ INFO:
 	JSR VGCNTR
 	LDA VGMSGA		;BLANK OUT LEVEL
 	STA SCLEVEL
-	STA SCLEVEL+2
+	STA SCLVL2
```

Once we go ahead and [do this for all instances, assemble and link, and then examine our output](./notebooks/tempest/notebooks/Build Tempest Sources for Version 1.ipynb) we have a version that builds without error and produces a matching binary.
```
.R LINKM
*BIN:ALEXEC/L,ALEXEC/A=OBJ:ALWELG,ALSCO2,ALDIS2,ALEXEC,ALSOUN,ALVROM/C
*ALCOIN,ALLANG,ALHAR2,ALTES2,ALEARO,ALVGUT
MULT DEF OF VGBRIT IN MODULE:  000C
MULT DEF OF VGLIST IN MODULE:  000C
MULT DEF OF XCOMP  IN MODULE:  000C
```

## Getting Files off the PDP-11 and Onto Our Local Machine
### The Dirty Way
We have a bunch of object files on our `tempest_original.rk05` disk now. We can [parse the contents of this
file on our local machine to extract the goodies](../notebooks/Extract%20Object%20Files%20from%20Tempest%20RK05%20Disk%20after%20Assembling%20and%20Linking.ipynb). If you can get this to work it's by far preferable to the tedious way below.

### The Tedious Way
This is tedious unfortunately. To get a single file off the PDP11 we do the following.

Press Ctrl-E to suspend the emulation. Now we set up the `ptp` (print device) to point to a
file on our local filesystem called `file.obj`. This name is arbitrary.

```
att ptp file.obj
```

Now we re-enter the emulation:
```
cont
```

Finally we copy a file from the PDP11, in this case one of our object files `ALDIS2.OBJ`, to the file
on our local filesystem:

```
COPY DK:ALDIS2.OBJ PC:
```

Now on our local filesystem we can rename `file.obj` to its correct name, e.g.:

```
mv file.obj ALDIS2.OBJ
```

We need to repeat this process for each file we're interested in.

## About Our Emulated Build Environment


### The Files in this Directory
File|Description
| --- | --- |
tempest.ini| Configuration file for PDP-11.
sy.rk05| The PDP-11/RT-11 system disk
tempest_original.rk05| Our cartridge disk containing the Tempest sources


### The Tempest Source Files: tempest_original.rk05 
The Tempest source files are available from the [Historical Sources GitHub repository](https://github.com/historicalsource/tempest).
In order to build them in RT-11 we needed to create a virtual RK05 cartridge disk that our emulated RT-11 can use. In a Jupyter notebook
we
[create this disk image with the tempest sources on it](../notebooks/Create%20RK05%20Disk%20Cartridge%20File%20Image%20From%20Tempest%20Sources.ipynb).
The format of these disk images is relatively simple (once you find the
[appropriate documentation](../material/AA-PD6PA-TC_RT-11_Volume_and_File_Formats_Manual_Aug91.pdf)).
And of course it helps to have [something to start from](https://github.com/tschak909/atari-coin-op-assembler/tree/main/coin-op)
thanks to [Thomas Cherryhomes](https://github.com/tschak909).

Our notebook generates an output file called `tempest_original.rk05`. In order to load this file as an RK05 disk cartrige in the
RT-11 emulator we include the following line in `tempest.ini`, the settings file we invoked when booted up our emulated enivironment
with the command `pdp11 tempest.ini`:
```
att rk1 tempest_original.rk05
```
This setting attaches it to the `RK1` device in RT-11. We can view the contents of the disk from with RT-11 using the following command:
```
DIR RK1:
```
This gives us:
```
ALVGUT.MAC    19                 ALCOIN.MAC     1
STATE2.MAP     1                 MBUCOD.V05    32
002X2 .DAT     1                 MBOX  .SAV    19
ALEXEC.LDA    77                 HLL65 .MAC     4
ALHARD.MAC     7                 ALSOUN.MAC    17
ALWELG.MAC   129                 TEMPST.DOC    16
ALHAR2.MAC     7                 ALDISP.MAC   111
MBUDOC.DOC    34                 ALSCO2.MAC    50
ALDIS2.MAC   111                 ALSCOR.MAC    50
ALCOMN.MAC    52                 ALVROM.MAC    77
ALLANG.MAC    14                 STATE2.COM     1
ALEXEC.MAP    12                 ALTES2.MAC    34
ALEARO.MAC    12                 VGMC  .MAC     8
STATE2.MAC     2                 ANVGAN.MAC    12
ALEXEC.COM     2                 ALEXEC.MAC    24
TEMPST.LDA    77                 MABOX .DAT     1
002X1 .DAT     1                 MBUCOD.MAP     2
MBUCOD.COM     1                 STATE2.SAV     1
ALDIAG.MAC     6                 COIN65.MAC    47
ALTEST.MAC    32                 ASCVG .MAC     2
 40 Files, 1106 Blocks
  0 Free blocks
```

## Sidenote: Viewing A Floppy Disk

Press Ctrl-E to suspend the emulation so we can issue a command in `simh`.

Now we can  attach the virtual floppy disk file. In this case we'll attach the
`linkm.x01` file containing a modified version of `LINKM`:

```
att rx0 linkm.x01
```

Now let's go back into RT-11:
```
cont
```

Load the floppy disk:
```
LOAD DX:
```

View the contents of the floppy:
```
DIR DX:
```

Which gives us:
```
LINK0 .MAC    62                 LNKOV1.MAC    40
LNKOV2.MAC    33                 LINKM .SAV    20
LNKOV4.MAC    23                 LNKOV3.MAC    23
LNKV2B.OBJ     2                 LNKLNK.BAT     2
LNKLNK.CTL     2                 LINK0 .OBJ    11
LNKOV1.OBJ     9                 LNKOV2.OBJ     6
LNKOV3.OBJ     6                 LNKOV4.OBJ     5
LNKLNK.LST     8
 15 Files, 252 Blocks
  234 Free blocks
```
## Sidenote: Building with Listings

An alternative invocation of the assembler will produce listing files. Again, you might need to do this piecemeal as I've found it can generate
errors when attempted all at once:

```
R MAC65
OBJ:ALWELG,OBJ:ALWELG.LST=ALWELG
OBJ:ALSCO2,OBJ:ALSCO2.LST=ALSCO2
```
```
R MAC65
OBJ:ALDIS2,OBJ:ALDIS2.LST=ALDIS2
OBJ:ALEXEC,OBJ:ALEXEC.LST=ALEXEC
```
```
R MAC65
OBJ:ALSOUN,OBJ:ALSOUN.LST=ALSOUN
OBJ:ALVROM,OBJ:ALVROM.LST=ALVROM
```

```
R MAC65
OBJ:ALCOIN,OBJ:ALCOIN.LST=ALCOIN
OBJ:ALLANG,OBJ:ALLANG.LST=ALLANG
```
```
R MAC65
OBJ:ALTES2,OBJ:ALTES2.LST=ALTES2
OBJ:ALHAR2,OBJ:ALHAR2.LST=ALHAR2
```
```
R MAC65
OBJ:ALEARO,OBJ:ALEARO.LST=ALEARO
OBJ:ALVGUT,OBJ:ALVGUT.LST=ALVGUT

```
```
R MAC65
OBJ:ALHARD,OBJ:ALHARD.LST=ALHARD
OBJ:ALDISP,OBJ:ALDISP.LST=ALDISP
OBJ:ALSCOR,OBJ:ALSCOR.LST=ALSCOR
OBJ:ALTEST,OBJ:ALTEST.LST=ALTEST
```
Example of building with a symbol cross-reference table:
```
R MAC65
OBJ:ALWELG/L:MEB,OBJ:ALWELG.LST=ALWELG/C
```
## Acknowledgments
This would not have been possible without the notes and files in [Thomas Cherrywood's repository](https://github.com/tschak909/atari-coin-op-assembler/).
There he builds the Centipede sources so pulling together these notes was largely a question of adapting and reusing his work.

