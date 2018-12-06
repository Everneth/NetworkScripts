import nbt
import logging
import os
import glob

numFound = False
logging.basicConfig(filename='script.log', level=logging.DEBUG)

# Level.dat
logging.info('Reading DIM1/level.dat')
end_dat = nbt.nbt.NBTFile('//home//minecraft//multicraft//servers//server1//world_Season5_the_end//level.dat', 'rb')
# Change Seed
logging.info('Current Seed: %d', end_dat['Data']['RandomSeed'].value)
end_dat['Data']['RandomSeed'].value += 1
logging.info('New Seed:     %d', end_dat['Data']['RandomSeed'].value)
# Add gateway tags back
logging.info('Restoring gateways...')
for i in range(0,19):
    numFound = False
    for gateway in end_dat['Data']['DimensionData']['1']['DragonFight']['Gateways']:
        if(gateway.value == i):
            numFound = True
    if(not numFound):
        end_dat['Data']['DimensionData']['1']['DragonFight']['Gateways'].tags.append(nbt.nbt.TAG_Int(value=i))
# Reset Dragon
logging.info('Resetting Dragon...')
end_dat['Data']['DimensionData'].clear()
#end_dat['Data']['DimensionData']['1']['DragonFight']['DragonKilled'].value = 0
#end_dat['Data']['DimensionData']['1']['DragonFight']['PreviouslyKilled'].value = 0
#end_dat['Data']['DimensionData']['1']['DragonFight']['DragonUUIDLeast'].value = 0
#end_dat['Data']['DimensionData']['1']['DragonFight']['DragonUUIDMost'].value = 0
logging.info('level.dat changed!')
end_dat.write_file()



for file in glob.glob("*.mca"):
    # Process Regions
    logging.info('Processing regions...')
    region = nbt.region.RegionFile(file, 'rb')
    logging.info('File: %s', file)
    count = 0
    # remove gateways
    for chunk in region:
        for level in chunk['Level']['TileEntities'].tags:
            for tag in level:
                if(tag == 'ExitPortal'):
                    logging.info('Portal found!')
                    if(level['y'].value == 75):
                        #print(level['y'].value)
                        chunk['Level']['TileEntities'].clear()

                        logging.info('Removing gateway')
                        logging.info('chunk (%d, %d)', chunk.loc.x, chunk.loc.z)
                        chunk.write_file('current.%d.%d.nbt' % (chunk.loc.x, chunk.loc.z))
                        current_file = nbt.nbt.NBTFile('current.%d.%d.nbt' % (chunk.loc.x, chunk.loc.z))
                        region.write_chunk(x=chunk.loc.x, z=chunk.loc.z, nbt_file=current_file)
                        os.remove(current_file)
    region.close()
for file in glob.glob("*.mca"):
    # Test Regions
    logging.info('Testing regions...')
    region = nbt.region.RegionFile(file, 'rb')
    logging.info('Test for portals...')
    for chunk in region:
        for level in chunk['Level']['TileEntities'].tags:
            for tag in level:
                if(tag == 'ExitPortal'):
                    isPortal = True
                    logging.warn('Portal found!')
                    print('Portal found!')
                    if(level['y'].value == 75):
                        print(level['y'].value)
                        count += 1
                        logging.error('Gateway found!')
    if(count > 0):
        logging.error('%d portals found.', count)
    else:
        logging.info('Regions processed successfully!')
    region.close()
logging.shutdown()