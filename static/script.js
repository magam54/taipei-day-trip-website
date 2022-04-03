// 動態卡片製作處理
function makebox(data){
    let len=data.data.length
    for (n=0 ; n < len ; n++){
        let title = data.data[n].name;
        let mrt = data.data[n].mrt;
        let cat = data.data[n].category;
        let id =data.data[n].id;
        let images = data.data[n].images[0];
        let gridLi = document.getElementById('gridLi');
        let card = document.createElement('div');
            card.classList.add('card');
        let img = document.createElement('img');
            img.src = images;
        let p1 = document.createElement('p');
            p1.classList.add('a');
            p1.textContent=title
        let p2 = document.createElement('p');
            p2.classList.add('b');
            p2.textContent=mrt;
        let span = document.createElement('span');
            span.classList.add('c');
            span.textContent=cat;
        let link = document.createElement('a');
        link.setAttribute('href','http://18.139.199.228:3000/attraction/'+id)
            card.append(img,p1,p2,span);
            link.append(card);
            gridLi.append(link);
    }
}

// 設定初始頁面網址&偵測對象
let url = new URL('http://18.139.199.228:3000/api/attractions?page=0')
let footer = document.getElementById("footer")

// 初始頁面且偵測滾動
function callback(entries){
    if(entries[0].isIntersecting){
        fetch(url)
        .then(function(taipei){
            return taipei.json();
        })
        .then(function(data){
            let p = data.nextPage
            if(p!=null){
                makebox(data);
                url.searchParams.set("page",p);
            }
            if(p==null){
                makebox(data);
                oberserver.unobserve(footer)
            }
        })
    }
}

const oberserver = new IntersectionObserver (callback)
oberserver.observe(footer);

// 關鍵字搜索偵測滾動
function callbackKeyword(entries){
    if(entries[0].isIntersecting){
        let keyword = document.getElementById("kw").value;
        url.searchParams.set("keyword",keyword);
        fetch(url)
        .then(function(taipei){
            return taipei.json();
        })
        .then(function(data){
            let p = data.nextPage
            if(p!=null){
                makebox(data);
                url.searchParams.set("page",p);
            }
            if(p==null){
                makebox(data);
                oberserverKW.unobserve(footer)
            }
        })
    }
}

const oberserverKW = new IntersectionObserver (callbackKeyword)

// 關鍵字搜索 點擊放大鏡觸發
document.getElementById("manifier").addEventListener("click",function(){
    keywordSearch()
})

// 關鍵字 按Enter觸發
document.getElementById("kw").addEventListener("keyup",function(e){
    if(e.key==="Enter"){
        keywordSearch()
    }
})

// 關鍵字搜尋
function keywordSearch(){
    oberserver.unobserve(footer)
    let keyword = document.getElementById("kw").value;
    url.searchParams.set("page",0);
    url.searchParams.set("keyword",keyword);
    let gridLi = document.getElementById("gridLi")
    fetch(url)
    .then(function(taipei){
        return taipei.json();
    })
    .then(function(data){
        let len=data.data.length
        if(len != 0){
            gridLi.innerHTML=""
            let p = data.nextPage
            if(p!=null){
                makebox(data);
                url.searchParams.set("page",p);
                oberserverKW.observe(footer);
            }
            if(p==null){
                makebox(data);
            }
        }
        if(len == 0){
            gridLi.innerHTML=""
            let ms = document.createElement('p');
            ms.textContent='找不到相關景點資料！'
            gridLi.append(ms);
        }   
    })
}

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