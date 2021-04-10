import * as jquery from "./jquery.min.js";

fetch("https://glidocoin-miner.herokuapp.com/myWallet/", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        username: "kingabel",
        password: "Exploxi2"
    })
}).then(async res=>{
    res.json().then(val=>{
        $("#walletAddress").text(val['walletAddress'])
        $("#account_status").html("<b style='text-transform:capitalize'><small>Account status: &nbsp; "+val['status']+"</small></b>");
    })
})

// $.post("/myWallet/", {
//     username: "kingabel",
//     password: "Exploxi2"
// }, (res)=>{
//     console.log("res:", res)
// }, "json")