export default class Login {
    constructor(){
    }
    showElem(obj) {
        $(obj).show();
    }
    toggleShow(obj1, obj2) {
        $(obj1).add(obj2).toggle('show');
    }
}