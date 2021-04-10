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
}).then(res=>{
    res.json().then(val=>{
        $("#wallet_address").text(val['walletAddress'])
        $("#start_miner").attr("onclick", "startMiner(this, '"+val['walletAddress']+"')")
        $("#stop_miner").attr("onclick", "stopMiner(this, '"+val['walletAddress']+"')")
        $("#account_status").html("<b style='text-transform:capitalize'><small>Account status: &nbsp; "+val['status']+"</small></b>");
    })
})

// $.post("/myWallet/", {
//     username: "kingabel",
//     password: "Exploxi2"
// }, (res)=>{
//     console.log("res:", res)
// }, "json")