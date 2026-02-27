import time
import httpx

SETTINGS_SOCKET = "/run/edge.sock"
SETTINGS_PATH = "webservices/noauth/settings"

SETTING_NAMES = [
    "AudioBalance",
    "AudioMute",
    "AudioVolume",
    "BuildTarget",
    "CPULoad15Minute",
    "CPULoad1Minute",
    "CPULoad5Minute",
    "ConnectedToHub",
    "ControllerCardBarcode",
    "CurrentProcesses",
    "CustomHostname",
    "DeviceTime",
    "DockerFileSystem",
    "DockerPruneLimit",
    "EdgeIotKeepAlive",
    "Enrolled",
    "Enrolling",
    "FamilyName",
    "Fan1Failed",
    "Fan2Failed",
    "FansMinOnTime",
    "FansOffTemp",
    "FansOn",
    "FansOnTemp",
    "FirmwareStatus",
    "FirmwareVersion",
    "Float",
    "FreeDiskSpace",
    "FreeRAM",
    "FreeSpaceOnVar",
    "HDMI_Jack",
    "HeadphoneJack",
    "HostAPMode",
    "IPAddress",
    "InternalCaseTemp",
    "IotedgeVersion",
    "LastTimeSync",
    "MachineID",
    "Manual_DNS_Server1",
    "Manual_DNS_Server2",
    "ManufactureDate",
    "ModelName",
    "NVME_AvailableEOLSpares",
    "NVME_Installed",
    "NVME_LifeTimeUsed",
    "NVME_LifeTimeWrites",
    "NetworkOnline",
    "OEM_ID",
    "PlayerLED",
    "PowerMode",
    "PoweredViaPoE",
    "Provisioned",
    "Provisioning",
    "ProxyAddress",
    "ProxyPassword",
    "ProxyPort",
    "ProxyScheme",
    "ProxyUsername",
    "ScopeId",
    "SerialNumber",
    "SeriesName",
    "SettingsDebugLevel",
    "SettingsPort8080",
    "SkillsRunning",
    "SuspendTopLedCntl",
    "ThermalZone0",
    "ThermalZone1",
    "ThermalZone2",
    "ThermalZone3",
    "ThermalZone4",
    "ThermalZone5",
    "TimeServer",
    "TopLedColor2Default",
    "TopLedColorDefault",
    "TotalDiskSpace",
    "TotalRAM",
    "USBFS_Memory",
    "UptimeInSeconds",
    "WebBrowser",
    "WebBrowserURL",
    "WindowManager",
    "WindowManagerCursor",
    "WindowManagerForceFullScreen",
    "Wired_Aux_IPv4_ManualAddress",
    "Wired_Aux_IPv4_Source",
    "Wired_IPv4_Address",
    "Wired_IPv4_Gateway",
    "Wired_IPv4_ManualAddress",
    "Wired_IPv4_ManualGateway",
    "Wired_IPv4_Source",
    "Wireless_IPv4_Address",
    "Wireless_IPv4_Gateway",
    "Wireless_IPv4_ManualAddress",
    "Wireless_IPv4_ManualGateway",
    "Wireless_IPv4_Source",
    "Wireless_SSID",
    "ZRamEnabled",
    "eMMC_LifeTimeEstTypA",
    "eMMC_LifeTimeEstTypB",
    "eMMC_LifeTimeWritesKB",
    "eMMC_PreEOLInfo",
    "ethaddr",
    "ethaddr2",
    "ethaddr_MFG",
    "wlanaddr",
]


def read_setting(client, base_url, name):
    response = client.get(f"{base_url}/{name}")
    response.raise_for_status()
    return response.json().get(name)


def main():
    transport, base_url = httpx.HTTPTransport(uds=SETTINGS_SOCKET), f"http://x/{SETTINGS_PATH}"
    print(f"Connecting via: {base_url}")

    while True:
        settings = {}
        with httpx.Client(transport=transport) as client:
            for name in SETTING_NAMES:
                try:
                    settings[name] = read_setting(client, base_url, name)
                except Exception as e:
                    settings[name] = f"ERROR: {e}"

        print(f"Settings: {settings}")
        time.sleep(10)


if __name__ == "__main__":
    main()
