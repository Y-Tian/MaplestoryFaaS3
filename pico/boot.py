import usb_cdc


# Use the standard console CDC serial port as the command channel.
# This gives the host one stable COM port plus USB HID keyboard output.
usb_cdc.enable(console=True, data=False)
