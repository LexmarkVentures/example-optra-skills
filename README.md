# Optra Edge Development Documents

## What is Optra

Optra is a comprehensive edge computing platform. It consists of custom Optra hardware running a read-only firmware stack on Ubuntu, designed to manage containerized applications—referred to as skills. These skills are deployed and monitored via a web-based portal, which also supports firmware updates and device management.

Unlike typical edge development environments like desktops or Jetson devices, Optra devices are locked down: there's no SSH access, all application code must run in a container, and development is not done directly on the device. This design simplifies secure, large-scale deployment of edge applications.

## Getting Started

1. [The Optra Portal](docs/optra-portal.md)
2. [Skill Configuration](docs/skills.md)
3. [Example skills](examples/README.md)

## Advanced

* [Building GPU Enabled VZ Images](docs/building-gpu-enabled-vz-images.md) - read before running machine learning models or graphics accelerated code
* [Developer Notes](docs/developer-notes.md) - info for devs
* [Control Panel](docs/control-panel.md) - for network and wifi info