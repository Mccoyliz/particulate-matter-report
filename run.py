from src.particulate_matter_report import ParticulateMatterReport

DEVICE_ID = "08BEAC0AB11E"

p = ParticulateMatterReport(DEVICE_ID)
p.run_report()
