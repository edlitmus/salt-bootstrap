#!/usr/bin/env python3
import datetime
import json
import os
import pathlib

os.chdir(os.path.abspath(os.path.dirname(__file__)))

# only test against current containers with systemd
# will add these when they become available with systemd
#    "amazonlinux-2",
#    "amazonlinux-2023",
#    "debian-11",
#    "debian-12",
#    "debian-13",
#    "fedora-40",
#    "photon-4",
#    "ubuntu-2004",
#    "ubuntu-2404",
LINUX_DISTROS = [
    "debian-12",
    "photon-5",
    "rockylinux-8",
    "rockylinux-9",
    "ubuntu-2204",
]

WINDOWS = [
    "windows-2022",
]

OSX = [
    "macos-12",
    "macos-13",
    "macos-14",
]

# only test against current containers with systemd
# will add these when they become available with systemd
#    "amazonlinux-2",
#    "amazonlinux-2023",
#    "debian-11",
#    "debian-13",
#    "fedora-40",
#    "photon-4",
#    "ubuntu-2004",
#    "ubuntu-2404",
STABLE_DISTROS = [
    "debian-12",
    "photon-5",
    "rockylinux-8",
    "rockylinux-9",
    "ubuntu-2204",
]

# only test against current containers with systemd
# will add these when they become available with systemd
#    "amazonlinux-2",
#    "amazonlinux-2023",
#    "debian-11",
#    "debian-13",
#    "fedora-40",
#    "photon-4",
#    "ubuntu-2004",
#    "ubuntu-2404",
ONEDIR_DISTROS = [
    "debian-12",
    "photon-5",
    "rockylinux-8",
    "rockylinux-9",
    "ubuntu-2204",
]

# only test against current containers with systemd
# will add these when they become available with systemd
#    "amazonlinux-2",
#    "amazonlinux-2023",
#    "photon-4",
#    "photon-5",
#    "rockylinux-8",
#    "ubuntu-2404",
ONEDIR_RC_DISTROS = [
    "debian-12",
    "photon-5",
    "rockylinux-9",
    "ubuntu-2204",
]

BLACKLIST_3006 = [
    "debian-12",
    "fedora-40",
    "ubuntu-2404",
]

BLACKLIST_3007 = [
    "photon-4",
    "photon-5",
]

#    "debian-12",
#    "rockylinux-9",
#    "ubuntu-2204",
BLACKLIST_GIT_3006 = [
    "amazonlinux-2",
    "amazonlinux-2023",
    "debian-11",
    "fedora-40",
    "photon-4",
    "photon-5",
    "ubuntu-2004",
    "ubuntu-2404",
]

#    "debian-12",
#    "rockylinux-9",
#    "ubuntu-2204",
BLACKLIST_GIT_3007 = [
    "amazonlinux-2",
    "amazonlinux-2023",
    "debian-11",
    "debian-13",
    "fedora-40",
    "photon-4",
    "photon-5",
    "ubuntu-2004",
    "ubuntu-2404",
]

##    "rockylinux-9",
BLACKLIST_GIT_MASTER = [
    "amazonlinux-2",
    "amazonlinux-2023",
    "debian-11",
    "debian-13",
    "fedora-40",
    "photon-4",
    "photon-5",
]

SALT_VERSIONS = [
    "3006",
    "3006-8",
    "3007",
    "3007-1",
    "master",
    "latest",
    "nightly",
]

ONEDIR_SALT_VERSIONS = [
    "3006",
    "3007",
    "latest",
]

ONEDIR_RC_SALT_VERSIONS = []

VERSION_DISPLAY_NAMES = {
    "3006": "v3006",
    "3006-8": "v3006.8",
    "3007": "v3007",
    "3007-1": "v3007.1",
    "master": "Master",
    "latest": "Latest",
    "nightly": "Nightly",
}

STABLE_VERSION_BLACKLIST = [
    "master",
    "nightly",
]

MAC_STABLE_VERSION_BLACKLIST = [
    "master",
    "nightly",
]

GIT_VERSION_BLACKLIST = [
    "3006-8",
    "3007-1",
    "nightly",
]

# TODO: Revert the commit relating to this section, once the Git-based builds
#       have been fixed for the distros listed below
#
#       Apparent failure is:
#
#           /usr/lib/python3.11/site-packages/setuptools/command/install.py:34:
#           SetuptoolsDeprecationWarning: setup.py install is deprecated.
#           Use build and pip and other standards-based tools.
#
GIT_DISTRO_BLACKLIST = [
    "rockylinux-8",
]

