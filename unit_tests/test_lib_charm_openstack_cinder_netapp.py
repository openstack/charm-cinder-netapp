# Copyright 2021 Canonical Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import charmhelpers

import charm.openstack.cinder_netapp as cinder_netapp

import charms_openstack.test_utils as test_utils


class TestCinderNetAppCharm(test_utils.PatchHelper):

    def _patch_config_and_charm(self, config):
        self.patch_object(charmhelpers.core.hookenv, 'config')

        def cf(key=None):
            if key is not None:
                return config[key]
            return config

        self.config.side_effect = cf
        c = cinder_netapp.CinderNetAppCharm()
        return c

    def test_cinder_base(self):
        charm = self._patch_config_and_charm({})
        self.assertEqual(charm.name, 'cinder_netapp')
        self.assertTrue(charm.stateless)
        config = {k: v for (k, v) in charm.cinder_configuration()}
        self.assertIn('netapp_storage_family', config)
        self.assertIsNone(config['netapp_storage_family'])
        self.assertIn('netapp_storage_protocol', config)
        self.assertIsNone(config['netapp_storage_protocol'])
        self.assertIn('netapp_server_hostname', config)
        self.assertIsNone(config['netapp_server_hostname'])
        self.assertIn('volume_backend_name', config)
        self.assertIsNone(config['volume_backend_name'])
        self.assertEqual(config.get('volume_driver'),
                         'cinder.volume.drivers.netapp.common.NetAppDriver')

    def test_cinder_https(self):
        charm = self._patch_config_and_charm({'netapp-server-port': 443})
        config = charm.cinder_configuration()
        self.assertIn(('netapp_transport_type', 'https'), config)

    def test_cinder_eseries(self):
        econfig = {'netapp-storage-family': 'eseries',
                   'netapp-controller-ips': '10.0.0.1',
                   'netapp-array-password': 'abc123',
                   'netapp-storage-pools': 'somePool',
                   'use-multipath': True}
        charm = self._patch_config_and_charm(econfig)
        config = charm.cinder_configuration()
        self.assertIn(('netapp_controller_ips',
                       econfig['netapp-controller-ips']), config)
        self.assertIn(('netapp_sa_password',
                       econfig['netapp-array-password']), config)
        self.assertIn(('netapp_storage_pools',
                       econfig['netapp-storage-pools']), config)
        self.assertIn(('use_multipath_for_image_xfer',
                       econfig['use-multipath']), config)
        self.assertFalse(any(q[0] == 'nfs_shares_config' for q in config))

        econfig = {'netapp-storage-protocol': 'nfs',
                   'netapp-nfs-shares-config': 'NFSCONFIG'}
        charm = self._patch_config_and_charm(econfig)
        config = charm.cinder_configuration()
        self.assertIn(('nfs_shares_config',
                       econfig['netapp-nfs-shares-config']), config)
