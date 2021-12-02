import re
import pandas as pd
from dateutil.parser import parse
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler, LabelEncoder, OneHotEncoder, OrdinalEncoder
from sklearn.compose import make_column_transformer

class Parsing ():

    def __init__(self,user_input_dict) -> None:
        self.user_input_dict = user_input_dict
        pass

    def get_user_input(self):
        cols_dict = {}
        cols_transf = {}
        cols_type = {}
        for name, item in self.user_input_dict.items():
            if item[0]:
                if item[2] not in cols_transf:        
                    cols_transf[item[2]] = []
                cols_transf[item[2]].append(name)   
                if item[1] not in cols_type:
                    cols_type[item[1]] = []          
                cols_type[item[1]].append(name)
        cols_dict['transform'] = cols_transf
        cols_dict['type'] = cols_type
        cols_dict 
        return cols_dict



    def parse_data(self,df):

        user_dict = self.get_user_input()
        user_type_transf = user_dict['type']
        int_pattern = re.compile('\d*')
        float_pattern = re.compile('\d*[.]\d*')
        df_error = pd.DataFrame()
        df_parsed = pd.DataFrame()
        for key_name in user_type_transf: 
            if 'int' in key_name:
                for column_name in user_type_transf['int']:
                    try:
                        int_column = []
                        for row in df[column_name].iteritems():
                            matches = re.findall(int_pattern, str(row[1]))
                            m = "".join(matches).strip()
                            try:
                                int_column.append(int(m))
                            except:
                                int_column.append(0)
                        df_parsed[column_name] = int_column
                    except:
                        df_error[column_name] = df[column_name]


            elif 'float' in key_name:
                try:
                    for column_name in user_type_transf['float']:
                        float_column = []
                        for row in df[column_name].iteritems():
                            matches = re.findall(float_pattern, str(row[1]))
                            m = "".join(matches).strip()
                            try:
                                float_column.append(float(m))
                            except:
                                float_column.append(0)
                        df_parsed[column_name] = float_column
                except:
                        df_error[column_name] = df[column_name]


            elif 'date' in key_name:
                try:
                    for column_name in user_type_transf['date']:
                        date_column = []
                        for row in df[column_name].iteritems():
                            str(row[1])
                            m = parse(str(row[1]))
                            date_column.append(m)
                        df_parsed[column_name] = date_column
                except:
                        df_error[column_name] = df[column_name]

            else:
                for column_name in user_type_transf[key_name]:
                        date_column = []
                        df_parsed[column_name] = df[column_name]    
        return df_parsed,df_error


    def scaler_encoder(self,df):
        user_dict = self.get_user_input()
        user_type_scale = user_dict['transform']
        scaler_list = []
        col_name_list = []
        for scaler, cols in user_type_scale.items():
            if scaler == 'StandardScaler':
                scaler_list.append((StandardScaler(),cols))
            elif scaler == 'MinMaxScaler':
                scaler_list.append((MinMaxScaler(),cols))
            elif scaler == 'RobustScaler':
                scaler_list.append((RobustScaler(),cols))
            elif scaler == 'OneHotEncoder':
                scaler_list.append((OneHotEncoder(handle_unknown='ignore', sparse=False),cols))
            elif scaler == 'OrdinalEncoder':
                scaler_list.append((OrdinalEncoder(),cols))

        [col_name_list.extend(col_name[1]) for col_name in scaler_list]
        for col_name in df.columns:
            if col_name not in col_name_list:
                col_name_list.append(col_name)
        print(col_name_list)
        preprocessor = make_column_transformer(*scaler_list, remainder='passthrough')
        preprocessor.fit(df)
        if ('LabelEncoder' or 'OneHotEncoder' or 'OrdinalEncoder') in user_type_scale:
            transf_columns_names = preprocessor.get_feature_names_out()
            transf_names_list = [
                col_name.rpartition('__')[2] for col_name in transf_columns_names]
            df_transformed_pre = preprocessor.transform(df)
            df_transformed = pd.DataFrame(df_transformed_pre, columns=transf_names_list)
        else:
            df_transformed_pre = preprocessor.transform(df)
            df_transformed = pd.DataFrame(df_transformed_pre,columns=col_name_list)
        return df_transformed

    def parse_and_transform(self,df):
        df_parsed,df_error = self.parse_data(df)
        print(df_parsed)
        df_trasnf = self.scaler_encoder(df_parsed)
        if df_error.empty:
           return df_trasnf,'Done'
        print(df_error)
        return pd.concat([df_trasnf, df_error], axis=1), f'Parse error in columns {df_error.columns}'    

if __name__ == '__main__':
    predictions = {'int_test':(True, 'int','MinMaxScaler'),
                'date':(True, 'date',None),
                'int_num':(True, 'int','RobustScaler'),
                'float_num':(True, 'float','StandardScaler'),
                'int_num_str':(True, 'int','StandardScaler'),
                'float_num_str':(True, 'float','MinMaxScaler'),
                'bin_cat' :(True, 'cat-bin','OrdinalEncoder'),
                'bin_cat_str' :(True, 'cat-bin','OrdinalEncoder'),
                'multi_cat_str' :(True, 'text',None),
                }
    int_test=['126 mins', '134 mins', '253_mins', '123,000', '53 seconds']
    date =['12/08/2012', '12 Aug 2022', '12/08/22','20-08-12','12-08-2021']
    int_num =[1,2000,346980,481464,654654]
    float_num =[13654.543,3546645.454,54654654.88,64655432.54654,6544453213.654521]
    int_num_str =['1','2000','b','481464654654','64654']
    float_num_str =['13654.543','asd','54654654.88','64655432.54654','6544453213.654521']
    bin_cat =[True,False,False,True,True]
    bin_cat_str =['Yes','No','No','Yes','Yes']
    multi_cat_str =['gdgd','adsdas','dfsfdfsdf','Ysfdfss','Yesdafbhdfgs']

    df = pd.DataFrame({'int_test': int_test,
                        'date': date,
                        'int_num':int_num,
                        'float_num':float_num,
                        'int_num_str': int_num_str,
                        'float_num_str':float_num_str,
                        'bin_cat' : bin_cat,
                        'bin_cat_str' : bin_cat_str,
                        'multi_cat_str':multi_cat_str})
    parse_type = Parsing(predictions)
    print(parse_type.parse_and_transform(df))