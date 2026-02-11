[![tests](https://github.com/boutetnico/ansible-role-elasticsearch/workflows/Test%20ansible%20role/badge.svg)](https://github.com/boutetnico/ansible-role-elasticsearch/actions?query=workflow%3A%22Test+ansible+role%22)
[![Ansible Galaxy](https://img.shields.io/badge/galaxy-boutetnico.elasticsearch-blue.svg)](https://galaxy.ansible.com/boutetnico/elasticsearch)

ansible-role-elasticsearch
==========================

This role installs and configures [ElasticSearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html).

Requirements
------------

Ansible 2.15 or newer.

Supported Platforms
-------------------

- [Debian - 12 (Bookworm)](https://wiki.debian.org/DebianBookworm)
- [Debian - 13 (Trixie)](https://wiki.debian.org/DebianTrixie)
- [Ubuntu - 22.04 (Jammy Jellyfish)](http://releases.ubuntu.com/22.04/)
- [Ubuntu - 24.04 (Noble Numbat)](http://releases.ubuntu.com/24.04/)

Role Variables
--------------

| Variable                          | Required | Default                         | Choices   | Comments                                       |
|-----------------------------------|----------|---------------------------------|-----------|------------------------------------------------|
| es_dependencies                   | true     |                                 | list      | See `defaults/main.yml`.                       |
| es_package_state                  | true     | `present`                       | string    | Use `latest` to upgrade ElasticSearch.         |
| es_user                           | true     | `elasticsearch`                 | string    |                                                |
| es_group                          | true     | `elasticsearch`                 | string    |                                                |
| es_network_host                   | true     | `0.0.0.0`                       | string    |                                                |
| es_http_port                      | true     | `9200`                          | int       |                                                |
| es_path_data                      | true     | `/var/lib/elasticsearch`        | string    |                                                |
| es_path_logs                      | true     | `/var/log/elasticsearch`        | string    |                                                |
| es_config                         | true     | `{}`                            | dict      |                                                |
| es_api_basic_auth_username        | true     | `elastic`                       | string    |                                                |
| es_api_basic_auth_password        | true     | `changeme`                      | string    |                                                |
| es_log4j2_template                | true     | `log4j2.properties.j2`          | string    |                                                |
| es_jvm_heap_size                  | true     | `1g`                            | string    |                                                |
| es_indices                        | true     | `[]`                            | list      | Indices to create.                             |
| es_plugins                        | true     | `[]`                            | list      | Plugins to install.                            |
| es_keystore_entries               | true     | `[]`                            | list      |                                                |
| es_users                          | true     | `{}`                            | dict      |                                                |
| es_roles                          | true     | `{}`                            | dict      |                                                |
| es_component_templates_fileglob   | true     | `""`                            | string    | Path to component index templates to install.  |
| es_index_templates_fileglob       | true     | `""`                            | string    | Path to composable index templates to install. |
| es_snapshot_repositories_fileglob | true     | `""`                            | string    |                                                |
| es_systemd_override               | true     |                                 | dict      | See `defaults/main.yml`.                       |

Dependencies
------------

Java 8+ or equivalent. For testing this roles uses `default-jre-headless` package.

Example Playbook
----------------

    - hosts: all
      roles:
        - role: ansible-role-elasticsearch

Testing
-------

    molecule test

License
-------

MIT

Author Information
------------------

[@boutetnico](https://github.com/boutetnico)
