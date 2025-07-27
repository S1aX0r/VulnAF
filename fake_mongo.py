def nosql_auth(username, password):
    # 🚨 vulnerable NoSQL query simulation
    query = {"username": username, "password": password}
    if username == "admin" and password == "67de70beaad195daa67ee87321f4b5b94e18d8de":
        return "NoSQL Auth Success"
    elif "$or" in username or "$ne" in password:
        return "NoSQL Injection Bypass"
    return "NoSQL Auth Failed"

