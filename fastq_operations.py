__author__ = 'ritesh'

import os, glob, logging
import subprocess
import read_xml as rx


def validateFiles(dataLocation):

    # check if it's a file or dir
    if os.path.exists(dataLocation):
        if os.path.isdir(dataLocation):

            logging.info('Input FASTQ data location ' + dataLocation + ' directory exists')

            fq_files = glob.glob(dataLocation + '/*.fq')

            if len(fq_files) < 1:
                logging.info('Input FASTQ data location ' + dataLocation + ' doesn\'t contain any .fq file')
                # check if .fastq extension files exist instead of .fq?
                fq_files = glob.glob(dataLocation + '/*.fastq')
                if len(fq_files) < 1:
                    print 'No .fq or .fastq files found'
                    logging.error('Input FASTQ data location ' + dataLocation + ' doesn\'t contain any .fq or .fastq file')
                    return None
                else:
                    logging.info('Input FASTQ data location ' + dataLocation + ' contains ' + str(len(fq_files)) +' .fastq files')

            return fq_files # Return a list of .fq files
        else:
            # check if this is fq file
            (dirname, filename) = os.path.split(dataLocation)
            (shortname, extension) = os.path.splitext(filename)

            if extension == '.fq' or extension == '.fastq':
                print('Input FASTQ data location ' + dataLocation + ' regular file exists')
                logging.info('Input FASTQ data location ' + dataLocation + ' regular file exists')
                return dataLocation # Return the file path
            else:
                print('Input FASTQ data location ' + dataLocation + ' doesn\'t have .fq or .fastq extension')
                logging.info('Input FASTQ data location ' + dataLocation + ' doesn\'t have .fq  or .fastq extension')
                return None  # Return None as no .fq present
    else:
        logging.error('Input FASTQ data location ' + dataLocation + ' doesn\'t exist')
        return None


def executeFastqcCommand(rawReadsLocation, outputDir):

    # Determine the location of executable
    xmlFile = 'configs/executables.xml'
    nodeName = 'FASTQC'
    fastqc_path = rx.extractLocationFromExecutables(xmlFile,nodeName)

    # create output dir if doesn't exist
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)
        logging.info('Directory created at ' + outputDir)

    # create fastqc command and execute
    for readFile in rawReadsLocation:
        fastqc_command = [fastqc_path,"-o", outputDir, readFile]
        logging.info('Fastqc command - ' + ' '.join(fastqc_command))
        subprocess.call(fastqc_command)


def performFastqc(rawReadsDir, outputDir):
    """
    Perform FASTQC operations
    """
    fqFiles = validateFiles(rawReadsDir)
    if fqFiles == None:
        logging.error('Exiting...No .fq files found')
        exit(0)
    else:
        executeFastqcCommand(fqFiles, outputDir)

if __name__=="__main__":

    #dataLocationDir = '/home/ritesh/Ritesh_Work/Data/Test'
    #validateFiles(dataLocationDir)

    #dataLocationFile = '/home/ritesh/Ritesh_Work/Data/Test/test1.fq'
    #validateFiles(dataLocationFile)

    #dataLocationFile = '/home/ritesh/Ritesh_Work/Data/Test/test3.fa'
    #validateFiles(dataLocationFile)

    #dataLocationFile = '/home/ritesh/Ritesh_Work/Data/Test/test5.fa'
    #validateFiles(dataLocationFile)

    #dataLocationFile = '/home/ritesh/Ritesh_Work/Data/'
    #validateFiles(dataLocationFile)

    dataLocationDir = '/home/ritesh/Ritesh_Work/Data/Test'
    outputDir = '/home/ritesh/Ritesh_Work/Data/Temp'
    performFastqc(dataLocationDir, outputDir)
