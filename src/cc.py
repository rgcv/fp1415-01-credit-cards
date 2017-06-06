# 81045 - Rui Ventura

##
## Constants
##

# Information about credit cards, compiled into tuples (in a table-like fashion,
# or 2-D array, where the first is the row's index and the second the column's.
# Certain rows may have more elements, even if of the same "category").

CC_INFO = (
    ## Generic example
    #('Abbreviation',
    # 'Issuer',
    # ('prefix-1','prefix-2', ..., 'prefix-n'),
    # (length-1, length-2, ..., length-n)),
    
    ## American Express
    ('AE',
     'American Express',
     ('34', '37'),
     (15,)),
    
    ## Diners Club International
    ('DCI',
     'Diners Club International',
     ('309', '36', '38', '39'),
     (14,)),
    
    ## Discover Card
    ('DC',
     'Discover Card',
     ('65',),
     (16,)),
    
    ## Maestro
    ('M',
     'Maestro',
     ('5018', '5020', '5038'),
     (13, 19)),
    
    ## Master Card
    ('MC',
     'Master Card',
     ('19', '50', '51', '52', '53', '54'),
     (16,)),
    
    ## Visa Electron
    ('VE',
     'Visa Electron',
     ('4026', '426', '4405', '4508'),
     (16,)),
    
    ## Visa
    ('V',
     'Visa',
     ('4024', '4532', '4556'),
     (13, 16))
)

# The category's index depends on the card's initial digit, as it is one less
# the given digit. For example: Initial digit = 1 => index = 0

CC_CATEGORIES = (
    'Companhias aereas',
    'Companhias aereas e outras atribuicoes futuras da industria',
    'Viagens e entretenimento e bancario / financeiro',
    'Servicos bancarios e financeiros',
    'Servicos bancarios e financeiros',
    'Merchandising e bancario / financeiro',
    'Petroleo e outras atribuicoes futuras da industria',
    'Saude, telecomunicacoes e outras atribuicoes futuras da industria',
    'Atribuicao nacional'
    )

# Indexes for different rows in CC_INFO

IDX_ABBREVIATION = 0
IDX_ISSUER       = 1
IDX_IIN_DIGITS   = 2
IDX_LENGTH       = 3



##
## Helper functions
##

def calc_soma(cc_str):
    """ Executes instructions 2 through 4 (w/o verification digit) of Luhn's
        Algorithm on cc_str
    Params: (string) 'CC Number (w/o verification)' cc_str
    Return: (int) 'Processed number's sum' cc_sum """
    
    cc_str_inverse = ''
    
    for c in cc_str:
        cc_str_inverse = c + cc_str_inverse
    
    cc_sum = 0
    for i in range(len(cc_str_inverse)):
        digit = eval(cc_str_inverse[i])
        
        if i % 2 == 0:
            digit = digit * 2
            if digit > 9:
                digit = digit - 9
        cc_sum = cc_sum + digit
    return cc_sum

def luhn_verifica(cc_str):
    """ Applies Luhn's algorithm to verify the given cc number
    Params: (string) 'CC Number' cc_str
    Return: (bool) True, if number is valid, False otherwise"""
    
    check_digit = eval(cc_str) % 10
    cc_str_wo_digit = eval(cc_str) // 10
    return (calc_soma(str(cc_str_wo_digit)) + check_digit) % 10 == 0

def comeca_por(str1, str2):
    """ Checks if str1 starts with str2
    Params: (string) 'Candidate string' str1
            (string) 'Potential prefix' str2
    Return: (bool) True, if str2 is a prefix of str2, False otherwise"""
    
    diff = len(str1) - len(str2)
    
    # By dividing the evaluated number by 10^diff, it'll reduce str1 to the
    # size of str2 (assuming str1 and str2 are integers, which is True, for this
    # application)
    return str(eval(str1) // (10 ** diff)) == str2

def comeca_por_um(str, strs):
    """ Checks if str starts with any of the strings in strs
    Params: (string) 'Candidate string' str
            (tuple) 'Tuple of potential prefixes' strs
    Return: (bool) True, if any of the strings in 'strs' is a prefix of str1,
        False otherwise"""
    
    for s in strs:
        if comeca_por(str, s):
            return True
    return False

def valida_iin(cc_str):
    """ Checks the number corresponding to the given string, validating the IIN
        digits and its length
    Params: (string) 'CC Number' cc_str
    Return: (string) 'Issuer'"""
    
    cc_len = len(cc_str)
    valid_iin, same_length = False, False
    
    # Look for the tuple with the details of the corresponding issuer given the
    # iin digits
    for cc_issuer in CC_INFO:
        # Checks the, if so, multiple prefixes
        for iin in cc_issuer[IDX_IIN_DIGITS]:
            if (not isinstance(iin, str) and comeca_por_um(cc_str, iin)) \
                or comeca_por(cc_str, iin):
                valid_iin = True
                # Do the same for possible lengths
                for length in cc_issuer[IDX_LENGTH]:
                    if cc_len == length:
                        same_length = True
            if valid_iin and same_length:
                return cc_issuer[IDX_ISSUER]
    return ''

def categoria(cc_str):
    """ Returns the category of the credit card number cc_str
    Params: (string) 'CC Number' cc_str
    Return: (string) 'CC Category'"""
    
    # Obtains the most significant digit dividing the number by 10^(length - 1)
    return CC_CATEGORIES[eval(cc_str) // 10 ** (len(cc_str) - 1) - 1]

def digito_verificacao(cc_str):
    """ Calculates the verification digit for the given credit card number
    Params: (string) 'CC Number' cc_str
    Return: (string) 'Verification digit'"""
    
    # Complements the sum with the digit that will make the resulting sum a
    # multiple of 10
    verification_digit = (10 - (calc_soma(cc_str) % 10))
    if verification_digit != 10:
        return str(verification_digit % 10)
    return '0'



##
## Main functions
##

from random import random

def verifica_cc(cc_num):
    """ Checks if cc_num is a valid credit card number
    Params: (int) 'CC Number' cc_num
    Return: (tuple) 'Category and Issuer', if valid,
            (string) 'Invalido' otherwise"""
    
    cc_str = str(cc_num)
    if luhn_verifica(cc_str) and valida_iin(cc_str) != '':
        return (categoria(cc_str), valida_iin(cc_str))
    return 'cartao invalido'

def gera_num_cc(issuer_abbrev):
    """ Generates a random credit card number based on the given abbreviation
    Params: (string) 'Issuer abbreviation' issuer_abbrev
    Return: (int) 'CC Number'"""
    
    cc_issuer = ()
    
    # Will choose the tuple, if found, with the issuer corresponding the given
    # abbreviation
    for i in range(len(CC_INFO)):
        if issuer_abbrev == CC_INFO[i][IDX_ABBREVIATION]:
            cc_issuer = CC_INFO[i]
    if len(cc_issuer) == 0:
        return 'Abreviatura invalida'
    
    # Choose one of the prefixes randomly based on the ones available, if there
    # are more than one
    iin_len = len(cc_issuer[IDX_IIN_DIGITS])
    iin_digits = cc_issuer[IDX_IIN_DIGITS][int(iin_len * random())]
    
    # O mesmo com os comprimentos
    lengths_len = len(cc_issuer[IDX_LENGTH])
    cc_len = cc_issuer[IDX_LENGTH][int(lengths_len * random())]
    
    cc_num = str(iin_digits)
    cc_len = cc_len - (len(iin_digits) + 1)
    
    for n in range(cc_len):
        cc_num = cc_num + str(int(10 * random()))
    
    return int(cc_num + digito_verificacao(cc_num))