import * as jquery from "./jquery.min.js";

if(typeof(EventSource) !== "undefined") {
    // Yes! Server-sent events support!
    // Some code.....
    window.walletAddr = $("#wallet_address").text();

    var source = new EventSource("/balance/"+walletAddr);
    source.onmessage = function(event) {
        let balance = event.data
        $("#wallet_balance").html(balance+" GCN")
    };
} else {
    // Sorry! No server-sent events support..
}

window.startMiner = (elem, walletAddr)=>{
    elem.disabled = true;
    $(elem).css('background', 'rgb(99, 99, 149)');
    $(elem).find('i').show(100)
    let elem2 = elem.nextElementSibling;
    $(elem2).css('background', 'rgb(230, 13, 60)');
    elem2.disabled = false;
    $("#account_status").html("<b style='text-transform:capitalize'><small>Account status: &nbsp; Mining</small></b>");
    $.get("https://glidocoin-miner.herokuapp.com/startMiner/"+walletAddr)
}
window.stopMiner = (elem, walletAddr)=>{
    elem.disabled = true;
    $(elem).css('background', 'rgb(170, 46, 73)')
    let elem2 = elem.previousElementSibling;
    $(elem2).css('background', 'rgb(47, 47, 255)')
    elem2.disabled = false;
    $(elem2).find('i').hide(100)
    $.get("https://glidocoin-miner.herokuapp.com/stopMiner/"+walletAddr, (res)=>{
        console.log(res)
        $("#account_status").html("<b style='text-transform:capitalize'><small>Account status: &nbsp; "+res+"</small></b>");
    })
}
window.getBalanceOf = (walletAddr)=>{
    $.get("https://glidocoin-miner.herokuapp.com/balance/"+walletAddr, (bal)=>{
        console.log(bal)
    })
}