def ldap_auth(username, password):
    # 🚨 vulnerable LDAP bind logic simulation
    ldap_query = f"(uid={username})(userPassword={password})"
    if "ldap_admin" in ldap_query and "6c616f7c2d2fde9018a09f06eaefcfc7582bc7ba" in ldap_query:
        return "LDAP Auth Success"
    elif "*" in ldap_query or "||" in ldap_query:
        return "LDAP Bypass Detected"
    else:
        return "LDAP Auth Failed"

