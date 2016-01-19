__author__ = 'ritesh'

import logging
import fastq_operations

def main():
    logging.basicConfig(filename='logs/pipeline.log', level=logging.INFO)
    logging.info('Started')

    # Perform FASTQC operation
    dataLocationDir = '/home/ritesh/Ritesh_Work/Data/Test'
    outputDir = '/home/ritesh/Ritesh_Work/Data/Temp'
    fastq_operations.performFastqc(dataLocationDir, outputDir)

    logging.info('Finished')

if __name__ == '__main__':
    main()