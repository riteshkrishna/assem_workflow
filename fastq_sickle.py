__author__ = 'ritesh'

import os, logging, subprocess
import read_xml as rx
import utilities

'''
    FASTQ trimming using quality by the SICKLE tool
'''


def executeFastqTrim_sickle(dataLocation, se_or_pe, outputDir, quality_type = 'illumina', quality_threhold = 20, *pairedFiles):
    '''
    :param dataLocation: Folder containing input data as .fq or .fasta
    :param se_or_pe: 'S' or 'P'
    :param outputDir:
    :param quality_type: 'illumina', 'sanger'or 'solexa'
    :param quality_threhold: integer value
    param pairedFiles: Pairing of files as specified by user in a dictionary format {'ForwardReads.fq:ReverseReads.fq'}.
    '''

    # Determine the location of executable
    xmlFile = 'configs/executables.xml'
    nodeName = 'SICKLE'
    tool_path = rx.extractLocationFromExecutables(xmlFile,nodeName)

    dataType = ['S','P']

    if se_or_pe not in dataType:
        logging.error('executeFastqTrim_sickle: Incorrect specification for read data type. Specify S or P, opposed to the provided option - ' + se_or_pe)
        return None

    # create output dir if doesn't exist
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)
        logging.info('executeFastqTrim_sickle: Directory created at ' + outputDir)

    if quality_type not in ['illumina', 'sanger', 'solexa']:
        logging.error('Quality type must be one of these : illumina, sanger, solexa')
        return None

    if se_or_pe == 'S':

        # expect a folder with .fq
        fq_files = utilities.get_fastq_files(dataLocation)
        if fq_files is None:
            logging.error('No FASTQ files found.')

        # Open file for recording cutadapt output
        reportFile = os.path.join(outputDir,'sickleReport.txt')
        report = open(reportFile, mode='w')

        for fq_file in fq_files:
            (dirname, filename) = os.path.split(fq_file)
            outPath = os.path.join(outputDir, filename)

            sickle_command = [tool_path, 'se', '-f', fq_file, '-t', quality_type, '-q', str(quality_threhold),'-o', outPath]

            print('sickle command - ' + ' '.join(sickle_command))
            logging.info('executeFastqTrim_sickle: sickle command - ' + ' '.join(sickle_command))
            p = subprocess.Popen(sickle_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            for line in p.stdout:
                report.write(str(line))
                p.stdout.flush()

        report.close()
        return 0
    else:
        # expect a folder and pairing of files. Files should be paired in same way as the adapters are specified.
        pairedFiles_dict = pairedFiles[0]
        if not isinstance(pairedFiles_dict, dict):
            logging.error('executeFastqTrim_sickle: requires dictionary format for using the Paired-end trimming')
            return None

        # Open file for recording cutadapt output
        reportFile = os.path.join(outputDir,'sickleReport.txt')
        report = open(reportFile, mode='w')

        strand1_files = pairedFiles_dict.keys()
        for st1_file in strand1_files:
            st2_file = pairedFiles_dict[st1_file]

            # Create full path for input files
            st1_file_path = os.path.join(dataLocation,st1_file)
            st2_file_path = os.path.join(dataLocation,st2_file)

            if os.path.exists(st1_file_path) & os.path.exists(st2_file_path):

                st1_outPath = os.path.join(outputDir, st1_file)
                st2_outPath = os.path.join(outputDir, st2_file)
                singles_outPath = os.path.join(outputDir,'trimmedSingles.fastq')

                sickle_command = [tool_path, 'pe', '-f', st1_file_path,'-r',st2_file_path, \
                                  '-t', quality_type, '-q', str(quality_threhold), \
                                  '-o', st1_outPath, '-p', st2_outPath, '-s',singles_outPath]

                print('sickle command - ' + ' '.join(sickle_command))
                logging.info('executeFastqTrim_sickle: sickle command - ' + ' '.join(sickle_command))
                p = subprocess.Popen(sickle_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                for line in p.stdout:
                    report.write(str(line))
                    p.stdout.flush()

            else: # Return with error message if file(s) don't exist
                msg = 'Check if files exist: ' + st1_file_path + ',' + st2_file_path
                logging.error(msg)
                return None

        report.close()
        return 0

if __name__=="__main__":

    # # Sickle single reads
    # dataLocationDir = '/home/ritesh/Ritesh_Work/Data/Test'
    # outputDir = '/home/ritesh/Ritesh_Work/Data/Temp'
    # se_or_pe = 'S'
    # quality_type = 'sanger'
    # quality_threhold = 20
    # exec_status = executeFastqTrim_sickle(dataLocationDir, se_or_pe, outputDir, quality_type, quality_threhold)

     # Sickle paired reads
     dataLocationDir = '/home/ritesh/Ritesh_Work/Data/Test'
     outputDir = '/home/ritesh/Ritesh_Work/Data/Temp'
     se_or_pe = 'P'
     quality_type = 'sanger'
     quality_threhold = 33
     pairedFiles = {'Output1.fastq':'Output2.fastq'}
     exec_status = executeFastqTrim_sickle(dataLocationDir, se_or_pe, outputDir, quality_type, quality_threhold,pairedFiles)

     if exec_status == None:
         print ('Failed')
     else:
         print ('Success')
