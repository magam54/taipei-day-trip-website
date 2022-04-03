async function getattraction(){
    await getuser()
    const res = await fetch('/api/booking')
    const data = await res.json()
    if (data.data==null){
        let box=document.querySelector('.detailText')
        box.innerHTML=""
        document.querySelector('.booking').innerHTML=""
        let msgbox=document.querySelector('.bookingDetail')
        let msg=document.createElement('p')
        msg.setAttribute('id','msg')
        msg.textContent="目前沒有任何待預訂的行程"
        msgbox.insertBefore(msg,box);
    }
    if (data.data!=null){
        attractionName=data.data.attraction.name
        date=data.data.date
        time=data.data.time
        price=data.data.price
        address=data.data.attraction.address
        image=data.data.attraction.image
        let box=document.querySelector('.bookingDetail')
        let detail=document.querySelector('.detailText')
        let images = document.createElement('img');
        images.src=image
        box.insertBefore(images,detail);
        document.getElementById('attractionName').textContent=attractionName
        document.getElementById('attractionDate').textContent=date
        document.getElementById('attractionPrice').textContent="新台幣 "+(price)+" 元"
        document.getElementById('attractionAddress').textContent=address
        document.getElementById('totalcost').textContent="總價"+"："+"新台幣 "+(price)+" 元"
        if(time=="morning"){
            time="早上9點到中午12點"
            document.getElementById('attractionTime').textContent=time
        }
        if(time=="afternoon"){
            time="下午2點到下午5點"
            document.getElementById('attractionTime').textContent=time
        }
    }
}
 getattraction()

let user=null;
async function getuser(){
    const res = await fetch('/api/user')
    const data = await res.json()
    user=data.data
    if (data.data==null){
        window.location.pathname="/";
    }
    if (data.data!=null){
        document.getElementById('nav_login').style.display="none"
        document.getElementById('nav_logout').style.display="grid"
        name=data.data.name
        document.getElementById('username').textContent=name
    }
}

// 刪除預定
document.getElementById('deletebtn').addEventListener("click",function(){
    fetch('/api/booking',{
        method:"DELETE"
    })
    .then(function(data){
        if(data.ok==true)
            location.reload();
    })
})

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