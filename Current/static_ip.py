import depthai as dai

(found, info) = dai.DeviceBootloader.getFirstAvailableDevice()

if found:
    print(f'Found device with name: {info.name}')
    print('-------------------------------------')

    with dai.DeviceBootloader(info) as bl:
        ipv4 = "192.168.1.200"
        mask = "255.255.255.0"
        gateway = "192.168.1.1"

        conf = dai.DeviceBootloader.Config()
        conf.setStaticIPv4(ipv4, mask, gateway)
        (success, error) = bl.flashConfig(conf)

        if not success:
            print(f"Flashing failed: {error}")
        else:
            print(f"Flashing successful.")
