__author__ = 'ritesh'

'''
    k-mer genie
'''
import os, logging, subprocess
import read_xml as rx
import utilities
import pandas as pd
import numpy as np


def prepare_inputFile(dataLocation, outputDir):
    '''
    kmer-genine requires input .fq files as a list in a text file, with each .fq filename listed on a new line.
    :param dataLocation: Location containing .fq/.fastq files
    :param outputDir: Location where the output will be written
    '''

    fq_files = utilities.get_fastq_files(dataLocation)
    if fq_files is None:
        logging.error('No FASTQ files found.')
        return None

    # create output dir if doesn't exist
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)
        logging.info('kmergenie: Directory created at ' + outputDir)

    # Open file for recording cutadapt output
    input_parameterFile = os.path.join(outputDir,'read_files')
    input_parameter = open(input_parameterFile, mode='w')

    for fq_file in fq_files:
        input_parameter.write(fq_file + '\n')

    input_parameter.close()
    return input_parameterFile


def call_kmergenie(dataLocation, outputDir):
    '''
    The function calls kmer-genie and captures screen output in report.txt file
    :param dataLocation: Location containing .fq/.fastq files
    :param outputDir: Location where the output will be written
    '''

    # Determine the location of executable
    xmlFile = 'configs/executables.xml'
    nodeName = 'KMERGENIE'
    kmergenie_path = rx.extractLocationFromExecutables(xmlFile,nodeName)

    input_parameterFile = prepare_inputFile(dataLocation, outputDir)

    if input_parameterFile is None:
        logging.error('Error creating kmer-genie parameter file')
        exit(0)

    # Need to change dir as the tool doesn't provide option to specify output path
    os.chdir(outputDir)

    # Open file for recording kmer-genie output
    reportFile = os.path.join(outputDir,'report.txt')
    report = open(reportFile, mode='w')

    kmergenie_command = [kmergenie_path, input_parameterFile]

    print('kmergenie command - ' + ' '.join(kmergenie_command))
    logging.info('kmergenie: kmergenie command - ' + ' '.join(kmergenie_command))
    p = subprocess.Popen(kmergenie_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout:
        report.write(str(line))
        p.stdout.flush()

    report.close()

    return 0

def lookfor_histogram_dat(outputDir):

    histogram_file = os.path.join(outputDir,'histograms.dat')

    if not os.path.exists(histogram_file):
        logging.error('Histogram.dat doesn\'t exist')
        return None
    else:
        table = pd.read_csv(histogram_file,' ')
        kmer_list = table['k']
        genome_size_list = table['genomic.kmers']
        index_k = np.argmax(genome_size_list)

        genome_size = genome_size_list[index_k]
        best_kmer = kmer_list[index_k]
        return (best_kmer, genome_size)

def determine_recommended_k_and_genomesize(outputDir):

    (best_kmer, genome_size) = lookfor_histogram_dat(outputDir)
    print ('Predicted best k-mer = ' + str(best_kmer) + '\t Predicted assembly size = ' + str(genome_size))


if __name__=="__main__":

    dataLocationDir = '/home/ritesh/Ritesh_Work/Data/Test'
    outputDir = '/home/ritesh/Ritesh_Work/Data/Temp'

    exec_status = call_kmergenie(dataLocationDir, outputDir)

    if exec_status == None:
        print ('Failed')
    else:
        print ('Success')

    determine_recommended_k_and_genomesize(outputDir)