LATEST_PKG_BLACKLIST = []

DISTRO_DISPLAY_NAMES = {
    "amazonlinux-2": "Amazon 2",
    "amazonlinux-2023": "Amazon 2023",
    "debian-11": "Debian 11",
    "debian-12": "Debian 12",
    "debian-13": "Debian 13",
    "fedora-40": "Fedora 40",
    "photon-4": "Photon OS 4",
    "photon-5": "Photon OS 5",
    "rockylinux-8": "Rocky Linux 8",
    "rockylinux-9": "Rocky Linux 9",
    "ubuntu-2004": "Ubuntu 20.04",
    "ubuntu-2204": "Ubuntu 22.04",
    "ubuntu-2404": "Ubuntu 24.04",
    "macos-12": "macOS 12",
    "macos-13": "macOS 13",
    "macos-14": "macOS 14",
    "windows-2022": "Windows 2022",
}

CONTAINER_SLUG_NAMES = {
    "amazonlinux-2": "systemd-amazonlinux-2",
    "amazonlinux-2023": "systemd-amazonlinux-2023",
    "debian-11": "systemd-debian-11",
    "debian-12": "systemd-debian-12",
    "debian-13": "systemd-debian-13",
    "fedora-40": "systemd-fedora-40",
    "photon-4": "systemd-photon-4",
    "photon-5": "systemd-photon-5",
    "rockylinux-8": "systemd-rockylinux-8",
    "rockylinux-9": "systemd-rockylinux-9",
    "ubuntu-2004": "systemd-ubuntu-20.04",
    "ubuntu-2204": "systemd-ubuntu-22.04",
    "ubuntu-2404": "systemd-ubuntu-24.04",
    "macos-12": "macos-12",
    "macos-13": "macos-13",
    "macos-14": "macOS 14",
    "windows-2022": "windows-2022",
}

TIMEOUT_DEFAULT = 20
TIMEOUT_OVERRIDES = {}
VERSION_ONLY_OVERRIDES = []

TEMPLATE = """
  {distro}:
    name: {display_name}{ifcheck}
    uses: {uses}
    needs:
      - lint
      - generate-actions-workflow
    with:
      distro-slug: {distro}
      display-name: {display_name}
      container-slug: {container_name}
      timeout: {timeout_minutes}{runs_on}
      instances: '{instances}'
"""


