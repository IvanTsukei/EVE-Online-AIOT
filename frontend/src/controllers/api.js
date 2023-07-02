const API_LINK = "http://localhost:5000/";

export async function ApiRequest (path, args) {
    let link = API_LINK + path;     
    if (args && Object.keys(args).length > 0) {
        let i = 0;
        Object.keys(args).forEach(key => {
            if (i > 0) {
                link += "&" + key + "=" + args[key];
            } else {
                link += "?" + key + "=" + args[key];
            }
            i++;
        });
    }

    let fetchArgs = {};
    let res = await fetch(link, fetchArgs).catch(err => {
        console.log(err)
    });
    return res;
}

export async function ApiPostRequest (path, args) {
    let link = API_LINK + path;
    let res = await fetch(link, {
        method: "post",
        credentials: 'include',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(args)
    }).catch(err => {
        console.log(err);
    });
    return res;
}
