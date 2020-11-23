import charms_openstack.charm

charms_openstack.charm.use_defaults('charm.default-select-release')


class CinderNetAppCharm(
        charms_openstack.charm.CinderStoragePluginCharm):

    name = 'cinder_netapp'
    version_package = 'cinder-common'
    release = 'ocata'
    packages = []
    release_pkg = 'cinder-common'
    stateless = True
    # Specify any config that the user *must* set.
    mandatory_config = [
        'netapp-storage-family', 'netapp-storage-protocol', 'netapp-server-hostname',
        'volume-backend-name']

    def cinder_configuration(self):
        service = self.config.get('volume-backend-name')
        volumedriver = 'cinder.volume.drivers.netapp.common.NetAppDriver'
        driver_options_extension = []
        driver_options_common = [
            ('netapp_storage_family', self.config.get('netapp-storage-family')),
            ('netapp_storage_protocol', self.config.get('netapp-storage-protocol')),
            ('netapp_vserver', self.config.get('netapp-vserver')),
            ('netapp_server_hostname', self.config.get('netapp-server-hostname')),
            ('netapp_server_port', self.config.get('netapp-server-port')),
            ('netapp_login', self.config.get('netapp-login')),
            ('netapp_password', self.config.get('netapp-password')),
            ('volume_driver', volumedriver),
            ('volume_backend_name', service)]

        if self.config.get('netapp-storage-family') == "eseries":
            driver_options_extension = [
                ('netapp_controller_ips', self.config.get('netapp-controller-ips')),
                ('netapp_sa_password', self.config.get('netapp-array-password')),
                ('netapp_storage_pools', self.config.get('netapp-storage-pools')),
                ('use_multipath_for_image_xfer', self.config.get('use-multipath'))]

        if self.config.get('netapp-storage-protocol') == "nfs":
            driver_options_extension = [
                ('nfs_shares_config', self.config.get('netapp-nfs-shares-config'))]

        return driver_options_common + driver_options_extension


class CinderNetAppCharmRocky(CinderNetAppCharm):

    # Ussuri needs py3 packages.
    release = 'rocky'
    version_package = 'cinder-common'
    packages = []

