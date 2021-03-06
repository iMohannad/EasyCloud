#!/bin/bash

echo "deb http://downloads.opennebula.org/repo/4.12/Ubuntu/14.04 stable opennebula" > /etc/apt/sources.list.d/opennebula.list

apt-get update

apt-get install opennebula opennebula-sunstone nfs-kernel-server  -y --force-yes

sed -i '31s/.*/:host: 0.0.0.0/' /etc/one/sunstone-server.conf

/etc/init.d/opennebula-sunstone restart

cat << EOT > /etc/exports 
/var/lib/one/ *(rw,sync,no_subtree_check,root_squash)
EOT

service nfs-kernel-server restart

#su - oneadmin
cp /var/lib/one/.ssh/id_rsa.pub /var/lib/one/.ssh/authorized_keys



service opennebula restart


/etc/init.d/opennebula-sunstone restart



