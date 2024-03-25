import os
import csv
import json
import subprocess
from reportlab.lib.pagesizes import mm
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import Paragraph
from pystrich.datamatrix import DataMatrixEncoder
from pprint import pprint as pp


QR_CODE = '/Volumes/Repo/storage-tests/atp/inventory/temp/qrcode.png'

#Generate configuration info from SPUSBDataType (BOT and UAS)
def getUSBDriveData(driveType):
    os.system('system_profiler SPUSBDataType -json > /Volumes/Repo/storage-tests/atp/inventory/temp/driveProf.json')
    with open ('/Volumes/Repo/storage-tests/atp/inventory/temp/driveProf.json', "r") as dr :
        driveData = json.load(dr)   
    for item in driveData['SPUSBDataType']:
        if "_items" in item:
            drive = item["_items"]
            if "Media" in drive[0]:
                stats = drive[0]

    name = stats["_name"]
    size = stats['Media'][0]["size"]
    serial = stats['serial_num']
    vendor = stats['manufacturer']
    product_id = stats['product_id']
    vendor_id = stats['vendor_id']

    configuration = f'Type: {driveType}; \nName: {name}; \nSize: {size}; \nVendor: {vendor}; \nSerial #: {serial}; \nProduct ID: {product_id}; \nVendor ID: {vendor_id}'
    configList = ["\nAdd to TSTT", name + " - " + size, driveType, str(configuration), "0\n"]
    
    return configList


#Generate configuration info from SPNVMeDataType (NVME)
def getNVMeDriveData(driveType):
    os.system('system_profiler SPNVMeDataType -json > Volumes/Repo/storage-tests/atp/inventory/temp/driveProf.json')
    with open ('Volumes/Repo/storage-tests/atp/inventory/temp/driveProf.json', "r") as dr :
        driveData = json.load(dr)
    for item in driveData['SPNVMeDataType']:
        drive = item['_items']
        if drive[0]['bsd_name'] == 'disk0':
            pass
        else:
            stats = drive[0]
    
    name = stats['_name']
    size = stats['size']
    serial = stats['device_serial']
    speed = stats['spnvme_linkspeed']

    configuration = f'Type: {driveType}; \nName: {name}; \nSize: {size}; \nSerial #: {serial}; \nLink Speed: {speed}'
    configList = ["\nAdd to TSTT" , name + " - " + size, driveType, str(configuration), "0\n"]
    print(configList)
    return configList


#Generate configuration info from SPSerialATADataType (AHCI)
def getAHCIDriveData(driveType):
  os.system('system_profiler SPSerialATADataType -json > /Volumes/Repo/storage-tests/atp/inventory/temp/driveProf.json')
  with open ('/Volumes/Repo/storage-tests/atp/inventory/temp/driveProf.json', "r") as dr :
    driveData = json.load(dr)
  device = driveData['SPSerialATADataType'][0]['_items']
  for item in device:
    name = item['_name']
    size = item['size']
    serial = item['device_serial']

  if "ST100" in name:
    name = "Buffalo MiniStation Thunderbolt"

  configuration = f'Type: {driveType}; \nName: {name}; \nSize: {size}; \nSerial: {serial}'
  configList = ["\nAdd to TSTT", name + '-' + size, driveType, str(configuration), "0\n"]

  return configList

