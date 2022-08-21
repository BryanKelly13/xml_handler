import shutil
import xml.etree.ElementTree as ET
import os
import os.path



def file_handler(dir, data_file, angle, B_field):
    os.chdir('../')
    analyzed_folder = os.getcwd()+'/analyzed_fits'
    data_folder = os.getcwd()+'/data_files'
    if not (os.path.isdir(analyzed_folder)):
        os.mkdir(analyzed_folder)
    if not (os.path.isdir(data_folder)):
        os.mkdir(data_folder)
    
    os.chdir(dir)
    for file in os.listdir(dir):
        src_dir = dir + '/' + file
        if file.endswith('.py'):
            continue
        elif file.startswith('data'):
            dest_dir = data_folder + '/' + file
            shutil.move(src_dir, dest_dir)
        else:
            field_setting_folder = analyzed_folder + '/' + B_field + 'G_setting'
            if not (os.path.isdir(field_setting_folder)):
                os.mkdir(field_setting_folder)
            
            sub_analyzed_folder = field_setting_folder + '/' + angle + '_deg'
            if not (os.path.isdir(sub_analyzed_folder)):
                os.mkdir(sub_analyzed_folder)
            dest_dir = sub_analyzed_folder + '/' + file
            shutil.move(src_dir, dest_dir)
    print("\n")
    print("Fit files moved to analyzed_fits directory")
    print("Data file moved to data_files directory")

def extract_data(B_field, angle, directory):
    #finds the uncalibrated fit & corresponding data (error in peak pos, volume, width)
    fit_list = []
    fit_err_list = []
    width_list = []
    width_err_list = []
    volume_list = []
    volume_err_list = []
    fit_counter = 0
    for file in os.listdir(directory):
        if file.endswith('.py'):
            continue
        elif file.startswith('data'):
            continue
        else:
            fit_counter += 1
            print('Starting fit:', fit_counter, 'now!' )
            mytree = ET.parse(file)
            myroot = mytree.getroot()
            for i in myroot[0]:
                if i.tag == 'peak':
                    for child in i.iter():
                        if child.tag == 'cal':
                            break
                        if child.tag == 'pos':
                            for newchild in child.iter():
                                if newchild.tag == 'value':
                                    fit_value = newchild.text
                                    fit_list.append(float(fit_value))
                                elif newchild.tag == 'error':
                                    fit_err = newchild.text
                                    fit_err_list.append(float(fit_err))
                        elif child.tag == 'vol':
                            for newchild in child.iter():
                                if newchild.tag == 'value':
                                    vol_value = newchild.text
                                    volume_list.append(float(vol_value))
                                elif newchild.tag == 'error':
                                    vol_err = newchild.text
                                    volume_err_list.append(float(vol_err))
                        elif child.tag == 'width':
                            for newchild in child.iter():
                                if newchild.tag == 'value':
                                    width_value = newchild.text
                                    width_list.append(float(width_value))
                                elif newchild.tag == 'error':
                                    width_err = newchild.text
                                    width_err_list.append(float(width_err))
    # print('Peaks', fit_list)
    # print('Peaks Err', fit_err_list)
    # print('Widths', width_list)
    # print('Width Err', width_err_list)
    # print('Volume',volume_list)
    # print('Volume err',volume_err_list)
    
    data = open("data_" + B_field + "G_" + angle + "deg.txt", 'w')
    list = []
    for val in zip(fit_list, fit_err_list, width_list, width_err_list, volume_list, volume_err_list):  #interleaves lists together
        list.append(val)
    print('Data extracted, writing to data_' + B_field + 'G_' + angle + 'deg.txt file!')
    print('Reminder, format for outputted data is: \n', 'Channel  (Err)  Width  (Err)  Volume  (Err)')
    # print(list) --> Unsorted list

    sorted_list = sorted(list, reverse=True)
    # print("New list \n", sorted_list)  ---> Sorted list

    for t in sorted_list:
        line = ' '.join(str(x) for x in t)
        data.write(line + '\n')
    data.close() 
    return data


def get_positions(directory):

    cal_data = []
    uncal_data = []

    for file in os.listdir(directory):
       print(file)
       if file.endswith('.py'):
           continue
       else:
           mytree = ET.parse(file)
           myroot = mytree.getroot()
           print(myroot)

           #finds the calibrated & uncalibrated positions of the fits
           for i in myroot[0]:
                if i.tag == 'peakMarker':
                    for child in i.iter():
                        if child.tag == 'cal':
                            cal = child.text
                        elif child.tag == 'uncal':
                            uncal = child.text
                    cal_data.append(cal)
                    uncal_data.append(uncal)

    print(cal_data)
    print(uncal_data)


def get_input():
    directory = os.getcwd()
    print("Enter B-Field and Angle settings")
    while True:
        try:
            B_field = int(input("B-Field (G): "))
        except ValueError:
            print("Invalid Input, try again")
        else:
            break
    while True:
        try:
            angle = int(input("Angle (degrees): "))
        except ValueError:
            print("Invalid Input, try again")
        else:
            break
    
    return directory, str(B_field), str(angle)

def test_func(B_field, angle, dir):
    pass

def main():
    dir, B_field, angle = get_input()
    #test_func(B_field, angle, dir)
    data_file = extract_data(B_field, angle, dir)
    
    
    #get_positions(dir)
    file_handler(dir, data_file, angle, B_field)

if __name__ == '__main__':
    main()