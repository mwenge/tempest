# Exploring the Source Code for Tempest
If you are impatient then you should [look here instead](https://github.com/mwenge/tempest_fun) where
we build Tempest with a single `make` command and play around with the source. 

If you are interested in the technical detail of building the sources, then read on.

<!-- vim-markdown-toc GFM -->

* [Building the Tempest Source Code: An Introduction](#building-the-tempest-source-code-an-introduction)
* [Extracting and Playing the ROMs](#extracting-and-playing-the-roms)
* [Building the Tempest Source Code: Version 1](#building-the-tempest-source-code-version-1)
* [Building the Tempest Source Code: Version 2A(Alt)](#building-the-tempest-source-code-version-2aalt)
* [Hacking the Source Code](#hacking-the-source-code)

<!-- vim-markdown-toc -->

## Building the Tempest Source Code: An Introduction
In 2021, the source code for Tempest [surfaced on the 'historicalsource'](https://github.com/historicalsource/tempest/) github repository.
In [the `atari_build` folder](./atari_build/) you'll find the steps for building the Tempest source
code at home. There are complications, but it can be done!

## Extracting and Playing the ROMs 
In [this Jupyter notebook](./notebooks/Reconstruct%20ROMs%20from%20Object%20FIles%20in%20the%20Tempest%20Source%20Dump.ipynb) we
extract the ROM data from the `ALEXEC.LDA` binary included in the source dump and play it on MAME!

## Building the Tempest Source Code: Version 1
In [this Jupyter notebook](./notebooks/Build%20Tempest%20Sources%20for%20Version%201.ipynb) we build and play Version 1 of Tempest.

## Building the Tempest Source Code: Version 2A(Alt) 
In [this Jupyter notebook](./notebooks/Build%20Tempest%20Sources%20for%20Version%202A(Alt).ipynb) we build and play Version 2A(alt) of Tempest.

## Hacking the Source Code
In [this separate repository](https://github.com/mwenge/tempest_fun) I automate the build process and try out some hacking
on the source code. This includes extending the number of maps to 32, various builds with new maps (in the spirit of 
[Tempest tubes](https://arcarc.xmission.com/Web%20Archives/ionpool.net%20(Dec-31-2020)/arcade/tempest_code_project/TempEd/tubes/tubes.html)),
and a version that mimics Tempest 2000.
