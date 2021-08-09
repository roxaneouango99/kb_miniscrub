# -*- coding: utf-8 -*-
#BEGIN_HEADER
# from lib.kb_miniscrub import run_kb_miniscrub
import logging
import os
from installed_clients.KBaseReportClient import KBaseReport
from installed_clients.ReadsUtilsClient import ReadsUtils
from . import run_command
#END_HEADER


class kb_miniscrub:
    '''
    Module Name:
    kb_miniscrub

    Module Description:
    A KBase module: kb_miniscrub
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = "git@github.com:roxaneouango99/kb_miniscrub.git"
    GIT_COMMIT_HASH = "c9444929a1baed09d517febb0c7e47d2fea6d47e"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.shared_folder = config['scratch']
        logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                            level=logging.INFO)
        #END_CONSTRUCTOR
        pass


    def run_kb_miniscrub(self, ctx, params):
        """
        This example function accepts any number of parameters and returns results in a KBaseReport
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "ReportResults" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN run_kb_miniscrub
        miniscrub_env = dict(os.environ)
        report = KBaseReport(self.callback_url)
        ru_client = ReadsUtils(self.callback_url)   
        output = run_command(
            params, 
            report, 
            ru_client, 
            self.shared_folder, 
            miniscrub_env
        )
        #END run_kb_miniscrub

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method run_kb_miniscrub return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
