initRetryTimesLimit = 3

COM_PORT_1 = "/dev/ttyUSB0"
COM_PORT_2 = "/dev/ttyUSB1"

COM_BAUD = 9600

LOG_LEVEL = "NOTIFY,DEBUG,ERROR"

INIT_CMD = "@\r\n"
SHOW_MSG_CMD = "D \"%S\"\r\n"
SHOW_DEFAULT_CMD = "DW\r\n"
WEIGHT_CMD = "SI\r\n"
TARE_CMD="TA\r\n"

DB_SPEC = ["localhost","3306","root","","serialdata"]


SAMPLE_INTERVAL = 10
ENABLED = False
RUNNING = False
CURRENT_SESSION = None
