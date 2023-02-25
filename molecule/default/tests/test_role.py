import pytest

import os

import testinfra.utils.ansible_runner

import requests

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize('name', [
  ('elasticsearch'),
])
def test_packages_are_installed(host, name):
    package = host.package(name)
    assert package.is_installed


@pytest.mark.parametrize('username,groupname,path', [
  ('root', 'root', '/etc/elasticsearch/elasticsearch.yml'),
  ('root', 'root', '/etc/elasticsearch/log4j2.properties'),
  ('root', 'root', '/etc/elasticsearch/jvm.options'),
])
def test_elasticsearch_config_file(host, username, groupname, path):
    config = host.file(path)
    assert config.exists
    assert config.is_file
    assert config.user == username
    assert config.group == groupname


@pytest.mark.parametrize('name', [
  ('elasticsearch'),
])
def test_service_is_running_and_enabled(host, name):
    service = host.service(name)
    assert service.is_enabled
    assert service.is_running


@pytest.mark.parametrize('endpoint,user,password', [
  ('http://127.0.0.1:9200/_cluster/health', 'elastic', 'changeme'),
])
def test_cluster_health(endpoint, user, password):
    response = requests.get(endpoint, auth=(user, password))
    data = response.json()
    assert data['status'] == 'green'
