# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"


Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "utopic64"
  config.vm.box_url = "http://cloud-images.ubuntu.com/vagrant/utopic/current/utopic-server-cloudimg-amd64-vagrant-disk1.box"
  config.vm.boot_timeout = 120

  config.vm.network :forwarded_port, guest: 8000, host: 8888 # Backend
  config.vm.network :forwarded_port, guest: 9001, host: 9002 # Supervisor
  config.vm.network :forwarded_port, guest: 4200, host: 4201 # Frontend
  config.vm.network :forwarded_port, guest: 5555, host: 5556 # Flower (Celery)

  config.vm.provider :virtualbox do |vb|
    vb.name = "rafee"
  end

  config.vm.provision :ansible do |ansible|
      ansible.playbook = "provisioning/site.yml"
      ansible.sudo = true
      ansible.limit = "vagrant"
      ansible.inventory_path = "provisioning/inventory"
      # ansible.verbose = "vvvv"
  end

end
