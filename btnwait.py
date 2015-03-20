import array
import fcntl
import sys

KEY_ENTER = 28

KEY_MAX = 0x2ff

def EVIOCGKEY(length):
	return 2 << (14+8+8) | length << (8+8) | ord('E') << 8 | 0x18

BUF_LEN = (KEY_MAX + 7) // 8

def test_bit(bit, bytes):
	return not bool(bytes[bit // 8] & 1 << bit % 8)

buf = array.array('B', [0] * BUF_LEN)

while True:
	with open("/dev/input/by-path/platform-gpio-keys.0-event",'r') as fd:
		ret = fcntl.ioctl(fd, EVIOCGKEY(len(buf)), buf)

	if ret < 0:
		print("ioctl error")
		sys.exit(1)

	key_code = KEY_ENTER
	key_state = test_bit(key_code, buf) and "pressed" or "released"
	if key_state == "pressed":
		break

print("Button pressed")
