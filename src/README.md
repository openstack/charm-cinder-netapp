# Overview

The cinder charm is the Openstack block storage (i.e: Volume) service, whereas the cinder-netapp charm works as a subordinate of cinder, implementing a backend based on NetApp.

> **Note**: The cinder-netapp charm is supported starting with Openstack Queens.

# Usage

## Configuration

This section covers common and/or important configuration options. See file `config.yaml` for the full list of options, along with their descriptions and default values. See the [Juju documentation][juju-docs-config-apps] for details on configuring applications.

### `netapp-storage-family`

The storage family type that is used for the storage system. Can be `ontap_cluster` for clustering data ONTAP, or `eseries`.

### `netapp-storage-protocol`

The SAN protocol to use. Can be either `iscsi` or `NFS`.

### `netapp-vserver`

Specifies the virtual storage server name on the storage cluster.

### `netapp-server-hostname`

The hostname or IP address for the storage server (can alternatively specify a proxy server).

### `netapp-server-port`

The TCP port used to communicate with the storage server or proxy.

If it's not specified, it will be deduced: For ONTAP drivers, it will be 80 for HTTP and 443 for HTTPS; for E-series, it will be 8080 and 8443, respectively.

### `netapp-login`

The username used to access the storage server or proxy.

### `netapp-password`

The password used to authenticate the `login` option.

### `netapp-nfs-shares-config`

Specifies a file that contains a list of NFS shares, each on its own line, to which the driver will attempt to provision
Cinder volumes.

### `netapp-controller-ips`

If the storage family is `eseries`, this option specifies a comma-separated list of controller hostnames or IP addresses
to be used for provisioning.

### `netapp-array-password`

The password for the NetApp E-series storage array.

### `netapp-storage-pools`

Specifies a comma-separated list of pool names to use.

### `use-multipath`

Whether to use multipath for image transfer.

### `netapp-enable-multiattach`

Specifies whether the driver should allow operations that involve multiple attachments to a volume.

### `volume-backend-name`

The service name to present to Cinder.

## Deployment

This charm's primary use is as a backend for the cinder charm. To do so, add a relation betweeen both charms:

    juju add-relation cinder-netapp:storage-backend cinder:storage-backend

# Documentation

The OpenStack Charms project maintains two documentation guides:

* [OpenStack Charm Guide][cg]: for project information, including development
  and support notes
* [OpenStack Charms Deployment Guide][cdg]: for charm usage information

# Bugs

Please report bugs on [Launchpad][lp-bugs-charm-cinder-netapp].

[cg]: https://docs.openstack.org/charm-guide
[cdg]: https://docs.openstack.org/project-deploy-guide/charm-deployment-guide
[lp-bugs-charm-cinder-netapp]: https://bugs.launchpad.net/charm-cinder-netapp/+filebug