# Create label for external drive. TSTT resource must be created and # provided
def create_label(name, TSTT, driveType, destination):
    pdfmetrics.registerFont(TTFont('sf-mono-regular', '/Volumes/Repo/storage-tests/atp/inventory/temp/fonts/sf-mono_regular.ttf'))
    pdfmetrics.registerFont(TTFont('sf-mono-light', '/Volumes/Repo/storage-tests/atp/inventory/temp/fonts/sf-mono_light.ttf'))
    pdfmetrics.registerFont(TTFont('sf-mono-medium', '/Volumes/Repo/storage-tests/atp/inventory/temp/fonts/sf-mono_medium.ttf'))
    pdfmetrics.registerFont(TTFont('sf-mono-heavy', '/Volumes/Repo/storage-tests/atp/inventory/temp/fonts/sf-mono_heavy.ttf'))
    pdfmetrics.registerFont(TTFont('sf-mono-semibold', '/Volumes/Repo/storage-tests/atp/inventory/temp/fonts/sf-mono_semibold.ttf'))
    pdfmetrics.registerFont(TTFont('sf-mono-bold', '/Volumes/Repo/storage-tests/atp/inventory/temp/fonts/sf-mono_bold.ttf'))

    width = 53.975
    height = 25.4

    c = canvas.Canvas(destination, pagesize=(width*mm, height*mm))

    styles = getSampleStyleSheet()
    normal_style = styles["Normal"]

    c.setFillColor(colors.white)
    c.rect(0, 0, width*mm, height*mm, stroke= 0,fill=True)

    name_style = ParagraphStyle("name_style",
        parent=normal_style,
        fontName="sf-mono-semibold",
        fontSize=10,
        alignment=1,  # Center alignment
        border = 0
    )
    # Draw the drive name
    name_paragraph = Paragraph(name, name_style)
    name_paragraph.wrapOn(c, width*mm-10, (height*mm/2)-4)
    name_paragraph.drawOn(c, 5, (height*mm/2)-15)

    # Draw the rdar://res/######
    c.setFont("sf-mono-bold", 8)
    c.setFillColor(colors.black)
    c.drawCentredString((width*mm/2)+10, height*mm-20, TSTT)

    # Draw the drive type
    c.setFont("sf-mono-bold", 11)
    c.setFillColor(colors.black)
    c.drawRightString(width*mm-20, 5, driveType)

    c.setFont("sf-mono-semibold", 6)
    c.setFillColor(colors.black)
    c.drawRightString(width, 5, "MSQA 2023")
    
    # Draw scannable QR code link to resource
    qr_encoder = DataMatrixEncoder(TSTT)
    qr_encoder.save(QR_CODE)
    c.drawImage(QR_CODE, 5, height*mm-35, width=30, height=30)

    c.save()
    print_pdf(destination)

def print_pdf(label):
        try:
            printers = subprocess.run(['lpstat', '-p'], capture_output=True)
            if 'DYMO' in printers.stdout.decode():
                    sp = subprocess.run(['/usr/bin/automator', '-i', label, 'print_label.workflow'], capture_output=True)
                    pp(sp)
        except Exception as e:
            print(e)


#Parse through ioreg to determine the type of drive and call necessary command
def getDriveInfo():
    os.system('ioreg > /Volumes/Repo/storage-tests/atp/inventory/temp/ioreg.txt')

    driveType = ""

    with open('/Volumes/Repo/storage-tests/atp/inventory/temp/ioreg.txt', 'r') as r:
        lines = r.readlines()

    for line in lines :  
        if 'IOUSBMassStorageUASDriver' in line:
            driveType = 'UAS'
            infoList = getUSBDriveData(driveType) 
        elif 'IONVMeBlockStorageDevice' in line:
            driveType = 'NVMe'
            infoList = getNVMeDriveData(driveType)  
        elif 'IOUSBMassStorageDriver' in line:
            driveType = 'BOT'
            infoList = getUSBDriveData(driveType)
        elif 'IOAHCIBlockStorageDevice' in line:
            driveType = 'AHCI'
            infoList = getAHCIDriveData(driveType)
        elif 'AppleSDXCBlockStorageDevice' in line:
            driveType = 'SDXC'
    return infoList



def main():
    try: 
        infoList = getDriveInfo()
        print(f"\nDrive information:  {infoList[1]} - {infoList[2]}")
        print("-" * 60)
        print(f'{infoList[3]}\nLocation: {infoList[4]}\n')

        """ # This if statment allows user to mark the location of a drive if desired. Otherwise, location is set to 0 on inventory sheet
        updateLocation = input("Update device location (Host - DUT)? (y/n): ")
        if updateLocation == 'y':
            infoList[4] = input("Enter DUT location: (Host - DUT): ")
        else:
            print("\nLocation set to 0\n")"""
        
        addToInv = input("Add to drive inventory? (y/n): ")
        if addToInv == 'y' :
            with open('/Volumes/Repo/storage-tests/atp/inventory/external_drives.csv', 'a', encoding = 'UTF8', newline= '') as drives_csv:
                writer = csv.writer(drives_csv)
                writer.writerow(infoList)
            print("Okay, added to inventory")
            print('Please create TSTT resource\n')
        else:
            print("Okay, not added to inventory\n")   
            print('Please create TSTT Resource\n')
    except:
        print('\nNo drives currently enumerated\n')
    else:
        label = input('Would you like to print a label? (y/n): ')    
        if label =='y':
            TSTT = input('Enter TSTT number: rdar://res/')
            create_label(infoList[1],f'rdar://res/{TSTT}',infoList[2],'/Volumes/Repo/storage-tests/atp/inventory/temp/labeltmp.pdf')
            print('\nGenerating Label\n')
        else:
            pass


if __name__ == "__main__":
    main()

