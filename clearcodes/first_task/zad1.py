import csv
import datetime
import pycountry

def csvOpening(file_name):
    '''
    in this function csv file is opened and each column is tested, that the file could be read.
    :param file_name: name a file wich you want to read
    :return: input_list with all csv records
    '''
    inputs_list = []
    with open(file_name, encoding='utf-8-sig', newline='') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            date = row[0]
            state_name = row[1]
            try:
                for each_letter in state_name:
                    if each_letter.isdigit():
                        raise ValueError("{} it's not a state name, try without integers.".format(state_name))

                datetime.datetime.strptime(str(date), "%m/%d/%Y")
                number_of_impressions = int(row[2])
                if row[3].find('%') == -1:
                    raise ValueError("{} CTR should be wrote in percentage.".format(row[3]))

                inputs_list.append(row)
            except ValueError:
                raise ValueError('Incorrect data format, should be (MM/DD/YYYY)')
            except ValueError:
                raise ValueError('{} is not an integer'.format(number_of_impressions))


    return inputs_list

def dateChanges(file_length):
    '''
    function is getting date from csv file and modify to expectations date format
    :param file_length it's used to iterating over csv file
    :return: date_out it's modified date
    '''
    date_in = file[file_length][0]
    date_out = datetime.datetime.strptime(str(date_in), "%m/%d/%Y").strftime("%Y-%m-%d")

    return date_out

def countryChanges(file_length, with_deleted):
    '''
    function is getting state names from input, next function is looking for the same country code in subdivision
    and countries, next will match from code alpha_2 with code alpha_3.
    :param file_length: it's used to iterating over csv file
    :param with_deleted: i didn't know what to do about emoticons so this parameter it's for 2 options,
    1) True => in output csv file function will delete all rows with emoticons
    2) False => in output csv file function will replace emoticons with XXX
    :return: country_code with 3 letters, another case will return 'XXX' if matches 'Unknown',
    another case if doesn't match anything, then will return None that will remove record.
    '''
    country_in = file[file_length][1]
    subdivisions = list(pycountry.subdivisions)
    if with_deleted == True:
        for state in subdivisions:
            if country_in == state.name:
                state_match = state.country_code
                country_out = pycountry.countries.get(alpha_2=state_match)
                return country_out.alpha_3
            elif country_in == 'Unknown':
                country_out = 'XXX'
                return country_out
    elif with_deleted == False:
        for state in subdivisions:
            if country_in == state.name:
                state_match = state.country_code
                country_out = pycountry.countries.get(alpha_2=state_match)
                return country_out.alpha_3
            else:
                country_out = 'XXX'
        return country_out

def impressionsDisplay(file_length):
    '''
    this function is getting numbers of impressions
    :param file_length: it's used to iterating over csv file
    :return: integer of numbers of impressions
    '''
    impressions_out = int(file[file_length][2])

    return impressions_out

def clicksDisplay(file_length):
    '''
    this function is getting the CTR rating and removing percentage symbol with spaces, then this string is changning
    to float, next function is counting the number of clicks
    :param file_length: it's used to iterating over csv file
    :return: number of clicks
    '''
    clicks_in = file[file_length][3]
    clicks_in = float(clicks_in.strip(' % '))/100
    clicks_out = round(clicks_in * int(impressionsDisplay(file_length)))

    return clicks_out

def csv_writing(with_deleted):
    '''
    this function is writing the modified data. as i wrote earlier, i didn't know what to do with emoticons,
    so in one case it will be remove rows.
    :param with_deleted: True or False to remove or not remove row with emoticon
    :return: csv_file with modified data
    '''
    with open('test1.csv', mode='w', encoding='utf-8-sig', newline='') as test1_file:
        test1_writer = csv.writer(test1_file, delimiter=',')
        if with_deleted == True:
            for row in range(file_length):
                date, country, impress, clicks = dateChanges(row), \
                                                 countryChanges(row, with_deleted), \
                                                 impressionsDisplay(row), \
                                                 clicksDisplay(row)
                if country == None:
                    continue
                test1_writer.writerow([date, country, impress, clicks])
        elif with_deleted == False:
            for row in range(file_length):
                test1_writer.writerow([dateChanges(row), \
                                                 countryChanges(row, with_deleted), \
                                                 impressionsDisplay(row), \
                                                 clicksDisplay(row)])


def main():
    '''
    function is to run all process with 2 global parameters for all above functions
    :return:
    '''
    global file
    file = csvOpening('inputs_data.csv')
    global file_length
    file_length = len(file)
    csv_writing(with_deleted=False)

main()