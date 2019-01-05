import sys
import pandas

if __name__ == '__main__':
    columns = [
        'Completed Date',
        'Reference'
    ]

    args = sys.argv
    args = args[1:]

    for arg in args:
        file = pandas.read_csv(arg, sep=';', index_col=False)
        local_columns = list(columns)
        local_columns += [col for col in file.columns if 'Paid' in col]
        file = file[local_columns]
        file[local_columns[0]] = pandas.to_datetime(file[local_columns[0]], yearfirst=True)
        file.rename(columns={list(file.filter(regex='.*Date').columns)[0]: 'Date'}, inplace=True)
        file.rename(columns={list(file.filter(regex='.*Reference').columns)[0]: 'Payee'}, inplace=True)
        file = file.fillna(0.00, axis=0)


        file['Paid In (GBP)'] = pandas.to_numeric(file['Paid In (GBP)'].str.replace(',', ''))
        file['Paid Out (GBP)'] = pandas.to_numeric(file['Paid Out (GBP)'].str.replace(',', ''))
        file = file.fillna(0.00, axis=0)

        file['Outflow'] = file['Paid Out (GBP)'] - file['Paid In (GBP)']
        file.drop(columns=list(file.filter(regex='Paid.*').columns), inplace=True, axis=1)
        file.to_csv(arg.split('.')[0] + '_processed' + '.csv', sep=',', index=False)
