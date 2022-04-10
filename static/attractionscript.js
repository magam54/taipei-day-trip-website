let pathVariable = window.location.pathname.split('/')[2];

let url = "http://18.139.199.228:3000/api/attractions/"+pathVariable



fetch(url).then((taipei)=>{
    return taipei.json();
})
.then((data)=>{
        let len=data.data.image.length;
        for (n=0 ; n < len ; n++){
            let title = data.data.name
            let subtitle = data.data.category+" at "+data.data.mrt
            let description=data.data.description
            let address=data.data.address
            let transport=data.data.transport
            let image=data.data.image[n]
            document.querySelector(".title").textContent=title
            document.querySelector(".mrt").textContent=subtitle
            document.querySelector(".description .intro").textContent=description
            document.querySelector(".description .address").textContent=address
            document.querySelector(".description .transhow").textContent=transport
            let carousel = document.querySelector(".imageCarousel")
            let btn = document.querySelector(".left")
            let images = document.createElement('img');
            images.src=image
            carousel.insertBefore(images,btn);
            let dots = document.querySelector(".dots")
            let dot = document.createElement('span')
            dot.classList.add("dot"+n)
            dots.append(dot)

        }
        let image0 = document.getElementsByTagName('img').item(0);
        image0.style.display='block'
        let dot0 =document.querySelectorAll('span[class^="dot"]').item(0)
        dot0.style.background="black"
})

// 輪播圖片
let index = 1
function slides(n){
    let slideindex = index+n;
    let length=document.getElementsByTagName('img').length;
    let array=document.getElementsByTagName('img');
    let dots=document.querySelectorAll('span[class^="dot"]')
    if (slideindex>length){
        slideindex=1;
        index=0
    }
    if (slideindex<=0){
        index=length+1
        slideindex=length
    }
    for(i=0;i<length;i++){
        array[i].style.display='none';
        dots[i].style.background="white"
    }
    array[slideindex-1].style.display='block';
    dots[slideindex-1].style.background="black"
    index=index+n ;
}


// 選擇時段
document.getElementsByName('tourtime').forEach(radio=>{
    radio.addEventListener('click',function(){
        if(radio.value=="morning"){
            document.querySelector(".price").textContent=2000
        }
        if(radio.value=="afternoon"){
            document.querySelector(".price").textContent=2500
        }
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

document.getElementById('bookingform').addEventListener("submit",function(e){
    e.preventDefault()
    let fd= new FormData(this)
    let fdjson={};
    for (pairs of fd.entries()){
        fdjson[pairs[0]]=pairs[1];
    }
    fdjson['attractionId']=pathVariable
    let price=document.getElementById('price').textContent
    fdjson['price']=price
    fetch('/api/booking',{
        method:"POST",
        body:JSON.stringify(fdjson),
        headers:{
            'content-type':'application/json'
        }
    })
    .then(response=>response.json())
    .then(function(data){
        if (data.error==true){
            document.getElementById('modal').style.visibility = "visible";
            document.getElementById('modalcard_login').style.display = "block";
        }
        if (data.ok==true){
            window.location.pathname="/booking";
        }
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

// 登入登出
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