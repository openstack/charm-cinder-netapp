import charms_openstack.charm

charms_openstack.charm.use_defaults('charm.default-select-release')


class CindernetappCharm(
        charms_openstack.charm.CinderStoragePluginCharm):

    name = 'cinder_netapp'
    release = 'stein'
    stateless = True
    version_package = 'cinder-common'
    packages = []
    # Specify any config that the user *must* set.
    mandatory_config = [
        'netapp_storage_family', 'netapp_storage_protocol', 'netapp_server_hostname',
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
            ('netapp_server_port', self.config.get('netapp-vserver-port')),
            ('netapp_login', self.config.get('netapp-login')),
            ('netapp_password', self.config.get('netapp-password')),
            ('netapp_lun_space_reservation', self.config.get('netapp-lun-space-reservation')),
            ('netapp_transport_type', self.config.get('netapp-transport-type')),
            ('volume_driver', volumedriver),
            ('volume_backend_name', service)]

        if self.config.get('netapp-storage-family') == "eseries":
            driver_options_extension = [
                ('netapp_controller_ips', self.config.get('netapp-controller-ips')),
                ('netapp_sa_password', self.config.get('netapp-array-password')),
                ('netapp_storage_pools', self.config.get('netapp-storage-pools')),
                ('use_multipath_for_image_xfer', self.config.get('use-multipath'))]

        return driver_options_common + driver_options_extension


class CindernetappCharmRocky(CindernetappCharm):

    # Rocky needs py3 packages.
    release = 'rocky'
    version_package = 'cinder-common'
    packages = []

