import logging
import os
import re
import subprocess

def run_command(params, report, ru_client, self, ctx, miniscrub_env):
    """
        This example function accepts any number of parameters and returns results in a KBaseReport
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "ReportResults" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String
    """
    print('#############################################################')
    print(params)
    """
    reads = ru_client.upload_reads({
        'fwd_file': params['parameter_1'],
        'interleaved': 0,
        'name': params['workspace_name'],
        'sequencing_tech': 'Unknown',
        'wsname': params['workspace_name'],
    })
    print('reads', reads)
    """
    proc = subprocess.run(
        ['python3', '-c', '"import sys; print(sys.executable)"'],
        check=True,
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )
    print(f'##############################{proc.stdout}')
    import sys
    print(f'python version: {sys.version}')
    print(f'python executable: {sys.executable}')
        
    input_reads_ref = '79/7/1'
    reads_info = ru_client.download_reads({
        'read_libraries': [input_reads_ref],
        'interleaved': 'true',
        'gzipped': None
    })['files'][input_reads_ref]

    miniscrub_env = dict(os.environ)
    miniscrub_env[
        "MINISCRUB_COMMAND"
    ] = f"""python3 miniscrub.py -h
    """
    subprocess.run(
        "/kb/module/scripts/miniscrub-run.sh".split(" "),
            check=True,
            env=miniscrub_env,
    )

    report_info = report.create({'report':{'objects_created':[],
                                'text_message': params['parameter_1']},
                                'workspace_name': params['workspace_name']
                            })
    output = {
        'report_name': report_info['name'],
        'report_ref': report_info['ref'],
        }
    return output
