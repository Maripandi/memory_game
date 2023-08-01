import pandas as pd
from game.models import Game,User,Score
class CustomFunctions:
    def __init__(self):
        self.symbl = ('@','#','$','%','&','*','_','!','-','+','=','/','\\',':',';','^','~')
    def password_validator(self,pwd):
        if len(pwd) < 8:
            return 'your password cannot be less then 8 character'
        else:
            check_upper = [True if i.isupper() else False for i in pwd]
            check_lower = [True if i.islower() else False for i in pwd]
            check_digit = [True if i.isdigit() else False for i in pwd]
            check_symbl = [True if i in self.symbl else False for i in pwd]
            if True not in check_digit:
                return 'number missing in your password'
            elif True not in check_upper:
                return 'Uppercase letter missing in your password'
            elif True not in check_lower:
                return 'lowercase letter missing in your password'
            elif True not in check_symbl:
                return 'Special Character missing in your password'
            else:
                return True

    def nameValidation(self,name,value):
        if len(value) == 0:
            return f'{ name } cannot be empty'
        elif value.isalpha():
            return True
        elif value.isdigit():
            return f'{ name } cannot be only numbers'
        elif value.isalnum():
            return True
        else:
            check_symbol = [True if i in self.symbl else (True if i.isnumeric() else False) for i in value]
            if False in check_symbol:
                return True
            else:
                return f'{ name } cannot be only numbers or symbols'
    
    @staticmethod
    def shuffedCards2x(objs):
        df = pd.DataFrame(objs)
        lambdafn1 = lambda x: '1'+str(x)
        lambdafn2 = lambda x: '2'+str(x)
        df1 = df.applymap(lambdafn2)
        df2 = df.applymap(lambdafn1)
        newdf = pd.concat([df1,df2],ignore_index=True)
        # newdf = df1.add(df2)
        # print(newdf)
        shuffledf = newdf.sample(frac=1) 
        return shuffledf
    
    # def leaderboards(request):
        
    #     scores_df = pd.DataFrame(Score.objects.all().values())
        
        
    #     users_df = pd.DataFrame(User.objects.all().values())
    #     # print(scores_df,'\n',users_df)
    #     df = pd.concat([scores_df,users_df])
    #     return df