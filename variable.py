#------------------信件--------------------#
Sender_email_account = 'eastek.intern@gmail.com'#寄件者帳號
Sender_email_password = 'Eastek2020'#寄件者密碼

handle_applicant_title = '申請結果確認信(to 申請人)' #申請確認信給申請人的主旨
check_applicant_title = '審核結果確認信(to 申請人)'#審核結果信給申請人的主旨
handle_verify_title = '申請通知信(to 審核者)'#申請審核通知信給審核人的主旨
check_verify_title = '審核結果確認信(to 審核者)'#審核確認信給審核人的主旨
#----------------審核機制------------------#
verify_group = ['審核-產品','審核-財務']#審核群組
verify_user = ['teddy']#審核人
verify_num = 1#審核人數
verify_check = {'verify_group':[False,False], 'verify_user':[False], 'verify_num':0}