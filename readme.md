This repository cntains our proof-of-concept implementation for our paper **A User-centric Approach to API Delegation: Enforcing Privacy Policies on OAuth Delegations**.




* `/browser-extension`: A Chrome extension browser extension that add Rich Authorization Request (RAR) parameters to the ongoing authorization reqeust to our API. 
* `/resource-server`: The baseline API which is protected by utAPI to enforce privacy policies on API response. For our OAuth implemetation we used [Authlete](https://www.authlete.com/) and deployed [`java-oauth-server`](https://github.com/authlete/java-oauth-server) as our authorization server. 




## Citation

```
@inproceedings{kalantari23utapia,
    author = {Kalantari, Shirin and Philippaerts, Pieter and Dimova, Yana and Hughes, Danny and Joosen, Wouter and De Decker, Bart},
    title = {A User-centric Approach to API Delegations Enforcing Privacy Policies on OAuth Delegations},
    booktitle = {Computer Security – ESORICS 2023  28th European Symposium on Research in Computer Security,},
    year = {2023}
}
```

