#!/bin/bash
# Network Management Scripts

# Copy main End island to a temporary directory
cp -f /home/minecraft/multicraft/servers/server1/world_Season5_the_end/DIM1/region/r.0.0.mca /home/minecraft/multicraft/servers/server1/process/
cp -f /home/minecraft/multicraft/servers/server1/world_Season5_the_end/DIM1/region/r.0.-1.mca /home/minecraft/multicraft/servers/server1/process/
cp -f /home/minecraft/multicraft/servers/server1/world_Season5_the_end/DIM1/region/r.-1.0.mca /home/minecraft/multicraft/servers/server1/process/
cp -f /home/minecraft/multicraft/servers/server1/world_Season5_the_end/DIM1/region/r.-1.-1.mca /home/minecraft/multicraft/servers/server1/process/

# Empty DIM1
rm -rf /home/minecraft/multicraft/servers/server1/world_Season5_the_end/DIM1/region/*

# Edit Level.dat
python3.6 /home/minecraft/multicraft/servers/server1/process/EndReset.py

# Move main End island regions back
