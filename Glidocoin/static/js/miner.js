import * as jquery from "./jquery.min.js";

let host = "https://glidocoin.herokuapp.com";
// host = ""; uncomment this to test on localhost

if(typeof(EventSource) !== "undefined") {
    // Yes! Server-sent events support!
    // Some code.....
    window.walletAddr = $("#wallet_address").text();

    var source = new EventSource("/balance/"+walletAddr);
    source.onmessage = function(event) {
        let balance = Math.round((event.data) * 1000000)/1000000
        console.log(Math.round((balance + Number.EPSILON) * 1000000)/1000000)
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
    $("#account_status").html("<b style='text-transform:capitalize'><small>Account status: &nbsp; <b>Mining</b></small></b>");
    $.get(host+"/startMiner/"+walletAddr, (res)=>{
        console.log(res)
    })
}
window.stopMiner = (elem, walletAddr)=>{
    elem.disabled = true;
    $(elem).css('background', 'rgb(170, 46, 73)')
    let elem2 = elem.previousElementSibling;
    $(elem2).css('background', 'rgb(47, 47, 255)')
    elem2.disabled = false;
    $(elem2).find('i').hide(100)
    $.get(host+"/stopMiner/"+walletAddr, (res)=>{
        console.log(res)
        $("#account_status").html("<b style='text-transform:capitalize'><small>Account status: &nbsp; <b>"+res+"</b></small></b>");
    })
}
window.getBalanceOf = (walletAddr)=>{
    $.get(host+"/balance/"+walletAddr, (bal)=>{
        console.log(bal)
    })
}