balances = {}
debts={}

from configparser import ConfigParser
config = ConfigParser()
config.read("config.ini")

file_name=input("Please type the name of the file withoux extension (case sensitive) : ")

with open('./movements_files/'+file_name+".txt") as f:
    for line in f:
        payer = line.split("|")[0].strip()
        currency = line.split("|")[1].strip()
        amount = line.split("|")[2].strip()
        beneficiaries = line.split("|")[3].split(",")
        if not (currency in balances): balances[currency]={}
        if payer in balances[currency] : 
            balances[currency][payer]+=float(amount)
        else: 
            balances[currency][payer]=float(amount)
        for beneficiary in beneficiaries:
            beneficiary_trim = beneficiary.strip()
            if beneficiary_trim in balances[currency]: 
                balances[currency][beneficiary_trim]-=float(amount)/len(beneficiaries)
            else : 
                balances[currency][beneficiary_trim]=float(amount)/len(beneficiaries)*(-1)

for currency in balances:
    balances_file=open("./balances_files/"+file_name+"_"+currency+'.txt', "w")
    for user in balances[currency]:
        L=user + " : " + str(round(balances[currency][user], int(config['ROUND_AMOUNTS']['number_of_decimals']))) + "\n"
        balances_file.writelines(L)
    balances_file.close

def all_balances_are_equal_to_0(currency):
    for user in balances[currency]:
        #if abs(balances[user])>1/(10**int(config['ROUND_AMOUNTS']['number_of_decimals'])): return False
        if abs(balances[currency][user])>0.0001: return False
    return True

def get_user_with_most_important_balance(currency,negative=False):
    most_important_balance_on_this_side=0
    user_most_important_balance_on_this_side=None
    for user in balances[currency] :
        balance = balances[currency][user]
        if (balance < 0 and negative ==True) or (balance > 0 and negative ==False):
            if abs(balance)>most_important_balance_on_this_side:
                most_important_balance_on_this_side = abs(balance)
                user_most_important_balance_on_this_side=user
    return user_most_important_balance_on_this_side

for currency in balances:
    debts[currency]=[]
    while not all_balances_are_equal_to_0(currency):
        user_with_highest_balance=get_user_with_most_important_balance(currency)
        user_with_lowest_balance=get_user_with_most_important_balance(currency,True)
        highest_balance = balances[currency][user_with_highest_balance]
        lowest_balance = balances[currency][user_with_lowest_balance]
        debt_amount = min(abs(highest_balance),abs(lowest_balance))

        debt={"has_to_pay":user_with_lowest_balance,"has_to_be_paid":user_with_highest_balance,"amount":debt_amount}
        
        balances[currency][user_with_highest_balance]-=debt_amount
        balances[currency][user_with_lowest_balance]+=debt_amount

        debts[currency].append(debt)

    debts_file=open("./debts_files/"+file_name+"_"+currency+'.txt', "w")

    for debt in debts[currency] :
        L=debt["has_to_pay"]+" owes "+debt["has_to_be_paid"]+" "+str(round(debt["amount"],int(config['ROUND_AMOUNTS']['number_of_decimals']))) +" " + currency+"\n"
        debts_file.writelines(L)
        #print(debt["has_to_pay"]+" owes "+debt["has_to_be_paid"]+" "+str(round(debt["amount"],int(config['ROUND_AMOUNTS']['number_of_decimals']))))

    debts_file.close