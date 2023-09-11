// Copyright 2018 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.


let rar = [
    {
      "type": "privacy_controls",
      "path": "/userinfo",
      "access_timeout":'1785196492',
      "patch":[
        { "op": "remove", "path":"/dob"},
        { "op": "remove", "path":"/occupations"},
        { "op": "replace", "path":"/gender", "value":"X"},
        { "op": "replace", "path":"/given_name", "value":"Foo"},
        { "op": "replace", "path":"/family_name", "value":"Bar"},
      ],
    }
]


chrome.webRequest.onBeforeRequest.addListener(
    function (details) {
      //This if branch retrieve the token from the authorization response
      // https://fapidev-api.authlete.net/api/mock/redirection/27938895921594#access_token=5dvQm1CY7IF4MJkBAtNQPB0tNt6Ao-KSvJcLxopMecs&token_type=Bearer&expires_in=86400&scope=trigger_request&iss=https%3A%2F%2Fauthlete.com
        if (details.url.indexOf("/api/authorization?") !== -1) {
            console.log("visited the authentication page\n")
            let newUrl = new URL(details.url);
            var referrerUrl = details.initiator;

            rar[0]["client_id"]  = newUrl.searchParams.get("client_id")
            if (referrerUrl) {
              rar[0]["application"] = referrerUrl
            }

            newUrl.searchParams.set('authorization_details', JSON.stringify(rar))

            return {redirectUrl: newUrl.toString()};

    }


    },
    {
        urls: ["<all_urls>"]
    },
    ["blocking"]
);
