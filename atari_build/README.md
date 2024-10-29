# Building Tempest Using the Original Atari Toolset

In the 1970 and early 1980s Atari developed its arcade games using PDP-11 computers manufactured by [Digital Equipment Corporation (DEC)](https://en.wikipedia.org/wiki/Digital_Equipment_Corporation).

The operating system Atari used on these computers was the RT-11. Thanks to a data dump that surfaced on [bitsavers.com](https://bitsavers.org/bits/Atari/arcade/) in late 2023 we have a copy of the toolchain Atari developed for the RT-11. This toolchain is the one we will use here, on an
emulated RT-11/PDP-11 environment, to build Tempest from the [sources](https://github.com/historicalsources/tempest) that appeared on the
[historicalsource](https://github.com/historicalsource) github repository in October 2021. The provenance of these sources is uncertain, but
as you will see they are definitely genuine: they allow us to build a Tempest that matches two known versions of the original arcade game.

This doc is intended to give a total beginner (like myself) an idea of how to go about building the Tempest sources from scratch on a modern linux
environment. It complements slightly more detailed Jupyter notebooks in this repository that allow you to perform the steps required for building both
versions of Tempest provided by the source dump. These are [Version 1](../notebooks/Build%20Tempest%20Sources%20for%20Version%201.ipynb), which
correspond to the ROM set that MAME (the modern arcade emulator) [refers to](https://github.com/mamedev/mame/blob/master/src/mame/atari/tempest.cpp) 
as 'Rev 1' and [Version 2A(Alt)](../notebooks/Build%20Tempest%20Sources%20for%20Version%202A(Alt).ipynb), which corresponds to the very last 
version of Tempest that was released and the ROM set that MAME refers to as 'Rev 3'. 

[This Jupyter notebook](../notebooks/Differences%20Between%20Rev1%20and%20Rev2A(Alt).ipynb) details the differences between these two revisions in terms of the changes and bugfixes that were made.

Enough preamble, let's try to build this thing.

<!-- vim-markdown-toc GFM -->

* [Prerequisites](#prerequisites)
* [Starting the Build Environment](#starting-the-build-environment)
* [Let's Build](#lets-build)
  * [Building Tempest Version 2A(alt)](#building-tempest-version-2aalt)
* [Let's Link](#lets-link)
* [Let's Play](#lets-play)
* [Sidenote: About Our Emulated Build Environment](#sidenote-about-our-emulated-build-environment)
  * [The Files in this Directory](#the-files-in-this-directory)
  * [The Tempest Source Files: tempest_original.rk05](#the-tempest-source-files-tempest_originalrk05)
* [Sidenote: Viewing A Floppy Disk](#sidenote-viewing-a-floppy-disk)
* [Sidenote: Building with Listings](#sidenote-building-with-listings)
* [Sidenote: Getting Files off the PDP-11 and Onto Our Local Machine](#sidenote-getting-files-off-the-pdp-11-and-onto-our-local-machine)
  * [The Dirty Way](#the-dirty-way)
  * [The Tedious Way](#the-tedious-way)
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

To view the sources on our tempest source code disk we have to do:

```
DIR RK1:
```
This gives:
```
.DIR RK1:
 
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
  24 Files, 828 Blocks
   5200 Free blocks
```

(See [The Tempest Source Files: tempest_original.rk05](#the-tempest-source-files-tempest_originalrk05) for how we created
this disk with the sources on it.)

### Building Tempest Version 2A(alt)

Now we can run the `MAC65` macro assembler to assemble each of the source files. Trying to assemble all the files in one
run does not seem to work in practice (some files get ignored), so we split the process in two below.

```
R MAC65
RK1:ALWELG=ALWELG
RK1:ALSCO2=ALSCO2
RK1:ALDIS2=ALDIS2
RK1:ALEXEC=ALEXEC
RK1:ALSOUN=ALSOUN
RK1:ALVROM=ALVROM

```

To run the second batch press `Ctrl-C` to 'close' the assembler first, then paste:

```
R MAC65
RK1:ALCOIN=ALCOIN
RK1:ALLANG=ALLANG
RK1:ALHAR2=ALHAR2
RK1:ALTES2=ALTES2
RK1:ALEARO=ALEARO
RK1:ALVGUT=ALVGUT

```

Below is the output of our build commands. The files are successfully assembled. Note that we have to press Ctrl-C
at the very end to 'close' the assembler.
```
.R MAC65
*RK1:ALWELG=ALWELG
RK1:ALSCO2=ALSCO2
RK1:ALDIS2=ALDIS2
RK1:ALEXEC=ALEXEC
RK1:ALSOUN=ALSOUN
RK1:ALVROM=ALVROM
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
*RK1:ALCOIN=ALCOIN
RK1:ALLANG=ALLANG
RK1:ERRORS DETECTED: 0
FREE CORE: 11118. WORDS

*ALHAR2=ALHAR2
RK1:ALTES2=ALTES2
RK1:ALEARO=ALEARO
RK1:ALVGUT=ALVGUT
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

As before, we can view the assembled files with a `DIR` command. Notice that we've written our object files to the same
disk as the sources. This will be helpful in [extracting them later](../notebooks/Build%20Tempest%20Sources%20for%20Version%202A(Alt).ipynb).

```
DIR RK1:
```

This shows us everything on the tempest disk but you'll notice our object files at the very end of
the listing:
```
.DIR RK1:

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
ALSCO2.OBJ    18                 ALDIS2.OBJ    32
ALEXEC.OBJ     8                 ALSOUN.OBJ     4
ALVROM.OBJ    13                 ALCOIN.OBJ     2
ALLANG.OBJ    12                 ALHAR2.OBJ     3
ALTES2.OBJ    11                 ALEARO.OBJ     3
ALVGUT.OBJ     2                 ALWELG.OBJ    40
 47 Files, 3126 Blocks
  2902 Free blocks

```

## Let's Link
Now that we have our assembled object files we need to collate them into a single 'executable' binary that will be called
`ALEXEC.LDA`. This process
is called linking and the Atari tool du-jour was `LINKM`.

The command to link our object files is:
```
R LINKM
RK1:ALEXEC/L,ALEXEC/A=RK1:ALWELG,ALSCO2,ALDIS2,ALEXEC,ALSOUN,ALVROM/C
ALCOIN,ALLANG,ALHAR2,ALTES2,ALEARO,ALVGUT
```


Unfortunately this does not work:
```
.R LINKM
*RK1:ALEXEC/L,ALEXEC/A=RK1:ALWELG,ALSCO2,ALDIS2,ALEXEC,ALSOUN,ALVROM/C
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

The problem is that our toolchain has not correctly interpreted lines like the following:
```
    63   0034    85    02G                      STA SCLEVEL+2
```
What we actually want it to assemble is something like this:
```
    63   0034    8D  0002G                      STA SCLEVEL+2
```

That is, we need it to recognize that `SCLEVEL` is a global value that is two bytes long and so requires the `8D` opcode
for the `STA` operation rather than the `85` opcode which is `STA` for a single-byte value.

The assembler recognises the need for `8D` correctly in this line:
```
    62   0031    8D  0000G                      STA SCLEVEL
```
What has thrown it off in our case is the offset of `+2`.

We don't know the version of `MAC65` used for building Tempest back in the day since there is nothing on the sources disk to tell us,
but the version we are using here is `VM 03.09`. The `LINKM` version on our disk (the one
we got via the bitsavers dump, along with our `MAC65`)  is `V04-06`. 
According to the `ALEXEC.MAP` file that came with our sources the version actually used to build Tempest was `V05.00`:
```
ATARI LINKM V05.00 LOAD MAP   27-AUG-81   16:46:53 
RK1:ALEXEC.SAV 
```
So we likely have the 'wrong' version of both assembler or linker or both.

Now, we could try patching the assembler and/or linker but that would take ages. Instead what we can do is fix up all instances of this issue in the
original source. For example, to fix `SCLEVEL+2` we can do the following:

```diff
--- a/ALVROM.MAC
+++ b/ALVROM.MAC
+SCLVL2	=SCLEVEL+2
--- a/ALSCO2.MAC
+++ b/ALSCO2.MAC
@@ -31,7 +31,8 @@
-	.GLOBL SCECOU,SCORES,HIILOC,LSYMB0,SCOBUF,SCLEVEL,VORBOX
+	.GLOBL SCECOU,SCORES,HIILOC,LSYMB0,SCOBUF,SCLEVEL,VORBOX,SCLVL2
-	STA SCLEVEL+2
+	STA SCLVL2
```

In case it's not apparent, we just create a new global variable for the 'offset' version used by the source, so instead of using
something like `SCALEVEL+2`, we create a variable called `SCLVL2` and assign the value of `SCALEVEL+2` to it.

Once we go ahead and [do this for all instances, assemble and link, and then examine our output](../notebooks/Build%20Tempest%20Sources%20for%20Version%202A(Alt).ipynb) we have a version that builds without error and produces a matching binary.
```
.R LINKM
*RK1:ALEXEC/L,ALEXEC/A=RK1:ALWELG,ALSCO2,ALDIS2,ALEXEC,ALSOUN,ALVROM/C
*ALCOIN,ALLANG,ALHAR2,ALTES2,ALEARO,ALVGUT
MULT DEF OF VGBRIT IN MODULE:  000C
MULT DEF OF VGLIST IN MODULE:  000C
MULT DEF OF XCOMP  IN MODULE:  000C
```

The `MULT DEF` warnings don't see to make any difference. We get a binary output called `ALEXEC.LDA` that is byte-for-byte identical to the one
both on the `historicalsource` disk and that can be used to generate the ROM files that float around the internet for playing Tempest on MAME.

## Let's Play
To demonstrate this in detail, there are two Jupyter notebooks that allow you to patch, build, and play Tempest from its sources in this repository:
* [Version 1](../notebooks/Build%20Tempest%20Sources%20for%20Version%201.ipynb)
* [Version 2A(Alt)](../notebooks/Build%20Tempest%20Sources%20for%20Version%202A(Alt).ipynb)

In each of these I've more or less automated the required steps. The source dump contains two versions of Tempest, which is why we have
two builds to choose from. Another doc worth checking out contains the [steps for extracting the ROMS from 
the binaries that comes with the source dump](../notebooks/Reconstruct%20ROMs%20from%20Object%20FIles%20in%20the%20Tempest%20Source%20Dump.ipynb) and playing them on MAME. 

## Sidenote: About Our Emulated Build Environment


### The Files in this Directory
File|Description
| --- | --- |
tempest.ini| Configuration file for PDP-11.
sy.rk05| The PDP-11/RT-11 system disk
sy_clean.rk05| A clean version of the PDP-11/RT-11 system disk
tempest_original.rk05| Our cartridge disk containing the Tempest sources
tempest_original_clean.rk05| A clean cartridge disk containing the Tempest sources
tempest_modified_clean.rk05| A clean cartridge disk containing the Tempest sources modified to build with our 'wrong' assembler/linker

Using the environment will write content to `sy.rk05` and building Tempest will write object files and binaries to
`tempest_original.rk05` so you will end up modifying both disks simply by using them.
The two 'clean' disk images above are provided so that you can revert the emulated environment to its original state at any point by
copying them over, e.g.: 
```
cp sy_clean.rk05 sy.rk05
cp tempest_original_clean.rk05 tempest_original.rk05
```

### The Tempest Source Files: tempest_original.rk05 
The Tempest source files are available from the [Historical Sources GitHub repository](https://github.com/historicalsource/tempest).
In order to build them in RT-11 we needed to create a virtual RK05 cartridge disk that our emulated RT-11 can use. In a Jupyter notebook
we
[create this disk image with the tempest sources on it](../notebooks/Create%20RK05%20Disk%20Cartridge%20File%20Image%20From%20Tempest%20Sources.ipynb).
If you're wondering where `rt11_utils` comes from in that notebook, it's a [short python file of utility functions I cooked up](../notebooks/rt11_utils.py) for reading and writing stuff from RT11 disks. The format of these disk images is relatively simple (once you find the
[appropriate documentation](../material/AA-PD6PA-TC_RT-11_Volume_and_File_Formats_Manual_Aug91.pdf)).
The `syk.r05` (which provides most of the RT-11 system) is copied from Thomas Cherryhome's [work on rebuilding the Centipede sources](https://github.com/tschak909/atari-coin-op-assembler/tree/main/coin-op). I also adapted the `tempest.ini` file from his work.

[Our notebook](../notebooks/Create%20RK05%20Disk%20Cartridge%20File%20Image%20From%20Tempest%20Sources.ipynb) generates
an output file called `tempest_original.rk05`. In order to load this file as an RK05 disk cartridge in the
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
RK1:ALWELG,RK1:ALWELG.LST=ALWELG
RK1:ALSCO2,RK1:ALSCO2.LST=ALSCO2
```
```
R MAC65
RK1:ALDIS2,RK1:ALDIS2.LST=ALDIS2
RK1:ALEXEC,RK1:ALEXEC.LST=ALEXEC
```
```
R MAC65
RK1:ALSOUN,RK1:ALSOUN.LST=ALSOUN
RK1:ALVROM,RK1:ALVROM.LST=ALVROM
```

```
R MAC65
RK1:ALCOIN,RK1:ALCOIN.LST=ALCOIN
RK1:ALLANG,RK1:ALLANG.LST=ALLANG
```
```
R MAC65
RK1:ALTES2,RK1:ALTES2.LST=ALTES2
RK1:ALHAR2,RK1:ALHAR2.LST=ALHAR2
```
```
R MAC65
RK1:ALEARO,RK1:ALEARO.LST=ALEARO
RK1:ALVGUT,RK1:ALVGUT.LST=ALVGUT

```
```
R MAC65
RK1:ALHARD,RK1:ALHARD.LST=ALHARD
RK1:ALDISP,RK1:ALDISP.LST=ALDISP
RK1:ALSCOR,RK1:ALSCOR.LST=ALSCOR
RK1:ALTEST,RK1:ALTEST.LST=ALTEST
```
Example of building with a symbol cross-reference table:
```
R MAC65
RK1:ALWELG/L:MEB,RK1:ALWELG.LST=ALWELG/C
```

## Sidenote: Getting Files off the PDP-11 and Onto Our Local Machine
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
## Acknowledgments
This would not have been possible without the notes and files in [Thomas Cherrywood's repository](https://github.com/tschak909/atari-coin-op-assembler/).
There he builds the Centipede sources so pulling together these notes was largely a question of adapting and reusing his work.

