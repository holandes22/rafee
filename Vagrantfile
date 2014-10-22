# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "trusty64"
  config.vm.box_url = "http://cloud-images.ubuntu.com/vagrant/trusty/current/trusty-server-cloudimg-amd64-vagrant-disk1.box"
  config.vm.boot_timeout = 120

  config.vm.network :forwarded_port, guest: 8000, host: 8888
  config.vm.network :forwarded_port, guest: 9001, host: 9002

  config.vm.provider :virtualbox do |vb|
    vb.name = "rafee"
  end

  config.vm.provision :ansible, run: "always" do |ansible|
      ansible.playbook = "provisioning/playbook.yml"
      ansible.sudo = true
      ansible.host_key_checking = false
  end

end
