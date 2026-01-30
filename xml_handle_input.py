import pathlib
import shutil
import xml.etree.ElementTree as ET
import os
import os.path
import argparse


def extract_values(parent, tag_name):
    """Helper function to extract 'value' and 'error' from a given tag."""
    value = error = None
    for elem in parent.iter(tag_name):
        for child in elem:
            if child.tag == 'value':
                value = float(child.text)
            elif child.tag == 'error':
                error = float(child.text)
    return value, error

def write_to_file(data_list, fname, file_suffix, reverse=False):
        # Interleave the data into tuples
        combined = list(zip(
            data_list['fit'],
            data_list['fit_err'],
            data_list['width'],
            data_list['width_err'],
            data_list['volume'],
            data_list['volume_err']
        ))

        # Sort and write to file
        combined_sorted = sorted(combined, reverse=reverse)
        filename = f"{fname}_{file_suffix}.txt"
        with open(filename, 'w') as f:
            for entry in combined_sorted:
                f.write('\t'.join(str(x) for x in entry) + '\n')
        return filename

def general_xml(file, fname):
    tree = ET.parse(file)
    root = tree.getroot()

    data = {
        'uncal': {'fit': [], 'fit_err': [], 'width': [], 'width_err': [], 'volume': [], 'volume_err': []},
        'cal':   {'fit': [], 'fit_err': [], 'width': [], 'width_err': [], 'volume': [], 'volume_err': []}
    }

    for fit in root.findall('.//peak'):
        for region in ['uncal', 'cal']:
            region_elem = fit.find(region)
            if region_elem is not None:
                pos_val, pos_err = extract_values(region_elem, 'pos')
                width_val, width_err = extract_values(region_elem, 'width')
                vol_val, vol_err = extract_values(region_elem, 'vol')

                if pos_val is not None:
                    data[region]['fit'].append(round(pos_val, 4))
                if pos_err is not None:
                    data[region]['fit_err'].append(round(pos_err, 4))
                if width_val is not None:
                    width_val = abs(width_val) if region == 'cal' else width_val
                    data[region]['width'].append(round(width_val, 4))
                if width_err is not None:
                    data[region]['width_err'].append(round(width_err, 4))
                if vol_val is not None:
                    data[region]['volume'].append(round(vol_val, 4))
                if vol_err is not None:
                    data[region]['volume_err'].append(round(vol_err, 4))
    
    # Write uncalibrated data
    uncal_filename = write_to_file(data['uncal'], fname, "uncalibrated_data", reverse=True)

    # Check for calibration
    if not data['cal']['fit'] or data['uncal']['fit'][0] == data['cal']['fit'][0]:
        print("Calibrated data not detected, only generating uncalibrated data set!")
        return uncal_filename, None

    # Write calibrated data
    cal_filename = write_to_file(data['cal'], fname, "calibrated_data", reverse=False)
    print("Calibrated data present, generating two files for calibrated & uncalibrated data!")
    
    return data['uncal'], data['cal']


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
