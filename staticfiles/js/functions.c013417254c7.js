window.showElem = (obj)=>{
    $(obj).show();
};
window.showElem = (obj1, obj2=null)=>{
    $(obj1).show(400);
    if (obj2 !== null){
        $(obj2).not(obj1).hide(400);
    }
    console.log(obj1, obj2)
};
window.toggleShow = (obj1, obj2)=>{
    $(obj1).add(obj2).toggle('show');
};

window.interests = {'data':[]};

window.watchInterests = (obj)=>{
    let elem = $(obj).find('p')[0];
    if (elem.innerText.includes(',')){
        window.interests.data.push(elem.innerText.split(',')[0].trim());
     
    let newArr = [];
    let x;
    for (x of window.interests.data){
        if (x !== "" && x !== null && x !== undefined){
            newArr.push(x);
        }
    }
    window.interests.data = newArr;

        Promise.all([
            $(obj).html(buildInterest(elem)),
            $(obj).append('<p class="no-margin inline-block">&nbsp;</p>'),
            getSelection().setPosition($('#interests p')[0], 1),
            $('#interests p').triggerHandler( "focus" ),
        ])
    }
};
window.buildInterest = (obj)=>{
    let interestsHtml = [];
    let arr = interests.data;
    let x;
    for (x of arr){
        if (x !== ""){
            interestsHtml.push(`<span style="display:inline-block;background:rgb(217, 117, 28);color:white;padding:6px 10px;white-space:nowrap;margin:2px 0" contenteditable="false">${x.trim()} &nbsp; <i class="fa fa-times cursor-pointer" data-interest="${x.trim()}" onclick="removeInterest(this)"></i></span>`)
        }
    }
    return interestsHtml.join(' ');
}
window.checkInterests = (obj)=>{
    Promise.all([
        $(obj).find('p').append(','),
        watchInterests(obj)
    ])
}
window.removeInterest = (obj)=>{
    let index = window.interests.data.findIndex((i)=> i == $(obj).data('interest'));
    delete window.interests.data[index];
    let newArr = [];
    let x;
    for (x of window.interests.data){
        if (x !== null && x !== undefined){
            newArr.push(x);
        }
    }
    window.interests.data = newArr;
    console.log(window.interests.data);
    $(obj).parent().remove();
}