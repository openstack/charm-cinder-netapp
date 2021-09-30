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


import charms_openstack.charm

charms_openstack.charm.use_defaults('charm.default-select-release')


class CinderNetAppCharm(
        charms_openstack.charm.CinderStoragePluginCharm):

    name = 'cinder_netapp'
    version_package = 'cinder-common'
    release = 'ocata'
    packages = []
    release_pkg = 'cinder-common'
    # iscsi is stateful, fibre channel can be either stateful or stateless,
    # nfs is stateless. Regardless, the driver may not cope well with
    # cinder-volume service clustering, so let's allow it to be configurable
    stateless = False
    # Specify any config that the user *must* set.
    mandatory_config = [
        'netapp-storage-family', 'netapp-storage-protocol',
        'netapp-server-hostname', 'volume-backend-name']

    def cinder_configuration(self):
        cget = self.config.get
        service = cget('volume-backend-name')

        # Regardless of stateless or stateful what we really want is whether
        # to configure cinder volume services as a cluster. This can be done
        # in different ways and for different reasons, ideally this
        # variable passed through relation should be renamed.
        self.stateless = cget('cluster-cinder-volume')

        volumedriver = 'cinder.volume.drivers.netapp.common.NetAppDriver'
        driver_options_extension = []
        driver_transport = []
        driver_options_common = [
            ('netapp_storage_family', cget('netapp-storage-family')),
            ('netapp_storage_protocol', cget('netapp-storage-protocol')),
            ('netapp_vserver', cget('netapp-vserver')),
            ('netapp_server_hostname', cget('netapp-server-hostname')),
            ('netapp_server_port', cget('netapp-server-port')),
            ('use_multipath_for_image_xfer', cget('use-multipath')),
            ('netapp_login', cget('netapp-login')),
            ('netapp_password', cget('netapp-password')),
            ('volume_driver', volumedriver),
            ('volume_backend_name', service)]

        if cget('netapp-server-port') == 443:
            driver_transport = [
                ('netapp_transport_type', "https")]

        if cget('netapp-storage-family') == "eseries":
            driver_options_extension = [
                ('netapp_controller_ips', cget('netapp-controller-ips')),
                ('netapp_sa_password', cget('netapp-array-password')),
                ('netapp_storage_pools', cget('netapp-storage-pools')),
                ('use_multipath_for_image_xfer', cget('use-multipath'))]

        if cget('netapp-storage-protocol') == "nfs":
            driver_options_extension += [
                ('nfs_shares_config', cget('netapp-nfs-shares-config'))]

        if cget('netapp-storage-protocol') in ("iscsi", "fc"):
            lun_space_reservation = cget(
                    'netapp-lun-space-reservation')
            lun_space_reservation = 'enabled' if lun_space_reservation is True else 'disabled'
            driver_options_extension += [
                ('netapp_pool_name_search_pattern', cget(
                    'netapp-pool-name-search-pattern')),
                ('netapp_lun_space_reservation', lun_space_reservation)]

        return (driver_options_common + driver_transport +
                driver_options_extension)


class CinderNetAppCharmRocky(CinderNetAppCharm):

    # Ussuri needs py3 packages.
    release = 'rocky'
    version_package = 'cinder-common'
    packages = []
