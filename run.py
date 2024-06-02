import sys
from src.particulate_matter_report import ParticulateMatterReport

DEFAULT_DEVICE_ID = "08BEAC0AB11E"
DEFAULT_PROJECT_NAME = "AirBox"


def main(device_id: str = DEFAULT_DEVICE_ID, project_name: str = DEFAULT_PROJECT_NAME):
    p = ParticulateMatterReport(device_id, project_name)
    p.run_report()


if __name__ == "__main__":
    device_id = DEFAULT_DEVICE_ID
    project_name = DEFAULT_PROJECT_NAME

    if len(sys.argv) > 1:
        device_id = sys.argv[1]

    if len(sys.argv) > 2:
        project_name = sys.argv[2]

    main(device_id, project_name)
