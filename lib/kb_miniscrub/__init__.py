import logging
import os
import re
import subprocess
import sys


def run_command(params, report, ru_client, shared_folder, miniscrub_env):
    """
        This example function accepts any number of parameters and returns results in a KBaseReport
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "ReportResults" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String
    """
    print(params)
    
    proc = subprocess.run(
        ['python3', '-c', '"import sys; print(sys.executable)"'],
        check=True,
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )
    
    print(f'python version: {sys.version}')
    print(f'python executable: {sys.executable}')
        
    input_reads_ref = params['input_reads_ref']
    reads_info = ru_client.download_reads({
        'read_libraries': [input_reads_ref],
        'interleaved': 'true',
        'gzipped': None
    })['files'][input_reads_ref]
    print(f'{reads_info}')

    reads_path = reads_info['files']['fwd']
    print(reads_path)

    miniscrub_env = dict(os.environ)
    
    out_path = os.path.join(shared_folder, 'reads.fastq')
    miniscrub_env[
        "MINISCRUB_COMMAND"
    ] = f"""python3 miniscrub.py --mask --verbose --output {out_path} {reads_path}
    """
    subprocess.run(
        "/kb/module/scripts/miniscrub-run.sh".split(" "),
        check=True,
        env=miniscrub_env,
    )
    with open(out_path, 'r') as file:
        data = file.readlines()
    if len(data) == 0:
        raise ValueError ('no lines found in FASTQ file:'+ str(out_path))

    new_reads = ru_client.upload_reads({
        'fwd_file': out_path,
        'interleaved': 0,
        'wsname': params['workspace_name'],
        'name': params['output_reads_name'],
        'source_reads_ref':input_reads_ref
    })['obj_ref']
    print(f'{new_reads}')

    report_info = report.create({
        'report':{
            'objects_created':[],
            'text_message': params['parameter_1']
        },
        'workspace_name': params['workspace_name']
    })
    output = {
        'report_name': report_info['name'],
        'report_ref': report_info['ref'],
        }
    return output
