import glob, logging


def get_fastq_files(dataLocation):

    '''
    List out .fq or .fastq files from a directory
    :param dataLocation:
    :return:
    '''

    fq_files = glob.glob(dataLocation + '/*.fq')
    if len(fq_files) < 1:
        logging.info('Input FASTQ data location ' + dataLocation + ' doesn\'t contain any .fq file')
        fq_files = glob.glob(dataLocation + '/*.fastq')
        if len(fq_files) < 1:
            print 'No .fq or .fastq files found'
            logging.error('Input FASTQ data location ' + dataLocation + ' doesn\'t contain any .fq or .fastq file')
            return None
        else:
            logging.info('Input FASTQ data location ' + dataLocation + ' contains ' + str(len(fq_files)) +' .fastq files')
    return fq_files
