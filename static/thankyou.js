
let url = new URLSearchParams(window.location.search)
let ordernumber=url.get('number')
document.getElementById('ordernumber').textContent=ordernumber;

let recordbtn=document.querySelector('.fa-suitcase-rolling')
recordbtn.addEventListener('click',function(){
    fetch('/api/order/'+ordernumber,{
        method:"GET",
        headers:{
            'content-type':'application/json'
        }
    })
    .then(response=>response.json())
    .then(function(data){
        attraction=data.data.trip.attraction.name
        price=data.data.price
        date=data.data.trip.date
        time=data.data.trip.time
        paystatus=data.data.status
        let box = document.getElementById('thankyou')
        let table=document.createElement('table')
        box.appendChild(table)
        let row1=document.createElement('tr')
        let head1_1=document.createElement('th');
        let head1_2=document.createElement('th');
        head1_1.innerText="項目"
        head1_2.innerText="內容"
        row1.append(head1_1,head1_2)
        let row2=document.createElement('tr')
        let head2_1=document.createElement('th');
        let head2_2=document.createElement('th');
        head2_1.innerText="景點名稱"
        head2_2.innerText=attraction
        row2.append(head2_1,head2_2)
        let row3=document.createElement('tr')
        let head3_1=document.createElement('th');
        let head3_2=document.createElement('th');
        head3_1.innerText="訂單金額"
        head3_2.innerText=price
        row3.append(head3_1,head3_2)
        let row4=document.createElement('tr')
        let head4_1=document.createElement('th');
        let head4_2=document.createElement('th');
        head4_1.innerText="預定日期"
        head4_2.innerText=date
        row4.append(head4_1,head4_2)
        let row5=document.createElement('tr')
        let head5_1=document.createElement('th');
        let head5_2=document.createElement('th');
        head5_1.innerText="行程時間"
        if (time=="morning"){
            head5_2.innerText="早上9點到中午12點"
        }
        if(time=="afternoon"){
            head5_2.innerText="下午2點到下午5點"
        }
        row5.append(head5_1,head5_2)
        let row6=document.createElement('tr')
        let head6_1=document.createElement('th');
        let head6_2=document.createElement('th');
        head6_1.innerText="付款狀態"
        if (paystatus==0){
            head6_2.innerText="已付款"
        }
        if(paystatus==1){
            head6_2.innerText="未付款"
        }
        row6.append(head6_1,head6_2)
        table.append(row1,row2,row3,row4,row5,row6)
        recordbtn.style.display="none"
    })
})


let user=null;
async function getuser(){
    const res = await fetch('/api/user')
    let data = await res.json()
    user=data.data
    if (data.data==null){
        document.getElementById('nav_login').style.display="grid"
        document.getElementById('nav_logout').style.display="none"
    }
    if (data.data!=null){
        document.getElementById('nav_login').style.display="none"
        document.getElementById('nav_logout').style.display="grid"
    }
}
getuser()


// 預定行程按鈕
document.getElementById('nav_booking').addEventListener("click",function(){
    if (user==null){
        document.getElementById('modal').style.visibility = "visible";
        document.getElementById('modalcard_login').style.display = "block";
    }
    if (user!=null){
        window.location.pathname="/booking";
    }
})

// 登出登入
document.getElementById('nav_login').addEventListener("click",function(){
    document.getElementById('modal').style.visibility = "visible";
    document.getElementById('modalcard_login').style.display = "block";
})
document.getElementById('registerbtn').addEventListener("click",function(){
    document.getElementById('modalcard_login').style.display = "none";
    document.getElementById('modalcard_register').style.display = "block";
})
document.getElementById('loginbtn').addEventListener("click",function(){
    document.getElementById('modalcard_login').style.display = "block";
    document.getElementById('modalcard_register').style.display = "none";
})
document.querySelectorAll('.closebtn').forEach(item=>{
    item.addEventListener("click",function(){
        document.getElementById('modal').style.visibility = "hidden"
        document.getElementById('modalcard_login').style.display = "none"
        document.getElementById('modalcard_register').style.display = "none"
    })
})

// 登入程序
document.getElementById('form_login').addEventListener("submit",function(e){
    e.preventDefault();
    let fd= new FormData(this)
    let fdjson={};
    for (pairs of fd.entries()){
        fdjson[pairs[0]]=pairs[1];
    }
    fetch('/api/user',{
        method:"PATCH",
        body:JSON.stringify(fdjson),
        headers:{
            'content-type':'application/json'
        }
    })
    .then(response=>response.json())
    .then(function(data){
        if (data.error==true){
            document.getElementById('modalcard_login').style.height = "300px";
            let text=data.message
            let message=document.getElementById("login_fail")
            message.innerText=text
        }
        if (data.ok==true){
            location.reload();
        }
    })
})

// 註冊程序
document.getElementById('form_register').addEventListener("submit",function(e){
    e.preventDefault();
    let fd= new FormData(this)
    let fdjson={};
    for (pairs of fd.entries()){
        fdjson[pairs[0]]=pairs[1];
    }
    fetch('/api/user',{
        method:"POST",
        body:JSON.stringify(fdjson),
        headers:{
            'content-type':'application/json'
        }
    })
    .then(response=>response.json())
    .then(function(data){
        if (data.error==true){
            document.getElementById('modalcard_register').style.height = "360px";
            let text=data.message
            let message=document.getElementById("register_mesg")
            message.innerText=text
        }
        if (data.ok==true){
            document.getElementById('modalcard_register').style.height = "360px";
            let text="註冊成功"
            let message=document.getElementById("register_mesg")
            message.innerText=text
        }
    })
})

// 登出程序
document.getElementById('nav_logout').addEventListener("click",function(e){
    e.preventDefault();
    fetch('/api/user',{
        method:"DELETE"
    })
    .then(function(data){
        if(data.ok==true)
            location.reload();
    })
})