def generate_test_jobs():
    test_jobs = ""
    needs = ["lint", "generate-actions-workflow"]

    test_jobs += "\n"
    for distro in OSX:
        test_jobs += "\n"
        runs_on = distro
        runs_on = f"\n      runs-on: {runs_on}"
        ifcheck = "\n    if: github.event_name == 'push' || needs.collect-changed-files.outputs.run-tests == 'true'"
        uses = "./.github/workflows/test-macos.yml"
        instances = []
        timeout_minutes = (
            TIMEOUT_OVERRIDES[distro]
            if distro in TIMEOUT_OVERRIDES
            else TIMEOUT_DEFAULT
        )

        for salt_version in SALT_VERSIONS:
            if salt_version == "latest":
                instances.append(salt_version)
                continue

            for bootstrap_type in ["stable"]:
                if bootstrap_type == "stable":
                    if salt_version in MAC_STABLE_VERSION_BLACKLIST:
                        continue

                test_target = f"{bootstrap_type}-{salt_version}"
                instances.append(test_target)

        for bootstrap_type in ["default"]:
            if distro not in STABLE_DISTROS:
                continue
            instances.append(bootstrap_type)

        if instances:
            needs.append(distro)
            test_jobs += TEMPLATE.format(
                distro=distro,
                runs_on=runs_on,
                uses=uses,
                ifcheck=ifcheck,
                instances=json.dumps(instances),
                display_name=DISTRO_DISPLAY_NAMES[distro],
                container_name=CONTAINER_SLUG_NAMES[distro],
                timeout_minutes=timeout_minutes,
            )

    test_jobs += "\n"
    for distro in WINDOWS:
        test_jobs += "\n"
        runs_on = f"\n      runs-on: {distro}"
        ifcheck = "\n    if: github.event_name == 'push' || needs.collect-changed-files.outputs.run-tests == 'true'"
        uses = "./.github/workflows/test-windows.yml"
        instances = []
        timeout_minutes = (
            TIMEOUT_OVERRIDES[distro]
            if distro in TIMEOUT_OVERRIDES
            else TIMEOUT_DEFAULT
        )

        for salt_version in SALT_VERSIONS:

            if salt_version == "latest":

                instances.append(salt_version)
                continue

            for bootstrap_type in ["stable"]:
                if bootstrap_type == "stable":
                    if salt_version in STABLE_VERSION_BLACKLIST:
                        continue

                test_target = f"{bootstrap_type}-{salt_version}"
                instances.append(test_target)

        for bootstrap_type in ["default"]:
            if distro not in STABLE_DISTROS:
                continue
            instances.append(bootstrap_type)

        if instances:
            needs.append(distro)
            test_jobs += TEMPLATE.format(
                distro=distro,
                runs_on=runs_on,
                uses=uses,
                ifcheck=ifcheck,
                instances=json.dumps(instances),
                display_name=DISTRO_DISPLAY_NAMES[distro],
                container_name=CONTAINER_SLUG_NAMES[distro],
                timeout_minutes=timeout_minutes,
            )

    test_jobs += "\n"
    for distro in LINUX_DISTROS:
        test_jobs += "\n"
        runs_on = ""
        ifcheck = "\n    if: github.event_name == 'push' || needs.collect-changed-files.outputs.run-tests == 'true'"
        uses = "./.github/workflows/test-linux.yml"
        instances = []
        timeout_minutes = (
            TIMEOUT_OVERRIDES[distro]
            if distro in TIMEOUT_OVERRIDES
            else TIMEOUT_DEFAULT
        )
        if distro in VERSION_ONLY_OVERRIDES:
            ifcheck = "\n    if: github.event_name == 'push'"

        for salt_version in SALT_VERSIONS:

            if salt_version == "latest":
                if distro in LATEST_PKG_BLACKLIST:
                    continue

                instances.append(salt_version)
                continue

            for bootstrap_type in (
                "stable",
                "git",
                "onedir",
                "onedir-rc",
            ):
                if bootstrap_type == "onedir":
                    if salt_version not in ONEDIR_SALT_VERSIONS:
                        continue
                    if distro not in ONEDIR_DISTROS:
                        continue

                if bootstrap_type == "onedir-rc":
                    if salt_version not in ONEDIR_RC_SALT_VERSIONS:
                        continue
                    if distro not in ONEDIR_RC_DISTROS:
                        continue

                if bootstrap_type == "stable":
                    if salt_version in STABLE_VERSION_BLACKLIST:
                        continue
                    if distro not in STABLE_DISTROS:
                        continue

                if bootstrap_type == "git":
                    if salt_version in GIT_VERSION_BLACKLIST:
                        continue
                    if distro in GIT_DISTRO_BLACKLIST:
                        continue

                BLACKLIST = {
                    "3006": BLACKLIST_3006,
                    "3006-8": BLACKLIST_3006,
                    "3007": BLACKLIST_3007,
                    "3007-1": BLACKLIST_3007,
                }
                if bootstrap_type == "git":
                    BLACKLIST = {
                        "3006": BLACKLIST_GIT_3006,
                        "3007": BLACKLIST_GIT_3007,
                        "master": BLACKLIST_GIT_MASTER,
                    }

                    # .0 versions are a virtual version for pinning to the first
                    # point release of a major release, such as 3003,
                    # there is no git version.
                    if salt_version.endswith("-0"):
                        continue

                if (
                    salt_version in ("3006", "3006-8", "3007", "3007-1", "master")
                    and distro in BLACKLIST[salt_version]
                ):
                    continue

                test_target = f"{bootstrap_type}-{salt_version}"
                instances.append(test_target)

        for bootstrap_type in ["default"]:
            if distro not in STABLE_DISTROS:
                continue
            instances.append(bootstrap_type)

        if instances:
            needs.append(distro)
            test_jobs += TEMPLATE.format(
                distro=distro,
                runs_on=runs_on,
                uses=uses,
                ifcheck=ifcheck,
                instances=json.dumps(instances),
                display_name=DISTRO_DISPLAY_NAMES[distro],
                container_name=CONTAINER_SLUG_NAMES[distro],
                timeout_minutes=timeout_minutes,
            )

    ci_src_workflow = pathlib.Path("ci.yml").resolve()
    ci_tail_src_workflow = pathlib.Path("ci-tail.yml").resolve()
    ci_dst_workflow = pathlib.Path("../ci.yml").resolve()
    ci_workflow_contents = ci_src_workflow.read_text() + test_jobs + "\n"
    ci_workflow_contents += ci_tail_src_workflow.read_text().format(
        needs="\n".join([f"      - {need}" for need in needs]).lstrip()
    )
    ci_dst_workflow.write_text(ci_workflow_contents)


if __name__ == "__main__":
    generate_test_jobs()
