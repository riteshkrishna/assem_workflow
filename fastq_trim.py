__author__ = 'ritesh'

import os, logging, subprocess
import read_xml as rx
import utilities

'''
    Adapter removal and fixed length trimming using the CUTADAPT tool
'''

def removeAdaptors_cutadapt(dataLocation, se_or_pe, adapterDict, fixBaseNumber, outputDir, *pairedFiles):
    '''
    :param adapterDict: Adaptar dictionary in form compatible with "cutadapt". Like [ADAPTER:-a] for a 3' adapter type,
    [ADAPTER:-g] for a 5' adapter,[ADAPTER$:-a] for anchored 3' adapter,[^ADAPTER:-g] for anchored 5' adapter, and
    [ADAPTER:b] for both 5' and 3' adapter type. Similarly, it can take -A, -B and -G for paired versions.
    Details - "http://cutadapt.readthedocs.org/en/stable/guide.html#removing-adapters"

    :param se_or_pe: Single or paired end data. Options - 'S' or 'P'
    :param fixBaseNumber: Remove fixed number of bases. -u option like -u 5 (remove first 5 bases)
    :param *pairedFiles: Pairing of files as specified by user. Required for paired-end data

    '''

    dataType = ['S','P']

    # Determine the location of executable
    xmlFile = 'configs/executables.xml'
    nodeName = 'CUTADAPT'
    tool_path = rx.extractLocationFromExecutables(xmlFile,nodeName)


    if se_or_pe not in dataType:
        logging.error('removeAdaptors_cutadapt: Incorrect specification for read data type. Specify S or P, opposed to the provided option - ' + se_or_pe)
        return None

    # create output dir if doesn't exist
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)
        logging.info('removeAdaptors_cutadapt: Directory created at ' + outputDir)

    # check if correct adapter types specified
    allowedAdapterTypes = ['-a', '-g', '-b', '-A', '-G', '-B'] # As specified by cutadapt

    userProvidedAdapterTypes = adapterDict.values()
    for type in userProvidedAdapterTypes:
        if type not in allowedAdapterTypes:
            logging.error('removeAdaptors_cutadapt: Wrong keys provided for specifying adapters. Wrong entry found is : ' + type)
            return None

    # Arrange adapter list to a string
    adapters = adapterDict.keys()
    adapter_parameter_format = ''
    for adapter in adapters:
        adapter_parameter_format = adapter_parameter_format + adapterDict[adapter] + ' ' + adapter + ' '

    print('Adapters and parameters :' + adapter_parameter_format)
    logging.info('removeAdaptors_cutadapt: Adapters and parameters :' + adapter_parameter_format)

    if se_or_pe == 'S':

        # expect a folder with .fq
        fq_files = utilities.get_fastq_files(dataLocation)
        if fq_files is None:
            logging.error('No FASTQ files found.')

        # Open file for recording cutadapt output
        reportFile = os.path.join(outputDir,'cutadaptReport.txt')
        report = open(reportFile, mode='w')

        for fq_file in fq_files:
            (dirname, filename) = os.path.split(fq_file)
            outPath = os.path.join(outputDir, filename)

            cutadapt_command = [tool_path, adapter_parameter_format, '-u',fixBaseNumber,'-o', outPath,fq_file]

            print('cutadapt command - ' + ' '.join(cutadapt_command))
            logging.info('removeAdaptors_cutadapt: cutadapt command - ' + ' '.join(cutadapt_command))
            p = subprocess.Popen(cutadapt_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            for line in p.stdout:
                report.write(str(line))
                p.stdout.flush()

        report.close()
        return 0
    else:
        # expect a folder and pairing of files. Files should be paired in same way as the adapters are specified.
        pairedFiles_dict = pairedFiles[0]
        if not isinstance(pairedFiles_dict, dict):
            logging.error('removeAdaptors_cutadapt: requires dictionary format for using the Paired-end trimming')
            return None

        # Open file for recording cutadapt output
        reportFile = os.path.join(outputDir,'cutadaptReport.txt')
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

                cutadapt_command = [tool_path, adapter_parameter_format, '-u',fixBaseNumber,'-o', st1_outPath, '-p',st2_outPath, st1_file_path, st2_file_path]

                print('cutadapt command - ' + ' '.join(cutadapt_command))
                logging.info('removeAdaptors_cutadapt: cutadapt command - ' + ' '.join(cutadapt_command))
                p = subprocess.Popen(cutadapt_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
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

    # # Cutadapt single reads
    # dataLocationDir = '/home/ritesh/Ritesh_Work/Data/Test'
    # outputDir = '/home/ritesh/Ritesh_Work/Data/Temp'
    # se_or_pe = 'S'
    # adapterDict ={'ADAPTER1':'-a','ADAPTER2':'-g'}
    # fixBaseNumber = str(10)
    # removeAdaptors_cutadapt(dataLocationDir, se_or_pe, adapterDict, fixBaseNumber, outputDir)

    # Cutadapt paired-end reads
    dataLocationDir = '/home/ritesh/Ritesh_Work/Data/Test'
    outputDir = '/home/ritesh/Ritesh_Work/Data/Temp'
    se_or_pe = 'P'
    adapterDict ={'ADAPTER1':'-a','ADAPTER2':'-A'}
    fixBaseNumber = str(10)
    pairedFiles = {'Output1.fastq':'Output2.fastq'}
    removeAdaptors_cutadapt(dataLocationDir, se_or_pe, adapterDict, fixBaseNumber, outputDir,pairedFiles)
