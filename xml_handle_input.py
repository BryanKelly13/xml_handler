from codecs import ascii_decode
import pathlib
import shutil
import xml.etree.ElementTree as ET
import os
import os.path
import argparse

'''
This is a branch of the xml_handle code that is modified to sort through gamma-ray spectra using the CeBrA detectors at the SPS

Takes one xml file that has fitted peaks in HDTV, loops through and creates 2 data files, one with uncalibrated information and one with
calibrated information --> the information is position, position err, width, width err, volume, volume err
'''

def general_xml(file, fname):
    mytree = ET.parse(file)
    myroot = mytree.getroot()
 
    uncal_fit_list = []
    uncal_fit_err_list = []
    uncal_width_list = []
    uncal_width_err_list = []
    uncal_volume_list = []
    uncal_volume_err_list = []

    cal_fit_list = []
    cal_fit_err_list = []
    cal_width_list = []
    cal_width_err_list = []
    cal_volume_list = []
    cal_volume_err_list = []

    for fit in myroot:
        for i in fit:
            if i.tag == 'peak':
                for child in i.iter():
                    if child.tag == 'uncal':
                        for j in child.iter():
                            if j.tag == 'pos':
                                for newchild in j.iter():
                                    if newchild.tag == 'value':
                                        fit_value = newchild.text
                                        uncal_fit_list.append(float(fit_value))
                                    elif newchild.tag == 'error':
                                        fit_err = newchild.text
                                        uncal_fit_err_list.append(float(fit_err))
                            elif j.tag == 'vol':
                                for newchild in j.iter():
                                    if newchild.tag == 'value':
                                        vol_value = newchild.text
                                        uncal_volume_list.append(float(vol_value))
                                    elif newchild.tag == 'error':
                                        vol_err = newchild.text
                                        uncal_volume_err_list.append(float(vol_err))
                            elif j.tag == 'width':
                                for newchild in j.iter():
                                    if newchild.tag == 'value':
                                        width_value = newchild.text
                                        uncal_width_list.append(float(width_value))
                                    elif newchild.tag == 'error':
                                        width_err = newchild.text
                                        uncal_width_err_list.append(float(width_err))

                    #gets the calibrated data information                
                    if child.tag == 'cal':
                        for j in child.iter():
                            if j.tag == 'pos':
                                for newchild in j.iter():
                                    if newchild.tag == 'value':
                                        fit_value = newchild.text
                                        cal_fit_list.append(float(fit_value))
                                    elif newchild.tag == 'error':
                                        fit_err = newchild.text
                                        cal_fit_err_list.append(float(fit_err))
                            elif j.tag == 'vol':
                                for newchild in j.iter():
                                    if newchild.tag == 'value':
                                        vol_value = newchild.text
                                        cal_volume_list.append(float(vol_value))
                                    elif newchild.tag == 'error':
                                        vol_err = newchild.text
                                        cal_volume_err_list.append(float(vol_err))
                            elif j.tag == 'width':
                                for newchild in j.iter():
                                    if newchild.tag == 'value':
                                        width_value = newchild.text
                                        cal_width_list.append(float(width_value))
                                    elif newchild.tag == 'error':
                                        width_err = newchild.text
                                        cal_width_err_list.append(float(width_err))
    
    # uncalibrated data handling
    uncal_list = []
    for val in zip(uncal_fit_list, uncal_fit_err_list, uncal_width_list, uncal_width_err_list, uncal_volume_list, uncal_volume_err_list):  #interleaves lists together
        uncal_list.append(val)
    sorted_uncal_list = sorted(uncal_list, reverse=True)

    uncal_data = open(fname + "_uncalibrated_data.txt", 'w')
    for t in sorted_uncal_list:
        line = ' '.join(str(x) for x in t)
        uncal_data.write(line + '\n')
    uncal_data.close()

    if (uncal_fit_list[0] == cal_fit_list[0]):  #case where the data is not energy calibrated
            print("Calibrated data not detected, only generating uncalibrated data set!")
            return uncal_data, []
    else:
        # calibrated data handling

        cal_list = []
        for val in zip(cal_fit_list, cal_fit_err_list, cal_width_list, cal_width_err_list, cal_volume_list, cal_volume_err_list):  #interleaves lists together
            cal_list.append(val)
        sorted_cal_list = sorted(cal_list, reverse=True)

        cal_data = open(fname + "_calibrated_data.txt", 'w')
        for t in sorted_cal_list:
            line = ' '.join(str(x) for x in t)
            cal_data.write(line + '\n')
        cal_data.close() 

        return uncal_data, cal_data

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("xml", type=pathlib.Path, help="Xml file for data to be extracted from")
    args = parser.parse_args()
    return args

def main():
    '''
    Current version will output an uncalibrated & calibrated data set of the given file as a positional argument to the script
    i.e. python3 xml_handle_cebra.py filename.txt is how to run and will return 2 files:
    filename_uncalibrated_data.txt
    filename_calibrated_data.txt

    Will only return one file if there is no calibrated data present in the xml file
    '''
    dir = os.getcwd()
    args = parseArgs()
    file = dir + '/' + str(args.xml)
    path_name, ext = os.path.splitext(file)
    fname = path_name.split('/')[-1]
    general_xml(file, str(fname))

    print("Data written successfully!")

if __name__ == '__main__':
    main()
