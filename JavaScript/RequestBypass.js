var currenturl = document.URL;
var tid, time, acc;

// Get player modified completion time and accuracy
time = parseFloat(prompt("Enter completion time (Please enter a time in seconds. Ex. \"22.6\"): ")).toFixed(1) * 10;
time = time.toString().replace(".","");
acc = prompt("Enter completion accuracy (Please enter a whole number 0-100): ").toString();

// Are you a part of a tournament, if so, get the tournament id from the url
if (currenturl.includes("?t=")) {tid = currenturl.split("=")[1]} else {tid = ""};

// Deal with fixedTime errors
if (fixedTime === 0 || fixedTime < time) {
    fixedTime = parseInt(time) + 1000; // Make sure it is more than time entered by user
}

async function get_token(currenturl,time) {
    const response = await fetch("https://www.purposegames.com/api/1.0/insert-token", {
      "headers": {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "no-cache",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "pragma": "no-cache",
        "sec-ch-ua": "\"Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"115\", \"Chromium\";v=\"115\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Chrome OS\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sec-gpc": "1"
      },
      "referrer": currenturl,
      "referrerPolicy": "no-referrer-when-downgrade",
      "body": `id=${gameId}&p=80&rt=${(fixedTime-parseInt(time)).toString()}&nonce=${gnon}&csrf=${mT}`,
      "method": "POST",
      "mode": "cors",
      "credentials": "include"
    });
    
    const data = await response.json();
    return data["token_id"];
}

(async function () {
    var token = await get_token(currenturl,time);
    console.log("Token: "+token);
    
    // Send altered post request (Submit score)
    fetch("https://www.purposegames.com/api/1.0/insert-score-and-time", {
      "headers": {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "no-cache",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "pragma": "no-cache",
        "sec-ch-ua": "\"Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"115\", \"Chromium\";v=\"115\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Chrome OS\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sec-gpc": "1"
      },
      "referrer": currenturl,
      "referrerPolicy": "no-referrer-when-downgrade",
      "body": `id=${gameId}&tid=${tid}&lid=&rt=${time}&p=${acc}&token=${token}&nonce=${gnon}&csrf=${mT}`,
      "method": "POST",
      "mode": "cors",
      "credentials": "include"
    });
})();
