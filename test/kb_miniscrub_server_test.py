# -*- coding: utf-8 -*-
import os
import time
import unittest
from configparser import ConfigParser

from kb_miniscrub.kb_miniscrubImpl import kb_miniscrub
from kb_miniscrub.kb_miniscrubServer import MethodContext
from kb_miniscrub.authclient import KBaseAuth as _KBaseAuth

from installed_clients.WorkspaceClient import Workspace


class kb_miniscrubTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = os.environ.get('KB_AUTH_TOKEN', None)
        config_file = os.environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('kb_miniscrub'):
            cls.cfg[nameval[0]] = nameval[1]
        # Getting username from Auth profile for token
        authServiceUrl = cls.cfg['auth-service-url']
        auth_client = _KBaseAuth(authServiceUrl)
        user_id = auth_client.get_user(token)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'kb_miniscrub',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = Workspace(cls.wsURL)
        cls.serviceImpl = kb_miniscrub(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']
        suffix = int(time.time() * 1000)
        cls.wsName = "test_ContigFilter_" + str(suffix)
        ret = cls.wsClient.create_workspace({'workspace': cls.wsName})  # noqa

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    def test_your_method(self):
        """
            We tried making kb_miniscrub outputs a FASTQ file 
            of scrubbed reads. However, MiniScrub only provides 
            an empty file as output. This unitest is intended to
            raise a value error as the MiniScrub method does not
            yet produce a FASTQ file of scrubbed reads.
        # We tried running the m ==> dw
        """
        with self.assertRaises(ValueError):
            ret = self.serviceImpl.run_kb_miniscrub(
                self.ctx, {
                'workspace_name': self.wsName,
                'parameter_1': 'Hello World!',
                'input_reads_ref': '79/7/1',
                # 'input_reads_ref': '58980/8/1',
                'output_reads_name': 'out_reads'
            })
       
