import time, random

print("User ID", "\t\t", "Traced users", "\t\t", "")

while(True): 
    N = 100
    user_id = []
    traced_no_of_users = []
    symptom_status = []
    ans = [0]*N

    

    for i in range(0, N):
        user_id.append(i)
        traced_no_of_users.append(random.randint(0, 5))
        symptom_status.append(random.randint(0,1))
        pro_of_traced_users = []
        time_of_contact = []

        for j in range(0, traced_no_of_users[i]):
            pro_of_traced_users.append(round(random.uniform(0.00, 1.00),4))
            time_of_contact.append(random.randint(0,10))
            if time_of_contact[j] < 3:
                ans[i] += (1 - ans[i])*(time_of_contact[j]/3)*pro_of_traced_users[j]
            else:
                ans[i] += (1 - ans[i])*pro_of_traced_users[j]

            if i == 99:
                print(ans[i], "#########", traced_no_of_users[i], "#########", pro_of_traced_users[j],"#######", time_of_contact[j])




    print(round(ans[99],2))
    print("\n")
    time.sleep(25)