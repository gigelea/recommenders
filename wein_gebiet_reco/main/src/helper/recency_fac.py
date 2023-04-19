# import numpy as np
# import helper

# def recency_fac_exp(num):
#     passed_months = helper.year_to_months(2019, 1)
# #     passed_months = vergangene_monate
#     if num <= 12:
#         return 1
#     elif num > 12 and num <= passed_months:
#         num -= 12
#         passed_months -= 12
#         recency = 1 - np.exp(-(passed_months-num + 1)/passed_months)
#         return recency
#     else:
#         return 0
    
# def recency_fac_reziproc(num):
#     passed_months = helper.year_to_months(2019, 1)
# #     passed_months = vergangene_monate
#     if num <= 12:
#         return 1
#     elif num > 12 and num <= passed_months:
#         num -= 12
#         passed_months -= 12
#         recency = 1/(np.sqrt(num) + 1/passed_months)
#         return recency
#     else:
#         return 0

# def recency_fac_linear(num):
#     passed_months = helper.year_to_months(2019, 1)
# #     passed_months = vergangene_monate
#     if num <= 12:
#         return 1
#     elif num > 12 and num <= passed_months:
#         num -= 12
#         passed_months -= 12
#         recency = (passed_months - num + 1)/passed_months
#         return recency
#     else:
#         return 0

# def recency_fac_square(num):
#     passed_months = helper.year_to_months(2019, 1)
# #     passed_months = vergangene_monate
#     if num <= 12:
#         return 1
#     elif num > 12 and num <= passed_months:
#         num -= 12
#         passed_months -= 12
#         recency = 1 - (num ** 2 + 1)/(passed_months ** 2)
#         return abs(recency)
#     else:
#         return 0