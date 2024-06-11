import pytest

import json


@pytest.mark.parametrize(
    "name",
    [
        ("elasticsearch"),
    ],
)
def test_packages_are_installed(host, name):
    package = host.package(name)
    assert package.is_installed


@pytest.mark.parametrize(
    "username,groupname,path",
    [
        ("root", "root", "/etc/elasticsearch/elasticsearch.yml"),
        ("root", "root", "/etc/elasticsearch/log4j2.properties"),
        ("root", "root", "/etc/elasticsearch/jvm.options"),
    ],
)
def test_elasticsearch_config_file(host, username, groupname, path):
    config = host.file(path)
    assert config.exists
    assert config.is_file
    assert config.user == username
    assert config.group == groupname


@pytest.mark.parametrize(
    "name",
    [
        ("elasticsearch"),
    ],
)
def test_service_is_running_and_enabled(host, name):
    service = host.service(name)
    assert service.is_enabled
    assert service.is_running


@pytest.mark.parametrize(
    "user,password",
    [
        ("elastic", "changeme"),
    ],
)
def test_cluster_health(host, user, password):
    command = f"curl -q -u {user}:{password} " f"http://127.0.0.1:9200/_cluster/health"
    output = host.run(command)
    if output.exit_status != 0:
        pytest.fail("Failed to reach ES API")
    data = json.loads(output.stdout)
    assert data["status"] == "green"


@pytest.mark.parametrize(
    "user,password,indice",
    [
        ("elastic", "changeme", "test-molecule"),
    ],
)
def test_indices_exist(host, user, password, indice):
    command = (
        f"curl -q -u {user}:{password} "
        f"http://127.0.0.1:9200/_cat/indices/{indice}?format=json"
    )
    output = host.run(command)
    if output.exit_status != 0:
        pytest.fail("Failed to reach ES API")
    data = json.loads(output.stdout)
    assert data[0]["health"] == "green"
    assert data[0]["status"] == "open"


@pytest.mark.parametrize(
    "plugin",
    [
        ("discovery-ec2"),
    ],
)
def test_plugins_exist(host, plugin):
    output = host.run("/usr/share/elasticsearch/bin/elasticsearch-plugin list")
    if output.exit_status != 0:
        pytest.fail("Failed to list ES plugins")
    assert plugin in output.stdout


@pytest.mark.parametrize(
    "entry",
    [
        ("s3.client.default.access_key"),
        ("s3.client.default.secret_key"),
    ],
)
def test_keystore_entries(host, entry):
    command = "/usr/share/elasticsearch/bin/elasticsearch-keystore list"
    output = host.run(command)
    if output.exit_status != 0:
        pytest.fail("Failed to list ES keystore entries")
    assert entry in output.stdout


@pytest.mark.parametrize(
    "user,roles",
    [
        ("molecule-user-1", "superuser,custom-role-1"),
        ("molecule-user-2", "custom-role-1"),
    ],
)
def test_users(host, user, roles):
    command = f"/usr/share/elasticsearch/bin/elasticsearch-users roles {user}"
    output = host.run(command)
    if output.exit_status != 0:
        pytest.fail("Failed to list ES users")
    assert user in output.stdout
    assert roles in output.stdout


@pytest.mark.parametrize(
    "user,password,template",
    [
        ("elastic", "changeme", "common"),
    ],
)
def test_component_templates_exist(host, user, password, template):
    command = (
        f"curl -q -u {user}:{password} "
        f"http://127.0.0.1:9200/_component_template/{template}"
    )
    output = host.run(command)
    if output.exit_status != 0:
        pytest.fail("Failed to reach ES API")
    data = json.loads(output.stdout)
    print(data)
    assert data["component_templates"][0]["name"] == template


@pytest.mark.parametrize(
    "user,password,template",
    [
        ("elastic", "changeme", "test-molecule"),
    ],
)
def test_composable_index_templates_exist(host, user, password, template):
    command = (
        f"curl -q -u {user}:{password} "
        f"http://127.0.0.1:9200/_index_template/{template}"
    )
    output = host.run(command)
    if output.exit_status != 0:
        pytest.fail("Failed to reach ES API")
    data = json.loads(output.stdout)
    print(data)
    assert data["index_templates"][0]["name"] == template


@pytest.mark.parametrize(
    "user,password,repository",
    [
        ("elastic", "changeme", "backup"),
    ],
)
def test_snapshot_repositories(host, user, password, repository):
    command = (
        f"curl -q -u {user}:{password} " f"http://127.0.0.1:9200/_snapshot/{repository}"
    )
    output = host.run(command)
    if output.exit_status != 0:
        pytest.fail("Failed to reach ES API")
    data = json.loads(output.stdout)
    assert repository in data
