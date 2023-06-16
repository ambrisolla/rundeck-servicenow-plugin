from argparse import ArgumentParser

class Arguments:
    
    parse = ArgumentParser(
        prog='Service Now integration - (Rundekc Plugin)')
    
    parse.add_argument(
        '-u',
        '--sn-username',
        required=True)
    
    parse.add_argument(
        '-p',
        '--sn-password',
        required=True)
    
    parse.add_argument(
        '-s',
        '--sn-server',
        required=True)
    
    parse.add_argument(
        '-r',
        '--rd-server',
        required=True)
    
    parse.add_argument(
        '-k',
        '--rd-token',
        required=True)
        
    parse.add_argument(
        '-a',
        '--action',
        required=True,
        choices=['open_change', 'close_change'])
    
    parse.add_argument(
        '-j',
        '--rd-ref-job',
        help='Referenced Rundeck job that contains \
                the payload to close the Change. \
                If empty, the job will try \
                to find a Change Number \
                associated with the current Rundeck job.',
                required=False)

    args = vars(parse.parse_args())

    SN_USERNAME = args['sn_username']
    SN_PASSWORD = args['sn_password']
    SN_SERVER = args['sn_server']
    RD_SERVER = args['rd_server']
    RD_TOKEN = args['rd_token']
    RD_REF_JOB = args['rd_ref_job']
    ACTION = args['action']